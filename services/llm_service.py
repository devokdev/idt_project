import time
import json
import logging
import re
import httpx
from typing import Dict, Any, Optional, List
from backend.app.config import settings

logger = logging.getLogger("llm_service")
logging.basicConfig(level=logging.INFO)

class LLMService:
    """
    High-Performance LLM Service powered by Groq LPU Cloud Engine.
    Supports ultra-fast inference across Groq models (openai/gpt-oss-20b, openai/gpt-oss-120b,
    qwen/qwen3.8-27b, groq/compound-mini), with fallback execution for offline/network-restricted setups.
    """
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        self.api_key = api_key or settings.GROQ_API_KEY
        self.base_url = (base_url or settings.GROQ_BASE_URL).rstrip("/")
        self.default_model = settings.DEFAULT_MODEL
        self.timeout = settings.LLM_TIMEOUT
        self.max_retries = settings.MAX_RETRIES

    def check_health(self) -> Dict[str, Any]:
        """Verify if Groq Cloud API service is reachable with current API key."""
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        try:
            with httpx.Client(timeout=4.0) as client:
                res = client.get(f"{self.base_url}/models", headers=headers)
                if res.status_code == 200:
                    models_data = res.json().get("data", [])
                    active_models = [m.get("id") for m in models_data if m.get("active", True)]
                    return {
                        "status": "healthy",
                        "provider": "Groq Cloud LPU",
                        "groq_reachable": True,
                        "available_models": active_models,
                        "selected_default": self.default_model
                    }
                else:
                    logger.warning(f"Groq API returned HTTP {res.status_code}: {res.text}")
        except Exception as e:
            logger.warning(f"Groq API not reachable at {self.base_url}: {e}. Fallback engine ready.")

        return {
            "status": "offline_fallback_ready",
            "provider": "Groq Cloud (Offline/Fallback)",
            "groq_reachable": False,
            "available_models": settings.SUPPORTED_MODELS,
            "selected_default": self.default_model
        }

    def generate(
        self, 
        prompt: str, 
        model: Optional[str] = None, 
        temperature: float = 0.2,
        system_prompt: Optional[str] = None,
        stream: bool = False,
        max_tokens: int = 2048
    ) -> Dict[str, Any]:
        """
        Executes text generation using Groq API with reasoning token unwrapping,
        automatic retries, timing metrics, and offline fallback.
        """
        target_model = model or self.default_model
        if target_model in ["phi3:mini", "phi3:latest", "codellama:latest", "starcoder2:latest", "auto"]:
            target_model = self.default_model

        start_time = time.time()
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        else:
            messages.append({
                "role": "system",
                "content": (
                    "You are an expert AI Project Mentor for final-year engineering students. "
                    "Provide authoritative, structured, clear, and technically grounded answers "
                    "referencing the student's project documents, rubric marks, and software standards."
                )
            })

        messages.append({"role": "user", "content": prompt})

        # Cap completion tokens for models with strict OTPM rate limits
        actual_max_tokens = 768 if "qwen" in target_model.lower() else min(max_tokens, 1536)

        payload = {
            "model": target_model,
            "messages": messages,
            "temperature": max(0.0, min(1.0, temperature)),
            "max_completion_tokens": actual_max_tokens
        }

        last_error = None
        for attempt in range(1, self.max_retries + 1):
            try:
                with httpx.Client(timeout=self.timeout) as client:
                    response = client.post(
                        f"{self.base_url}/chat/completions",
                        headers=headers,
                        json=payload
                    )
                    if response.status_code == 200:
                        data = response.json()
                        latency = (time.time() - start_time) * 1000
                        choice = data.get("choices", [{}])[0]
                        msg_obj = choice.get("message", {})
                        
                        # Extract content or reasoning if content is empty
                        raw_content = msg_obj.get("content") or ""
                        reasoning_content = msg_obj.get("reasoning") or ""
                        
                        final_text = raw_content.strip()
                        if not final_text and reasoning_content.strip():
                            final_text = reasoning_content.strip()

                        # Strip thinking tags if present in some open-source models
                        final_text = re.sub(r"<think>[\s\S]*?</think>", "", final_text).strip()

                        usage = data.get("usage", {})
                        p_tokens = usage.get("prompt_tokens", len(prompt.split()))
                        c_tokens = usage.get("completion_tokens", len(final_text.split()))

                        return {
                            "text": final_text,
                            "model": target_model,
                            "latency_ms": round(latency, 2),
                            "prompt_eval_count": p_tokens,
                            "eval_count": c_tokens,
                            "is_fallback": False,
                            "provider": "Groq Cloud LPU"
                        }
                    elif response.status_code == 404:
                        logger.warning(f"Model '{target_model}' not found in Groq. Falling back.")
                        last_error = f"Model {target_model} 404 Not Found"
                        break
                    else:
                        last_error = f"HTTP {response.status_code}: {response.text}"
                        logger.warning(f"Groq API error on attempt {attempt}: {last_error}")
            except (httpx.RequestError, httpx.TimeoutException) as e:
                last_error = str(e)
                logger.warning(f"Attempt {attempt}/{self.max_retries} failed connecting to Groq ({e}). Retrying...")
                time.sleep(0.4 * attempt)

        # High quality fallback synthesis if Groq cloud is unreachable
        logger.info(f"Using deterministic fallback response for model '{target_model}'.")
        fallback_text = self._generate_fallback_response(prompt, target_model)
        latency = (time.time() - start_time) * 1000
        return {
            "text": fallback_text,
            "model": target_model,
            "latency_ms": round(latency, 2),
            "prompt_eval_count": len(prompt.split()),
            "eval_count": len(fallback_text.split()),
            "is_fallback": True,
            "provider": "Academic Mentor Engine (Fallback)",
            "warning": f"Generated via Academic Mentor Engine ({last_error})"
        }

    def _generate_fallback_response(self, prompt: str, model: str) -> str:
        """
        Universal dynamic RAG summarizer when external cloud API is offline.
        Extracts, ranks, and structures factual sentences from retrieved context documents.
        """
        prompt_lower = prompt.lower()
        
        # Check if RAG context is present in the assembled prompt
        if "### academic & project guidelines context:" in prompt_lower:
            try:
                context_part = prompt.split("### ACADEMIC & PROJECT GUIDELINES CONTEXT:")[1].split("### INSTRUCTION FOR MENTOR:")[0].strip()
                student_q = prompt.split("Student Question:")[1].split("Mentor Answer:")[0].strip()
                
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
                
                q_words = set(w.lower() for w in student_q.replace("?", "").replace(",", "").split() if len(w) > 2)
                
                ranked_points = []
                for pt in meaningful_points:
                    pt_lower = pt.lower()
                    overlap = sum(2 if w in pt_lower else 0 for w in q_words)
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
