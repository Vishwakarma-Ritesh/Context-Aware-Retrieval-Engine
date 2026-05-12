"""Document loading with local JSON and optional S3 support."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from app.core.logging import get_logger
from app.utils.aws_helpers import AwsDatasetLoader, AwsS3Location

LOGGER = get_logger(__name__)


class DocumentLoader:
    def __init__(
        self,
        dataset_path: Path,
        aws_region: str,
        aws_s3_bucket: str | None = None,
        aws_s3_key: str | None = None,
    ) -> None:
        self.dataset_path = dataset_path
        self.aws_region = aws_region
        self.aws_s3_bucket = aws_s3_bucket
        self.aws_s3_key = aws_s3_key

    def load(self) -> list[dict[str, Any]]:
        if self.aws_s3_bucket and self.aws_s3_key:
            payload = AwsDatasetLoader(
                AwsS3Location(
                    bucket=self.aws_s3_bucket,
                    key=self.aws_s3_key,
                    region=self.aws_region,
                )
            ).fetch_json()
            if payload:
                LOGGER.info(
                    "Loaded dataset from S3",
                    extra={"context": {"bucket": self.aws_s3_bucket, "key": self.aws_s3_key}},
                )
                return json.loads(payload)

        LOGGER.info(
            "Loaded dataset from local filesystem",
            extra={"context": {"path": str(self.dataset_path)}},
        )
        return json.loads(self.dataset_path.read_text(encoding="utf-8"))
