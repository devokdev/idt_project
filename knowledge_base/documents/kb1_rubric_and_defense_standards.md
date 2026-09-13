# Comprehensive Final-Year Engineering Project Evaluation Rubric, Viva Defense Standards & Academic Guidelines

## 1. Official 100-Mark Comprehensive Grading Distribution

Final-year computer science engineering capstone and major project evaluations are strictly structured around a standardized 100-mark distribution. The assessment is conducted by a joint examination committee comprising internal faculty supervisors and appointed external examiners from industry or premier academic institutions.

```
+-----------------------------------------------------------------------------------+
|               100-MARK COMPREHENSIVE PROJECT EVALUATION SCHEME                   |
+------------------------------------+--------+-------------------------------------+
| Evaluation Component               | Marks  | Focus Areas & Validation Criteria    |
+------------------------------------+--------+-------------------------------------+
| 1. Problem Formulation & Scope     | 15 M   | Real-world gap, novel objectives,   |
|                                    |        | IEEE/ACM literature survey (3-5 yrs)|
| 2. System Architecture & Design    | 20 M   | C4 diagrams, modular microservices, |
|                                    |        | DB schema 3NF/BCNF, API contracts   |
| 3. Technical Implementation        | 35 M   | Clean code, test coverage >80%,     |
|                                    |        | CI/CD, concurrency, zero memory leak|
| 4. Validation & Empirical Results  | 15 M   | P95/P99 latency, F1, MRR, ablation, |
|                                    |        | comparative benchmarks, load tests  |
| 5. Viva Voce Defense & Knowledge   | 15 M   | Cross-questioning, DSA/OS/DB depth, |
|                                    |        | defense of technical trade-offs     |
+------------------------------------+--------+-------------------------------------+
| TOTAL SCORE                        | 100 M  | Minimum Passing Score: 50 Marks     |
+------------------------------------+--------+-------------------------------------+
```

---

## 2. Detailed 4-Tier Scoring Rubric Matrix

The examination committee evaluates candidate performance using a four-tier mastery matrix across all five core evaluation dimensions:

### Tier 1: Problem Formulation, Motivation & Literature Review (15 Marks)
* **Exemplary (13 - 15 Marks)**:
  - Formulates a crisp, unambiguous engineering problem addressing verified operational, technical, or industrial bottlenecks.
  - Cites at least 15 to 20 peer-reviewed papers from IEEE Xplore, ACM Digital Library, or Springer published within the preceding 36 months.
  - Presents a structured comparative table explicitly isolating the limitations of existing state-of-the-art approaches and formulating quantitative target goals.
* **Proficient (10 - 12 Marks)**:
  - Clear problem definition with adequate industrial motivation.
  - Cites 8 to 12 relevant academic papers; literature survey correctly identifies current techniques but provides limited critique of foundational bottlenecks.
* **Developing (6 - 9 Marks)**:
  - Vague or overbroad problem definition (e.g., "build an AI chatbot").
  - Outdated or superficial citations (e.g., blog posts, generic tutorials, pre-2018 survey papers).
* **Unsatisfactory (0 - 5 Marks)**:
  - Plagiarized problem statement, absence of technical objectives, lack of scholarly review.

### Tier 2: System Architecture, Schema & High-Level Design (20 Marks)
* **Exemplary (18 - 20 Marks)**:
  - Full C4 model documentation (Context, Container, Component, and Code level diagrams) alongside formal UML sequence and state charts.
  - Decoupled microservices architecture with isolated fault domains, bounded contexts, and explicit asynchronous messaging boundaries.
  - Relational schemas normalized to 3NF/BCNF, or explicit justification for denormalized document stores and HNSW vector spaces.
  - Complete OpenAPI 3.0 REST/gRPC specifications with schema validation, idempotent semantics, and TLS transport security.
* **Proficient (14 - 17 Marks)**:
  - Solid monolithic or modular architecture with clear diagrams.
  - Database schema covers all system entities with foreign key constraints, indices, and defined API payloads.
* **Developing (8 - 13 Marks)**:
  - Architecture diagram is an undifferentiated single block or confusing diagram without explicit protocols or network boundaries.
  - Database schema lacks normalization, lacks foreign key constraints, or mixes storage concerns indiscriminately.
