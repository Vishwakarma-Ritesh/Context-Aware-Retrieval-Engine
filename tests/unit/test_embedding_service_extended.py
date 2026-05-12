from pathlib import Path
from unittest.mock import patch

import numpy as np

from app.services.embeddings.embedding_service import EmbeddingService


class FakeSentenceTransformer:
    def __init__(self, model_name: str, local_files_only: bool = True) -> None:
        self.model_name = model_name
        self.local_files_only = local_files_only

    def encode(self, texts, normalize_embeddings=True):
        assert normalize_embeddings is True
        return np.asarray([[1.0, 0.0], [0.0, 1.0]][: len(texts)], dtype="float32")


def reset_embedding_singleton():
    EmbeddingService._model = None
    EmbeddingService._model_name = None
    EmbeddingService._model_load_failed = False


def test_embedding_service_uses_model_path_when_available(tmp_path: Path):
    reset_embedding_singleton()
    model_dir = tmp_path / "local-model"
    model_dir.mkdir()

    with patch("app.services.embeddings.embedding_service.SentenceTransformer", FakeSentenceTransformer):
        service = EmbeddingService(model_name=str(model_dir))
        vectors = service.embed_texts(["alpha", "beta"]).vectors

    assert vectors == [[1.0, 0.0], [0.0, 1.0]]


def test_embedding_service_marks_uncached_models_as_failed():
    reset_embedding_singleton()
    service = EmbeddingService(model_name="not-cached-model")

    assert service._get_model() is None
    assert EmbeddingService._model_load_failed is True


def test_embedding_service_detects_cache_hit_signal():
    reset_embedding_singleton()
    service = EmbeddingService(model_name="repo/model")

    with patch("app.services.embeddings.embedding_service.try_to_load_from_cache", return_value="/tmp/modules.json"):
        assert service._is_model_cached_locally() is True
