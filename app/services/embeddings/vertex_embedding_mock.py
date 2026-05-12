"""Mocked Vertex AI generative behavior for retrieval query expansion."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class MockGenerationResponse:
    text: str
    reasoning: list[str]


class MockGenerativeModel:
    """Heuristic rewrite model that behaves like a lightweight generative layer."""

    def __init__(self) -> None:
        self._pattern_catalog = [
            (
                {"peak", "load", "traffic", "spike", "surge"},
                [
                    "infrastructure autoscaling",
                    "horizontal pod autoscaler behavior",
                    "load balancer traffic distribution",
                    "sudden high demand spikes",
                ],
                "Expanded a capacity-oriented query toward autoscaling and traffic management signals.",
            ),
            (
                {"cache", "latency", "redis", "response", "throughput", "read", "responsive"},
                [
                    "redis caching strategy",
                    "read-through cache",
                    "cache hit ratio",
                    "read-heavy workload optimization",
                    "latency reduction under repeated requests",
                ],
                "Expanded a performance query toward cache effectiveness and request reuse.",
            ),
            (
                {"resilience", "availability", "failure", "outage", "downtime", "avoid"},
                [
                    "high availability architecture",
                    "graceful degradation",
                    "multi-az failover",
                    "circuit breaker and retry behavior",
                ],
                "Expanded a resilience query toward availability and failure recovery mechanisms.",
            ),
            (
                {"deploy", "release", "pipeline", "rollback", "shipping", "safe", "production"},
                [
                    "ci/cd pipeline gates",
                    "progressive deployment rollout",
                    "canary analysis",
                    "automated rollback safeguards",
                    "service health verification",
                ],
                "Expanded a delivery query toward operational release controls.",
            ),
            (
                {"gateway", "routing", "api", "edge", "requests"},
                [
                    "api gateway routing policy",
                    "rate limiting",
                    "authentication offload",
                    "north-south traffic management",
                ],
                "Expanded an API entrypoint query toward gateway enforcement and routing.",
            ),
        ]

    def generate_content(self, query: str) -> MockGenerationResponse:
        lowered_tokens = {token.strip("?,.!").lower() for token in query.split()}
        normalized_tokens = lowered_tokens | {
            token[:-1] for token in lowered_tokens if token.endswith("s") and len(token) > 3
        }
        scored_matches: list[tuple[int, list[str], str]] = []
        reasoning: list[str] = []

        for triggers, phrases, note in self._pattern_catalog:
            overlap = normalized_tokens & triggers
            if overlap:
                scored_matches.append((len(overlap), phrases, note))

        scored_matches.sort(key=lambda item: item[0], reverse=True)
        expansions: list[str] = []
        for _, phrases, note in scored_matches[:2]:
            expansions.extend(phrases)
            reasoning.append(note)

        if not expansions:
            expansions.extend(
                [
                    "distributed systems behavior",
                    "service reliability controls",
                    "observability-driven diagnosis",
                ]
            )
            reasoning.append("Applied a generic distributed systems enrichment fallback.")

        deduplicated = []
        seen = set()
        for phrase in expansions:
            if phrase not in seen:
                deduplicated.append(phrase)
                seen.add(phrase)

        expanded_query = f"{query.strip()} {' '.join(deduplicated)}".strip()
        return MockGenerationResponse(text=expanded_query, reasoning=reasoning)
