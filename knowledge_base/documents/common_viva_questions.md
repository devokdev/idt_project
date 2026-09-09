# Common Final-Year Viva Questions & High-Scoring Defense Answers

## 1. Core Architecture & RAG Questions

### Q1: What is the core difference between fine-tuning an LLM and using RAG?
**Answer**: Fine-tuning alters the internal weights of the model with domain datasets, which is computationally expensive and suffers from catastrophic forgetting. RAG decouples knowledge storage from the language model by dynamically retrieving relevant facts from a vector database at query time, ensuring up-to-date facts, zero hallucination of private guidelines, and transparent citations.

### Q2: Why did you choose ChromaDB over relational databases like MySQL for context search?
**Answer**: Relational databases excel at structured ACID queries and exact keyword matching (B-Tree indexes), but fail at semantic/conceptual similarity search. ChromaDB implements Hierarchical Navigable Small World (HNSW) graph indexing over dense vector spaces, enabling sub-millisecond Approximate Nearest Neighbor (ANN) search with cosine distance metrics.

### Q3: How do you choose the chunk size and overlap in your RAG pipeline?
**Answer**: We configured a chunk size of 500 words with an 80-word sliding window overlap. A chunk size that is too small loses sentence context and discourse cohesion, while an excessively large chunk dilutes semantic density in the embedding vector. The overlap guarantees that sentences spanning boundary transitions are not artificially clipped.

---

## 2. System Performance & Engineering Questions

### Q4: How do you measure and mitigate model hallucinations?
**Answer**: We implement a Hallucination Detector service that parses the claims in the generated response and computes semantic entailment against the retrieved reference chunks. If an LLM assertion cannot be mapped to the retrieved context chunks with a minimum threshold (>0.60), it is flagged as an unsupported claim.

### Q5: How is your application containerized and deployed?
**Answer**: The system uses Docker Compose with isolated network bridges. The backend, retriever, and LLM services run as distinct services, with the persistent ChromaDB directory bind-mounted to preserve vector collections across container restarts.

### Q6: What metrics did you use to evaluate your RAG pipeline?
**Answer**: We evaluated using Information Retrieval metrics (Precision@K, Recall@K, Mean Reciprocal Rank - MRR), Generation metrics (Correctness, Semantic Relevance, Hallucination Rate), and System metrics (P95 Latency in milliseconds, Token throughput, and Memory/CPU footprint).
