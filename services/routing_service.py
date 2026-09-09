from typing import Dict, Any

class RoutingService:
    """
    Classifies prompt complexity and selects optimal LLM:
    - Simple / Definition / Fast Query -> Phi-3 Mini (Fast, low memory)
    - Code Snippets / Repository / Code syntax -> StarCoder2
    - Architecture / Full Design / Complex Multi-step -> Code Llama 7B Instruct
    """
    @staticmethod
    def route_model(prompt: str) -> Dict[str, Any]:
        p = prompt.lower()
        word_count = len(p.split())
        
        # Coding & Syntax patterns
        coding_signals = ["code", "function", "class", "syntax", "def ", "import ", "regex", "sql query", "fix bug"]
        if any(sig in p for sig in coding_signals):
            return {
                "selected_model": "starcoder2:latest",
                "complexity": "medium_code_focused",
                "rationale": "Query requires specialized code completion or debugging (routed to StarCoder2)."
            }
        
        # Complex Architecture & Full Design
        complex_signals = [
            "architecture", "system design", "microservices", "trade-off", "roadmap",
            "lifecycle", "rubric", "comprehensive", "step by step", "docker compose"
        ]
        if any(sig in p for sig in complex_signals) or word_count > 25:
            return {
                "selected_model": "codellama:latest",
                "complexity": "high_architectural",
                "rationale": "Query requires complex multi-step reasoning and architectural synthesis (routed to Code Llama 7B)."
            }

        # Simple factual / definition queries
        return {
            "selected_model": "phi3:mini",
            "complexity": "low_simple_qa",
            "rationale": "Query is concise or definitional; routed to Phi-3 Mini for lowest latency."
        }

routing_service = RoutingService()
