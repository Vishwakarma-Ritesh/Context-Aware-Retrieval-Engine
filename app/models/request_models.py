"""Request models with graceful fallback when Pydantic is unavailable."""

from __future__ import annotations

from dataclasses import dataclass

try:
    from pydantic import BaseModel, Field
except ImportError:  # pragma: no cover - exercised only in dependency-light environments
    BaseModel = None
    Field = None


if BaseModel:

    class SearchRequest(BaseModel):
        query: str = Field(..., min_length=1, max_length=1000)
        top_k: int = Field(default=3, ge=1, le=10)

else:

    @dataclass(slots=True)
    class SearchRequest:
        query: str
        top_k: int = 3
