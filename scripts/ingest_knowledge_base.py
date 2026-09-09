import os
import sys
import time
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from rag.document_loader import DocumentLoader
from rag.chunker import TextChunker
from services.retrieval_service import retrieval_service
from backend.app.config import settings

def ingest_knowledge_base():
    print("=" * 60)
    print("INGESTING KNOWLEDGE BASE DOCUMENTS INTO CHROMADB")
    print("=" * 60)
    
    docs_dir = settings.DOCUMENTS_DIR
    print(f"Reading documents from: {docs_dir}")
    
    start_time = time.time()
    loaded_docs = DocumentLoader.load_directory(docs_dir, recursive=True)
    print(f"Loaded {len(loaded_docs)} document files.")
    
    chunker = TextChunker(chunk_size=settings.CHUNK_SIZE, chunk_overlap=settings.CHUNK_OVERLAP)
    chunks = chunker.chunk_documents(loaded_docs)
    print(f"Generated {len(chunks)} text chunks with sliding overlap.")
    
    count = retrieval_service.add_documents(chunks)
    elapsed = round(time.time() - start_time, 2)
    
    stats = retrieval_service.get_stats()
    print("-" * 60)
    print(f"Ingestion Completed in {elapsed}s!")
    print(f"Total Vectors in '{settings.COLLECTION_NAME}': {stats['default_collection_count']}")
    print(f"Vector Dimensions: {stats['embedding_dimension']}")
    print(f"Storage Path: {stats['db_path']}")
    print("=" * 60)

    # Verification Query Test
    test_query = "What is the weightage for technical implementation in evaluation rubric?"
    print(f"\nRunning Verification Similarity Query: '{test_query}'")
    results = retrieval_service.retrieve(test_query, top_k=2)
    for idx, r in enumerate(results, 1):
        print(f"\nResult {idx} (Score: {r['score']}, Source: {r['source']}):")
        print(f"{r['content'][:250]}...\n")

if __name__ == "__main__":
    ingest_knowledge_base()
