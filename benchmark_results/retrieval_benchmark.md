# Retrieval Benchmark Report

## Summary

- Strategy A avg recall@k: 0.417
- Strategy A avg MRR: 0.417
- Strategy B avg recall@k: 0.833
- Strategy B avg MRR: 0.875

## Query Analysis

### Query: How does the system handle peak load?

**Expanded query**: How does the system handle peak load? infrastructure autoscaling horizontal pod autoscaler behavior load balancer traffic distribution sudden high demand spikes

| Strategy | Rank | Document | Score | Preview |
|---|---:|---|---:|---|
| strategy_a | 1 | doc-cicd | 0.274 | Each deployment passes through build validation, unit tests, contract checks, and a canary stage bef... |
| strategy_a | 2 | doc-k8s-hpa | 0.193 | The platform handles burst traffic by running stateless API pods behind a Kubernetes Horizontal Pod ... |
| strategy_a | 3 | doc-service-mesh | 0.185 | East-west traffic inside the cluster is mediated by a service mesh that standardizes mTLS, retry bud... |
| strategy_b | 1 | doc-traffic-spikes | 0.267 | The operations playbook assumes that demand spikes arrive faster than infrastructure can always prov... |
| strategy_b | 2 | doc-load-balancing | 0.248 | External traffic lands on an application load balancer and is fanned into the cluster through an ing... |
| strategy_b | 3 | doc-k8s-hpa | 0.232 | The platform handles burst traffic by running stateless API pods behind a Kubernetes Horizontal Pod ... |

**Observations**

- Top-ranked document changed from ['doc-cicd'] to ['doc-traffic-spikes'] after expansion.
- Expanded retrieval surfaced additional relevant context from doc-traffic-spikes, doc-load-balancing.

**Relevance analysis**

- Strategy A recall@k: 0.3333333333333333
- Strategy B recall@k: 1.0
- Strategy A MRR: 0.5
- Strategy B MRR: 1.0

Expanded retrieval performed better when the rewrite injected infrastructure-specific vocabulary that matched the indexed engineering content more directly.

### Query: What keeps the backend responsive when reads surge?

**Expanded query**: What keeps the backend responsive when reads surge? redis caching strategy read-through cache cache hit ratio read-heavy workload optimization latency reduction under repeated requests infrastructure autoscaling horizontal pod autoscaler behavior load balancer traffic distribution sudden high demand spikes

| Strategy | Rank | Document | Score | Preview |
|---|---:|---|---:|---|
| strategy_a | 1 | doc-backend-resilience | 0.198 | When downstream dependencies become slow or unavailable, the service layer applies request timeouts,... |
| strategy_a | 2 | doc-redis-cache | 0.183 | Read-heavy endpoints use a Redis read-through cache keyed by tenant and resource version. Popular ob... |
| strategy_a | 3 | doc-api-gateway | 0.176 | The API gateway enforces authentication, rate limiting, and per-route routing policy before requests... |
| strategy_b | 1 | doc-redis-cache | 0.255 | Read-heavy endpoints use a Redis read-through cache keyed by tenant and resource version. Popular ob... |
| strategy_b | 2 | doc-observability | 0.155 | Prometheus metrics, distributed traces, and structured application logs feed the operational dashboa... |
| strategy_b | 3 | doc-traffic-spikes | 0.151 | The operations playbook assumes that demand spikes arrive faster than infrastructure can always prov... |

**Observations**

- Top-ranked document changed from ['doc-backend-resilience'] to ['doc-redis-cache'] after expansion.
- Expanded retrieval achieved a stronger top-1 similarity score.
- Expanded retrieval surfaced additional relevant context from doc-observability, doc-traffic-spikes.

**Relevance analysis**

- Strategy A recall@k: 0.5
- Strategy B recall@k: 1.0
- Strategy A MRR: 0.5
- Strategy B MRR: 1.0

Expanded retrieval performed better when the rewrite injected infrastructure-specific vocabulary that matched the indexed engineering content more directly.

### Query: How do we avoid outages during service failures?

**Expanded query**: How do we avoid outages during service failures? high availability architecture graceful degradation multi-az failover circuit breaker and retry behavior

| Strategy | Rank | Document | Score | Preview |
|---|---:|---|---:|---|
| strategy_a | 1 | doc-observability | 0.125 | Prometheus metrics, distributed traces, and structured application logs feed the operational dashboa... |
| strategy_a | 2 | doc-microservices | 0.120 | Services are organized around bounded business capabilities rather than database tables. That keeps ... |
| strategy_a | 3 | doc-service-mesh | 0.109 | East-west traffic inside the cluster is mediated by a service mesh that standardizes mTLS, retry bud... |
| strategy_b | 1 | doc-service-mesh | 0.217 | East-west traffic inside the cluster is mediated by a service mesh that standardizes mTLS, retry bud... |
| strategy_b | 2 | doc-observability | 0.213 | Prometheus metrics, distributed traces, and structured application logs feed the operational dashboa... |
| strategy_b | 3 | doc-microservices | 0.201 | Services are organized around bounded business capabilities rather than database tables. That keeps ... |

**Observations**

- Top-ranked document changed from ['doc-observability'] to ['doc-service-mesh'] after expansion.
- Expanded retrieval achieved a stronger top-1 similarity score.

**Relevance analysis**

- Strategy A recall@k: 0.3333333333333333
- Strategy B recall@k: 0.3333333333333333
- Strategy A MRR: 0.3333333333333333
- Strategy B MRR: 1.0

Expanded retrieval performed better when the rewrite injected infrastructure-specific vocabulary that matched the indexed engineering content more directly.

### Query: How are releases kept safe in production?

**Expanded query**: How are releases kept safe in production? ci/cd pipeline gates progressive deployment rollout canary analysis automated rollback safeguards service health verification

| Strategy | Rank | Document | Score | Preview |
|---|---:|---|---:|---|
| strategy_a | 1 | doc-aws-ha | 0.247 | Production workloads are spread across multiple availability zones with stateless compute in an Auto... |
| strategy_a | 2 | doc-service-mesh | 0.074 | East-west traffic inside the cluster is mediated by a service mesh that standardizes mTLS, retry bud... |
| strategy_a | 3 | doc-observability | 0.053 | Prometheus metrics, distributed traces, and structured application logs feed the operational dashboa... |
| strategy_b | 1 | doc-aws-ha | 0.207 | Production workloads are spread across multiple availability zones with stateless compute in an Auto... |
| strategy_b | 2 | doc-cicd | 0.156 | Each deployment passes through build validation, unit tests, contract checks, and a canary stage bef... |
| strategy_b | 3 | doc-observability | 0.118 | Prometheus metrics, distributed traces, and structured application logs feed the operational dashboa... |

**Observations**

- Expanded retrieval surfaced additional relevant context from doc-cicd.

**Relevance analysis**

- Strategy A recall@k: 0.5
- Strategy B recall@k: 1.0
- Strategy A MRR: 0.3333333333333333
- Strategy B MRR: 0.5

Expanded retrieval performed better when the rewrite injected infrastructure-specific vocabulary that matched the indexed engineering content more directly.
