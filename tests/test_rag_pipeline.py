import pytest
from rag.rag_pipeline import rag_pipeline

def test_rag_pipeline_execution():
    question = "What are the key deliverables for the final-year project synopsis?"
    res = rag_pipeline.run(question=question, model="codellama:latest", use_rag=True)
    
    assert "answer" in res
    assert len(res["answer"]) > 20
    assert "latency_ms" in res
    assert "retrieval_time_ms" in res
    assert res["used_rag"] is True

def test_rag_vs_non_rag_comparison():
    question = "How is the project evaluation rubric distributed?"
    comp = rag_pipeline.compare_rag_vs_non_rag(question)
    
    assert "with_rag" in comp
    assert "without_rag" in comp
    assert "analysis" in comp
    assert comp["with_rag"]["used_rag"] is True
    assert comp["without_rag"]["used_rag"] is False
