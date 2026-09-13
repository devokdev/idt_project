from typing import Dict, Any

class RoutingService:
    """
    Classifies prompt complexity and selects optimal Groq LPU Model:
    - Code Snippets / Repository / Syntax / Debugging -> openai/gpt-oss-120b or openai/gpt-oss-20b
    - Fast Math / Logic / Reasoning -> qwen/qwen3.8-27b
    - Concise QA / Tool routing -> groq/compound-mini
    - Complex Architecture / Full Design / Rubrics -> openai/gpt-oss-120b
    """
    @staticmethod
    def route_model(prompt: str) -> Dict[str, Any]:
        p = prompt.lower()
        word_count = len(p.split())
        
        # Coding & Syntax patterns
        coding_signals = ["code", "function", "class", "syntax", "def ", "import ", "regex", "sql query", "fix bug", "ast", "test"]
        if any(sig in p for sig in coding_signals):
            return {
                "selected_model": "openai/gpt-oss-120b",
                "complexity": "code_intelligence",
                "rationale": "Query targets code architecture, syntax validation, or debugging (routed to OpenAI GPT-OSS 120B)."
            }
        
        # Complex Architecture & System Design
        complex_signals = [
            "architecture", "system design", "microservices", "trade-off", "roadmap",
            "lifecycle", "rubric", "comprehensive", "step by step", "docker compose"
        ]
        if any(sig in p for sig in complex_signals) or word_count > 25:
            return {
                "selected_model": "openai/gpt-oss-20b",
                "complexity": "high_architectural",
                "rationale": "Query requires multi-faceted academic synthesis and rubric cross-referencing (routed to OpenAI GPT-OSS 20B)."
            }

        # Fast reasoning & logic
        math_logic_signals = ["calculate", "marks", "formula", "precision", "mrr", "percentage", "time complexity"]
        if any(sig in p for sig in math_logic_signals):
            return {
                "selected_model": "qwen/qwen3.8-27b",
                "complexity": "logic_reasoning",
                "rationale": "Query involves mathematical formulation or algorithmic complexity (routed to Qwen 3.8 27B)."
            }

        # Simple factual / definitional queries
        return {
            "selected_model": "groq/compound-mini",
            "complexity": "fast_qa",
            "rationale": "Query is concise or definitional; routed to Groq Compound Mini for ultra-low latency."
        }

routing_service = RoutingService()
