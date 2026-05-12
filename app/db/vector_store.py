"""Reusable vector store abstraction."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from app.db.faiss_index import FaissIndex
from app.services.ingestion.chunker import ChunkRecord


@dataclass(slots=True)
class RetrievalHit:
    chunk_id: str
    document_id: str
    title: str
    content: str
    score: float
    rank: int
    metadata: dict[str, Any]


class VectorStore:
    def __init__(self, dimension: int) -> None:
        self.dimension = dimension
        self._index = FaissIndex(dimension)
        self._chunks: list[ChunkRecord] = []

    def add_chunks(self, chunks: list[ChunkRecord], embeddings: list[list[float]]) -> None:
        if len(chunks) != len(embeddings):
            raise ValueError("Chunk and embedding counts must match.")
        self._chunks.extend(chunks)
        self._index.add(embeddings)

    def search(self, query_vector: list[float], top_k: int) -> list[RetrievalHit]:
        hits = self._index.search(query_vector, top_k)
        results: list[RetrievalHit] = []
        for rank, hit in enumerate(hits, start=1):
            chunk = self._chunks[hit.index]
            results.append(
                RetrievalHit(
                    chunk_id=chunk.chunk_id,
                    document_id=chunk.document_id,
                    title=chunk.title,
                    content=chunk.content,
                    score=hit.score,
                    rank=rank,
                    metadata=chunk.metadata,
                )
            )
        return results

    def snapshot(self) -> list[dict[str, Any]]:
        return [asdict(chunk) for chunk in self._chunks]
