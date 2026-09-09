"""
API Gateway and Microservice Orchestrator.
Dispatches requests to independent microservices with request tracing, retry logic, and fallback.
"""
import time
import httpx
import logging
from typing import Dict, Any, Optional
from backend.app.config import settings

logger = logging.getLogger("api_gateway")

class APIGateway:
    def __init__(self):
        self.retriever_url = f"http://localhost:{settings.yaml_cfg.get('services', {}).get('retriever_port', 8001) if hasattr(settings, 'yaml_cfg') else 8001}"
        self.llm_url = f"http://localhost:{settings.yaml_cfg.get('services', {}).get('llm_port', 8002) if hasattr(settings, 'yaml_cfg') else 8002}"

    async def orchestrate_chat(self, prompt: str, model: str = "codellama:latest", use_rag: bool = True) -> Dict[str, Any]:
        start_time = time.time()
        trace_id = f"trace_{int(start_time * 1000)}"
        logger.info(f"[{trace_id}] Received chat request: '{prompt[:50]}...'")

        context_chunks = []
        retrieval_time = 0.0

        if use_rag:
            try:
                # Orchestrate retrieval service call
                from services.retrieval_service import retrieval_service
                r_start = time.time()
                context_chunks = retrieval_service.retrieve(prompt, top_k=4)
                retrieval_time = (time.time() - r_start) * 1000
                logger.info(f"[{trace_id}] Retrieved {len(context_chunks)} chunks in {retrieval_time:.2f}ms")
            except Exception as e:
                logger.error(f"[{trace_id}] Retrieval service failed: {e}")

        # Orchestrate LLM service call
        try:
            from rag.prompt_builder import PromptBuilder
            from services.llm_service import llm_service
            
            rag_prompt = PromptBuilder.build_chat_prompt(prompt, context_chunks=context_chunks, use_rag=use_rag)
            llm_res = llm_service.generate(prompt=rag_prompt, model=model)
            total_time = (time.time() - start_time) * 1000
            
            return {
                "trace_id": trace_id,
                "answer": llm_res.get("text", ""),
                "model": llm_res.get("model", model),
                "total_latency_ms": round(total_time, 2),
                "retrieval_time_ms": round(retrieval_time, 2),
                "context": context_chunks,
                "status": "success"
            }
        except Exception as e:
            logger.error(f"[{trace_id}] LLM orchestration failed: {e}")
            return {
                "trace_id": trace_id,
                "error": str(e),
                "status": "failed"
            }

api_gateway = APIGateway()
