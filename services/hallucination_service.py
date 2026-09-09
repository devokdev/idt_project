import re
from typing import List, Dict, Any
from services.embedding_service import embedding_service
import numpy as np

class HallucinationService:
    """
    Validates LLM generated answers against retrieved context chunks:
    1. Extracts factual statements and sentences from the generated text.
    2. Calculates semantic grounding/entailment against retrieved context.
    3. Computes supported vs unsupported claims and hallucination percentage.
    """
    def __init__(self):
        self.embedder = embedding_service

    def analyze_hallucination(self, answer: str, context_chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not context_chunks or not answer.strip():
            return {
                "hallucination_rate": 0.0,
                "supported_claims_count": 0,
                "unsupported_claims_count": 0,
                "total_claims": 0,
                "groundedness_score": 1.0,
                "claim_breakdown": []
            }

        # Extract sentences as individual claims
        raw_sentences = re.split(r'(?<=[.!?])\s+', answer)
        claims = [s.strip() for s in raw_sentences if len(s.strip().split()) >= 4]

        if not claims:
            return {
                "hallucination_rate": 0.0,
                "supported_claims_count": 0,
                "unsupported_claims_count": 0,
                "total_claims": 0,
                "groundedness_score": 1.0,
                "claim_breakdown": []
            }

        context_texts = [c.get("content", "") for c in context_chunks]
        context_corpus = " ".join(context_texts)
        
        # Embed claims and context chunks
        claim_vectors = self.embedder.embed_texts(claims)
        ctx_vectors = self.embedder.embed_texts(context_texts)

        claim_breakdown = []
        supported_count = 0

        for idx, (claim, c_vec) in enumerate(zip(claims, claim_vectors)):
            # Compute max cosine similarity with any context chunk
            max_sim = 0.0
            for ctx_vec in ctx_vectors:
                sim = float(np.dot(c_vec, ctx_vec))
                if sim > max_sim:
                    max_sim = sim

            # Exact keyword substring check bonus
            claim_words = set(re.findall(r'\w+', claim.lower()))
            overlap_ratio = len(claim_words.intersection(set(re.findall(r'\w+', context_corpus.lower())))) / max(len(claim_words), 1)
            
            combined_confidence = round(0.7 * max_sim + 0.3 * overlap_ratio, 3)
            is_supported = combined_confidence >= 0.45

            if is_supported:
                supported_count += 1

            claim_breakdown.append({
                "claim": claim,
                "max_similarity_score": round(max_sim, 3),
                "is_supported": is_supported,
                "confidence": combined_confidence
            })

        unsupported_count = len(claims) - supported_count
        hallucination_rate = round((unsupported_count / len(claims)) * 100, 2)
        groundedness_score = round(supported_count / len(claims), 3)

        return {
            "hallucination_rate": hallucination_rate,
            "supported_claims_count": supported_count,
            "unsupported_claims_count": unsupported_count,
            "total_claims": len(claims),
            "groundedness_score": groundedness_score,
            "claim_breakdown": claim_breakdown
        }

hallucination_service = HallucinationService()
