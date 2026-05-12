"""Response models with Pydantic compatibility."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

try:
    from pydantic import BaseModel, Field
except ImportError:  # pragma: no cover - exercised only in dependency-light environments
    BaseModel = None
    Field = None


if BaseModel:

    class RetrievalHitResponse(BaseModel):
        chunk_id: str
        document_id: str
        title: str
        score: float
        content: str
        rank: int


    class SearchResponse(BaseModel):
        original_query: str
        expanded_query: str
        strategy_a: list[RetrievalHitResponse] = Field(default_factory=list)
        strategy_b: list[RetrievalHitResponse] = Field(default_factory=list)
        scores: dict[str, list[float]] = Field(default_factory=dict)
        observations: list[str] = Field(default_factory=list)


    class BenchmarkResponse(BaseModel):
        queries: list[dict[str, Any]]
        summary: dict[str, Any]

else:

    @dataclass(slots=True)
    class RetrievalHitResponse:
        chunk_id: str
        document_id: str
        title: str
        score: float
        content: str
        rank: int


    @dataclass(slots=True)
    class SearchResponse:
        original_query: str
        expanded_query: str
        strategy_a: list[RetrievalHitResponse] = field(default_factory=list)
        strategy_b: list[RetrievalHitResponse] = field(default_factory=list)
        scores: dict[str, list[float]] = field(default_factory=dict)
        observations: list[str] = field(default_factory=list)


    @dataclass(slots=True)
    class BenchmarkResponse:
        queries: list[dict[str, Any]]
        summary: dict[str, Any]
