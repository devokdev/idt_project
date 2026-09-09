import os
import time
import logging
import chromadb
from chromadb.config import Settings as ChromaSettings
from typing import List, Dict, Any, Optional
from backend.app.config import settings
from services.embedding_service import embedding_service

logger = logging.getLogger("retrieval_service")

class RetrievalService:
    """
    ChromaDB Persistent Vector Store and Top-K Cosine Similarity Retrieval Service.
    """
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or settings.CHROMA_DB_DIR
        os.makedirs(self.db_path, exist_ok=True)
        self.client = chromadb.PersistentClient(path=self.db_path)
        self.default_collection_name = settings.COLLECTION_NAME
        self.code_collection_name = settings.CODE_COLLECTION_NAME
        self.embedder = embedding_service
        self._ensure_collections()

    def _ensure_collections(self):
        try:
            self.collection = self.client.get_or_create_collection(
                name=self.default_collection_name,
                metadata={"hnsw:space": "cosine"}
            )
            self.code_collection = self.client.get_or_create_collection(
                name=self.code_collection_name,
                metadata={"hnsw:space": "cosine"}
            )
            logger.info(f"Connected to ChromaDB collections: {self.default_collection_name}, {self.code_collection_name}")
        except Exception as e:
            logger.error(f"Failed to initialize ChromaDB collections: {e}")

    def add_documents(self, chunks: List[Dict[str, Any]], collection_name: Optional[str] = None) -> int:
        if not chunks:
            return 0
        
        target_collection = self.code_collection if collection_name == self.code_collection_name else self.collection
        
        ids = []
        texts = []
        metadatas = []
        
        for idx, chunk in enumerate(chunks):
            cid = chunk.get("chunk_id") or f"doc_{int(time.time()*1000)}_{idx}"
            content = chunk.get("content", "").strip()
            if not content:
                continue
            
            raw_meta = chunk.get("metadata", {})
            # Chroma requires flat primitive metadata (str, int, float, bool)
            clean_meta = {}
            for k, v in raw_meta.items():
                if isinstance(v, (str, int, float, bool)):
                    clean_meta[k] = v
                else:
                    clean_meta[k] = str(v)
            clean_meta["source"] = str(raw_meta.get("source", "knowledge_base"))
            
            ids.append(cid)
            texts.append(content)
            metadatas.append(clean_meta)

        if not texts:
            return 0

        embeddings = self.embedder.embed_texts(texts)
        target_collection.upsert(
            ids=ids,
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas
        )
        logger.info(f"Ingested {len(texts)} chunks into collection '{target_collection.name}'")
        return len(texts)

    def retrieve(
        self, 
        query: str, 
        top_k: Optional[int] = None, 
        threshold: Optional[float] = None,
        collection_name: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        k = top_k or settings.TOP_K
        min_thresh = threshold if threshold is not None else settings.SIMILARITY_THRESHOLD
        target_col = self.code_collection if collection_name == self.code_collection_name else self.collection

        total_count = target_col.count()
        if total_count == 0:
            logger.warning(f"Collection '{target_col.name}' is empty. Returning 0 chunks.")
            return []

        query_vector = self.embedder.embed_query(query)
        actual_k = min(k, total_count)
        
        try:
            results = target_col.query(
                query_embeddings=[query_vector],
                n_results=actual_k,
                include=["documents", "metadatas", "distances"]
            )
        except Exception as e:
            logger.error(f"Chroma query failed: {e}")
            return []

        formatted_results = []
        if results and "documents" in results and results["documents"]:
            docs = results["documents"][0]
            metas = results["metadatas"][0] if "metadatas" in results else [{}] * len(docs)
            distances = results["distances"][0] if "distances" in results else [0.0] * len(docs)
            ids = results["ids"][0] if "ids" in results else [""] * len(docs)

            for doc_text, meta, dist, cid in zip(docs, metas, distances, ids):
                # Cosine distance to similarity: similarity = 1 - distance
                similarity_score = round(1.0 - float(dist), 4)
                if similarity_score >= min_thresh or len(formatted_results) < 2:
                    formatted_results.append({
                        "content": doc_text,
                        "source": meta.get("source", "Knowledge Base"),
                        "score": similarity_score,
                        "chunk_id": cid,
                        "metadata": meta
                    })

        # Deduplicate results based on content hash or slice
        unique_results = []
        seen = set()
        for r in formatted_results:
            key = r["content"][:100]
            if key not in seen:
                seen.add(key)
                unique_results.append(r)

        return sorted(unique_results, key=lambda x: x["score"], reverse=True)

    def get_stats(self) -> Dict[str, Any]:
        return {
            "default_collection_count": self.collection.count(),
            "code_collection_count": self.code_collection.count(),
            "embedding_dimension": self.embedder.dimension,
            "db_path": self.db_path
        }

retrieval_service = RetrievalService()
