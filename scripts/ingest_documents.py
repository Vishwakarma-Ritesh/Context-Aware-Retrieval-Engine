"""Inspect the corpus and chunking behavior."""

from __future__ import annotations

from app.core.config import get_settings
from app.services.ingestion.chunker import DocumentChunker
from app.services.ingestion.document_loader import DocumentLoader


def main() -> None:
    settings = get_settings()
    loader = DocumentLoader(
        dataset_path=settings.dataset_path,
        aws_region=settings.aws_region,
        aws_s3_bucket=settings.aws_s3_bucket,
        aws_s3_key=settings.aws_s3_key,
    )
    documents = loader.load()
    chunks = DocumentChunker().chunk_documents(documents)
    print(f"Loaded {len(documents)} documents and produced {len(chunks)} chunks.")


if __name__ == "__main__":
    main()