* **Unsatisfactory (0 - 7 Marks)**:
  - Absence of architecture diagrams; non-functional interfaces, missing API contracts.

### Tier 3: Technical Implementation, Code Quality & Engineering Rigor (35 Marks)
* **Exemplary (31 - 35 Marks)**:
  - Adherence to clean code principles (SOLID, DRY, KISS) with uniform directory layouts and idiomatic naming standards.
  - Comprehensive automated test suite combining Unit, Integration, and Mock tests achieving $>80\%$ statement and branch coverage via `pytest-cov` or `jest`.
  - Fully automated CI/CD pipeline (GitHub Actions / GitLab CI) executing linting (Flake8, Black), type verification (`mypy`), security scanning (`bandit`, `trivy`), and automated test execution on every pull request.
  - Containerization using production multi-stage Dockerfiles adhering to the Principle of Least Privilege (non-root execution, minimal scratch/alpine base images).
  - Robust exception handling with deterministic HTTP error envelopes, graceful degradation, and structured JSON telemetry logs.
* **Proficient (24 - 30 Marks)**:
  - Functional codebase implementing all core user stories with moderate automated test coverage (50% - 79%).
  - Working Docker configuration; standard error handling and clear repository structure.
* **Developing (15 - 23 Marks)**:
  - System operates partially with frequent runtime exceptions during live demonstration.
  - Code coverage $<30\%$; hardcoded database credentials or environment variables; monolithic spaghetti files.
* **Unsatisfactory (0 - 14 Marks)**:
  - Application fails to boot; missing dependencies; non-functional core modules; evidence of copied repositories without comprehension.

### Tier 4: Validation, Quantitative Benchmarks & Ablation Studies (15 Marks)
* **Exemplary (13 - 15 Marks)**:
  - Rigorous mathematical evaluation using domain-appropriate metrics:
    - For RAG/Retrieval: Precision@K, Recall@K, Mean Reciprocal Rank (MRR), Normalized Discounted Cumulative Gain (NDCG), and Hallucination Reduction Rate.
    - For Systems: P50, P90, P95, and P99 latency percentiles under concurrent load (Locust/k6), memory RSS profiles, and CPU utilization traces.
  - Controlled ablation study explicitly demonstrating the quantitative delta between baseline implementations and proposed enhancements (e.g., RAG vs. No-RAG, HNSW vs. Flat Indexing).
  - Visualization of results via automated charts (error bars, confusion matrices, latency CDF curves).
* **Proficient (10 - 12 Marks)**:
  - Standard performance evaluation with summary metrics (e.g., average latency, accuracy, basic precision/recall).
  - Visual charts present in the report, though lacking deep statistical distribution analysis or ablation comparisons.
* **Developing (5 - 9 Marks)**:
  - Subjective validation (e.g., "system worked well when tested manually").
  - Lack of standardized test datasets or benchmark questions.
* **Unsatisfactory (0 - 4 Marks)**:
  - Complete omission of quantitative evaluation or fabricated performance claims.

### Tier 5: Viva Voce Defense, Technical Depth & Individual Mastery (15 Marks)
* **Exemplary (13 - 15 Marks)**:
  - Candidate defends architectural decisions with deep theoretical rigor, citing time/space algorithmic complexity, kernel mechanisms, and concurrency primitives.
  - Demonstrates clear individual mastery of written code; accurately traces system call lifecycles, memory management, and network packet flow.
  - Gracefully addresses external examiner edge-case scenarios, failure modes, and scalability bottlenecks.
* **Proficient (10 - 12 Marks)**:
  - Explains individual modules clearly and answers standard viva questions regarding language features, database queries, and deployment commands.
* **Developing (5 - 9 Marks)**:
  - Struggles to explain code sections authored by other teammates; relies on superficial buzzwords without grasping underlying mechanics.
* **Unsatisfactory (0 - 4 Marks)**:
  - Incapable of explaining the repository codebase; total lack of individual contribution.

---

## 3. Washington Accord & Outcome-Based Education (OBE) Mapping

Final-year B.Tech projects are audited for NBA (National Board of Accreditation) and ABET compliance under the Washington Accord. The project must explicitly map to Programme Outcomes (POs):

