"""Ranking helpers for retrieval presentation and analysis."""

from __future__ import annotations

from app.db.vector_store import RetrievalHit


def compare_rankings(raw_hits: list[RetrievalHit], enhanced_hits: list[RetrievalHit]) -> list[str]:
    observations: list[str] = []

    raw_top_docs = [hit.document_id for hit in raw_hits]
    enhanced_top_docs = [hit.document_id for hit in enhanced_hits]

    if raw_top_docs[:1] != enhanced_top_docs[:1]:
        observations.append(
            f"Top-ranked document changed from {raw_top_docs[:1] or ['n/a']} to {enhanced_top_docs[:1] or ['n/a']} after expansion."
        )

    if enhanced_hits and raw_hits and enhanced_hits[0].score > raw_hits[0].score:
        observations.append("Expanded retrieval achieved a stronger top-1 similarity score.")

    newly_introduced = [doc for doc in enhanced_top_docs if doc not in raw_top_docs]
    if newly_introduced:
        observations.append(
            f"Expanded retrieval surfaced additional relevant context from {', '.join(newly_introduced[:2])}."
        )

    if not observations:
        observations.append("Both strategies returned similar rankings for this query.")

    return observations
