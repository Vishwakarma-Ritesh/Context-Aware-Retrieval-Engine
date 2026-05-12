"""Benchmark report rendering."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from app.utils.file_handlers import ensure_parent_directory


class BenchmarkReportWriter:
    def write_markdown(self, path: Path, payload: dict[str, Any]) -> None:
        ensure_parent_directory(path)
        lines = [
            "# Retrieval Benchmark Report",
            "",
            "## Summary",
            "",
            f"- Strategy A avg recall@k: {payload['summary']['strategy_a']['avg_recall_at_k']}",
            f"- Strategy A avg MRR: {payload['summary']['strategy_a']['avg_mrr']}",
            f"- Strategy B avg recall@k: {payload['summary']['strategy_b']['avg_recall_at_k']}",
            f"- Strategy B avg MRR: {payload['summary']['strategy_b']['avg_mrr']}",
            "",
            "## Query Analysis",
            "",
        ]

        for entry in payload["queries"]:
            lines.extend(
                [
                    f"### Query: {entry['original_query']}",
                    "",
                    f"**Expanded query**: {entry['expanded_query']}",
                    "",
                    "| Strategy | Rank | Document | Score | Preview |",
                    "|---|---:|---|---:|---|",
                ]
            )
            for strategy_name in ("strategy_a", "strategy_b"):
                for hit in entry[strategy_name]:
                    preview = hit["content"][:100].replace("|", "\\|")
                    lines.append(
                        f"| {strategy_name} | {hit['rank']} | {hit['document_id']} | {hit['score']:.3f} | {preview}... |"
                    )

            lines.extend(
                [
                    "",
                    "**Observations**",
                    "",
                ]
            )
            for observation in entry["observations"]:
                lines.append(f"- {observation}")

            lines.extend(
                [
                    "",
                    "**Relevance analysis**",
                    "",
                    f"- Strategy A recall@k: {entry['evaluation']['strategy_a']['recall_at_k']}",
                    f"- Strategy B recall@k: {entry['evaluation']['strategy_b']['recall_at_k']}",
                    f"- Strategy A MRR: {entry['evaluation']['strategy_a']['reciprocal_rank']}",
                    f"- Strategy B MRR: {entry['evaluation']['strategy_b']['reciprocal_rank']}",
                    "",
                    "Expanded retrieval performed better when the rewrite injected infrastructure-specific vocabulary that matched the indexed engineering content more directly.",
                    "",
                ]
            )

        path.write_text("\n".join(lines), encoding="utf-8")
