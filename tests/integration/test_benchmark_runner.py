from pathlib import Path

from app.services.benchmark.benchmark_runner import BenchmarkRunner
from app.services.embeddings.embedding_service import EmbeddingService


def test_benchmark_runner_produces_summary(tmp_path: Path):
    results_path = tmp_path / "benchmark.json"
    markdown_path = tmp_path / "benchmark.md"
    runner = BenchmarkRunner(
        dataset_path=Path("data/raw/technical_documents.json"),
        benchmark_queries_path=Path("data/benchmark_queries.json"),
        benchmark_results_path=results_path,
        benchmark_markdown_path=markdown_path,
        embedding_service=EmbeddingService(model_name="missing-model"),
        aws_region="us-east-1",
        aws_s3_bucket=None,
        aws_s3_key=None,
        top_k=3,
    )

    payload = runner.run_and_report()

    assert "summary" in payload
    assert results_path.exists()
    assert markdown_path.exists()
    assert payload["summary"]["strategy_b"]["avg_recall_at_k"] >= payload["summary"]["strategy_a"]["avg_recall_at_k"]
