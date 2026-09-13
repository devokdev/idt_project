import pytest
from services.llm_service import llm_service

def test_llm_service_health():
    health = llm_service.check_health()
    assert "status" in health
    assert "available_models" in health
    assert health.get("groq_reachable") is True

def test_llm_generation_and_fallback():
    prompt = "Explain the final-year project evaluation rubric."
    result = llm_service.generate(prompt=prompt, model="openai/gpt-oss-20b")
    assert "text" in result
    assert len(result["text"]) > 20
    assert result["model"] == "openai/gpt-oss-20b"
    assert "latency_ms" in result
    assert result["latency_ms"] >= 0

def test_llm_routing_models():
    for model in ["openai/gpt-oss-20b", "openai/gpt-oss-120b", "qwen/qwen3.8-27b"]:
        res = llm_service.generate(prompt="What is GitFlow?", model=model, max_tokens=50)
        assert res["model"] == model
        assert len(res["text"]) > 10
