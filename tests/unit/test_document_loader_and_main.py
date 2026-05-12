import json
from pathlib import Path
from unittest.mock import Mock, patch

from app.main import create_app, run
from app.services.ingestion.document_loader import DocumentLoader


def test_document_loader_prefers_s3_when_available(tmp_path: Path):
    local_path = tmp_path / "docs.json"
    local_path.write_text(json.dumps([{"document_id": "local"}]), encoding="utf-8")

    with patch("app.services.ingestion.document_loader.AwsDatasetLoader.fetch_json", return_value='[{"document_id":"s3"}]'):
        documents = DocumentLoader(
            dataset_path=local_path,
            aws_region="us-east-1",
            aws_s3_bucket="bucket",
            aws_s3_key="key",
        ).load()

    assert documents[0]["document_id"] == "s3"


def test_document_loader_falls_back_to_local(tmp_path: Path):
    local_path = tmp_path / "docs.json"
    local_path.write_text(json.dumps([{"document_id": "local"}]), encoding="utf-8")

    documents = DocumentLoader(
        dataset_path=local_path,
        aws_region="us-east-1",
    ).load()

    assert documents[0]["document_id"] == "local"


def test_main_run_and_create_app_execute_expected_paths(monkeypatch):
    fake_runner = Mock()
    fake_runner.run_and_report.return_value = {"ok": True}

    with patch("app.main.BenchmarkRunner.from_settings", return_value=fake_runner):
        run()

    app = create_app()

    assert fake_runner.run_and_report.called
    assert app.title == "Semantic RAG Engine"
