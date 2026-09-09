import pytest
from services.retrieval_service import retrieval_service

def test_retrieval_service():
    stats = retrieval_service.get_stats()
    assert stats["embedding_dimension"] == 384
    
    query = "What is the weightage for technical implementation in evaluation rubric?"
    results = retrieval_service.retrieve(query, top_k=3)
    assert isinstance(results, list)
    if results:
        assert "content" in results[0]
        assert "score" in results[0]
        assert results[0]["score"] >= 0.0

def test_retrieval_deduplication():
    results = retrieval_service.retrieve("Git workflow and conventional commits", top_k=4)
    # Check that returned chunks are unique
    seen = set()
    for r in results:
        assert r["content"][:50] not in seen
        seen.add(r["content"][:50])
