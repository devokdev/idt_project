import pytest
from services.repo_analyzer_service import repo_analyzer_service
from backend.app.config import BASE_DIR

def test_repo_indexer_and_query():
    # Index current repository files
    index_res = repo_analyzer_service.index_repository(str(BASE_DIR))
    assert "indexed_files" in index_res
    assert index_res["indexed_files"] > 0
    
    # Run a repository architectural query
    query = "How does the RAG pipeline interact with the retrieval service?"
    answer_res = repo_analyzer_service.answer_repository_query(query, top_k=3)
    
    assert "answer" in answer_res
    assert len(answer_res["answer"]) > 10
    assert "referenced_files" in answer_res
    assert "latency_ms" in answer_res
