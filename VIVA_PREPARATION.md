# University Capstone Project Viva Voce Preparation Guide
> **20 Comprehensive Technical Viva Questions, In-Depth Model Answers, Architectural Justifications, and Examiner Defense Tactics.**

---

### Q1: What is the core architecture of your AI Project Mentor system?
**Model Answer:**
"Our system follows a decoupled 3-tier microservice architecture. The **Presentation Layer** uses a responsive glassmorphic frontend communicating via async REST endpoints. The **Application & Gateway Layer** is built on FastAPI with asynchronous routers, dynamic model routing, and safety guardrails. The **Data & Vector Layer** uses ChromaDB with persistent HNSW SQLite indexing and a 384-dimensional SentenceTransformer (`all-MiniLM-L6-v2`) embedding pipeline. Multi-model inference is coordinated via Ollama across Code Llama 7B, StarCoder2, and Phi-3 Mini."

---

### Q2: Why did you choose RAG (Retrieval-Augmented Generation) instead of fine-tuning an open-source LLM?
**Model Answer:**
"Fine-tuning modifies the internal weights of the model, which introduces catastrophic forgetting, high computational training costs, and stale knowledge whenever university project policies or grading rubrics change. In contrast, RAG decouples knowledge storage from generation. When rubrics or deadlines update, we simply update the vector database in milliseconds with zero retraining downtime. Furthermore, RAG allows us to cite exact source chunks and reduce parametric hallucinations."

---

### Q3: What is the algorithmic time complexity of vector retrieval in ChromaDB?
**Model Answer:**
"ChromaDB utilizes the Hierarchical Navigable Small World (HNSW) graph algorithm for vector indexing. HNSW offers an average query time complexity of **$\mathcal{O}(\log N)$**, compared to the brute-force exhaustive search complexity of **$\mathcal{O}(N \cdot d)$**, where $N$ is the number of documents and $d$ is embedding dimensionality. The indexing construction time is $\mathcal{O}(N \log N)$."

---

### Q4: Why did you choose `all-MiniLM-L6-v2` as the embedding model?
**Model Answer:**
"We selected `all-MiniLM-L6-v2` due to its optimal balance between retrieval accuracy and latency. It outputs a compact 384-dimensional vector with an inference speed under 15ms on CPU and 3ms on GPU. In contrast to 1536-dim models (like text-embedding-ada-002), 384 dimensions reduce vector storage footprints by 75% and accelerate cosine similarity calculations by $\approx 4\times$ while retaining an average MRR above 0.88 on academic text."

---

### Q5: How does your chunking strategy (500 words with 80 words overlap) prevent information loss?
**Model Answer:**
"A 500-word window captures coherent semantic units such as full rubric criteria, grading sections, or complete function definitions. The 80-word sliding overlap ($\approx 16\%$) ensures that cross-boundary concepts, such as criteria spanning paragraph breaks or split code blocks, are never severed at chunk edges. This maintains semantic continuity across embedding vector representations."

---

### Q6: How does the system detect and quantify hallucinations?
**Model Answer:**
"We implement a hybrid grounding verification service in `services/hallucination_service.py`. The generated answer is tokenized into individual factual propositions. Each proposition is cross-evaluated for lexical overlap and semantic cosine similarity against the retrieved context chunks. A claim with $< 0.40$ semantic similarity is flagged as an 'unsupported claim'. The metric is computed as:
$$\text{Hallucination Rate} = \left(\frac{\text{Count of Unsupported Claims}}{\text{Total Claims in Answer}}\right) \times 100\%$$"

---

### Q7: Explain the dynamic model routing strategy used in your application.
**Model Answer:**
"Our dynamic router (`services/routing_service.py`) analyzes query intent using keyword heuristic patterns and token classification:
- **Code Llama 7B Instruct**: Selected for architectural reasoning, design patterns, proposal review, and final evaluation criteria.
- **StarCoder2**: Selected for code syntax generation, AST analysis, unit test synthesis, and debugging.
- **Phi-3 Mini (3.8B)**: Selected for lightweight conversational questions, definitions, and high-frequency FAQ prompts to minimize server latency."

---

### Q8: How does your codebase intelligence analyzer work without executing student code?
**Model Answer:**
"We utilize Python's standard `ast` (Abstract Syntax Tree) library in `services/repo_analyzer_service.py`. It parses the code statically without execution, extracting class definitions, inheritance trees, function signatures, docstrings, and imported libraries. These metadata representations are vectorized and ingested into the `repository_code_kb` collection in ChromaDB, enabling semantic queries over the student's actual codebase structure safely without code-injection vulnerabilities."

---

### Q9: What security guardrails are implemented to protect the LLM gateway?
**Model Answer:**
"In `services/guardrails_service.py`, we implement input and output validation:
1. **Prompt Injection Defense**: Regex filters detecting instructions such as `ignore previous instructions`, `system prompt override`, or role impersonation.
2. **Harmful/Dangerous Code Patterns**: Detection of `os.system('rm -rf')`, `eval()`, malicious subprocess calls, and credential exposure.
3. **Off-Topic Filtering**: Boundary filters ensuring student questions remain aligned with university academic disciplines."

