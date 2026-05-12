"""Evaluation helpers for retrieval benchmarking."""

from __future__ import annotations

from dataclasses import dataclass

from app.db.vector_store import RetrievalHit


@dataclass(slots=True)
class QueryEvaluation:
    recall_at_k: float
    reciprocal_rank: float
    hit_count: int


def evaluate_hits(hits: list[RetrievalHit], relevant_document_ids: set[str]) -> QueryEvaluation:
    matched_ranks = [hit.rank for hit in hits if hit.document_id in relevant_document_ids]
    hit_count = len(matched_ranks)
    recall_at_k = hit_count / max(len(relevant_document_ids), 1)
    reciprocal_rank = 1 / matched_ranks[0] if matched_ranks else 0.0
    return QueryEvaluation(
        recall_at_k=recall_at_k,
        reciprocal_rank=reciprocal_rank,
        hit_count=hit_count,
    )


def summarize_evaluations(scores: list[QueryEvaluation]) -> dict[str, float]:
    if not scores:
        return {"avg_recall_at_k": 0.0, "avg_mrr": 0.0}

    return {
        "avg_recall_at_k": round(sum(score.recall_at_k for score in scores) / len(scores), 3),
        "avg_mrr": round(sum(score.reciprocal_rank for score in scores) / len(scores), 3),
    }
