"""Query rewriting for AI-enhanced retrieval."""

from __future__ import annotations

from dataclasses import dataclass

from app.services.embeddings.vertex_embedding_mock import MockGenerativeModel


@dataclass(slots=True)
class ExpandedQuery:
    original_query: str
    expanded_query: str
    reasoning: list[str]


class QueryExpander:
    def __init__(self, model: MockGenerativeModel | None = None) -> None:
        self.model = model or MockGenerativeModel()

    def expand(self, query: str) -> ExpandedQuery:
        response = self.model.generate_content(query)
        return ExpandedQuery(
            original_query=query,
            expanded_query=response.text,
            reasoning=response.reasoning,
        )
