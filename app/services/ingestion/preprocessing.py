"""Preprocessing primitives for technical corpora."""

from __future__ import annotations

import re


def normalize_text(text: str) -> str:
    cleaned = re.sub(r"\s+", " ", text).strip()
    cleaned = cleaned.replace("–", "-")
    return cleaned


def approximate_token_count(text: str) -> int:
    return len(text.split())
