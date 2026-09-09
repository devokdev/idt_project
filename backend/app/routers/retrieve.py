import time
from fastapi import APIRouter
from backend.app.schemas.pydantic_models import (
    RetrieveRequest, RetrieveResponse, ContextChunk,
    EmbedRequest, EmbedResponse, SuggestionResponse
)
from services.retrieval_service import retrieval_service
from services.embedding_service import embedding_service

router = APIRouter(prefix="", tags=["Retrieval & Embeddings"])

SUGGESTION_DATABASE = [
    "How is the final-year project evaluation rubric scored?",
    "What is the recommended tech stack and architecture for my project?",
    "What are the mandatory deliverables for project synopsis?",
    "What is the standard Git branching workflow for team projects?",
    "What are the most common viva defense questions for external examiners?",
    "How to compute precision, recall, and MRR for RAG evaluation?",
    "How to dockerize FastAPI and ChromaDB with Docker Compose?",
    "What are the guidelines for academic plagiarism and thesis submission?"
]

@router.post("/retrieve", response_model=RetrieveResponse)
async def retrieve_endpoint(request: RetrieveRequest):
    """Retrieve top-K semantic context chunks from ChromaDB."""
    start = time.time()
    results = retrieval_service.retrieve(
        query=request.query,
        top_k=request.top_k,
        threshold=request.min_score or 0.2,
        collection_name=request.collection
    )
    latency = (time.time() - start) * 1000

    chunks = [
        ContextChunk(
            content=r["content"],
            source=r["source"],
            score=r["score"],
            chunk_id=r.get("chunk_id"),
            metadata=r.get("metadata")
        ) for r in results
    ]

    return RetrieveResponse(
        query=request.query,
        results=chunks,
        total_retrieved=len(chunks),
        latency_ms=round(latency, 2)
    )

@router.post("/embed", response_model=EmbedResponse)
async def embed_endpoint(request: EmbedRequest):
    """Generates dense vector embeddings for input texts."""
    vectors = embedding_service.embed_texts(request.texts)
    return EmbedResponse(
        embeddings=vectors,
        dimension=embedding_service.dimension,
        count=len(vectors)
    )

@router.get("/suggestions", response_model=SuggestionResponse)
async def suggestions_endpoint(q: str = ""):
    """Prompt autocomplete suggestions while typing."""
    q_clean = q.lower().strip()
    if not q_clean:
        return SuggestionResponse(query_prefix=q, suggestions=SUGGESTION_DATABASE[:5])
    
    matches = [s for s in SUGGESTION_DATABASE if q_clean in s.lower()]
    if not matches:
        matches = SUGGESTION_DATABASE[:5]
    
    return SuggestionResponse(query_prefix=q, suggestions=matches[:5])
