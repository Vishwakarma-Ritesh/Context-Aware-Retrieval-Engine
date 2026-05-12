import io
import json
import logging
from types import SimpleNamespace
from unittest.mock import Mock, patch

from app.core.config import get_settings
from app.core.logging import JsonFormatter
from app.core.security import generate_request_id, sanitize_query
from app.models.request_models import SearchRequest
from app.models.response_models import BenchmarkResponse, RetrievalHitResponse, SearchResponse
from app.utils.aws_helpers import AwsDatasetLoader, AwsS3Location
from app.utils.similarity import cosine_similarity, normalize_vector


def test_settings_honors_environment(monkeypatch):
    get_settings.cache_clear()
    monkeypatch.setenv("TOP_K", "5")
    monkeypatch.setenv("CACHE_EMBEDDINGS", "false")
    settings = get_settings()

    assert settings.top_k == 5
    assert settings.cache_embeddings is False

    get_settings.cache_clear()


def test_security_helpers_validate_queries():
    assert sanitize_query("  peak   load  ") == "peak load"
    assert len(generate_request_id()) == 32

    try:
        sanitize_query("   ")
    except ValueError as exc:
        assert "must not be empty" in str(exc)
    else:  # pragma: no cover - defensive assertion
        raise AssertionError("Expected ValueError for empty query")


def test_response_models_hold_structured_payloads():
    request = SearchRequest(query="how does it scale?", top_k=2)
    hit = RetrievalHitResponse(
        chunk_id="chunk-1",
        document_id="doc-1",
        title="Autoscaling",
        score=0.99,
        content="content",
        rank=1,
    )
    response = SearchResponse(
        original_query=request.query,
        expanded_query="expanded",
        strategy_a=[hit],
        strategy_b=[hit],
        scores={"strategy_a": [0.99], "strategy_b": [0.99]},
        observations=["improved"],
    )
    benchmark = BenchmarkResponse(queries=[{"query": request.query}], summary={"ok": True})

    assert response.strategy_a[0].document_id == "doc-1"
    assert benchmark.summary["ok"] is True


def test_json_formatter_and_similarity_helpers():
    formatter = JsonFormatter()
    record = logging.LogRecord(
        name="semantic-rag",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg="formatted",
        args=(),
        exc_info=None,
    )
    record.context = {"query": "peak load"}
    payload = json.loads(formatter.format(record))

    assert payload["message"] == "formatted"
    assert payload["context"]["query"] == "peak load"
    assert normalize_vector([3.0, 4.0]) == [0.6, 0.8]
    assert round(cosine_similarity([1.0, 0.0], [1.0, 0.0]), 3) == 1.0


def test_aws_dataset_loader_returns_payload_and_fallbacks():
    location = AwsS3Location(bucket="bucket", key="docs.json", region="us-east-1")
    body = io.BytesIO(b'[{"document_id":"doc"}]')
    fake_client = Mock()
    fake_client.get_object.return_value = {"Body": body}

    with patch("app.utils.aws_helpers.boto3") as boto3_mock:
        boto3_mock.client.return_value = fake_client
        payload = AwsDatasetLoader(location).fetch_json()

    assert "document_id" in payload

    with patch("app.utils.aws_helpers.boto3", None):
        assert AwsDatasetLoader(location).fetch_json() is None
