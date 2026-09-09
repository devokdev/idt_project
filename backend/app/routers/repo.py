from fastapi import APIRouter
from backend.app.schemas.pydantic_models import (
    RepoQuestionRequest, RepoQuestionResponse, ContextChunk
)
from services.repo_analyzer_service import repo_analyzer_service
from backend.app.config import BASE_DIR

router = APIRouter(prefix="", tags=["Repository Code Intelligence"])

@router.post("/repo/index")
async def index_repository_endpoint(project_path: str = None):
    """Indexes codebase files and AST structures into the code vector store."""
    target_path = project_path or str(BASE_DIR)
    result = repo_analyzer_service.index_repository(target_path)
    return result

@router.post("/repo/query", response_model=RepoQuestionResponse)
async def query_repository_endpoint(request: RepoQuestionRequest):
    """Answers codebase questions spanning multiple files, imports, and architecture."""
    result = repo_analyzer_service.answer_repository_query(
        question=request.question,
        top_k=request.top_k
    )
    
    chunks = [
        ContextChunk(
            content=c["content"],
            source=c["source"],
            score=c["score"],
            chunk_id=c.get("chunk_id"),
            metadata=c.get("metadata")
        ) for c in result["context_chunks"]
    ]

    return RepoQuestionResponse(
        question=result["question"],
        answer=result["answer"],
        referenced_files=result["referenced_files"],
        context_chunks=chunks,
        latency_ms=result["latency_ms"]
    )
