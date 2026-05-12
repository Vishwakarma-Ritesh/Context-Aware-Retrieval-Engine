# AWS-Ready Architecture

The current implementation is local-first, but the boundaries were chosen so the same service can move into AWS without a redesign:

- Corpus storage can shift from `data/raw/technical_documents.json` to S3 by setting `AWS_S3_BUCKET` and `AWS_S3_KEY`.
- The in-memory vector store can be replaced by a managed retrieval backend while keeping the `VectorStore` abstraction stable.
- Structured logs are already container-friendly and map cleanly into CloudWatch.
- The Docker image and Kubernetes manifests support ECS, EKS, or an internal platform path.

For a free-tier friendly path, the easiest deployment is a single container plus S3-backed corpus snapshots. For production growth, the next step would be ECS or EKS with a managed vector service, a metadata store, and a scheduled benchmark job that publishes retrieval reports after every corpus refresh.
