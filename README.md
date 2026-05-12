# Semantic RAG Engine

`semantic-rag-engine` is a production-minded local Retrieval-Augmented Generation benchmark service built for a senior GenAI assessment. It compares raw vector search against AI-enhanced retrieval, keeps the architecture modular enough to evolve into a managed platform, and produces benchmark artifacts that show whether query expansion improves retrieval quality for realistic engineering questions.

## What it implements

- Strategy A: direct query embedding followed by vector similarity search
- Strategy B: heuristic query rewrite with mocked Vertex AI behavior before embedding and search
- Local embedding generation through `sentence-transformers/all-MiniLM-L6-v2`
- FAISS-backed vector search with a pure Python fallback for dependency-light environments
- Structured benchmark output in terminal, JSON, and Markdown formats
- Optional FastAPI `POST /search` endpoint
- Lightweight AWS integration through optional S3 dataset loading

## Architecture

The runtime is separated into clear boundaries:

- `app/services/ingestion`: corpus loading, normalization, and chunking
- `app/services/embeddings`: model loading, caching, and embedding generation
- `app/db`: vector indexing and retrieval metadata mapping
- `app/services/retrieval`: query expansion, semantic search, and ranking comparison
- `app/services/benchmark`: evaluation, reporting, and benchmark execution
- `app/api`: optional FastAPI transport for search requests

The ingestion and retrieval layers are reusable across the benchmark runner and the API endpoint, so the benchmark path is not a one-off script. That makes the project look and behave like an internal platform service.

## Retrieval flow

1. Load the engineering corpus from local JSON or S3.
2. Normalize and chunk documents into indexable retrieval units.
3. Generate dense embeddings with `EmbeddingService`.
4. Store normalized vectors in FAISS using cosine similarity.
5. Run Strategy A directly on the original query.
6. Run Strategy B after expanding the query with a mocked Vertex AI rewrite model.
7. Compare rankings and score both strategies using recall@k and mean reciprocal rank.

## Why cosine similarity

Cosine similarity is preferred over Euclidean distance for dense text embeddings because the relative direction of the vector usually carries more semantic meaning than the raw magnitude. When two queries point in a similar direction in embedding space, cosine similarity keeps them close even if one vector has a larger norm. Euclidean distance is more sensitive to magnitude shifts and is therefore a weaker default for normalized semantic embeddings.

## Architecture Note

For submission-ready documentation focused on similarity metric selection and the production migration path to Vertex AI Vector Search, see:

- [Semantic RAG Architecture Note (PDF)](docs/semantic-rag-architecture-note.pdf)
- [Semantic RAG Architecture Note (PPTX)](docs/semantic-rag-architecture-note.pptx)

## Local setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements/dev.txt
python -m app.main
```

If the heavyweight ML dependencies are not installed, the code falls back to a deterministic local embedding path so the benchmark still runs. For the assessment submission, install the full requirements so the primary path uses `sentence-transformers` and `faiss-cpu`.

## Docker setup

```bash
docker compose -f infra/docker/docker-compose.yml up --build
```

## AWS setup

Set the following environment variables if the corpus should be loaded from S3 instead of the local JSON file:

```bash
AWS_REGION=us-east-1
AWS_S3_BUCKET=my-rag-dataset-bucket
AWS_S3_KEY=technical_documents.json
```

If S3 is unavailable or the object cannot be fetched, the loader falls back to the local dataset automatically.

## Benchmark behavior

Running `python -m app.main` executes the benchmark suite and prints a strategy-by-strategy comparison for each query. It also writes:

- `benchmark_results/benchmark_results.json`
- `benchmark_results/retrieval_benchmark.md`

Each query entry includes the original query, expanded query, top retrieved chunks, similarity scores, ranking observations, and structured evaluation metrics.

## Optional API

Install API dependencies and run:

```bash
uvicorn app.main:create_app --factory --host 0.0.0.0 --port 8000
```

Example request:

```json
{
  "query": "How does the system handle peak load?",
  "top_k": 3
}
```

## Migration path to Vertex AI Matching Engine

The current design isolates vector indexing behind `VectorStore`, which is the seam to replace when moving to Vertex AI Matching Engine or another managed vector database. The same applies to query expansion: `QueryExpander` already abstracts the generative step, so the local mocked model can be replaced with a real Vertex AI `GenerativeModel` client without touching the retriever contract.

## Production scaling discussion

For a production rollout, the next steps would be:

- persist chunk metadata in PostgreSQL or DynamoDB
- move vector search from local FAISS to a managed vector backend
- publish benchmark reports on every corpus refresh or model change
- run background ingestion jobs rather than rebuilding indexes inline
- add request authentication, rate limiting, and usage telemetry to the API layer

This repo is intentionally local and assessment-friendly, but the dependency boundaries are aligned with a realistic internal retrieval platform.
