"""Embedding service with singleton model loading and local fallback behavior."""

from __future__ import annotations

import hashlib
import math
from pathlib import Path
from dataclasses import dataclass
from threading import Lock
from typing import Iterable

from app.core.constants import FALLBACK_EMBEDDING_DIMENSION
from app.core.logging import get_logger
from app.utils.similarity import normalize_vector

LOGGER = get_logger(__name__)

try:
    import numpy as np
except ImportError:  # pragma: no cover - exercised when numpy is unavailable
    np = None

try:
    from sentence_transformers import SentenceTransformer
except ImportError:  # pragma: no cover - exercised when sentence-transformers is unavailable
    SentenceTransformer = None

try:
    from huggingface_hub import try_to_load_from_cache
    from huggingface_hub.constants import _CACHED_NO_EXIST
except ImportError:  # pragma: no cover - exercised when huggingface-hub is unavailable
    try_to_load_from_cache = None
    _CACHED_NO_EXIST = object()


@dataclass(slots=True)
class EmbeddingBatch:
    texts: list[str]
    vectors: list[list[float]]


class EmbeddingService:
    """Model-backed embedding generator tuned for reuse inside a local service."""

    _model = None
    _model_name: str | None = None
    _model_load_failed = False
    _model_lock = Lock()

    def __init__(self, model_name: str, cache_embeddings: bool = True) -> None:
        self.model_name = model_name
        self.cache_embeddings = cache_embeddings
        self._cache: dict[str, list[float]] = {}

    def embed_query(self, query: str) -> list[float]:
        return self.embed_texts([query]).vectors[0]

    def embed_texts(self, texts: Iterable[str]) -> EmbeddingBatch:
        text_list = list(texts)
        uncached = [text for text in text_list if text not in self._cache]
        transient_vectors: dict[str, list[float]] = {}
        if uncached:
            generated = self._encode_batch(uncached)
            for text, vector in zip(uncached, generated):
                if self.cache_embeddings:
                    self._cache[text] = vector
                else:
                    transient_vectors[text] = vector

        return EmbeddingBatch(
            texts=text_list,
            vectors=[
                self._cache[text]
                if text in self._cache
                else transient_vectors[text]
                if text in transient_vectors
                else self._encode_single(text)
                for text in text_list
            ],
        )

    def _encode_batch(self, texts: list[str]) -> list[list[float]]:
        model = self._get_model()
        if model is not None and np is not None:
            LOGGER.info(
                "Generating embeddings with sentence-transformers",
                extra={"context": {"batch_size": len(texts), "model": self.model_name}},
            )
            encoded = model.encode(texts, normalize_embeddings=True)
            return [row.tolist() for row in encoded]

        LOGGER.info(
            "sentence-transformers unavailable; using deterministic local embedding fallback",
            extra={"context": {"batch_size": len(texts), "model": self.model_name}},
        )
        return [self._fallback_encode(text) for text in texts]

    def _encode_single(self, text: str) -> list[float]:
        return self._encode_batch([text])[0]

    def _get_model(self):
        if SentenceTransformer is None:
            return None

        with self._model_lock:
            if self.__class__._model_load_failed and self.__class__._model_name == self.model_name:
                return None
            if self.__class__._model is None or self.__class__._model_name != self.model_name:
                if not self._is_model_cached_locally():
                    LOGGER.info(
                        "Embedding model not cached locally; using fallback encoder",
                        extra={"context": {"model": self.model_name}},
                    )
                    self.__class__._model = None
                    self.__class__._model_name = self.model_name
                    self.__class__._model_load_failed = True
                    return None
                try:
                    LOGGER.info(
                        "Loading embedding model",
                        extra={"context": {"model": self.model_name}},
                    )
                    self.__class__._model = SentenceTransformer(
                        self.model_name,
                        local_files_only=True,
                    )
                    self.__class__._model_name = self.model_name
                    self.__class__._model_load_failed = False
                except Exception as exc:  # pragma: no cover - depends on local model availability
                    LOGGER.warning(
                        "Failed to initialize embedding model; falling back to local encoder",
                        extra={"context": {"model": self.model_name, "error": str(exc)}},
                    )
                    self.__class__._model = None
                    self.__class__._model_name = self.model_name
                    self.__class__._model_load_failed = True
        return self.__class__._model

    def _is_model_cached_locally(self) -> bool:
        if Path(self.model_name).exists():
            return True
        if try_to_load_from_cache is None:
            return False

        required_files = [
            "modules.json",
            "config.json",
            "sentence_bert_config.json",
        ]
        for filename in required_files:
            cached = try_to_load_from_cache(repo_id=self.model_name, filename=filename)
            if cached and cached is not _CACHED_NO_EXIST:
                return True
        return False

    def _fallback_encode(self, text: str) -> list[float]:
        vector = [0.0] * FALLBACK_EMBEDDING_DIMENSION
        tokens = [token.lower() for token in text.split()]
        for token in tokens:
            token_hash = hashlib.sha256(token.encode("utf-8")).digest()
            for idx in range(0, 8):
                bucket = token_hash[idx] % FALLBACK_EMBEDDING_DIMENSION
                direction = 1.0 if token_hash[idx + 8] % 2 == 0 else -1.0
                weight = 1.0 + (token_hash[idx + 16] / 255.0)
                vector[bucket] += direction * weight

        lexical_boost_terms = {
            "autoscale": ["autoscaling", "horizontal", "hpa"],
            "traffic": ["spikes", "load", "balancer"],
            "cache": ["redis", "latency", "hit-rate"],
            "deploy": ["rollout", "pipeline", "ci/cd"],
            "resilience": ["failover", "circuit", "graceful"],
        }
        normalized_text = text.lower()
        for root, synonyms in lexical_boost_terms.items():
            if root in normalized_text:
                for synonym in synonyms:
                    bucket = int(hashlib.md5(synonym.encode("utf-8")).hexdigest(), 16) % FALLBACK_EMBEDDING_DIMENSION
                    vector[bucket] += math.log(len(synonym) + 1)

        return normalize_vector(vector)
