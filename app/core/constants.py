"""Application constants."""

from __future__ import annotations

DEFAULT_EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
FALLBACK_EMBEDDING_DIMENSION = 384
DEFAULT_TOP_K = 3
DEFAULT_BENCHMARK_PATH = "data/benchmark_queries.json"
DEFAULT_DATASET_PATH = "data/raw/technical_documents.json"
DEFAULT_RESULTS_PATH = "benchmark_results/benchmark_results.json"
DEFAULT_MARKDOWN_REPORT_PATH = "benchmark_results/retrieval_benchmark.md"
REQUEST_ID_HEADER = "x-request-id"
MAX_QUERY_LENGTH = 1_000
MAX_CHUNK_TOKENS = 120
