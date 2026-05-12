"""Dependency graph for API routes."""

from __future__ import annotations

from functools import lru_cache

from app.core.config import get_settings
from app.services.benchmark.benchmark_runner import BenchmarkRunner


@lru_cache(maxsize=1)
def get_retriever():
    settings = get_settings()
    runner = BenchmarkRunner.from_settings(settings)
    return runner.build_retriever()
