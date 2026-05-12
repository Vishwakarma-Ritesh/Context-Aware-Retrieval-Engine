"""Benchmark execution pipeline."""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from app.core.config import Settings
from app.core.logging import get_logger
from app.db.vector_store import VectorStore
from app.services.benchmark.benchmark_report import BenchmarkReportWriter
from app.services.benchmark.evaluation import evaluate_hits, summarize_evaluations
from app.services.embeddings.embedding_service import EmbeddingService
from app.services.ingestion.chunker import DocumentChunker
from app.services.ingestion.document_loader import DocumentLoader
from app.services.retrieval.query_expander import QueryExpander
from app.services.retrieval.retriever import Retriever
from app.services.retrieval.semantic_search import SemanticSearchService
from app.utils.json_writer import write_json

LOGGER = get_logger(__name__)


class BenchmarkRunner:
    def __init__(
        self,
        dataset_path: Path,
        benchmark_queries_path: Path,
        benchmark_results_path: Path,
        benchmark_markdown_path: Path,
        embedding_service: EmbeddingService,
        aws_region: str,
        aws_s3_bucket: str | None,
        aws_s3_key: str | None,
        top_k: int,
    ) -> None:
        self.dataset_path = dataset_path
        self.benchmark_queries_path = benchmark_queries_path
        self.benchmark_results_path = benchmark_results_path
        self.benchmark_markdown_path = benchmark_markdown_path
        self.embedding_service = embedding_service
        self.aws_region = aws_region
        self.aws_s3_bucket = aws_s3_bucket
        self.aws_s3_key = aws_s3_key
        self.top_k = top_k

    @classmethod
    def from_settings(cls, settings: Settings) -> "BenchmarkRunner":
        return cls(
            dataset_path=settings.dataset_path,
            benchmark_queries_path=settings.benchmark_queries_path,
            benchmark_results_path=settings.benchmark_results_path,
            benchmark_markdown_path=settings.benchmark_markdown_path,
            embedding_service=EmbeddingService(
                model_name=settings.embedding_model_name,
                cache_embeddings=settings.cache_embeddings,
            ),
            aws_region=settings.aws_region,
            aws_s3_bucket=settings.aws_s3_bucket,
            aws_s3_key=settings.aws_s3_key,
            top_k=settings.top_k,
        )

    def build_retriever(self) -> Retriever:
        documents = DocumentLoader(
            dataset_path=self.dataset_path,
            aws_region=self.aws_region,
            aws_s3_bucket=self.aws_s3_bucket,
            aws_s3_key=self.aws_s3_key,
        ).load()
        chunks = DocumentChunker().chunk_documents(documents)
        embedded_chunks = self.embedding_service.embed_texts([chunk.content for chunk in chunks]).vectors
        vector_store = VectorStore(dimension=len(embedded_chunks[0]))
        vector_store.add_chunks(chunks, embedded_chunks)
        semantic_search = SemanticSearchService(
            embedding_service=self.embedding_service,
            vector_store=vector_store,
        )
        return Retriever(semantic_search=semantic_search, query_expander=QueryExpander())

    def run(self) -> dict[str, Any]:
        retriever = self.build_retriever()
        queries = json.loads(self.benchmark_queries_path.read_text(encoding="utf-8"))

        strategy_a_scores = []
        strategy_b_scores = []
        query_results: list[dict[str, Any]] = []

        for benchmark_query in queries:
            comparison = retriever.compare_strategies(
                query=benchmark_query["query"],
                top_k=benchmark_query.get("top_k", self.top_k),
            )
            relevant_ids = set(benchmark_query["relevant_document_ids"])
            strategy_a_eval = evaluate_hits(comparison.strategy_a, relevant_ids)
            strategy_b_eval = evaluate_hits(comparison.strategy_b, relevant_ids)
            strategy_a_scores.append(strategy_a_eval)
            strategy_b_scores.append(strategy_b_eval)

            query_results.append(
                {
                    **comparison.to_dict(),
                    "evaluation": {
                        "strategy_a": asdict(strategy_a_eval),
                        "strategy_b": asdict(strategy_b_eval),
                    },
                }
            )

        return {
            "queries": query_results,
            "summary": {
                "strategy_a": summarize_evaluations(strategy_a_scores),
                "strategy_b": summarize_evaluations(strategy_b_scores),
            },
        }

    def run_and_report(self) -> dict[str, Any]:
        payload = self.run()
        write_json(self.benchmark_results_path, payload)
        BenchmarkReportWriter().write_markdown(self.benchmark_markdown_path, payload)
        self._print_terminal_report(payload)
        return payload

    def _print_terminal_report(self, payload: dict[str, Any]) -> None:
        for query_result in payload["queries"]:
            print("=" * 66)
            print(f"QUERY: {query_result['original_query']}")
            print("=" * 66)
            print()
            print("STRATEGY A - RAW VECTOR SEARCH")
            self._print_hits(query_result["strategy_a"])
            print()
            print("EXPANDED QUERY:")
            print(query_result["expanded_query"])
            print()
            print("STRATEGY B - AI-ENHANCED RETRIEVAL")
            self._print_hits(query_result["strategy_b"])
            print()
            print("OBSERVATIONS")
            for observation in query_result["observations"]:
                print(f"- {observation}")
            print()

        print("=" * 66)
        print("BENCHMARK SUMMARY")
        print("=" * 66)
        print(
            f"Strategy A  recall@k={payload['summary']['strategy_a']['avg_recall_at_k']:.3f}  "
            f"mrr={payload['summary']['strategy_a']['avg_mrr']:.3f}"
        )
        print(
            f"Strategy B  recall@k={payload['summary']['strategy_b']['avg_recall_at_k']:.3f}  "
            f"mrr={payload['summary']['strategy_b']['avg_mrr']:.3f}"
        )

    @staticmethod
    def _print_hits(hits: list[dict[str, Any]] | list[Any]) -> None:
        for hit in hits:
            row = hit if isinstance(hit, dict) else asdict(hit)
            preview = row["content"][:96].replace("\n", " ")
            print(
                f"{row['rank']}. [{row['document_id']}] score={row['score']:.3f} "
                f"{row['title']} :: {preview}..."
            )
