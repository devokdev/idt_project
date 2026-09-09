# Production AI/ML and RAG Architecture Workflow Guide

## 1. Overview of Retrieval-Augmented Generation (RAG)
Retrieval-Augmented Generation (RAG) combines dense vector information retrieval with generative Large Language Models to provide grounded, domain-specific, hallucination-resistant answers.

```
Query -> Embedding Model -> Dense Vector -> Approximate Nearest Neighbor (ANN) Vector Search -> Top-K Context Chunks -> Contextual Prompt Synthesis -> Generative LLM -> Grounded Answer
```

## 2. RAG Pipeline Stages
1. **Document Ingestion**:
   - Ingest multiple formats (PDF, Markdown, JSON, Source Code).
   - Sanitize text, strip non-printable tokens, and preserve hierarchical metadata (e.g. document title, section, page).
2. **Semantic Chunking**:
   - Chunk size: 300 to 500 tokens (words) to maintain semantic cohesion.
   - Chunk overlap: 10% to 20% (50 to 80 words) to avoid context clipping across paragraph boundaries.
3. **Dense Vector Embeddings**:
   - Model: `all-MiniLM-L6-v2` (384 dimensions) or `bge-small-en-v1.5`.
   - Normalization: L2 normalization is applied to vectors to allow Cosine Similarity to be computed as an efficient dot product.
4. **Vector Database**:
   - ChromaDB / Qdrant / Milvus with HNSW (Hierarchical Navigable Small World) indexing for sub-millisecond retrieval.
5. **Context Aggregation & Grounding**:
   - Deduplication of overlapping retrieved segments.
   - Injecting strict grounding instructions into the system prompt: *"Only answer using the facts provided in the academic context. Do not invent citations."*

## 3. Large Language Model Selection Criteria
- **Code Llama 7B Instruct**: Specialized for code generation, software architecture design, debugging, and repository understanding.
- **StarCoder2**: Optimized for multi-language code completion, repository indexing, and syntax validation.
- **Phi-3 Mini (3.8B)**: Highly efficient, low-memory footprint model capable of fast reasoning, summarization, and query classification.

## 4. Evaluation Metrics for LLM Systems
- **Precision@K & Recall@K**: Measures the proportion of relevant chunks retrieved in top K results.
- **Mean Reciprocal Rank (MRR)**: Evaluates the ranking quality of the first relevant chunk.
- **Hallucination Rate**: Percentage of claims made in the LLM response that cannot be verified by the retrieved context.
- **Latency (ms)**: End-to-end user wait time split across Embedding Time, Retrieval Time, and LLM Token Generation Time.
