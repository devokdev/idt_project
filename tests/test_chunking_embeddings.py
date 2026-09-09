import pytest
from rag.chunker import TextChunker
from rag.document_loader import DocumentLoader
from services.embedding_service import embedding_service
from backend.app.config import settings
from pathlib import Path

def test_document_loader():
    doc_path = Path(settings.DOCUMENTS_DIR) / "project_guidelines.md"
    loaded = DocumentLoader.load_file(str(doc_path))
    assert len(loaded) > 0
    assert "content" in loaded[0]
    assert loaded[0]["metadata"]["source"] == "project_guidelines.md"

def test_chunker_sliding_window():
    chunker = TextChunker(chunk_size=50, chunk_overlap=10)
    sample_text = "Word " * 150
    doc = {"content": sample_text, "metadata": {"source": "test.md"}}
    chunks = chunker.chunk_document(doc)
    assert len(chunks) > 1
    assert "chunk_index" in chunks[0]["metadata"]
    assert chunks[0]["chunk_id"].startswith("test.md_chunk_0")

def test_embedding_service():
    texts = ["FastAPI backend architecture", "ChromaDB vector store retrieval"]
    embeddings = embedding_service.embed_texts(texts)
    assert len(embeddings) == 2
    assert len(embeddings[0]) == 384
