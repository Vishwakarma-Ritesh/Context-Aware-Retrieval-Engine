"""Search route for comparing raw and expanded retrieval."""

from __future__ import annotations

from dataclasses import asdict, is_dataclass

from app.api.dependencies.search_dependencies import get_retriever
from app.core.security import sanitize_query
from app.models.request_models import SearchRequest

try:
    from fastapi import APIRouter, Depends, HTTPException
except ImportError:  # pragma: no cover - API is optional
    APIRouter = None
    Depends = None
    HTTPException = Exception


router = APIRouter(prefix="/search", tags=["search"]) if APIRouter else None


def _serialize_hits(hits):
    return [asdict(hit) if is_dataclass(hit) else hit for hit in hits]


if router:

    @router.post("")
    def search(request: SearchRequest, retriever=Depends(get_retriever)):
        try:
            query = sanitize_query(request.query)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

        comparison = retriever.compare_strategies(query=query, top_k=request.top_k)
        return {
            "original_query": comparison.original_query,
            "expanded_query": comparison.expanded_query,
            "strategy_a": _serialize_hits(comparison.strategy_a),
            "strategy_b": _serialize_hits(comparison.strategy_b),
            "scores": {
                "strategy_a": [hit.score for hit in comparison.strategy_a],
                "strategy_b": [hit.score for hit in comparison.strategy_b],
            },
            "observations": comparison.observations,
        }
