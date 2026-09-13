from fastapi import APIRouter
from backend.app.schemas.pydantic_models import ModelsListResponse, ModelInfo
from services.llm_service import llm_service
from backend.app.config import settings

router = APIRouter(prefix="", tags=["Models & Inference Engines"])

MODEL_REGISTRY = [
    {
        "name": "openai/gpt-oss-20b",
        "description": "OpenAI GPT Open-Source 20B on Groq LPU - Ultra-low latency conversational mentor and RAG synthesizer.",
        "size": "20 Billion Parameters (LPU Hosted)",
    },
    {
        "name": "openai/gpt-oss-120b",
        "description": "OpenAI GPT Open-Source 120B on Groq LPU - Massive reasoning capacity for deep architectural trade-offs and code intelligence.",
        "size": "120 Billion Parameters (LPU Hosted)",
    },
    {
        "name": "qwen/qwen3.8-27b",
        "description": "Alibaba Qwen 3.8 27B on Groq LPU - High-speed reasoning, mathematics, and structured logic formulation.",
        "size": "27 Billion Parameters (LPU Hosted)",
    }
]

@router.get("/models", response_model=ModelsListResponse)
async def list_models():
    """Lists supported and active Groq LPU models."""
    health_status = llm_service.check_health()
    available_in_groq = health_status.get("available_models", [])
    
    models_info = []
    for m in MODEL_REGISTRY:
        is_avail = (m["name"] in available_in_groq) or health_status.get("groq_reachable", False)
        models_info.append(ModelInfo(
            name=m["name"],
            description=m["description"],
            size=m["size"],
            status="Available / High-Speed LPU" if is_avail else "Ready via Groq Cloud API",
            is_available=is_avail
        ))

    return ModelsListResponse(
        models=models_info,
        current_default=settings.DEFAULT_MODEL
    )
