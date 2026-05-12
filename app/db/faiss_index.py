"""FAISS-backed similarity index with a pure Python fallback path."""

from __future__ import annotations

from dataclasses import dataclass

from app.core.logging import get_logger
from app.utils.similarity import cosine_similarity, normalize_vector

LOGGER = get_logger(__name__)

try:
    import faiss
except ImportError:  # pragma: no cover - exercised when faiss is unavailable
    faiss = None

try:
    import numpy as np
except ImportError:  # pragma: no cover - exercised when numpy is unavailable
    np = None


@dataclass(slots=True)
class IndexSearchHit:
    index: int
    score: float


class FaissIndex:
    def __init__(self, dimension: int) -> None:
        self.dimension = dimension
        self._vectors: list[list[float]] = []
        self._index = None

        if faiss is not None:
            self._index = faiss.IndexFlatIP(dimension)

    def add(self, vectors: list[list[float]]) -> None:
        if not vectors:
            return

        normalized = [normalize_vector(vector) for vector in vectors]
        if self._index is not None and np is not None:
            array = np.asarray(normalized, dtype="float32")
            self._index.add(array)
            LOGGER.info("Indexed vectors with FAISS", extra={"context": {"count": len(vectors)}})
            return

        self._vectors.extend(normalized)
        LOGGER.info(
            "Indexed vectors with Python fallback search",
            extra={"context": {"count": len(vectors)}},
        )

    def search(self, query_vector: list[float], top_k: int) -> list[IndexSearchHit]:
        normalized_query = normalize_vector(query_vector)
        if self._index is not None and np is not None:
            query = np.asarray([normalized_query], dtype="float32")
            scores, indices = self._index.search(query, top_k)
            return [
                IndexSearchHit(index=int(idx), score=float(score))
                for score, idx in zip(scores[0], indices[0])
                if idx >= 0
            ]

        scored = [
            IndexSearchHit(index=idx, score=cosine_similarity(normalized_query, candidate))
            for idx, candidate in enumerate(self._vectors)
        ]
        return sorted(scored, key=lambda hit: hit.score, reverse=True)[:top_k]
