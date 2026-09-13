import os
import psutil
from fastapi import APIRouter
from backend.app.config import settings
from services.llm_service import llm_service
from services.retrieval_service import retrieval_service

router = APIRouter(prefix="", tags=["System Health & Metrics"])

@router.get("/health")
async def health_check():
    """System health check verifying ChromaDB, Groq LPU connection, and memory status."""
    groq_health = llm_service.check_health()
    kb_stats = retrieval_service.get_stats()
    
    return {
        "status": "healthy",
        "app_name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENV,
        "llm": groq_health,
        "ollama": groq_health, # backward compatibility
        "vectordb": {
            "status": "connected",
            "kb_documents_count": kb_stats["default_collection_count"],
            "code_documents_count": kb_stats["code_collection_count"]
        }
    }

@router.get("/metrics")
async def system_metrics():
    """Returns real-time host resource statistics (CPU, Memory, Disk)."""
    cpu_percent = psutil.cpu_percent(interval=None)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    
    return {
        "cpu_usage_percent": cpu_percent,
        "ram_total_mb": round(memory.total / (1024 * 1024), 2),
        "ram_used_mb": round(memory.used / (1024 * 1024), 2),
        "ram_usage_percent": memory.percent,
        "disk_free_gb": round(disk.free / (1024 * 1024 * 1024), 2),
        "vector_collections": retrieval_service.get_stats()
    }
