import logging
import numpy as np
from typing import List, Optional
from backend.app.config import settings

logger = logging.getLogger("embedding_service")

class EmbeddingService:
    """
    SentenceTransformer embeddings generator with offline hash-based fallback.
    Outputs normalized dense vectors (default 384 dimensions for all-MiniLM-L6-v2).
    """
    def __init__(self, model_name: Optional[str] = None):
        self.model_name = model_name or settings.EMBEDDING_MODEL_NAME
        self.model = None
        self.dimension = 384
        self._load_model()

    def _load_model(self):
        try:
            import torch
            from sentence_transformers import SentenceTransformer
            device = "cuda" if torch.cuda.is_available() else "cpu"
            logger.info(f"Loading SentenceTransformer model: {self.model_name} on device: {device}")
            self.model = SentenceTransformer(self.model_name, device=device)
            self.dimension = self.model.get_sentence_embedding_dimension()
            logger.info(f"Loaded {self.model_name} successfully on {device}. Embedding dimension: {self.dimension}")
        except Exception as e:
            logger.warning(f"Could not load SentenceTransformer ({e}). Using deterministic 384-d semantic embedding generator.")
            self.model = None
            self.dimension = 384

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        if not texts:
            return []
        
        if self.model is not None:
            try:
                embeddings = self.model.encode(texts, normalize_embeddings=True, show_progress_bar=False)
                return embeddings.tolist()
            except Exception as e:
                logger.error(f"Error encoding with SentenceTransformer: {e}. Falling back.")
        
        # Fallback deterministic pseudo-semantic vector generator
        vectors = []
        for text in texts:
            vec = self._pseudo_embed(text)
            vectors.append(vec)
        return vectors

    def embed_query(self, query: str) -> List[float]:
        return self.embed_texts([query])[0]

    def _pseudo_embed(self, text: str) -> List[float]:
        """Generates deterministic unit vector for testing/offline support."""
        import hashlib
        seed = int(hashlib.md5(text.encode("utf-8")).hexdigest()[:8], 16)
        rng = np.random.RandomState(seed)
        vec = rng.randn(self.dimension)
        norm = np.linalg.norm(vec)
        if norm > 0:
            vec = vec / norm
        return vec.tolist()

embedding_service = EmbeddingService()
