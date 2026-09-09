from fastapi import APIRouter
from backend.app.schemas.pydantic_models import ModelsListResponse, ModelInfo
from services.llm_service import llm_service
from backend.app.config import settings

router = APIRouter(prefix="", tags=["Models & Inference Engines"])

MODEL_REGISTRY = [
    {
        "name": "codellama:latest",
        "description": "Code Llama 7B Instruct - Specialized for code generation, software architecture, and debugging.",
        "size": "3.8 GB",
    },
    {
        "name": "starcoder2:latest",
        "description": "StarCoder2 - Multi-language code intelligence and syntax validation model.",
        "size": "1.7 GB",
    },
    {
        "name": "phi3:latest",
        "description": "Phi-3 Mini (3.8B) - Lightweight, fast reasoning, high-efficiency model.",
        "size": "2.2 GB",
    }
]

@router.get("/models", response_model=ModelsListResponse)
async def list_models():
    """Lists supported and installed LLM models."""
    health_status = llm_service.check_health()
    available_in_ollama = health_status.get("available_models", [])
    
    models_info = []
    for m in MODEL_REGISTRY:
        is_avail = (m["name"] in available_in_ollama) or health_status.get("ollama_reachable", False)
        models_info.append(ModelInfo(
            name=m["name"],
            description=m["description"],
            size=m["size"],
            status="Available / Ready" if is_avail else "Download required (ollama pull)",
            is_available=is_avail
        ))

    return ModelsListResponse(
        models=models_info,
        current_default=settings.DEFAULT_MODEL
    )
