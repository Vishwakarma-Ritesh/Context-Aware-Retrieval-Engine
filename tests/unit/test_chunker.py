from app.services.ingestion.chunker import DocumentChunker


def test_chunker_generates_traceable_chunk_ids():
    documents = [
        {
            "document_id": "doc-test",
            "title": "Test",
            "source": "local",
            "paragraphs": ["one two three", "four five six"],
        }
    ]

    chunks = DocumentChunker(max_chunk_tokens=3).chunk_documents(documents)

    assert chunks[0].chunk_id == "doc-test-chunk-0"
    assert chunks[1].chunk_id == "doc-test-chunk-1"
