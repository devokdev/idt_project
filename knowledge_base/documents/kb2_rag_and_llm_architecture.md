# Comprehensive Retrieval-Augmented Generation (RAG) & Large Language Model (LLM) Systems Architecture Master

## 1. End-to-End 5-Tier RAG Architecture & Lifecycle Mechanics

Retrieval-Augmented Generation (RAG) bridges the gap between parametric memory (static neural weights) and non-parametric knowledge (dynamic, verifiable document databases). The production lifecycle is partitioned into five distinct operational stages:

```
+---------------------------------------------------------------------------------------------------+
|                         PRODUCTION 5-TIER RAG PIPELINE ARCHITECTURE                               |
+---------------------------------------------------------------------------------------------------+
| 1. Ingestion Layer      : PDF/Markdown -> AST/Text Extraction -> Cleaning -> Unicode Sanitization |
| 2. Chunking Layer       : Fixed-Token Window (500 tokens) + Overlap (80 tokens) + Sentence Boundary |
| 3. Embedding Vectorizer : all-MiniLM-L6-v2 (384 Dimensions) + L2 Euclidean Normalization           |
| 4. Vector Store (HNSW)  : Hierarchical Navigable Small World Graph (M=16, efConstruction=64)      |
| 5. Context Synthesis    : Top-K Extraction -> Reranking -> System Grounding Prompt -> Groq LPU    |
+---------------------------------------------------------------------------------------------------+
```

---

## 2. Mathematical Foundations of Vector Search & Dense Embeddings

### 2.1 The Embedding Vector Space
A dense embedding model maps an input textual sequence $T = (w_1, w_2, \dots, w_n)$ into a continuous vector space $\mathbb{R}^d$, where $d = 384$ for `all-MiniLM-L6-v2`:

$$\vec{v} = f_{\theta}(T) \in \mathbb{R}^{384}$$

To eliminate magnitude distortion caused by varying chunk word counts, every vector is explicitly normalized using the Euclidean $L_2$ norm:

$$\hat{v} = \frac{\vec{v}}{\|\vec{v}\|_2} = \frac{\vec{v}}{\sqrt{\sum_{i=1}^{d} v_i^2}}$$

### 2.2 Distance Metrics in $\mathbb{R}^d$
For unit-normalized vectors ($\|\hat{u}\|_2 = \|\hat{v}\|_2 = 1$), the cosine similarity reduces directly to the algebraic dot product:

$$\text{CosineSimilarity}(\hat{u}, \hat{v}) = \frac{\hat{u} \cdot \hat{v}}{\|\hat{u}\|_2 \|\hat{v}\|_2} = \hat{u} \cdot \hat{v} = \sum_{i=1}^{d} u_i v_i$$

The relationship between Squared Euclidean Distance ($L_2^2$) and Cosine Similarity for normalized vectors is deterministic:

$$\|\hat{u} - \hat{v}\|_2^2 = \|\hat{u}\|_2^2 + \|\hat{v}\|_2^2 - 2(\hat{u} \cdot \hat{v}) = 1 + 1 - 2\cos(\theta) = 2(1 - \cos(\theta))$$

Consequently, minimizing Euclidean distance is mathematically equivalent to maximizing Cosine Similarity.

### 2.3 Hierarchical Navigable Small World (HNSW) Graph Mechanics
ChromaDB employs the HNSW algorithm for Approximate Nearest Neighbor (ANN) search:
- **Hierarchical Layers**: The index maintains a hierarchy of proximity graphs. The top layer ($l = l_{\max}$) contains sparse nodes with long-range links, enabling rapid skips across distant vector clusters. Lower layers contain increasingly dense connectivity.
- **Search Traversal**:
  1. Search commences at the entry point in top layer $l_{\max}$.
  2. The algorithm greedily traverses the graph by moving to the neighbor closest to the query vector $\vec{q}$.
  3. When a local minimum is reached in layer $l$, the search drops to the corresponding node in layer $l-1$.
  4. At layer 0 (ground layer), a priority queue of size $efSearch$ expands neighbors to return the top-$K$ nearest vectors.
- **Computational Complexity**:
  - Exact Exhaustive Flat Search (k-NN): $\mathcal{O}(N \cdot d)$ time.
  - HNSW Search: $\mathcal{O}(\log N \cdot d)$ average time complexity.
  - HNSW Construction: $\mathcal{O}(N \log N \cdot d)$ time.

---

## 3. Sliding-Window Text Segmentation & Chunking Strategies

A naive split of documents by character count truncates sentences midway, corrupting semantic meaning. Our production pipeline enforces sliding-window segmentation with strict boundary alignment:

```
Document Stream: [========================= Complete Document =========================]
Chunk 1:        [---------- Chunk Size: 500 Tokens ----------]
Overlap 1:                                 [-- 80 Tokens --]
Chunk 2:                                   [---------- Chunk Size: 500 Tokens ----------]
Overlap 2:                                                             [-- 80 Tokens --]
Chunk 3:                                                               [---------- ...]
```

### Why 500 Tokens with 80 Token Overlap?
1. **Context Retention across Boundaries**: If an important concept (e.g., "The evaluation criteria for technical implementation is 35 marks") spans the division boundary between two adjacent chunks, an 80-token overlap guarantees that at least one chunk contains the complete, unbroken propositional clause.
2. **Transformer Attention Budget**: Models like `all-MiniLM-L6-v2` have a maximum positional embedding sequence length of 512 tokens. Keeping the target chunk size at 500 tokens ensures input text never suffers silent tail-truncation during vector encoding.
3. **Information Density**: Chunks smaller than 100 tokens lack sufficient semantic context for accurate vector placement; chunks larger than 1,000 tokens dilute the query-specific signal with extraneous noise.

---

## 4. Large Language Model (LLM) Transformer Mechanics

Modern generative models utilized in this platform (`openai/gpt-oss-20b`, `openai/gpt-oss-120b`, `qwen/qwen3.8-27b`) are decoder-only autoregressive transformers.

### 4.1 Scaled Dot-Product Self-Attention
Given an input sequence mapped to Query ($Q$), Key ($K$), and Value ($V$) matrices of dimension $d_k$:

$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$

- **The Scaling Factor $\frac{1}{\sqrt{d_k}}$**: As embedding dimension $d_k$ grows large, the dot products $QK^T$ grow large in magnitude, pushing the softmax function into regions with extremely small gradients ($\approx 0$), causing the vanishing gradient phenomenon. Dividing by $\sqrt{d_k}$ preserves unit variance and stable gradients.
- **Causal Masking**: In decoder-only transformers, an upper-triangular attention mask filled with $-\infty$ is applied before softmax, ensuring token $i$ can only attend to preceding tokens $j \le i$.

### 4.2 Multi-Head Attention (MHA) & Grouped-Query Attention (GQA)
Instead of computing attention once, Multi-Head Attention projects $Q, K, V$ into $h$ distinct representation subspaces:

$$\text{MultiHead}(Q, K, V) = \text{Concat}(\text{head}_1, \dots, \text{head}_h)W^O$$

$$\text{head}_i = \text{Attention}(QW_i^Q, KW_i^K, VW_i^V)$$

- **Grouped-Query Attention (GQA)**: In models like Qwen and modern GPT architectures, multiple query heads share a single Key and Value head. This dramatically reduces the memory footprint of the Key-Value (KV) cache during generation while retaining model reasoning capacity.

### 4.3 Key-Value (KV) Caching & FlashAttention
- **Autoregressive Bottleneck**: In standard token-by-token generation, recalculating Keys and Values for all past tokens at step $t$ results in $\mathcal{O}(t^2)$ redundant compute.
- **KV Cache**: Key and Value tensors for historical tokens are stored in high-bandwidth memory (HBM). Each new generation step only computes $Q$ for the single new token and attends to the cached $K$ and $V$ tensors, reducing per-token step complexity to $\mathcal{O}(t)$.
- **FlashAttention-2**: Standard attention writes the $N \times N$ attention matrix to High Bandwidth Memory (HBM) and reads it back for softmax. FlashAttention tiles the computation into GPU Static RAM (SRAM), computing softmax incrementally via online normalizers without ever materializing the massive intermediate $N \times N$ matrix in global memory, yielding a 2x-4x speedup.

---

## 5. Free-Tier Groq Cloud LPU Architecture & Selected Models

The platform orchestrates three high-speed models running on Groq's Language Processing Unit (LPU) Tensor Streaming Processor (TSP) architecture. Unlike conventional GPUs (Nvidia H100/A100) constrained by memory bandwidth latency, LPUs operate with deterministic Instruction Set Architecture (ISA) and massive on-chip SRAM, achieving $>300\text{ tokens/sec}$:

```
+------------------------+-------------------+--------------------+-------------------------------------------+
| Model Identifier       | Parameter Scale   | Groq Architecture  | Optimal Specialization & Routing Policy    |
+------------------------+-------------------+--------------------+-------------------------------------------+
| openai/gpt-oss-20b     | 20 Billion Params | Groq LPU Hosted    | High-speed QA, RAG context synthesis,     |
|                        |                   | Ultra-low latency  | interactive conversational mentoring.     |
+------------------------+-------------------+--------------------+-------------------------------------------+
| openai/gpt-oss-120b    | 120 Billion Params| Groq LPU Hosted    | Complex multi-file architectural design,  |
|                        |                   | High Reasoning     | rigorous code refactoring, AST analysis.  |
+------------------------+-------------------+--------------------+-------------------------------------------+
| qwen/qwen3.8-27b       | 27 Billion Params | Groq LPU Hosted    | Mathematical formulation, structured JSON |
|                        |                   | High-speed logic   | outputs, algorithmic proofs & DSA logic.  |
+------------------------+-------------------+--------------------+-------------------------------------------+
```

