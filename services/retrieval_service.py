import os
import time
import logging
import chromadb
from typing import List, Dict, Any, Optional
from backend.app.config import settings
from services.embedding_service import embedding_service
from rag.document_loader import DocumentLoader
from rag.chunker import TextChunker

logger = logging.getLogger("retrieval_service")

class RetrievalService:
    """
    Resilient ChromaDB Vector Store and Top-K Cosine Similarity Retrieval Service.
    Supports PersistentClient with fallback to in-memory EphemeralClient when corrupt
    sqlite handles are encountered.
    """
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or settings.CHROMA_DB_DIR
        self.default_collection_name = settings.COLLECTION_NAME
        self.code_collection_name = settings.CODE_COLLECTION_NAME
        self.embedder = embedding_service
        self.client = None
        self.collection = None
        self.code_collection = None
        self._init_client()

    def _init_client(self):
        try:
            os.makedirs(self.db_path, exist_ok=True)
            self.client = chromadb.PersistentClient(path=self.db_path)
            self._ensure_collections()
        except Exception as e:
            logger.warning(f"PersistentClient error ({e}). Initializing high-speed in-memory EphemeralClient.")
            self.client = chromadb.EphemeralClient()
            self._ensure_collections()
            self._auto_seed_knowledge_base()

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

    def _auto_seed_knowledge_base(self):
        """Auto-seeds core documents if starting on an ephemeral/fresh collection."""
        try:
            docs = DocumentLoader.load_directory(settings.DOCUMENTS_DIR)
            chunker = TextChunker(chunk_size=settings.CHUNK_SIZE, chunk_overlap=settings.CHUNK_OVERLAP)
            chunks = chunker.chunk_documents(docs)
            self.add_documents(chunks)
            logger.info(f"Auto-seeded {len(chunks)} knowledge chunks into ChromaDB.")
        except Exception as e:
            logger.warning(f"Auto-seed warning: {e}")

    def add_documents(self, chunks: List[Dict[str, Any]], collection_name: Optional[str] = None) -> int:
        if not chunks:
            return 0
        
        target_collection = self.code_collection if collection_name == self.code_collection_name else self.collection
        if target_collection is None:
            self._ensure_collections()
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

        if target_col is None:
            self._ensure_collections()
            target_col = self.collection

        try:
            total_count = target_col.count()
        except Exception:
            self._ensure_collections()
            target_col = self.code_collection if collection_name == self.code_collection_name else self.collection
            total_count = target_col.count()

        if total_count == 0:
            logger.info(f"Collection '{target_col.name}' is empty. Auto-seeding...")
            self._auto_seed_knowledge_base()
            total_count = target_col.count()

        if total_count == 0:
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
                similarity_score = round(1.0 - float(dist), 4)
                if similarity_score >= min_thresh or len(formatted_results) < 2:
                    formatted_results.append({
                        "content": doc_text,
                        "source": meta.get("source", "Knowledge Base"),
                        "score": similarity_score,
                        "chunk_id": cid,
                        "metadata": meta
                    })

        unique_results = []
        seen = set()
        for r in formatted_results:
            key = r["content"][:100]
            if key not in seen:
                seen.add(key)
                unique_results.append(r)

        return sorted(unique_results, key=lambda x: x["score"], reverse=True)

    def get_stats(self) -> Dict[str, Any]:
        cnt = self.collection.count() if self.collection else 0
        code_cnt = self.code_collection.count() if self.code_collection else 0
        return {
            "default_collection_count": cnt,
            "code_collection_count": code_cnt,
            "embedding_dimension": self.embedder.dimension,
            "db_path": self.db_path
        }

retrieval_service = RetrievalService()