```
+------+---------------------------------+-----------------------------------------------------------+
| PO   | Programme Outcome Descriptor   | Project Implementation Evidence & Demonstration           |
+------+---------------------------------+-----------------------------------------------------------+
| PO1  | Engineering Knowledge           | Mathematical formulation of vector spaces, HNSW graphs,  |
|      |                                 | time complexity of retrieval O(log N) vs O(N).            |
| PO2  | Problem Analysis                | Deconstruction of LLM hallucination and context clipping  |
|      |                                 | using empirical ablation experiments.                     |
| PO3  | Design / Development of Systems| Decoupled microservices architecture with REST gateways,  |
|      |                                 | persistence layers, and deterministic error handling.     |
| PO4  | Conduct Investigations          | Synthetic benchmarking across 30 questions measuring      |
|      |                                 | Precision@4, Recall@4, MRR, and P95 latency profiles.     |
| PO5  | Modern Tool Usage               | Fast LPU engines (Groq), SentenceTransformers, ChromaDB,   |
|      |                                 | Docker Compose, Uvicorn, Git, and Pytest.                 |
| PO6  | The Engineer and Society        | Democratizing access to academic mentorship and syllabus  |
|      |                                 | guidance for underprivileged engineering students.        |
| PO8  | Ethics & Academic Integrity     | Strict plagiarism limits (<=15%), open-source licensing   |
|      |                                 | compliance, transparent citation of foundational models.  |
| PO9  | Individual and Team Work        | Git branch management, PR review workflows, and modular  |
|      |                                 | ownership of decoupled microservice components.           |
| PO10 | Communication                   | High-quality technical report, clear C4 diagrams, and     |
|      |                                 | confident oral defense during external viva examination.  |
| PO12 | Life-long Learning              | Rapid adaptation to state-of-the-art transformer models,   |
|      |                                 | FlashAttention-2, and vector similarity search.           |
+------+---------------------------------+-----------------------------------------------------------+
```

---

## 4. Academic Integrity, Plagiarism Limits & Thesis Standards

1. **Plagiarism Ceiling**:
   - The overall document similarity index must **not exceed 15%** when evaluated using certified academic plagiarism engines (Turnitin, Urkund, DrillBit).
   - Any single external source must contribute **$<1\%$** similarity.
   - Methodology, algorithmic formulation, test results, and analysis chapters must have **0% verbatim similarity**.
2. **Git Version Control & Contribution Audit**:
   - The team repository must show continuous development history across the academic semesters.
   - "Big-bang commits" (pushing 10,000 lines in a single commit before deadlines) will trigger an academic integrity audit.
   - Branching Strategy: `main` (production-ready, tagged releases), `develop` (integration), and `feature/<feature-name>` (developer work).
   - Conventional Commits standard mandatory:
     - `feat: implement sliding window text chunker with overlap`
     - `fix: resolve race condition in token bucket rate limiter`
     - `test: add unit test suite for AST code symbol extractor`
     - `docs: update C4 container architecture diagrams`
3. **Thesis Structure & IEEE Standards**:
   - Chapter 1: Introduction, Problem Statement, Objectives, Scope.
   - Chapter 2: Literature Review & Related Work (Survey Table).
   - Chapter 3: System Requirements Specification & Feasibility Study.
   - Chapter 4: System Architecture & Detailed Module Design.
   - Chapter 5: Technical Implementation & Algorithmic Mechanics.
   - Chapter 6: Empirical Results, Validation & Ablation Benchmarks.
   - Chapter 7: Conclusion, Societal Impact & Future Enhancements.
   - References: Minimum 20 references formatted strictly in standard IEEE style.

---

## 5. Comprehensive Viva Voce Defense Question Bank & Model Answers

