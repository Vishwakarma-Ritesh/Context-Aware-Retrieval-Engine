"""Security and input hygiene helpers."""

from __future__ import annotations

import re
from uuid import uuid4

from app.core.constants import MAX_QUERY_LENGTH


def generate_request_id() -> str:
    return uuid4().hex


def sanitize_query(query: str) -> str:
    normalized = re.sub(r"\s+", " ", query or "").strip()
    if not normalized:
        raise ValueError("Query must not be empty.")
    if len(normalized) > MAX_QUERY_LENGTH:
        raise ValueError(f"Query exceeds maximum length of {MAX_QUERY_LENGTH} characters.")
    return normalized
