"""
Prompt templates and builders for the AI Project Mentor.
"""

from typing import List, Dict, Any, Optional

SYSTEM_PROMPT_MENTOR = """You are the AI Project Mentor, an expert senior software architect, AI/ML researcher, and academic advisor for final-year engineering and computer science students.

Your role:
1. Provide concrete, modern, industry-standard architectural advice and guidance.
2. Emphasize best practices, modular code structure, security, scalability, and clean API design.
3. Be clear, encouraging, structured, and pedagogical.
4. When relevant guidelines or documentation context are provided, GROUND your answer strictly on the provided context. If the context does not contain sufficient details to answer factually, state what is known and clarify what requires external research.
5. Provide code snippets, diagram suggestions, and step-by-step roadmaps when asked.
"""

SYSTEM_PROMPT_NON_RAG = """You are a helpful software engineering assistant for students. Answer the question directly to the best of your knowledge."""

SYSTEM_PROMPT_REPO_AGENT = """You are a Senior Codebase Architect and Repository Intelligence Assistant. 
Analyze the provided code snippets and directory structures to explain flows, architectural decisions, and cross-file dependencies with precise references.
"""

class PromptBuilder:
    @staticmethod
    def build_chat_prompt(
        question: str, 
        context_chunks: Optional[List[Dict[str, Any]]] = None,
        use_rag: bool = True
    ) -> str:
        """
        Builds a structured prompt combining System instructions, Context documents, and Student Question.
        """
        if not use_rag or not context_chunks:
            return f"{SYSTEM_PROMPT_MENTOR}\n\nStudent Question:\n{question}\n\nMentor Answer:"

        # Format retrieved context
        formatted_context_list = []
        for i, chunk in enumerate(context_chunks, 1):
            source = chunk.get("source", "Unknown Source")
            content = chunk.get("content", "").strip()
            score = chunk.get("score", 0.0)
            formatted_context_list.append(
                f"--- [Document {i} | Source: {source} | Similarity Score: {score:.3f}] ---\n{content}\n"
            )
        
        context_block = "\n".join(formatted_context_list)
        
        rag_prompt = (
            f"{SYSTEM_PROMPT_MENTOR}\n\n"
            f"### ACADEMIC & PROJECT GUIDELINES CONTEXT:\n"
            f"{context_block}\n"
            f"### INSTRUCTION FOR MENTOR:\n"
            f"- Ground your response using the verified Academic & Project Guidelines above.\n"
            f"- Cite the relevant sources (e.g., [Project Guidelines], [Evaluation Rubric]) in your answer.\n"
            f"- Give practical, high-scoring recommendations for final-year project evaluations.\n\n"
            f"Student Question:\n{question}\n\n"
            f"Mentor Answer:"
        )
        return rag_prompt

    @staticmethod
    def build_comparison_prompts(question: str, context_chunks: List[Dict[str, Any]]) -> Dict[str, str]:
        """
        Returns two prompts: one with RAG context and one without RAG for comparative study.
        """
        return {
            "without_rag": PromptBuilder.build_chat_prompt(question, context_chunks=None, use_rag=False),
            "with_rag": PromptBuilder.build_chat_prompt(question, context_chunks=context_chunks, use_rag=True)
        }

    @staticmethod
    def build_repo_analysis_prompt(question: str, code_contexts: List[Dict[str, Any]]) -> str:
        """
        Builds prompt for codebase understanding and multi-file dependency inspection.
        """
        formatted_code = []
        for i, item in enumerate(code_contexts, 1):
            filepath = item.get("source", "code_file")
            content = item.get("content", "")
            formatted_code.append(f"File: {filepath}\n```python\n{content}\n```\n")
            
        code_block = "\n".join(formatted_code)
        
        return (
            f"{SYSTEM_PROMPT_REPO_AGENT}\n\n"
            f"### REPOSITORY CONTEXT & CODE SNIPPETS:\n"
            f"{code_block}\n"
            f"### QUESTION:\n{question}\n\n"
            f"Architectural Explanation & Flow Analysis:"
        )
