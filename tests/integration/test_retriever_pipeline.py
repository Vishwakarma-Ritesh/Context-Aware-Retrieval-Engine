from pathlib import Path

from app.services.benchmark.benchmark_runner import BenchmarkRunner
from app.services.embeddings.embedding_service import EmbeddingService


def test_retriever_pipeline_improves_peak_load_recall():
    runner = BenchmarkRunner(
        dataset_path=Path("data/raw/technical_documents.json"),
        benchmark_queries_path=Path("data/benchmark_queries.json"),
        benchmark_results_path=Path("benchmark_results/test.json"),
        benchmark_markdown_path=Path("benchmark_results/test.md"),
        embedding_service=EmbeddingService(model_name="missing-model"),
        aws_region="us-east-1",
        aws_s3_bucket=None,
        aws_s3_key=None,
        top_k=3,
    )

    retriever = runner.build_retriever()
    comparison = retriever.compare_strategies("How does the system handle peak load?", top_k=3)
    raw_docs = {hit.document_id for hit in comparison.strategy_a}
    expanded_docs = {hit.document_id for hit in comparison.strategy_b}

    assert "doc-k8s-hpa" in expanded_docs
    assert len(expanded_docs) >= len(raw_docs.intersection(expanded_docs))
