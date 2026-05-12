"""Document chunking for semantic indexing."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from app.core.constants import MAX_CHUNK_TOKENS
from app.services.ingestion.preprocessing import approximate_token_count, normalize_text


@dataclass(slots=True)
class ChunkRecord:
    chunk_id: str
    document_id: str
    title: str
    content: str
    source: str
    chunk_index: int
    metadata: dict[str, Any]


class DocumentChunker:
    def __init__(self, max_chunk_tokens: int = MAX_CHUNK_TOKENS) -> None:
        self.max_chunk_tokens = max_chunk_tokens

    def chunk_documents(self, documents: list[dict[str, Any]]) -> list[ChunkRecord]:
        chunks: list[ChunkRecord] = []
        for document in documents:
            paragraphs = document.get("paragraphs", [])
            buffer: list[str] = []
            buffer_tokens = 0
            chunk_index = 0

            for paragraph in paragraphs:
                normalized = normalize_text(paragraph)
                token_count = approximate_token_count(normalized)

                if buffer and buffer_tokens + token_count > self.max_chunk_tokens:
                    chunks.append(
                        self._build_chunk(
                            document=document,
                            chunk_index=chunk_index,
                            content=" ".join(buffer),
                        )
                    )
                    buffer = []
                    buffer_tokens = 0
                    chunk_index += 1

                buffer.append(normalized)
                buffer_tokens += token_count

            if buffer:
                chunks.append(
                    self._build_chunk(
                        document=document,
                        chunk_index=chunk_index,
                        content=" ".join(buffer),
                    )
                )

        return chunks

    def _build_chunk(self, document: dict[str, Any], chunk_index: int, content: str) -> ChunkRecord:
        document_id = document["document_id"]
        return ChunkRecord(
            chunk_id=f"{document_id}-chunk-{chunk_index}",
            document_id=document_id,
            title=document["title"],
            content=content,
            source=document.get("source", "local"),
            chunk_index=chunk_index,
            metadata={
                "topic": document.get("topic"),
                "keywords": document.get("keywords", []),
                "document_id": document_id,
            },
        )
