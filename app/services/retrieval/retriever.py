"""Retrieval orchestrator for raw and AI-enhanced strategies."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from app.db.vector_store import RetrievalHit
from app.services.retrieval.query_expander import QueryExpander
from app.services.retrieval.ranking import compare_rankings
from app.services.retrieval.semantic_search import SemanticSearchService


@dataclass(slots=True)
class RetrievalComparison:
    original_query: str
    expanded_query: str
    strategy_a: list[RetrievalHit]
    strategy_b: list[RetrievalHit]
    observations: list[str]
    expansion_reasoning: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "original_query": self.original_query,
            "expanded_query": self.expanded_query,
            "strategy_a": [asdict(hit) for hit in self.strategy_a],
            "strategy_b": [asdict(hit) for hit in self.strategy_b],
            "observations": self.observations,
            "expansion_reasoning": self.expansion_reasoning,
        }


class Retriever:
    def __init__(self, semantic_search: SemanticSearchService, query_expander: QueryExpander) -> None:
        self.semantic_search = semantic_search
        self.query_expander = query_expander

    def compare_strategies(self, query: str, top_k: int) -> RetrievalComparison:
        raw_hits = self.semantic_search.search(query, top_k=top_k)
        expanded = self.query_expander.expand(query)
        enhanced_hits = self.semantic_search.search(expanded.expanded_query, top_k=top_k)
        observations = compare_rankings(raw_hits=raw_hits, enhanced_hits=enhanced_hits)
        return RetrievalComparison(
            original_query=query,
            expanded_query=expanded.expanded_query,
            strategy_a=raw_hits,
            strategy_b=enhanced_hits,
            observations=observations,
            expansion_reasoning=expanded.reasoning,
        )
