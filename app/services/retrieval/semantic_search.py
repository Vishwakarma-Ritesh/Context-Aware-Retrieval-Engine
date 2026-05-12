"""Semantic search service."""

from __future__ import annotations

from app.db.vector_store import RetrievalHit, VectorStore
from app.services.embeddings.embedding_service import EmbeddingService


class SemanticSearchService:
    def __init__(self, embedding_service: EmbeddingService, vector_store: VectorStore) -> None:
        self.embedding_service = embedding_service
        self.vector_store = vector_store

    def search(self, query: str, top_k: int) -> list[RetrievalHit]:
        query_vector = self.embedding_service.embed_query(query)
        return self.vector_store.search(query_vector, top_k)
