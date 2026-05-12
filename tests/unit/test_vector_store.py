from app.db.vector_store import VectorStore
from app.services.ingestion.chunker import ChunkRecord


def test_vector_store_returns_ranked_hits():
    store = VectorStore(dimension=3)
    chunks = [
        ChunkRecord(
            chunk_id="a",
            document_id="doc-a",
            title="A",
            content="autoscaling policy",
            source="local",
            chunk_index=0,
            metadata={},
        ),
        ChunkRecord(
            chunk_id="b",
            document_id="doc-b",
            title="B",
            content="redis cache",
            source="local",
            chunk_index=0,
            metadata={},
        ),
    ]
    store.add_chunks(chunks, embeddings=[[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]])

    hits = store.search([1.0, 0.0, 0.0], top_k=1)

    assert hits[0].document_id == "doc-a"
    assert hits[0].rank == 1
