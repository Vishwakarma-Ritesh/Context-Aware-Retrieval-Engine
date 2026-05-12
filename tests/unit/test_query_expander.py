from types import SimpleNamespace
from unittest.mock import MagicMock

from app.services.retrieval.query_expander import QueryExpander


def test_query_expander_uses_model_response():
    mock_model = MagicMock()
    mock_model.generate_content.return_value = SimpleNamespace(
        text="expanded query text",
        reasoning=["expanded for autoscaling"],
    )

    expanded = QueryExpander(model=mock_model).expand("handle peak load")

    assert expanded.expanded_query == "expanded query text"
    assert expanded.reasoning == ["expanded for autoscaling"]
    mock_model.generate_content.assert_called_once_with("handle peak load")


def test_query_expander_enriches_peak_load_queries():
    expanded = QueryExpander().expand("How does the system handle peak load?")

    assert "autoscaling" in expanded.expanded_query.lower()
    assert expanded.reasoning
