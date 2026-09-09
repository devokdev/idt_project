import time
import json
import logging
import httpx
from typing import Dict, Any, Optional, List
from backend.app.config import settings

logger = logging.getLogger("llm_service")
logging.basicConfig(level=logging.INFO)

class LLMService:
    """
    Robust Ollama LLM Service supporting Code Llama, StarCoder2, and Phi-3 Mini.
    Includes timeouts, exponential retry backoff, fallback execution, and simulated inference
    for zero-dependency offline environments/testing.
    """
    def __init__(self, base_url: Optional[str] = None):
        self.base_url = (base_url or settings.OLLAMA_BASE_URL).rstrip("/")
        self.default_model = settings.DEFAULT_MODEL
        self.timeout = settings.LLM_TIMEOUT
        self.max_retries = settings.MAX_RETRIES

    def check_health(self) -> Dict[str, Any]:
        """Verify if Ollama service is reachable."""
        try:
            with httpx.Client(timeout=3.0) as client:
                res = client.get(f"{self.base_url}/api/tags")
                if res.status_code == 200:
                    models_data = res.json().get("models", [])
                    model_names = [m.get("name") for m in models_data]
                    return {
                        "status": "healthy",
                        "ollama_reachable": True,
                        "available_models": model_names
                    }
        except Exception as e:
            logger.warning(f"Ollama server not reachable at {self.base_url}: {e}. Mock/Fallback mode active.")
        
        return {
            "status": "offline_fallback_ready",
            "ollama_reachable": False,
            "available_models": settings.SUPPORTED_MODELS
        }

    def generate(
        self, 
        prompt: str, 
        model: Optional[str] = None, 
        temperature: float = 0.2,
        system_prompt: Optional[str] = None,
        stream: bool = False
    ) -> Dict[str, Any]:
        """
        Executes text generation with automatic retries, timing metrics, and offline fallback.
        """
        target_model = model or self.default_model
        start_time = time.time()
        
        payload = {
            "model": target_model,
            "prompt": prompt,
            "stream": stream,
            "options": {
                "temperature": temperature,
                "top_p": 0.9,
                "num_ctx": 1536,
                "num_predict": 512
            }
        }
        if system_prompt:
            payload["system"] = system_prompt

        last_error = None
        for attempt in range(1, self.max_retries + 1):
            try:
                with httpx.Client(timeout=self.timeout) as client:
                    response = client.post(
                        f"{self.base_url}/api/generate",
                        json=payload
                    )
                    if response.status_code == 200:
                        data = response.json()
                        latency = (time.time() - start_time) * 1000
                        return {
                            "text": data.get("response", ""),
                            "model": target_model,
                            "latency_ms": round(latency, 2),
                            "prompt_eval_count": data.get("prompt_eval_count", len(prompt.split())),
                            "eval_count": data.get("eval_count", len(data.get("response", "").split())),
                            "is_fallback": False
                        }
                    elif response.status_code == 404:
                        logger.warning(f"Model '{target_model}' not found in local Ollama instance (HTTP 404). Falling back immediately.")
                        break
                    else:
                        logger.warning(f"Ollama returned HTTP {response.status_code} on attempt {attempt}: {response.text}")
            except (httpx.RequestError, httpx.TimeoutException) as e:
                last_error = str(e)
                logger.warning(f"Attempt {attempt}/{self.max_retries} failed connecting to Ollama ({e}). Retrying...")
                time.sleep(0.5 * (1.5 ** attempt))

        # If Ollama is offline or model is pulling, provide high-quality fallback synthesis
        logger.info(f"Using deterministic architectural fallback response for model '{target_model}'.")
        fallback_text = self._generate_fallback_response(prompt, target_model)
        latency = (time.time() - start_time) * 1000
        return {
            "text": fallback_text,
            "model": target_model,
            "latency_ms": round(latency, 2),
            "prompt_eval_count": len(prompt.split()),
            "eval_count": len(fallback_text.split()),
            "is_fallback": True,
            "warning": f"Generated via Academic Mentor Engine (Ollama daemon offline: {last_error})"
        }

    def _generate_fallback_response(self, prompt: str, model: str) -> str:
        """
        Universal dynamic RAG summarizer when Ollama is offline or pulling models.
        Extracts, ranks, and structures factual sentences from retrieved context documents for any question.
        """
        prompt_lower = prompt.lower()
        
        # Check if RAG context is present in the assembled prompt
        if "### academic & project guidelines context:" in prompt_lower:
            try:
                context_part = prompt.split("### ACADEMIC & PROJECT GUIDELINES CONTEXT:")[1].split("### INSTRUCTION FOR MENTOR:")[0].strip()
                student_q = prompt.split("Student Question:")[1].split("Mentor Answer:")[0].strip()
                
                # Clean document delimiters and extract sections
                lines = [l.strip() for l in context_part.split("\n") if l.strip()]
                
                meaningful_points = []
                current_section = ""
                for line in lines:
                    if line.startswith("---") or line.startswith("==="):
                        continue
                    if line.startswith("### ") or line.startswith("## "):
                        current_section = line.lstrip("#").strip()
                        continue
                    cleaned = line.lstrip("*-#0123456789. ").strip()
                    if len(cleaned) > 15:
                        if current_section and not cleaned.startswith(current_section):
                            meaningful_points.append(f"**{current_section}**: {cleaned}")
                        else:
                            meaningful_points.append(cleaned)
                
                # Extract query keywords
                q_words = set(w.lower() for w in student_q.replace("?", "").replace(",", "").split() if len(w) > 2)
                
                # Rank sentences by keyword overlap and semantic relevance
                ranked_points = []
                for pt in meaningful_points:
                    pt_lower = pt.lower()
                    overlap = sum(2 if w in pt_lower else 0 for w in q_words)
                    # Boost Q&A and rubric answers
                    if "answer" in pt_lower or "rubric" in pt_lower or "guideline" in pt_lower or "deliverable" in pt_lower:
                        overlap += 1
                    ranked_points.append((overlap, pt))
                
                ranked_points.sort(key=lambda x: x[0], reverse=True)
                top_facts = [pt for _, pt in ranked_points[:7]] if ranked_points else meaningful_points[:5]
                
                formatted_facts = "\n".join([f"{i+1}. {fact}" for i, fact in enumerate(top_facts)])
                
                return (
                    f"### AI Project Mentor Guidance [{model}]:\n\n"
                    f"Based on the official university academic guidelines and project documentation:\n\n"
                    f"{formatted_facts}\n\n"
                    f"**Actionable Next Steps**:\n"
                    f"- Verify deliverables against the official university project rubrics.\n"
                    f"- Ensure code test coverage meets or exceeds standard evaluation thresholds (>80%).\n"
                    f"- Document all architectural decisions and API specifications in your project report."
                )
            except Exception as e:
                logger.error(f"Error in dynamic RAG extraction: {e}")
        
        # General response when RAG is disabled or no context is found
        return (
            f"### AI Project Mentor Guidance [{model}]:\n\n"
            "For your final-year project inquiry, follow these standard steps:\n"
            "1. **Requirements & Scope**: Define clear input-output specifications with strict validation schemas.\n"
            "2. **Architecture**: Decouple business logic, vector storage, and API routing microservices.\n"
            "3. **Quantitative Metrics**: Measure latency (P95/P99), accuracy, and resource utilization (RAM/CPU).\n"
            "4. **Verification**: Implement comprehensive Pytest unit and integration test suites for every component."
        )

# Global singleton
llm_service = LLMService()
