import time
from fastapi import APIRouter, HTTPException
from backend.app.schemas.pydantic_models import (
    ChatRequest, ChatResponse, ContextChunk,
    CompareModelsRequest, CompareModelsResponse, CompareModelResult
)
from rag.rag_pipeline import rag_pipeline
from services.retrieval_service import retrieval_service
from services.guardrails_service import guardrails_service
from services.routing_service import routing_service
from services.hallucination_service import hallucination_service
from services.llm_service import llm_service
from rag.prompt_builder import PromptBuilder
from backend.app.config import settings

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
        confidence_score=hallucination_eval["groundedness_score"],
        is_fallback=result.get("is_fallback", False),
        warning=result.get("warning") or (f"Fallback Engine: {result.get('answer_error')}" if result.get("is_fallback") else None)
    )

@router.post("/compare-models", response_model=CompareModelsResponse)
async def compare_models_endpoint(request: CompareModelsRequest):
    """
    Simultaneously compares multiple Groq Cloud models on the exact same student question,
    measuring latency, grounding score, hallucination rate, and generated response side-by-side.
    """
    guard_check = guardrails_service.validate_input(request.prompt)
    if not guard_check["is_valid"]:
        raise HTTPException(status_code=400, detail=guard_check["reason"])

    models_to_compare = request.models or [
        "openai/gpt-oss-20b", "openai/gpt-oss-120b", "qwen/qwen3.8-27b"
    ]

    retrieval_start = time.time()
    context_chunks = []
    if request.use_rag:
        context_chunks = retrieval_service.retrieve(
            query=request.prompt,
            top_k=request.top_k,
            threshold=settings.SIMILARITY_THRESHOLD
        )
    retrieval_ms = round((time.time() - retrieval_start) * 1000, 2)

    prompt = PromptBuilder.build_chat_prompt(
        question=request.prompt,
        context_chunks=context_chunks,
        use_rag=request.use_rag
    )

    results = []
    for model_name in models_to_compare:
        gen = llm_service.generate(
            prompt=prompt,
            model=model_name,
            temperature=0.2,
            max_tokens=1536
        )
        answer = gen.get("text", "")
        latency = gen.get("latency_ms", 0.0)
        provider = gen.get("provider", "Groq Cloud LPU")

        h_eval = hallucination_service.analyze_hallucination(
            answer=answer,
            context_chunks=context_chunks
        )

        results.append(CompareModelResult(
            model=model_name,
            answer=answer,
            latency_ms=latency,
            grounding_score=h_eval.get("groundedness_score", 1.0),
            hallucination_rate=h_eval.get("hallucination_rate", 0.0),
            token_count=gen.get("eval_count", len(answer.split())),
            provider=provider
        ))

    context_objects = [
        ContextChunk(
            content=c["content"],
            source=c["source"],
            score=c["score"],
            chunk_id=c.get("chunk_id"),
            metadata=c.get("metadata")
        ) for c in context_chunks
    ]

    return CompareModelsResponse(
        prompt=request.prompt,
        used_rag=request.use_rag,
        retrieved_chunks_count=len(context_chunks),
        retrieval_latency_ms=retrieval_ms,
        results=results,
        context=context_objects
    )
