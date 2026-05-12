"""Environment-driven application settings."""

from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from app.core.constants import (
    DEFAULT_BENCHMARK_PATH,
    DEFAULT_DATASET_PATH,
    DEFAULT_EMBEDDING_MODEL,
    DEFAULT_MARKDOWN_REPORT_PATH,
    DEFAULT_RESULTS_PATH,
    DEFAULT_TOP_K,
)

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - dependency optional in local bootstrap mode
    load_dotenv = None


def _bool_env(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    project_name: str
    environment: str
    log_level: str
    embedding_model_name: str
    dataset_path: Path
    benchmark_queries_path: Path
    benchmark_results_path: Path
    benchmark_markdown_path: Path
    top_k: int
    cache_embeddings: bool
    aws_region: str
    aws_s3_bucket: str | None
    aws_s3_key: str | None
    enable_api: bool


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    if load_dotenv:
        load_dotenv()

    return Settings(
        project_name=os.getenv("PROJECT_NAME", "semantic-rag-engine"),
        environment=os.getenv("APP_ENV", "local"),
        log_level=os.getenv("LOG_LEVEL", "INFO"),
        embedding_model_name=os.getenv("EMBEDDING_MODEL_NAME", DEFAULT_EMBEDDING_MODEL),
        dataset_path=Path(os.getenv("DATASET_PATH", DEFAULT_DATASET_PATH)),
        benchmark_queries_path=Path(os.getenv("BENCHMARK_QUERIES_PATH", DEFAULT_BENCHMARK_PATH)),
        benchmark_results_path=Path(os.getenv("BENCHMARK_RESULTS_PATH", DEFAULT_RESULTS_PATH)),
        benchmark_markdown_path=Path(
            os.getenv("BENCHMARK_MARKDOWN_PATH", DEFAULT_MARKDOWN_REPORT_PATH)
        ),
        top_k=int(os.getenv("TOP_K", str(DEFAULT_TOP_K))),
        cache_embeddings=_bool_env("CACHE_EMBEDDINGS", True),
        aws_region=os.getenv("AWS_REGION", "us-east-1"),
        aws_s3_bucket=os.getenv("AWS_S3_BUCKET"),
        aws_s3_key=os.getenv("AWS_S3_KEY"),
        enable_api=_bool_env("ENABLE_API", False),
    )
