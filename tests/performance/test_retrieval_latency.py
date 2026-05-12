import time
from pathlib import Path

from app.services.benchmark.benchmark_runner import BenchmarkRunner
from app.services.embeddings.embedding_service import EmbeddingService


def test_retrieval_latency_is_reasonable_for_local_assessment_workload():
    runner = BenchmarkRunner(
        dataset_path=Path("data/raw/technical_documents.json"),
        benchmark_queries_path=Path("data/benchmark_queries.json"),
        benchmark_results_path=Path("benchmark_results/perf.json"),
        benchmark_markdown_path=Path("benchmark_results/perf.md"),
        embedding_service=EmbeddingService(model_name="missing-model"),
        aws_region="us-east-1",
        aws_s3_bucket=None,
        aws_s3_key=None,
        top_k=3,
    )

    retriever = runner.build_retriever()
    start = time.perf_counter()
    retriever.compare_strategies("How does the system handle peak load?", top_k=3)
    elapsed = time.perf_counter() - start

    assert elapsed < 1.0