### Q1: "Why did you implement Retrieval-Augmented Generation (RAG) instead of fine-tuning the base LLM on your documents?"
* **Model Defense**:
  "Fine-tuning modifies the internal parametric weights of the model ($\Delta W$). While effective for altering linguistic tone, syntax, or specialized terminology, fine-tuning exhibits critical failure modes for factual knowledge retrieval:
  1. **Catastrophic Forgetting**: Updating weights on localized documents frequently degrades the general reasoning and instructional capabilities of the base model.
  2. **Hallucination Risk**: Parametric memory does not produce verifiable citations. The model answers from probabilistic next-token predictions rather than discrete source lookups.
  3. **Data Staleness & Cost**: Every time university guidelines or course rubrics change, the model must be retrained at significant GPU compute cost.
  4. **Access Control**: Fine-tuning cannot enforce granular document-level access control.
  In contrast, RAG decouples parametric reasoning from non-parametric external knowledge. The LLM remains frozen as a pure reasoning engine, while ChromaDB provides dynamically updatable, verifiable, and cited ground truth with sub-50ms retrieval latency."

### Q2: "Explain the time and space complexity of your vector retrieval mechanism."
* **Model Defense**:
  "Our vector store utilizes Hierarchical Navigable Small World (HNSW) graphs.
  - **Query Time Complexity**: Naive vector similarity search evaluates cosine distance across all $N$ vectors, resulting in $\mathcal{O}(N \cdot d)$ linear complexity, where $d = 384$. HNSW organizes vectors into a multi-layer hierarchical graph structure analogous to skip-lists. Top layers have long-distance links for rapid geometric traversal, while bottom layers contain dense local clustering. This reduces average query time complexity to $\mathcal{O}(\log N \cdot d)$, allowing sub-10ms retrieval across tens of thousands of document chunks.
  - **Space Complexity**: The graph index requires $\mathcal{O}(N \cdot M \cdot d)$ where $M$ is the number of bidirectional links per vector node (typically $16 \le M \le 64$).
  - **Index Construction Complexity**: Building the graph requires $\mathcal{O}(N \log N \cdot d)$ time."

### Q3: "How do you detect and prevent memory leaks and concurrency bottlenecks in your backend service?"
* **Model Defense**:
  "We employ several architectural safeguards:
  1. **Asynchronous Non-Blocking I/O**: The backend is implemented in FastAPI on an asynchronous event loop (Uvicorn / `asyncio`). Long-running operations like external Groq LLM API calls use non-blocking HTTP clients (`httpx.AsyncClient`) to ensure worker threads are never starved.
  2. **Garbage Collection of Syntax Trees**: When our AST code analyzer processes student repositories, parsed syntax trees are transiently inspected and explicitly dereferenced to allow Python's generational garbage collector to reclaim heap memory immediately.
  3. **Connection Pooling**: ChromaDB uses a singleton persistent client connection rather than re-instantiating client handles per HTTP request.
  4. **Profiling**: Memory footprint is profiled under sustained load using `psutil` and `tracemalloc`, verifying that Resident Set Size (RSS) memory stabilizes under steady-state execution."

### Q4: "What happens if ChromaDB returns irrelevant context chunks? How does your pipeline prevent hallucinated responses?"
* **Model Defense**:
  "Our architecture implements a multi-layered guardrail:
  1. **Similarity Score Thresholding**: Retrieved chunks whose cosine distance exceeds a strict threshold (e.g., cosine similarity $< 0.35$ or Euclidean distance $> 1.1$) are filtered out before prompt construction.
  2. **System Prompt Grounding Directives**: The system prompt explicitly instructs the LLM: *'Answer the question solely using the provided context chunks. If the provided context does not contain sufficient facts to answer the question, state explicitly: I do not have sufficient information in the verified knowledge base to answer this query.'*
  3. **Hallucination Scoring Layer**: The output is evaluated by measuring factual overlap (N-gram entailment and entity intersection) between the model's generated response and the retrieved context passages. If the hallucination index exceeds 40%, the response is flagged."

### Q5: "What is the significance of the 80% test coverage requirement in your rubric?"
* **Model Defense**:
  "The 80% test coverage standard (measured across line and branch coverage) guarantees that:
  1. All critical execution branches, conditional routing choices, and error handling blocks are validated against regression.
  2. Edge cases—such as malformed JSON payloads, empty retrieval results, API gateway timeouts, and invalid model selection parameters—fail gracefully with deterministic HTTP 4xx/5xx status codes rather than unhandled server crashes.
  3. Continuous Integration automatically blocks merge requests that lower test coverage below the threshold, upholding strict software engineering discipline."
