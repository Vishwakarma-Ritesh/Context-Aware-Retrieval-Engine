from app.services.embeddings.embedding_service import EmbeddingService


def test_embedding_service_is_deterministic_in_fallback_mode():
    service = EmbeddingService(model_name="missing-model", cache_embeddings=True)
    first = service.embed_query("redis cache latency")
    second = service.embed_query("redis cache latency")

    assert first == second
    assert len(first) == 384


def test_embedding_service_batches_texts():
    service = EmbeddingService(model_name="missing-model", cache_embeddings=False)
    batch = service.embed_texts(["one", "two"])

    assert batch.texts == ["one", "two"]
    assert len(batch.vectors) == 2
