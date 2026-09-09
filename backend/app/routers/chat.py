from fastapi import APIRouter, HTTPException
from backend.app.schemas.pydantic_models import ChatRequest, ChatResponse, ContextChunk
from rag.rag_pipeline import rag_pipeline
from services.guardrails_service import guardrails_service
from services.routing_service import routing_service
from services.hallucination_service import hallucination_service

router = APIRouter(prefix="", tags=["Chat & Mentoring"])

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Main Chat & Project Mentoring endpoint.
    Applies guardrails, model routing, RAG context retrieval, LLM generation, and hallucination scoring.
    """
    # 1. Guardrail input validation
    guard_check = guardrails_service.validate_input(request.prompt)
    if not guard_check["is_valid"]:
        raise HTTPException(status_code=400, detail=guard_check["reason"])

    # 2. Dynamic Model Routing if model is set to default
    target_model = request.model
    if not target_model or target_model == "auto":
        route_decision = routing_service.route_model(request.prompt)
        target_model = route_decision["selected_model"]

    # 3. Execute RAG Pipeline
    result = rag_pipeline.run(
        question=request.prompt,
        model=target_model,
        use_rag=request.use_rag,
        top_k=request.top_k,
        temperature=request.temperature or 0.2
    )

    # 4. Hallucination analysis
    hallucination_eval = hallucination_service.analyze_hallucination(
        answer=result["answer"],
        context_chunks=result["context"]
    )

    context_objects = [
        ContextChunk(
            content=c["content"],
            source=c["source"],
            score=c["score"],
            chunk_id=c.get("chunk_id"),
            metadata=c.get("metadata")
        ) for c in result["context"]
    ]

    return ChatResponse(
        answer=result["answer"],
        model=result["model"],
        latency_ms=result["latency_ms"],
        retrieval_time_ms=result["retrieval_time_ms"],
        llm_time_ms=result["llm_time_ms"],
        used_rag=result["used_rag"],
        context=context_objects,
        guardrail_status=guard_check.get("domain_classification", "passed"),
        confidence_score=hallucination_eval["groundedness_score"]
    )
