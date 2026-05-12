"""Application entrypoint for benchmark execution and optional API creation."""

from __future__ import annotations

from app.core.config import get_settings
from app.core.logging import configure_logging, get_logger
from app.services.benchmark.benchmark_runner import BenchmarkRunner

LOGGER = get_logger(__name__)

try:
    from fastapi import FastAPI
except ImportError:  # pragma: no cover - API is optional
    FastAPI = None


def run() -> None:
    settings = get_settings()
    configure_logging(settings.log_level)
    LOGGER.info("Starting semantic retrieval benchmark", extra={"context": {"env": settings.environment}})
    runner = BenchmarkRunner.from_settings(settings)
    runner.run_and_report()


def create_app():
    settings = get_settings()
    configure_logging(settings.log_level)
    if FastAPI is None:
        raise RuntimeError("FastAPI is not installed. Install requirements/dev.txt or requirements/prod.txt.")

    from app.api.middleware.request_context import RequestContextMiddleware
    from app.api.routes.search import router as search_router

    app = FastAPI(title="Semantic RAG Engine", version="0.1.0")
    app.add_middleware(RequestContextMiddleware)
    if search_router:
        app.include_router(search_router)
    return app


if __name__ == "__main__":
    run()
