from fastapi.testclient import TestClient

from app.main import create_app


def test_search_api_returns_comparison_payload():
    client = TestClient(create_app())
    response = client.post("/search", json={"query": "How does the system handle peak load?", "top_k": 3})

    assert response.status_code == 200
    payload = response.json()
    assert payload["expanded_query"]
    assert len(payload["strategy_a"]) == 3
    assert len(payload["strategy_b"]) == 3
    assert "x-request-id" in response.headers


def test_search_api_rejects_empty_queries():
    client = TestClient(create_app())
    response = client.post("/search", json={"query": "   ", "top_k": 3})

    assert response.status_code == 400
