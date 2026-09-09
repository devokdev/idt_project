import re
import numpy as np
from typing import List, Dict, Any, Set
from services.embedding_service import embedding_service

class EvaluationMetrics:
    """
    Quantitative evaluation metric calculator:
    - Information Retrieval: Precision@K, Recall@K, MRR (Mean Reciprocal Rank)
    - Response Quality: Correctness (Ground truth alignment), Semantic Relevance
    - Grounding: Hallucination Rate, Unsupported Claims
    - Code: Code Execution / Syntax Pass Rate
    """
    @staticmethod
    def precision_at_k(retrieved_sources: List[str], expected_sources: List[str], k: int = 4) -> float:
        if not retrieved_sources or not expected_sources:
            return 0.0
        top_k_retrieved = retrieved_sources[:k]
        relevant_retrieved = [s for s in top_k_retrieved if any(exp in s for exp in expected_sources)]
        return round(len(relevant_retrieved) / len(top_k_retrieved), 4)

    @staticmethod
    def recall_at_k(retrieved_sources: List[str], expected_sources: List[str], k: int = 4) -> float:
        if not retrieved_sources or not expected_sources:
            return 0.0
        top_k_retrieved = retrieved_sources[:k]
        relevant_retrieved = [s for s in top_k_retrieved if any(exp in s for exp in expected_sources)]
        return round(len(relevant_retrieved) / len(expected_sources), 4)

    @staticmethod
    def mean_reciprocal_rank(retrieved_sources: List[str], expected_sources: List[str]) -> float:
        for rank, source in enumerate(retrieved_sources, 1):
            if any(exp in source for exp in expected_sources):
                return round(1.0 / rank, 4)
        return 0.0

    @staticmethod
    def compute_semantic_relevance(generated_text: str, ground_truth: str) -> float:
        if not generated_text.strip() or not ground_truth.strip():
            return 0.0
        vecs = embedding_service.embed_texts([generated_text, ground_truth])
        sim = float(np.dot(vecs[0], vecs[1]))
        return round(max(0.0, min(1.0, (sim + 1.0) / 2.0)), 4)

    @staticmethod
    def compute_correctness(generated_text: str, ground_truth: str) -> float:
        """Combines semantic similarity and key-fact token recall."""
        sem_sim = EvaluationMetrics.compute_semantic_relevance(generated_text, ground_truth)
        
        gt_words = set(re.findall(r'\b\w{3,}\b', ground_truth.lower()))
        gen_words = set(re.findall(r'\b\w{3,}\b', generated_text.lower()))
        
        overlap = len(gt_words.intersection(gen_words)) / max(len(gt_words), 1)
        score = 0.6 * sem_sim + 0.4 * overlap
        return round(min(1.0, score), 4)

    @staticmethod
    def compute_code_pass_rate(code_snippets: List[str]) -> float:
        """Tests if generated code blocks compile with python AST parser."""
        if not code_snippets:
            return 1.0
        passed = 0
        import ast
        for code in code_snippets:
            try:
                ast.parse(code)
                passed += 1
            except Exception:
                pass
        return round(passed / len(code_snippets), 4)
