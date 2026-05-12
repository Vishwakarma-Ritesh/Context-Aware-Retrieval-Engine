"""Rebuild the local retrieval index and print a short summary."""

from __future__ import annotations

from app.core.config import get_settings
from app.services.benchmark.benchmark_runner import BenchmarkRunner


def main() -> None:
    runner = BenchmarkRunner.from_settings(get_settings())
    retriever = runner.build_retriever()
    comparison = retriever.compare_strategies("How does the system handle peak load?", top_k=3)
    print(f"Index rebuilt successfully. Top raw document: {comparison.strategy_a[0].document_id}")


if __name__ == "__main__":
    main()
