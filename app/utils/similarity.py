"""Similarity helpers shared across the retrieval stack."""

from __future__ import annotations

import math
from typing import Iterable


def normalize_vector(vector: Iterable[float]) -> list[float]:
    values = list(vector)
    norm = math.sqrt(sum(value * value for value in values))
    if norm == 0:
        return values
    return [value / norm for value in values]


def cosine_similarity(vector_a: Iterable[float], vector_b: Iterable[float]) -> float:
    a = list(vector_a)
    b = list(vector_b)
    if len(a) != len(b):
        raise ValueError("Vectors must share the same dimensionality.")
    denominator = math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b))
    if denominator == 0:
        return 0.0
    return sum(x * y for x, y in zip(a, b)) / denominator
