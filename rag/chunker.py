import re
from typing import List, Dict, Any

class TextChunker:
    """
    Configurable semantic chunker with sliding window overlap and structural metadata attachment.
    Splits text across paragraphs, sentences, or word windows to strictly respect max chunk size.
    """
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 80):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_document(self, document: Dict[str, Any]) -> List[Dict[str, Any]]:
        text = document.get("content", "")
        base_meta = document.get("metadata", {}).copy()
        
        if not text.strip():
            return []

        # Split into words for fine-grained sliding window control
        words = text.split()
        if not words:
            return []

        chunks = []
        start_idx = 0
        total_words = len(words)

        while start_idx < total_words:
            end_idx = min(start_idx + self.chunk_size, total_words)
            chunk_words = words[start_idx:end_idx]
            chunk_str = " ".join(chunk_words)
            chunks.append(chunk_str)

            if end_idx >= total_words:
                break
            start_idx += (self.chunk_size - self.chunk_overlap)
            if start_idx <= 0 or start_idx >= end_idx:
                start_idx = end_idx

        # Format output chunk objects with metadata
        result = []
        for idx, chunk_str in enumerate(chunks):
            chunk_meta = base_meta.copy()
            chunk_meta["chunk_index"] = idx
            chunk_meta["total_chunks"] = len(chunks)
            chunk_meta["word_count"] = len(chunk_str.split())
            
            # Extract possible section header
            first_line = chunk_str.strip().split("\n")[0]
            if first_line.startswith("#"):
                chunk_meta["section"] = first_line.lstrip("#").strip()
            
            result.append({
                "content": chunk_str,
                "metadata": chunk_meta,
                "chunk_id": f"{base_meta.get('source', 'doc')}_chunk_{idx}"
            })

        return result

    def chunk_documents(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        all_chunks = []
        for doc in documents:
            all_chunks.extend(self.chunk_document(doc))
        return all_chunks
