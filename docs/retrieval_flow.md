# Retrieval Flow

Strategy A is intentionally minimal: the raw user query is embedded and sent directly through vector similarity search. This represents the baseline many teams start with when building semantic search quickly.

Strategy B inserts a lightweight rewrite stage before embedding generation. The mocked Vertex AI model enriches vague engineering questions with domain-specific language such as autoscaling, cache hit ratio, multi-AZ failover, and canary rollback. That rewritten query then follows the same embedding and vector search path as Strategy A.

Both strategies share the same chunk index and scoring method. That makes the benchmark fair: the only variable is the richer retrieval query. When Strategy B improves recall or rank, the gain comes from better semantic intent representation rather than a different datastore or scorer.
