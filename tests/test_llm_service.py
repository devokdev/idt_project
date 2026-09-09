import pytest
from services.llm_service import llm_service

def test_llm_service_health():
    health = llm_service.check_health()
    assert "status" in health
    assert "available_models" in health

def test_llm_generation_and_fallback():
    prompt = "Explain the final-year project evaluation rubric."
    result = llm_service.generate(prompt=prompt, model="codellama:latest")
    assert "text" in result
    assert len(result["text"]) > 20
    assert result["model"] == "codellama:latest"
    assert "latency_ms" in result
    assert result["latency_ms"] >= 0

def test_llm_routing_models():
    for model in ["codellama:latest", "starcoder2:latest", "phi3:latest"]:
        res = llm_service.generate(prompt="What is GitFlow?", model=model)
        assert res["model"] == model
        assert len(res["text"]) > 10