---

## 6. Mathematical Evaluation Metrics for Information Retrieval & RAG

To quantitatively benchmark RAG pipeline performance, our system computes standardized academic metrics across our curated 30-question evaluation dataset:

### 6.1 Precision@K
Measures the proportion of retrieved chunks that are genuinely relevant to the ground truth query:

$$\text{Precision@K} = \frac{|\{\text{Retrieved Chunks in Top-K}\} \cap \{\text{Relevant Ground Truth Chunks}\}|}{K}$$

### 6.2 Recall@K
Measures the proportion of all relevant ground truth documents that were successfully captured in the top-$K$ retrieved results:

$$\text{Recall@K} = \frac{|\{\text{Retrieved Chunks in Top-K}\} \cap \{\text{Relevant Ground Truth Chunks}\}|}{|\{\text{Total Relevant Ground Truth Chunks}\}|}$$

### 6.3 Mean Reciprocal Rank (MRR)
Evaluates the positional quality of retrieval by scoring how early the first relevant document chunk appears in the ranked list:

$$\text{MRR} = \frac{1}{|Q|} \sum_{i=1}^{|Q|} \frac{1}{\text{rank}_i}$$

Where $\text{rank}_i$ is the 1-based index position of the first relevant document chunk retrieved for query $i$. If no relevant document is retrieved, $\frac{1}{\text{rank}_i} = 0$.

### 6.4 Hallucination Rate & Groundedness Ratio
- **Hallucination Rate**: The percentage of factual statements asserted by the LLM that cannot be mathematically entailed from the retrieved context:

$$\text{Hallucination Rate} = \frac{\text{Unverified / Contradictory Assertions}}{\text{Total Factual Assertions Made}} \times 100\%$$

- **Groundedness Score**: The lexical and semantic N-gram entailment score between the generated answer $A$ and the concatenated retrieved context $C$:

$$\text{Groundedness}(A, C) = \frac{|\text{Tokens}(A) \cap \text{Tokens}(C)|}{|\text{Tokens}(A)|}$$

---

## 7. Complete Python Implementation Reference: Custom RAG Pipeline

Below is the verified, standalone Python implementation demonstrating our core chunking, embedding, retrieval, and prompt injection pipeline:

```python
import numpy as np
import re
from typing import List, Dict, Any

class StandaloneRAGPipeline:
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 80):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.corpus_chunks: List[Dict[str, Any]] = []

    def sliding_window_chunk(self, text: str, source_doc: str) -> List[Dict[str, Any]]:
        words = text.split()
        chunks = []
        start = 0
        step = self.chunk_size - self.chunk_overlap
        chunk_idx = 0
        
        while start < len(words):
            end = min(start + self.chunk_size, len(words))
            chunk_text = " ".join(words[start:end])
            chunks.append({
                "chunk_id": f"{source_doc}_chunk_{chunk_idx}",
                "source": source_doc,
                "text": chunk_text,
                "token_count": end - start
            })
            if end == len(words):
                break
            start += step
            chunk_idx += 1
        return chunks

    def compute_l2_normalized_dot_product(self, query_vec: np.ndarray, doc_vecs: np.ndarray) -> np.ndarray:
        # Normalize query
        q_norm = query_vec / (np.linalg.norm(query_vec) + 1e-10)
        # Normalize docs along axis 1
        d_norms = doc_vecs / (np.linalg.norm(doc_vecs, axis=1, keepdims=True) + 1e-10)
        # Cosine similarity is direct dot product
        return np.dot(d_norms, q_norm)

    def build_grounded_system_prompt(self, query: str, retrieved_chunks: List[Dict[str, Any]]) -> str:
        context_blocks = "\n\n".join([
            f"--- SOURCE: {c['source']} (Chunk ID: {c['chunk_id']}) ---\n{c['text']}"
            for c in retrieved_chunks
        ])
        
        prompt = f"""You are the verified AI Project Mentor for final-year B.Tech CSE students.
Your responses must be strictly grounded in the provided reference context.

CONTEXT INFORMATION:
{context_blocks}

STUDENT QUERY:
{query}

GROUNDING INSTRUCTIONS:
1. Answer the query thoroughly using exclusively facts present in the context above.
2. If the context does not provide sufficient details, explicitly say:
   'The verified knowledge base does not contain sufficient details to answer this query.'
3. Always cite the exact source document name in your answer.
"""
        return prompt
```
