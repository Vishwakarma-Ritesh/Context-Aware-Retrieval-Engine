# Architecture Overview

The service is organized like an internal backend component rather than a notebook project. Ingestion, embeddings, vector indexing, retrieval orchestration, benchmarking, API transport, and infrastructure concerns are separated by package boundaries so the retrieval stack can evolve without forcing changes into unrelated layers.

At runtime, the benchmark flow is:

1. Load the technical corpus from local JSON or optionally from S3.
2. Normalize and chunk documents into retrieval-ready records.
3. Generate embeddings through `EmbeddingService`.
4. Store normalized vectors in a `VectorStore` backed by FAISS when available.
5. Compare raw retrieval against AI-enhanced retrieval with query expansion.
6. Score each strategy using recall@k and reciprocal rank.
7. Persist JSON and Markdown benchmark artifacts.

The same retrieval pipeline is also reused by the optional FastAPI endpoint, which keeps the API layer thin and prevents benchmark-only logic from leaking into transport code.
