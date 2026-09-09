import re
from typing import Dict, Any, List
from backend.app.config import settings

class GuardrailsService:
    """
    Input validation, safety guardrails, domain relevance checking, and output sanitization.
    """
    def __init__(self):
        self.blocked_keywords = [
            "hack into university database",
            "steal credentials",
            "bypass authentication maliciously",
            "confidential exam paper leak",
            "exploit zero-day",
            "ddos attack script"
        ]
        self.academic_domains = [
            "project", "architecture", "rag", "fastapi", "docker", "llm", "database",
            "git", "viva", "rubric", "evaluation", "proposal", "code", "ml", "ai",
            "thesis", "testing", "pytest", "pipeline", "guidelines", "marks"
        ]

    def validate_input(self, prompt: str) -> Dict[str, Any]:
        cleaned = prompt.strip()
        
        # Length checks
        if len(cleaned) < settings.guardrails_config.get("min_prompt_length", 3) if hasattr(settings, "guardrails_config") else len(cleaned) < 3:
            return {
                "is_valid": False,
                "reason": "Prompt is too short. Please provide a clear question."
            }
        if len(cleaned) > 4000:
            return {
                "is_valid": False,
                "reason": "Prompt exceeds maximum length of 4000 characters."
            }

        prompt_lower = cleaned.lower()
        
        # Block malicious or disallowed keywords
        for keyword in self.blocked_keywords:
            if keyword in prompt_lower:
                return {
                    "is_valid": False,
                    "reason": f"Security Guardrail Triggered: Request violates academic ethical guidelines ({keyword})."
                }

        # Check domain relevance (soft guardrail)
        matches = [d for d in self.academic_domains if d in prompt_lower]
        if not matches and len(cleaned.split()) > 4:
            # Still allow, but flag as general query
            return {
                "is_valid": True,
                "domain_classification": "general_or_out_of_scope",
                "warning": "Note: Your question may not be directly related to final-year project guidance."
            }

        return {
            "is_valid": True,
            "domain_classification": "academic_project_in_scope"
        }

guardrails_service = GuardrailsService()
