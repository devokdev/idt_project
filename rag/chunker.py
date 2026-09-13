import re
from typing import List, Dict, Any

class TextChunker:
    """
    Configurable semantic chunker with paragraph and sliding window splitting.
    Splits larger documents into coherent thematic chunks with sliding overlap.
    """
    def __init__(self, chunk_size: int = 150, chunk_overlap: int = 40):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_document(self, document: Dict[str, Any]) -> List[Dict[str, Any]]:
        text = document.get("content", "")
        base_meta = document.get("metadata", {}).copy()
        
        if not text.strip():
            return []

        # Split across markdown sections (## ) first if possible
        sections = re.split(r'\n(?=##?\s+)', text)
        chunks = []

        for sec in sections:
            sec_clean = sec.strip()
            if not sec_clean:
                continue
            words = sec_clean.split()
            if len(words) <= self.chunk_size:
                chunks.append(sec_clean)
            else:
                # Sliding window over large sections
                start = 0
                while start < len(words):
                    end = min(start + self.chunk_size, len(words))
                    sub_words = words[start:end]
                    chunks.append(" ".join(sub_words))
                    if end >= len(words):
                        break
                    start += (self.chunk_size - self.chunk_overlap)

        result = []
        for idx, chunk_str in enumerate(chunks):
            chunk_meta = base_meta.copy()
            chunk_meta["chunk_index"] = idx
            chunk_meta["total_chunks"] = len(chunks)
            chunk_meta["word_count"] = len(chunk_str.split())
            
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