---

### Q10: How do you measure retrieval quality? Explain Precision@K, Recall@K, and MRR.
**Model Answer:**
"1. **Precision@K**: The proportion of retrieved chunks in the top $K$ that are relevant:
   $$\text{Precision@K} = \frac{|\text{Relevant Chunks} \cap \text{Top-K Retrieved}|}{K}$$
2. **Recall@K**: The proportion of all relevant guideline chunks that were successfully retrieved in the top $K$.
3. **MRR (Mean Reciprocal Rank)**: Measures where the first relevant chunk appears in the ranked results:
   $$\text{MRR} = \frac{1}{|Q|} \sum_{i=1}^{|Q|} \frac{1}{\text{rank}_i}$$"

---

### Q11: What happens if the local Ollama instance crashes or model tags are missing?
**Model Answer:**
"The system is built with high-availability resiliency patterns in `services/llm_service.py`:
1. It implements an exponential backoff retry mechanism (3 attempts with jitter).
2. It detects HTTP 404/504 errors and immediately falls back to a deterministic, self-contained rule-based and knowledge-grounded synthesis engine, guaranteeing $0\%$ API 500 error rates for end-users."

---

### Q12: Why is cosine similarity used instead of Euclidean distance for embeddings?
**Model Answer:**
"Cosine similarity measures the cosine of the angle between two multi-dimensional vectors, evaluating directional semantic orientation regardless of vector magnitude (document length). When embedding vectors are L2-normalized ($\|v\|_2 = 1$), cosine similarity is mathematically equivalent to the inner dot product:
$$\text{Cosine}(A, B) = \frac{A \cdot B}{\|A\| \|B\|} = A \cdot B$$
This allows ultra-fast hardware SIMD dot product acceleration."

---

### Q13: How does Docker Compose isolate your microservices?
**Model Answer:**
"In `docker/docker-compose.yml`, we define independent network bridges (`mentor-net`) with distinct resource constraints. The `backend` container hosts the FastAPI gateway, the `retriever` container isolates the ChromaDB persistence layer, and the `llm` container manages Ollama. Services communicate strictly over internal DNS aliases with health checks and restart policies."

---

### Q14: What is the maximum acceptable plagiarism percentage according to academic standards?
**Model Answer:**
"According to the university thesis guidelines ingested in our knowledge base (`project_guidelines.md`), the maximum allowed similarity index is **15%** (excluding standard bibliographic references and mathematical formulas), verified via Turnitin or Urkund."

---

### Q15: What is the distribution of marks in the final-year capstone evaluation rubric?
**Model Answer:**
"Based on `evaluation_rubric.md`:
- Problem Formulation & Literature Review: **15 Marks**
- System Architecture & Engineering Design: **20 Marks**
- Technical Implementation & Code Quality: **35 Marks**
- Validation, Quantitative Metrics & Testing: **15 Marks**
- Project Viva Voce & Presentation Defense: **15 Marks**
Total: **100 Marks**."

---

### Q16: How did you validate that RAG improved answer correctness?
**Model Answer:**
"We executed automated multi-model benchmarking across 30 diagnostic questions (`evaluation/datasets/evaluation_30_questions.json`). The non-RAG baseline scored an average correctness of 58.2% with a 38.4% hallucination rate. With RAG enabled, correctness increased to **92.4%**, semantic relevance to **94.1%**, and hallucination dropped to **4.2%**."

---

### Q17: What is the role of Pydantic v2 in your application layer?
**Model Answer:**
"Pydantic v2 enforces compile-time and runtime type safety, schema validation, and automatic serialization/deserialization. It prevents malformed client inputs (e.g., negative `top_k`, empty message strings, invalid model names) through strict field constraints and generates self-documenting OpenAPI (Swagger) specifications at `/docs`."

---

### Q18: How does the system handle concurrent users querying the vector database?
**Model Answer:**
"FastAPI runs asynchronously with `asyncio` event loops on Uvicorn workers. In `retrieval_service.py`, ChromaDB reads are executed concurrently through non-blocking I/O threads. SQLite write operations are constrained to single-worker ingestion cycles to avoid database locks."

---

### Q19: If you had another month to work on this project, what enhancements would you add?
**Model Answer:**
"We would implement:
1. **Hybrid Sparse-Dense Retrieval**: Combining BM25 keyword search with dense SentenceTransformer embeddings using Reciprocal Rank Fusion (RRF).
2. **Cross-Encoder Reranking**: Incorporating a `bge-reranker-large` model to re-score top-20 retrieved candidate chunks to top-4.
3. **Agentic Workflows**: Multi-step tool use allowing the mentor to automatically generate Git pull requests, auto-fix lint errors, and plot test coverage charts directly."

---

### Q20: What was your individual contribution to this engineering project?
**Model Answer:**
"I architected the end-to-end multi-model pipeline: implemented the FastAPI backend gateway and Pydantic schemas, designed the ChromaDB vector retrieval pipeline with 500-word sliding window chunking, developed the AST codebase intelligence analyzer, authored the automated multi-model benchmark evaluation suite across 30 academic test cases, and containerized the solution into production Docker microservices."
