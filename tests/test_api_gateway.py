import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_chat_endpoint_success():
    payload = {
        "prompt": "What are the common viva defense questions for final-year projects?",
        "model": "codellama:latest",
        "use_rag": True,
        "top_k": 3
    }
    response = client.post("/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert data["model"] == "codellama:latest"
    assert "latency_ms" in data
    assert data["used_rag"] is True

def test_retrieve_endpoint():
    payload = {
        "query": "Evaluation rubric breakdown and marks",
        "top_k": 2
    }
    response = client.post("/retrieve", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert "total_retrieved" in data

def test_embed_endpoint():
    payload = {
        "texts": ["Sentence 1", "Sentence 2"]
    }
    response = client.post("/embed", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["dimension"] == 384
    assert data["count"] == 2

def test_models_endpoint():
    response = client.get("/models")
    assert response.status_code == 200
    data = response.json()
    assert "models" in data
    assert len(data["models"]) >= 3

def test_suggestions_endpoint():
    response = client.get("/suggestions?q=rubric")
    assert response.status_code == 200
    data = response.json()
    assert "suggestions" in data
    assert len(data["suggestions"]) > 0
