"""AWS utility helpers with a local-first fallback path."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

try:
    import boto3
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:  # pragma: no cover - exercised only when boto3 is absent
    boto3 = None

    class BotoCoreError(Exception):
        """Fallback boto core error."""


    class ClientError(Exception):
        """Fallback boto client error."""


@dataclass(slots=True)
class AwsS3Location:
    bucket: str
    key: str
    region: str


class AwsDatasetLoader:
    """Best-effort S3 loader for dataset hydration."""

    def __init__(self, location: AwsS3Location) -> None:
        self.location = location

    def fetch_json(self) -> str | None:
        if boto3 is None:
            return None

        client = boto3.client("s3", region_name=self.location.region)
        try:
            response: dict[str, Any] = client.get_object(
                Bucket=self.location.bucket,
                Key=self.location.key,
            )
        except (BotoCoreError, ClientError):
            return None

        body = response["Body"].read()
        return body.decode("utf-8")
