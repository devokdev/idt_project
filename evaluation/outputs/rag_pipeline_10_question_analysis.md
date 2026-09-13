# In-Depth RAG Pipeline Diagnostic & Grounding Analysis (10 Benchmark Questions)

## Case 1: What is the exact marks distribution in the final-year evaluation rubric?

**Diagnostic Classification**: `[PASS] Correct Retrieval & High Grounding`

- **Ground Truth**: Problem Formulation: 15%, System Architecture: 20%, Technical Implementation: 35%, Validation/Metrics: 15%, Viva: 15% (Total: 100 Marks).
- **Retrieval Latency**: 2.96 ms | **Total Latency**: 1417.2 ms
- **Groundedness Score**: 0.917 | **Hallucination Rate**: 8.33%

### Retrieved Context Chunks:
> **Chunk 1 (Source: `evaluation_rubric.md`, Similarity: 0.451)**:
> # Final-Year Project Evaluation Rubric and Grading Criteria...

> **Chunk 2 (Source: `evaluation_rubric.md`, Similarity: 0.389)**:
> ## 2. Detailed Performance Level Rubric

### Component 1: Technical Implementation (35 Marks)
- **Exemplary (30 - 35 Marks)**: Production-grade code, end-to-end working system, zero critical bugs during demo, clean Docker Compose setup, comprehensive...

> **Chunk 3 (Source: `common_viva_questions.md`, Similarity: 0.359)**:
> ## 1. Core Architecture & RAG Questions

### Q1: What is the core difference between fine-tuning an LLM and using RAG?
**Answer**: Fine-tuning alters the internal weights of the model with domain datasets, which is computationally expensive and suffe...

> **Chunk 4 (Source: `evaluation_rubric.md`, Similarity: 0.355)**:
> ## 1. Overall Grade Distribution (Total: 100 Marks)

| Evaluation Component | Weightage | Description |
| :--- | :--- | :--- |
| **1. Problem Formulation & Literature Survey** | **15 Marks** | Clear problem statement, novelty, review of 10+ recent IE...

### Generated RAG Answer:
**Exact Marks Distribution (Total = 100 marks)**  
*(as defined in the official evaluation rubric – see [Evaluation Rubric] section 1)*

| Evaluation Component | Weightage | Description |
|-----------------------|-----------|-------------|
| **1. Problem Formulation & Literature Survey** | **15 marks** | Clear problem statement, novelty, review of 10 + recent IEEE/ACM publications (last 3–5 years), benchmark comparisons. |
| **2. Architectural Design & Methodology** | **20 marks** | Robust system architecture, C4 models, modularity, database normalization, API contract definitions. |
| **3. Technical Implementation & Quality** | **35 marks** | Code quality, error handling, design patterns, separation of concerns, concurrency, automated test coverage > 80 %. |
| **4. Validation, Metrics & Experimentation** | **15 marks** | Quantitative evaluation: precision/recall, latency, throughput, confusion matrix, ablation studies, baseline comparisons. |
| **5. Defense, Presentation & Viva Voce** | **15 marks** | Individual student technical competence, ability to explain architectural decisions, live system demo, QA handling. |

**Key Take‑aways**

1. **Total Marks**: 100  
2. **Highest‑weighted component**: Technical Implementation & Quality (35 marks) – this is where you’ll earn the most points, so focus on clean, production‑grade code, robust error handling, and comprehensive automated tests.  
3. **Balanced evaluation**: The rubric ensures that both *design* (20 marks) and *validation* (15 marks) are valued, encouraging a well‑rounded project rather than a single “working demo.”  
4. **Defense**: The final 15 marks are awarded during the viva; prepare to articulate your architectural choices, trade‑offs, and experimental results clearly.

> **Reference**: [Evaluation Rubric – Overall Grade Distribution] (Document 4).

### Comparison without RAG:
I’m not able to provide the exact marks distribution for your final‑year evaluation because the rubric you’re referring to hasn’t been supplied.  
If you can share the rubric (or a link to the document that contains it), I’ll be able to:

1. **Break down the weightings** for each assessment component (e.g., project proposal, design documentation, implementation, testing, presentation, report, etc.).  
2. **Explain how each component maps to the overall grade** (percentage or points).  
3. **Highlight any bonus or penalty criteria** that might affect the final score.  

In the meantime, here’s a **generic template** that many universities use for final‑year projects. Feel free to compare it with your own rubric and let me know which parts differ:

| Component | Weight (%) | Typical Deliverables |
|-----------|------------|----------------------|
| Project Proposal & Feasibility Study | 10 % | Written proposal, stakeholder analysis, risk assessment |
| System Design & Architecture | 15 % | UML diagrams, architectural patterns, technology stack justification |
| Implementation / Code Quality | 30 % | Source code, build scripts, CI/CD pipeline, code reviews |
| Testing & Validation | 15 % | Unit/integration tests, test coverage reports, performance benchmarks |
| Documentation & Reporting | 10 % | Final report, user manual, API docs |
| Presentation & Demonstration | 10 % | Oral presentation, live demo, Q&A |
| Peer Review / Self‑Assessment | 5 % | Self‑evaluation, peer feedback |

**Total** | **100 %**

If your rubric includes additional categories (e.g., ethical considerations, sustainability, or innovation), just let me know and I can adjust the breakdown accordingly.

### Analytical Finding:
Retriever fetched authoritative rubric/guidelines; answer grounded strictly on extracted facts.

---

## Case 2: What are the requirements for an Exemplary score in Quantitative Validation?

**Diagnostic Classification**: `[WARN] Parametric Hallucination despite Context`

- **Ground Truth**: Rigorous metrics computed on verified datasets (F1, MRR, latency P95/P99, RAM/CPU profiling) with comparative charts.
- **Retrieval Latency**: 3.0 ms | **Total Latency**: 2008.5 ms
- **Groundedness Score**: 0.4 | **Hallucination Rate**: 60.0%

### Retrieved Context Chunks:
> **Chunk 1 (Source: `project_proposal_template.md`, Similarity: 0.300)**:
> ## 2. Executive Summary / Abstract (250 Words)
Briefly describe the engineering problem being solved, the proposed methodology, the key technologies utilized, and expected measurable outcomes.

---...

> **Chunk 2 (Source: `ai_ml_workflow_documentation.md`, Similarity: 0.289)**:
> ## 4. Evaluation Metrics for LLM Systems
- **Precision@K & Recall@K**: Measures the proportion of relevant chunks retrieved in top K results.
- **Mean Reciprocal Rank (MRR)**: Evaluates the ranking quality of the first relevant chunk.
- **Hallucinati...

> **Chunk 3 (Source: `common_viva_questions.md`, Similarity: 0.274)**:
> ## 2. System Performance & Engineering Questions

### Q4: How do you measure and mitigate model hallucinations?
**Answer**: We implement a Hallucination Detector service that parses the claims in the generated response and computes semantic entailmen...

> **Chunk 4 (Source: `common_viva_questions.md`, Similarity: 0.267)**:
> ## 1. Core Architecture & RAG Questions

### Q1: What is the core difference between fine-tuning an LLM and using RAG?
**Answer**: Fine-tuning alters the internal weights of the model with domain datasets, which is computationally expensive and suffe...

### Generated RAG Answer:
**Exemplary Quantitative Validation**  
*(Grounded in the project guidelines and evaluation metrics outlined in the provided documents)*  

| Metric | Target for “Exemplary” | Why it matters | How to demonstrate it |
|--------|------------------------|----------------|-----------------------|
| **Precision@K** (K = 10) | **≥ 0.90** | Indicates that the top‑10 retrieved chunks are almost all relevant. | Report the precision curve for K = 1, 5, 10 on a held‑out test set; show that 90 % of the top‑10 chunks contain the answer. |
| **Recall@K** (K = 10) | **≥ 0.85** | Ensures that most relevant facts are captured within the first 10 results. | Compute recall on the same test set; demonstrate that 85 % of the gold‑standard relevant chunks appear in the top‑10. |
| **Mean Reciprocal Rank (MRR)** | **≥ 0.75** | Measures how early the first correct chunk appears. | Show the MRR calculation over all queries; an MRR ≥ 0.75 means the first correct chunk is usually within the top‑4. |
| **Hallucination Rate** | **≤ 5 %** | Low hallucination guarantees that the LLM’s claims are supported by retrieved context. | Use the Hallucination Detector service described in Q4 of the viva guide; report the percentage of unsupported claims. |
| **Latency (ms)** | **P95 ≤ 200 ms** | End‑to‑end user wait time must be sub‑200 ms for a production‑grade system. | Split latency into Embedding, Retrieval, and Token‑generation components; provide a latency histogram and confirm the 95th percentile is ≤ 200 ms. |
| **Token Throughput** | **≥ 200 tokens/s** | Demonstrates scalability under load. | Run a load‑test (e.g., 100 concurrent users) and show sustained throughput. |
| **Resource Footprint** | **CPU ≤ 4 cores, RAM ≤ 8 GB** | Indicates efficient deployment. | Provide a resource‑usage profile during peak load. |

### Why These Targets?
- **Precision & Recall** are the core IR metrics for a Retrieval‑Augmented Generation (RAG) pipeline; they directly reflect the quality of the vector search (see [Document 2] and [Document 3] Q6).  
- **MRR** captures ranking quality, which is critical for user satisfaction when the first relevant chunk is returned quickly.  
- **Hallucination Rate** is a mandatory metric for any LLM‑based system; the guidelines in [Document 3] Q4 emphasize the need for a detector that flags unsupported claims.  
- **Latency** and **throughput** are system‑level metrics that demonstrate the solution’s readiness for real‑world deployment, as highlighted in [Document 3] Q5.  
- **Resource Footprint** ensures the architecture is lightweight enough for containerised deployment (Docker Compose, isolated network bridges) as described in [Document 3] Q5.

### How to Achieve an Exemplary Score
1. **Chunking Strategy** – Use the 500‑word chunk size with 80‑word overlap (per [Document 4] Q3) to preserve context while keeping vectors dense.  
2. **Embedding Model** – Choose a high‑accuracy sentence‑embedding model (e.g., `all-MiniLM-L6-v2`) and fine‑tune it on domain data if necessary.  
3. **Vector Store** – Deploy ChromaDB with HNSW indexing (per [Document 4] Q2) and tune the `ef` and `M` parameters for optimal recall/latency trade‑off.  
4. **Retrieval Pipeline** – Cache

### Comparison without RAG:
**Answer – What constitutes an “Exemplary” score in the *Quantitative Validation* section**

> **NOTE:** The exact wording of the rubric, the grading rubric marks, and any project‑specific guidelines you received from your supervisor or the course handbook are the ultimate authority.  
> If you can share the rubric or the relevant excerpt, I can tailor this answer to match the precise wording and weightings.  
> In the meantime, the following checklist is based on common industry‑grade and academic standards for quantitative validation in software/ML projects.  Use it as a *template* and compare it against your own rubric.

| # | Requirement | Why it matters | Typical “Exemplary” evidence |
|---|-------------|----------------|------------------------------|
| 1 | **Clear, reproducible experimental design** | Ensures that results can be independently verified. | A detailed README or Jupyter notebook that documents data splits, random seeds, hyper‑parameter settings, and the exact command‑line or API calls used. |
| 2 | **Appropriate statistical metrics** | Demonstrates that you chose the right measure for the problem (e.g., RMSE for regression, F1‑score for imbalanced classification). | Reported metrics with confidence intervals or standard deviations, and a justification for each metric. |
| 3 | **Robustness checks / sensitivity analysis** | Shows that the model’s performance is stable across reasonable variations. | Experiments varying training‑validation split, hyper‑parameters, or data augmentation, with results plotted or tabulated. |
| 4 | **Baseline comparison** | Contextualizes your model’s performance. | Comparison against at least two baselines (e.g., a simple rule‑based model and a state‑of‑the‑art benchmark). |
| 5 | **Statistical significance testing** | Provides evidence that improvements are not due to chance. | p‑values from paired t‑tests, Wilcoxon signed‑rank tests, or bootstrap confidence intervals, with a clear interpretation. |
| 6 | **Error analysis** | Reveals where the model fails and informs future work. | Visualizations (confusion matrix, error heatmaps) and a written discussion of common failure modes. |
| 7 | **Scalability / runtime analysis** | Demonstrates that the solution can handle realistic workloads. | Profiling results (CPU/GPU usage, memory consumption) and a discussion of bottlenecks and potential optimizations. |
| 8 | **Reproducibility & documentation** | Enables others to replicate the study. | A Dockerfile or Conda environment file, version‑controlled code, and a reproducibility checklist. |
| 9 | **Compliance with software standards** | Shows professional‑grade engineering. | Adherence to coding style guidelines (PEP‑8, Google Style), unit tests covering >90 % of the code, and static analysis warnings cleared. |
|10 | **Clear, concise reporting** | Communicates findings effectively. | A well‑structured report or presentation with an executive summary, methodology, results, discussion, and future work. |

---

### How to map this to your rubric

1. **Locate the rubric section** that lists the *Quantitative Validation* criteria.  
2. **Match each rubric item** to the table above.  
3. **Score each item**:  
   * *Exemplary* – Meets or exceeds the requirement with thorough evidence.  
   * *Proficient* – Meets the requirement but lacks depth or documentation.  
   * *Developing* – Meets the minimum but is incomplete or poorly documented.  
   * *Emerging* – Does not meet the requirement.  

4. **Document your evidence** in the report or submission portal, referencing the exact rubric item numbers.

---

### Quick checklist for your submission

- [ ] **Experiment reproducibility** – seed, split, command line.  
- [ ] **Metrics & justification** – list & explain.  
- [ ] **Baseline & comparison** – at least two.  
- [ ] **Statistical tests** – p‑values or confidence intervals.  
- [ ] **Error analysis** – visual + narrative.  
- [ ] **Scalability metrics** – runtime, memory.

### Analytical Finding:
LLM injected additional generic statements not present in retrieved context.

---

## Case 3: What is the maximum allowed plagiarism similarity percentage for thesis submission?

**Diagnostic Classification**: `[WARN] Parametric Hallucination despite Context`

- **Ground Truth**: Similarity index must not exceed 15% using Turnitin or Urkund.
- **Retrieval Latency**: 4.99 ms | **Total Latency**: 2166.24 ms
- **Groundedness Score**: 0.048 | **Hallucination Rate**: 95.24%

### Retrieved Context Chunks:
> **Chunk 1 (Source: `common_viva_questions.md`, Similarity: 0.298)**:
> ## 2. System Performance & Engineering Questions

### Q4: How do you measure and mitigate model hallucinations?
**Answer**: We implement a Hallucination Detector service that parses the claims in the generated response and computes semantic entailmen...

> **Chunk 2 (Source: `ai_ml_workflow_documentation.md`, Similarity: 0.263)**:
> ## 4. Evaluation Metrics for LLM Systems
- **Precision@K & Recall@K**: Measures the proportion of relevant chunks retrieved in top K results.
- **Mean Reciprocal Rank (MRR)**: Evaluates the ranking quality of the first relevant chunk.
- **Hallucinati...

> **Chunk 3 (Source: `common_viva_questions.md`, Similarity: 0.257)**:
> ## 1. Core Architecture & RAG Questions

### Q1: What is the core difference between fine-tuning an LLM and using RAG?
**Answer**: Fine-tuning alters the internal weights of the model with domain datasets, which is computationally expensive and suffe...

> **Chunk 4 (Source: `ai_ml_workflow_documentation.md`, Similarity: 0.237)**:
> ## 3. Large Language Model Selection Criteria
- **Code Llama 7B Instruct**: Specialized for code generation, software architecture design, debugging, and repository understanding.
- **StarCoder2**: Optimized for multi-language code completion, reposi...

### Generated RAG Answer:
**Answer**

The documents you shared (the RAG‑pipeline documentation, evaluation metrics, and core architecture questions) do **not** contain any information about the plagiarism policy or the maximum similarity percentage allowed for a thesis submission.  
Because the policy is institution‑specific, you’ll need to consult the official guidelines issued by your university’s graduate school, the department handbook, or the plagiarism‑check service (e.g., Turnitin, iThenticate) that your institution uses.

---

### What you should do next

| Step | Action | Why it matters |
|------|--------|----------------|
| 1 | **Locate the official thesis guidelines** | These documents usually specify the acceptable similarity threshold (e.g., 20 %, 25 %, or 30 %) and any additional requirements (e.g., which parts of the thesis are exempt from the check). |
| 2 | **Check the plagiarism‑check tool’s settings** | Some tools allow you to exclude certain sections (bibliography, code listings, tables) or to set a custom threshold. |
| 3 | **Run a pre‑submission check** | Use the same tool your university mandates to get an accurate similarity report before you submit. |
| 4 | **Review flagged passages** | Even if the overall similarity is below the threshold, you may still need to paraphrase or properly cite any highlighted text. |
| 5 | **Document your process** | Keep a record of the similarity report and any revisions you made; this can be useful if the committee asks for proof of originality. |

---

### Typical thresholds (for context)

| Institution | Common threshold | Notes |
|-------------|------------------|-------|
| UK universities (e.g., Oxford, Cambridge) | 15 %–20 % | Often lower for first‑year dissertations; higher for senior theses. |
| US universities | 20 %–25 % | Turnitin reports are usually accepted if below 25 %. |
| Australian universities | 25 % | Some departments allow up to 30 % for literature reviews. |

> **Caution:** These numbers are illustrative. Your university may have a stricter or more lenient policy, and the threshold can vary by faculty or program.

---

### Quick checklist for reducing similarity

1. **Paraphrase effectively** – rewrite sentences in your own words while preserving meaning.
2. **Cite properly** – use the citation style mandated by your department (APA, IEEE, Chicago, etc.).
3. **Use quotation marks** for any verbatim excerpts and include a citation.
4. **Avoid large blocks of copied text** – even if cited, they can inflate similarity scores.
5. **Include a “Methodology” or “Literature Review” section** that synthesizes sources rather than reproducing them.

---

**Bottom line:**  
The maximum allowed plagiarism similarity percentage is *not* specified in the documents you provided. Please refer to your university’s official thesis or dissertation guidelines, or contact the graduate school office, to obtain the exact figure. Once you have that number, you can run a similarity check and adjust your manuscript accordingly.

### Comparison without RAG:
**Short answer:**  
There is no single “universal” percentage that applies to every university or department.  Most UK and US institutions set a **similarity threshold of 15 – 20 %** for a thesis, but the exact figure—and how it is interpreted—depends on the specific university’s plagiarism policy, the department’s handbook, and the rubric that your supervisor has agreed upon.  

Below is a practical, step‑by‑step guide to determine the exact limit for your situation and to keep your similarity score comfortably below it.

---

## 1. Locate the official policy

| Source | What to look for | Why it matters |
|--------|------------------|----------------|
| **University Thesis Handbook** | “Plagiarism and similarity” section | Gives the *official* threshold and any special rules (e.g., “no more than 10 % for the entire document, but up to 25 % if all matches are properly cited”). |
| **Department/Faculty Guidelines** | “Submission requirements” | Departments sometimes tighten the rule (e.g., 12 % for engineering, 15 % for humanities). |
| **Rubric / Assessment Criteria** | “Academic integrity” or “Originality” | The rubric may explicitly state the maximum similarity score or the penalty for exceeding it. |
| **Supervisor / Thesis Coordinator** | Personal confirmation | Supervisors often know the *practical* threshold used in grading and can confirm any recent changes. |

> **If you cannot find a written policy**:  
> 1. Check the university’s *Academic Integrity* or *Student Handbook* online.  
> 2. Email the *Academic Integrity Office* or *Student Services* with a concise question: “What is the maximum similarity score allowed for a final‑year thesis?”  
> 3. Ask your supervisor for confirmation.

---

## 2. Typical thresholds (by region)

| Region | Typical threshold | Notes |
|--------|-------------------|-------|
| **UK (e.g., UoA, UoB, UoC)** | 15 % (whole document) | Some universities allow up to 20 % if all matches are cited. |
| **US (e.g., MIT, Stanford)** | 10 % – 15 % | Many use Turnitin; the “acceptable” range is often 10 % for the whole document. |
| **Australia** | 15 % – 20 % | Some institutions have a “no more than 10 % for the abstract” rule. |
| **Canada** | 15 % – 20 % | Similar to UK, but check the specific university. |
| **Europe (non‑UK)** | 10 % – 15 % | Varies widely; always confirm. |

> **Bottom line:** Aim for **< 10 %** similarity if you want a comfortable margin, unless your institution explicitly allows a higher threshold.

---

## 3. How similarity scores are calculated

| Tool | What it matches | How it is reported | What counts as “plagiarism” |
|------|-----------------|--------------------|-----------------------------|
| **Turnitin / iThenticate** | Exact phrases, parap

### Analytical Finding:
LLM injected additional generic statements not present in retrieved context.

---

## Case 4: Why is L2 normalization applied to embedding vectors before vector search?

**Diagnostic Classification**: `[WARN] Parametric Hallucination despite Context`

- **Ground Truth**: L2 normalization enables cosine similarity to be computed directly via dot products.
- **Retrieval Latency**: 5.05 ms | **Total Latency**: 939.91 ms
- **Groundedness Score**: 0.733 | **Hallucination Rate**: 26.67%

### Retrieved Context Chunks:
> **Chunk 1 (Source: `ai_ml_workflow_documentation.md`, Similarity: 0.365)**:
> ## 2. RAG Pipeline Stages
1. **Document Ingestion**:
   - Ingest multiple formats (PDF, Markdown, JSON, Source Code).
   - Sanitize text, strip non-printable tokens, and preserve hierarchical metadata (e.g. document title, section, page).
2. **Semant...

> **Chunk 2 (Source: `ai_ml_workflow_documentation.md`, Similarity: 0.279)**:
> ## 1. Overview of Retrieval-Augmented Generation (RAG)
Retrieval-Augmented Generation (RAG) combines dense vector information retrieval with generative Large Language Models to provide grounded, domain-specific, hallucination-resistant answers.

```
...

> **Chunk 3 (Source: `common_viva_questions.md`, Similarity: 0.266)**:
> ## 1. Core Architecture & RAG Questions

### Q1: What is the core difference between fine-tuning an LLM and using RAG?
**Answer**: Fine-tuning alters the internal weights of the model with domain datasets, which is computationally expensive and suffe...

> **Chunk 4 (Source: `project_guidelines.md`, Similarity: 0.228)**:
> ## 1. Introduction and Objectives
The Final-Year Capstone Project is the culminating academic requirement for Bachelor of Engineering (B.E./B.Tech) students. The objective is to design, develop, test, and demonstrate an innovative engineering solutio...

### Generated RAG Answer:
### AI Project Mentor Guidance [openai/gpt-oss-20b]:

Based on the official university academic guidelines and project documentation:

1. **2. RAG Pipeline Stages**: Normalization: L2 normalization is applied to vectors to allow Cosine Similarity to be computed as an efficient dot product.
2. **1. Overview of Retrieval-Augmented Generation (RAG)**: Query -> Embedding Model -> Dense Vector -> Approximate Nearest Neighbor (ANN) Vector Search -> Top-K Context Chunks -> Contextual Prompt Synthesis -> Generative LLM -> Grounded Answer
3. **Q2: Why did you choose ChromaDB over relational databases like MySQL for context search?**: Answer**: Relational databases excel at structured ACID queries and exact keyword matching (B-Tree indexes), but fail at semantic/conceptual similarity search. ChromaDB implements Hierarchical Navigable Small World (HNSW) graph indexing over dense vector spaces, enabling sub-millisecond Approximate Nearest Neighbor (ANN) search with cosine distance metrics.
4. **Q3: How do you choose the chunk size and overlap in your RAG pipeline?**: Answer**: We configured a chunk size of 500 words with an 80-word sliding window overlap. A chunk size that is too small loses sentence context and discourse cohesion, while an excessively large chunk dilutes semantic density in the embedding vector. The overlap guarantees that sentences spanning boundary transitions are not artificially clipped.
5. **2. RAG Pipeline Stages**: Dense Vector Embeddings**:
6. **1. Overview of Retrieval-Augmented Generation (RAG)**: Retrieval-Augmented Generation (RAG) combines dense vector information retrieval with generative Large Language Models to provide grounded, domain-specific, hallucination-resistant answers.
7. **Q1: What is the core difference between fine-tuning an LLM and using RAG?**: Answer**: Fine-tuning alters the internal weights of the model with domain datasets, which is computationally expensive and suffers from catastrophic forgetting. RAG decouples knowledge storage from the language model by dynamically retrieving relevant facts from a vector database at query time, ensuring up-to-date facts, zero hallucination of private guidelines, and transparent citations.

**Actionable Next Steps**:
- Verify deliverables against the official university project rubrics.
- Ensure code test coverage meets or exceeds standard evaluation thresholds (>80%).
- Document all architectural decisions and API specifications in your project report.

### Comparison without RAG:
### AI Project Mentor Guidance [openai/gpt-oss-20b]:

For your final-year project inquiry, follow these standard steps:
1. **Requirements & Scope**: Define clear input-output specifications with strict validation schemas.
2. **Architecture**: Decouple business logic, vector storage, and API routing microservices.
3. **Quantitative Metrics**: Measure latency (P95/P99), accuracy, and resource utilization (RAM/CPU).
4. **Verification**: Implement comprehensive Pytest unit and integration test suites for every component.

### Analytical Finding:
LLM injected additional generic statements not present in retrieved context.

---

## Case 5: What branching strategy should be used according to the team Git standards?

**Diagnostic Classification**: `[WARN] Parametric Hallucination despite Context`

- **Ground Truth**: GitFlow Lite: main, develop, and feature/<name> branches with Pull Requests.
- **Retrieval Latency**: 4.06 ms | **Total Latency**: 1001.52 ms
- **Groundedness Score**: 0.667 | **Hallucination Rate**: 33.33%

### Retrieved Context Chunks:
> **Chunk 1 (Source: `ai_ml_workflow_documentation.md`, Similarity: 0.278)**:
> ## 2. RAG Pipeline Stages
1. **Document Ingestion**:
   - Ingest multiple formats (PDF, Markdown, JSON, Source Code).
   - Sanitize text, strip non-printable tokens, and preserve hierarchical metadata (e.g. document title, section, page).
2. **Semant...

> **Chunk 2 (Source: `git_workflow_standards.md`, Similarity: 0.249)**:
> ## 1. Git Branching Strategy (GitFlow Lite)
For team collaboration in academic and production environments, use the following branching model:

```
  main (production releases, tags v1.0.0)
   ↑
  develop (integration branch)
   ↑ 
  feature/rag-retr...

> **Chunk 3 (Source: `common_viva_questions.md`, Similarity: 0.248)**:
> ## 2. System Performance & Engineering Questions

### Q4: How do you measure and mitigate model hallucinations?
**Answer**: We implement a Hallucination Detector service that parses the claims in the generated response and computes semantic entailmen...

> **Chunk 4 (Source: `git_workflow_standards.md`, Similarity: 0.239)**:
> # Git Workflow & Version Control Standards for Engineering Projects...

### Generated RAG Answer:
### AI Project Mentor Guidance [openai/gpt-oss-20b]:

Based on the official university academic guidelines and project documentation:

1. **1. Git Branching Strategy (GitFlow Lite)**: For team collaboration in academic and production environments, use the following branching model:
2. **1. Git Branching Strategy (GitFlow Lite)**: main (production releases, tags v1.0.0)
3. **1. Git Branching Strategy (GitFlow Lite)**: develop (integration branch)
4. **1. Git Branching Strategy (GitFlow Lite)**: feature/rag-retriever  feature/api-gateway  feature/eval-metrics
5. **1. Git Branching Strategy (GitFlow Lite)**: `main`**: Protected branch. Only fully tested and reviewed releases are merged here.
6. **1. Git Branching Strategy (GitFlow Lite)**: `develop`**: Central integration branch for ongoing development.
7. **1. Git Branching Strategy (GitFlow Lite)**: `feature/<name>`**: Feature branches branched from `develop` and merged via Pull Requests.

**Actionable Next Steps**:
- Verify deliverables against the official university project rubrics.
- Ensure code test coverage meets or exceeds standard evaluation thresholds (>80%).
- Document all architectural decisions and API specifications in your project report.

### Comparison without RAG:
### AI Project Mentor Guidance [openai/gpt-oss-20b]:

For your final-year project inquiry, follow these standard steps:
1. **Requirements & Scope**: Define clear input-output specifications with strict validation schemas.
2. **Architecture**: Decouple business logic, vector storage, and API routing microservices.
3. **Quantitative Metrics**: Measure latency (P95/P99), accuracy, and resource utilization (RAM/CPU).
4. **Verification**: Implement comprehensive Pytest unit and integration test suites for every component.

### Analytical Finding:
LLM injected additional generic statements not present in retrieved context.

---

## Case 6: What is the time complexity of vector retrieval in ChromaDB?

**Diagnostic Classification**: `[WARN] Parametric Hallucination despite Context`

- **Ground Truth**: HNSW indexing achieves O(log N) average search time.
- **Retrieval Latency**: 6.0 ms | **Total Latency**: 914.39 ms
- **Groundedness Score**: 0.75 | **Hallucination Rate**: 25.0%

### Retrieved Context Chunks:
> **Chunk 1 (Source: `ai_ml_workflow_documentation.md`, Similarity: 0.415)**:
> ## 4. Evaluation Metrics for LLM Systems
- **Precision@K & Recall@K**: Measures the proportion of relevant chunks retrieved in top K results.
- **Mean Reciprocal Rank (MRR)**: Evaluates the ranking quality of the first relevant chunk.
- **Hallucinati...

> **Chunk 2 (Source: `common_viva_questions.md`, Similarity: 0.389)**:
> ## 1. Core Architecture & RAG Questions

### Q1: What is the core difference between fine-tuning an LLM and using RAG?
**Answer**: Fine-tuning alters the internal weights of the model with domain datasets, which is computationally expensive and suffe...

> **Chunk 3 (Source: `common_viva_questions.md`, Similarity: 0.368)**:
> ## 2. System Performance & Engineering Questions

### Q4: How do you measure and mitigate model hallucinations?
**Answer**: We implement a Hallucination Detector service that parses the claims in the generated response and computes semantic entailmen...

> **Chunk 4 (Source: `ai_ml_workflow_documentation.md`, Similarity: 0.348)**:
> ## 1. Overview of Retrieval-Augmented Generation (RAG)
Retrieval-Augmented Generation (RAG) combines dense vector information retrieval with generative Large Language Models to provide grounded, domain-specific, hallucination-resistant answers.

```
...

### Generated RAG Answer:
### AI Project Mentor Guidance [openai/gpt-oss-20b]:

Based on the official university academic guidelines and project documentation:

1. **Q1: What is the core difference between fine-tuning an LLM and using RAG?**: Answer**: Fine-tuning alters the internal weights of the model with domain datasets, which is computationally expensive and suffers from catastrophic forgetting. RAG decouples knowledge storage from the language model by dynamically retrieving relevant facts from a vector database at query time, ensuring up-to-date facts, zero hallucination of private guidelines, and transparent citations.
2. **Q5: How is your application containerized and deployed?**: Answer**: The system uses Docker Compose with isolated network bridges. The backend, retriever, and LLM services run as distinct services, with the persistent ChromaDB directory bind-mounted to preserve vector collections across container restarts.
3. **1. Overview of Retrieval-Augmented Generation (RAG)**: Query -> Embedding Model -> Dense Vector -> Approximate Nearest Neighbor (ANN) Vector Search -> Top-K Context Chunks -> Contextual Prompt Synthesis -> Generative LLM -> Grounded Answer
4. **Q2: Why did you choose ChromaDB over relational databases like MySQL for context search?**: Answer**: Relational databases excel at structured ACID queries and exact keyword matching (B-Tree indexes), but fail at semantic/conceptual similarity search. ChromaDB implements Hierarchical Navigable Small World (HNSW) graph indexing over dense vector spaces, enabling sub-millisecond Approximate Nearest Neighbor (ANN) search with cosine distance metrics.
5. **Q3: How do you choose the chunk size and overlap in your RAG pipeline?**: Answer**: We configured a chunk size of 500 words with an 80-word sliding window overlap. A chunk size that is too small loses sentence context and discourse cohesion, while an excessively large chunk dilutes semantic density in the embedding vector. The overlap guarantees that sentences spanning boundary transitions are not artificially clipped.
6. **Q6: What metrics did you use to evaluate your RAG pipeline?**: Answer**: We evaluated using Information Retrieval metrics (Precision@K, Recall@K, Mean Reciprocal Rank - MRR), Generation metrics (Correctness, Semantic Relevance, Hallucination Rate), and System metrics (P95 Latency in milliseconds, Token throughput, and Memory/CPU footprint).
7. **1. Overview of Retrieval-Augmented Generation (RAG)**: Retrieval-Augmented Generation (RAG) combines dense vector information retrieval with generative Large Language Models to provide grounded, domain-specific, hallucination-resistant answers.

**Actionable Next Steps**:
- Verify deliverables against the official university project rubrics.
- Ensure code test coverage meets or exceeds standard evaluation thresholds (>80%).
- Document all architectural decisions and API specifications in your project report.

### Comparison without RAG:
### AI Project Mentor Guidance [openai/gpt-oss-20b]:

For your final-year project inquiry, follow these standard steps:
1. **Requirements & Scope**: Define clear input-output specifications with strict validation schemas.
2. **Architecture**: Decouple business logic, vector storage, and API routing microservices.
3. **Quantitative Metrics**: Measure latency (P95/P99), accuracy, and resource utilization (RAM/CPU).
4. **Verification**: Implement comprehensive Pytest unit and integration test suites for every component.

### Analytical Finding:
LLM injected additional generic statements not present in retrieved context.

---

## Case 7: How do you handle 504 Gateway Timeouts when calling Ollama models?

**Diagnostic Classification**: `[WARN] Parametric Hallucination despite Context`

- **Ground Truth**: Increase timeout_seconds, check VRAM loading, and verify Ollama port 11434.
- **Retrieval Latency**: 5.0 ms | **Total Latency**: 952.82 ms
- **Groundedness Score**: 0.75 | **Hallucination Rate**: 25.0%

### Retrieved Context Chunks:
> **Chunk 1 (Source: `git_workflow_standards.md`, Similarity: 0.279)**:
> ## 2. Conventional Commit Message Standards
Every commit must follow the Conventional Commits specification:
- `feat: add ChromaDB persistent vector retrieval service`
- `fix: handle HTTP 504 timeout when Ollama is loading model weights`
- `docs: upd...

> **Chunk 2 (Source: `project_proposal_template.md`, Similarity: 0.259)**:
> ## 6. Gantt Chart & Semester Roadmap
- Weeks 1-4: Requirements analysis, literature survey, and initial prototype.
- Weeks 5-8: Core API development and database integration.
- Weeks 9-12: Algorithmic optimization, quantitative benchmarking, and UI c...

> **Chunk 3 (Source: `common_viva_questions.md`, Similarity: 0.241)**:
> ## 2. System Performance & Engineering Questions

### Q4: How do you measure and mitigate model hallucinations?
**Answer**: We implement a Hallucination Detector service that parses the claims in the generated response and computes semantic entailmen...

> **Chunk 4 (Source: `evaluation_rubric.md`, Similarity: 0.203)**:
> ## 3. External Examiner Viva Voce Expectations
External examiners evaluate each individual team member on:
1. Identifying exactly which files and modules the student wrote personally.
2. Explaining time and space complexity of custom algorithms.
3. J...

### Generated RAG Answer:
### AI Project Mentor Guidance [openai/gpt-oss-20b]:

Based on the official university academic guidelines and project documentation:

1. **2. Conventional Commit Message Standards**: `fix: handle HTTP 504 timeout when Ollama is loading model weights`
2. **Q4: How do you measure and mitigate model hallucinations?**: Answer**: We implement a Hallucination Detector service that parses the claims in the generated response and computes semantic entailment against the retrieved reference chunks. If an LLM assertion cannot be mapped to the retrieved context chunks with a minimum threshold (>0.60), it is flagged as an unsupported claim.
3. **Q5: How is your application containerized and deployed?**: Answer**: The system uses Docker Compose with isolated network bridges. The backend, retriever, and LLM services run as distinct services, with the persistent ChromaDB directory bind-mounted to preserve vector collections across container restarts.
4. **3. External Examiner Viva Voce Expectations**: Explaining how failures, network timeouts, and model hallucinations are mitigated.
5. **Q6: What metrics did you use to evaluate your RAG pipeline?**: Answer**: We evaluated using Information Retrieval metrics (Precision@K, Recall@K, Mean Reciprocal Rank - MRR), Generation metrics (Correctness, Semantic Relevance, Hallucination Rate), and System metrics (P95 Latency in milliseconds, Token throughput, and Memory/CPU footprint).
6. **2. Conventional Commit Message Standards**: `docs: update evaluation rubric documentation and guidelines`
7. **2. Conventional Commit Message Standards**: Every commit must follow the Conventional Commits specification:

**Actionable Next Steps**:
- Verify deliverables against the official university project rubrics.
- Ensure code test coverage meets or exceeds standard evaluation thresholds (>80%).
- Document all architectural decisions and API specifications in your project report.

### Comparison without RAG:
## 1. Why a 504 Gateway Timeout Appears

| Layer | What Happens | Typical Cause |
|-------|--------------|---------------|
| **Client → API Gateway** | The gateway forwards the request to the Ollama service. | The gateway’s upstream timeout is reached before the Ollama server replies. |
| **API Gateway → Ollama** | Ollama processes the request (e.g., token‑generation, model inference

### Analytical Finding:
LLM injected additional generic statements not present in retrieved context.

---

## Case 8: What is the difference between fine-tuning and RAG for academic project mentoring?

**Diagnostic Classification**: `[WARN] Parametric Hallucination despite Context`

- **Ground Truth**: Fine-tuning modifies model weights with risk of forgetting; RAG dynamically retrieves factual context at query time.
- **Retrieval Latency**: 6.59 ms | **Total Latency**: 1025.4 ms
- **Groundedness Score**: 0.765 | **Hallucination Rate**: 23.53%

### Retrieved Context Chunks:
> **Chunk 1 (Source: `project_guidelines.md`, Similarity: 0.469)**:
> ## 1. Introduction and Objectives
The Final-Year Capstone Project is the culminating academic requirement for Bachelor of Engineering (B.E./B.Tech) students. The objective is to design, develop, test, and demonstrate an innovative engineering solutio...

> **Chunk 2 (Source: `common_viva_questions.md`, Similarity: 0.389)**:
> ## 1. Core Architecture & RAG Questions

### Q1: What is the core difference between fine-tuning an LLM and using RAG?
**Answer**: Fine-tuning alters the internal weights of the model with domain datasets, which is computationally expensive and suffe...

> **Chunk 3 (Source: `project_proposal_template.md`, Similarity: 0.347)**:
> ## 3. Problem Statement & Motivation
- **The Core Problem**: Define exactly what real-world or academic problem is being tackled.
- **Existing Gaps**: Why do current existing tools or approaches fall short?
- **Proposed Innovation**: What is novel ab...

> **Chunk 4 (Source: `common_viva_questions.md`, Similarity: 0.310)**:
> ## 2. System Performance & Engineering Questions

### Q4: How do you measure and mitigate model hallucinations?
**Answer**: We implement a Hallucination Detector service that parses the claims in the generated response and computes semantic entailmen...

### Generated RAG Answer:
### AI Project Mentor Guidance [openai/gpt-oss-20b]:

Based on the official university academic guidelines and project documentation:

1. **Q1: What is the core difference between fine-tuning an LLM and using RAG?**: Answer**: Fine-tuning alters the internal weights of the model with domain datasets, which is computationally expensive and suffers from catastrophic forgetting. RAG decouples knowledge storage from the language model by dynamically retrieving relevant facts from a vector database at query time, ensuring up-to-date facts, zero hallucination of private guidelines, and transparent citations.
2. **1. Introduction and Objectives**: The Final-Year Capstone Project is the culminating academic requirement for Bachelor of Engineering (B.E./B.Tech) students. The objective is to design, develop, test, and demonstrate an innovative engineering solution addressing real-world problems.
3. **Q6: What metrics did you use to evaluate your RAG pipeline?**: Answer**: We evaluated using Information Retrieval metrics (Precision@K, Recall@K, Mean Reciprocal Rank - MRR), Generation metrics (Correctness, Semantic Relevance, Hallucination Rate), and System metrics (P95 Latency in milliseconds, Token throughput, and Memory/CPU footprint).
4. **Q3: How do you choose the chunk size and overlap in your RAG pipeline?**: Answer**: We configured a chunk size of 500 words with an 80-word sliding window overlap. A chunk size that is too small loses sentence context and discourse cohesion, while an excessively large chunk dilutes semantic density in the embedding vector. The overlap guarantees that sentences spanning boundary transitions are not artificially clipped.
5. **3. Problem Statement & Motivation**: The Core Problem**: Define exactly what real-world or academic problem is being tackled.
6. **Q2: Why did you choose ChromaDB over relational databases like MySQL for context search?**: Answer**: Relational databases excel at structured ACID queries and exact keyword matching (B-Tree indexes), but fail at semantic/conceptual similarity search. ChromaDB implements Hierarchical Navigable Small World (HNSW) graph indexing over dense vector spaces, enabling sub-millisecond Approximate Nearest Neighbor (ANN) search with cosine distance metrics.
7. **Q4: How do you measure and mitigate model hallucinations?**: Answer**: We implement a Hallucination Detector service that parses the claims in the generated response and computes semantic entailment against the retrieved reference chunks. If an LLM assertion cannot be mapped to the retrieved context chunks with a minimum threshold (>0.60), it is flagged as an unsupported claim.

**Actionable Next Steps**:
- Verify deliverables against the official university project rubrics.
- Ensure code test coverage meets or exceeds standard evaluation thresholds (>80%).
- Document all architectural decisions and API specifications in your project report.

### Comparison without RAG:
### AI Project Mentor Guidance [openai/gpt-oss-20b]:

For your final-year project inquiry, follow these standard steps:
1. **Requirements & Scope**: Define clear input-output specifications with strict validation schemas.
2. **Architecture**: Decouple business logic, vector storage, and API routing microservices.
3. **Quantitative Metrics**: Measure latency (P95/P99), accuracy, and resource utilization (RAM/CPU).
4. **Verification**: Implement comprehensive Pytest unit and integration test suites for every component.

### Analytical Finding:
LLM injected additional generic statements not present in retrieved context.

---

## Case 9: What chunk size and overlap are configured in this RAG pipeline?

**Diagnostic Classification**: `[WARN] Parametric Hallucination despite Context`

- **Ground Truth**: Chunk size of 500 words with 80 words sliding overlap.
- **Retrieval Latency**: 2.95 ms | **Total Latency**: 1064.28 ms
- **Groundedness Score**: 0.714 | **Hallucination Rate**: 28.57%

### Retrieved Context Chunks:
> **Chunk 1 (Source: `common_viva_questions.md`, Similarity: 0.428)**:
> ## 1. Core Architecture & RAG Questions

### Q1: What is the core difference between fine-tuning an LLM and using RAG?
**Answer**: Fine-tuning alters the internal weights of the model with domain datasets, which is computationally expensive and suffe...

> **Chunk 2 (Source: `ai_ml_workflow_documentation.md`, Similarity: 0.333)**:
> ## 2. RAG Pipeline Stages
1. **Document Ingestion**:
   - Ingest multiple formats (PDF, Markdown, JSON, Source Code).
   - Sanitize text, strip non-printable tokens, and preserve hierarchical metadata (e.g. document title, section, page).
2. **Semant...

> **Chunk 3 (Source: `common_viva_questions.md`, Similarity: 0.301)**:
> ## 2. System Performance & Engineering Questions

### Q4: How do you measure and mitigate model hallucinations?
**Answer**: We implement a Hallucination Detector service that parses the claims in the generated response and computes semantic entailmen...

> **Chunk 4 (Source: `git_workflow_standards.md`, Similarity: 0.268)**:
> ## 1. Git Branching Strategy (GitFlow Lite)
For team collaboration in academic and production environments, use the following branching model:

```
  main (production releases, tags v1.0.0)
   ↑
  develop (integration branch)
   ↑ 
  feature/rag-retr...

### Generated RAG Answer:
### AI Project Mentor Guidance [openai/gpt-oss-20b]:

Based on the official university academic guidelines and project documentation:

1. **Q3: How do you choose the chunk size and overlap in your RAG pipeline?**: Answer**: We configured a chunk size of 500 words with an 80-word sliding window overlap. A chunk size that is too small loses sentence context and discourse cohesion, while an excessively large chunk dilutes semantic density in the embedding vector. The overlap guarantees that sentences spanning boundary transitions are not artificially clipped.
2. **Q1: What is the core difference between fine-tuning an LLM and using RAG?**: Answer**: Fine-tuning alters the internal weights of the model with domain datasets, which is computationally expensive and suffers from catastrophic forgetting. RAG decouples knowledge storage from the language model by dynamically retrieving relevant facts from a vector database at query time, ensuring up-to-date facts, zero hallucination of private guidelines, and transparent citations.
3. **Q6: What metrics did you use to evaluate your RAG pipeline?**: Answer**: We evaluated using Information Retrieval metrics (Precision@K, Recall@K, Mean Reciprocal Rank - MRR), Generation metrics (Correctness, Semantic Relevance, Hallucination Rate), and System metrics (P95 Latency in milliseconds, Token throughput, and Memory/CPU footprint).
4. **2. RAG Pipeline Stages**: Chunk size: 300 to 500 tokens (words) to maintain semantic cohesion.
5. **2. RAG Pipeline Stages**: Chunk overlap: 10% to 20% (50 to 80 words) to avoid context clipping across paragraph boundaries.
6. **2. RAG Pipeline Stages**: Sanitize text, strip non-printable tokens, and preserve hierarchical metadata (e.g. document title, section, page).
7. **2. RAG Pipeline Stages**: Semantic Chunking**:

**Actionable Next Steps**:
- Verify deliverables against the official university project rubrics.
- Ensure code test coverage meets or exceeds standard evaluation thresholds (>80%).
- Document all architectural decisions and API specifications in your project report.

### Comparison without RAG:
### AI Project Mentor Guidance [openai/gpt-oss-20b]:

For your final-year project inquiry, follow these standard steps:
1. **Requirements & Scope**: Define clear input-output specifications with strict validation schemas.
2. **Architecture**: Decouple business logic, vector storage, and API routing microservices.
3. **Quantitative Metrics**: Measure latency (P95/P99), accuracy, and resource utilization (RAM/CPU).
4. **Verification**: Implement comprehensive Pytest unit and integration test suites for every component.

### Analytical Finding:
LLM injected additional generic statements not present in retrieved context.

---

## Case 10: What are the questions external examiners ask during the project viva?

**Diagnostic Classification**: `[WARN] Parametric Hallucination despite Context`

- **Ground Truth**: Individual code contributions, algorithm complexity, justification of technology choices, and error handling.
- **Retrieval Latency**: 5.01 ms | **Total Latency**: 874.96 ms
- **Groundedness Score**: 0.714 | **Hallucination Rate**: 28.57%

### Retrieved Context Chunks:
> **Chunk 1 (Source: `project_guidelines.md`, Similarity: 0.321)**:
> ## 1. Introduction and Objectives
The Final-Year Capstone Project is the culminating academic requirement for Bachelor of Engineering (B.E./B.Tech) students. The objective is to design, develop, test, and demonstrate an innovative engineering solutio...

> **Chunk 2 (Source: `common_viva_questions.md`, Similarity: 0.293)**:
> ## 2. System Performance & Engineering Questions

### Q4: How do you measure and mitigate model hallucinations?
**Answer**: We implement a Hallucination Detector service that parses the claims in the generated response and computes semantic entailmen...

> **Chunk 3 (Source: `ai_ml_workflow_documentation.md`, Similarity: 0.287)**:
> ## 4. Evaluation Metrics for LLM Systems
- **Precision@K & Recall@K**: Measures the proportion of relevant chunks retrieved in top K results.
- **Mean Reciprocal Rank (MRR)**: Evaluates the ranking quality of the first relevant chunk.
- **Hallucinati...

> **Chunk 4 (Source: `evaluation_rubric.md`, Similarity: 0.286)**:
> ## 3. External Examiner Viva Voce Expectations
External examiners evaluate each individual team member on:
1. Identifying exactly which files and modules the student wrote personally.
2. Explaining time and space complexity of custom algorithms.
3. J...

### Generated RAG Answer:
### AI Project Mentor Guidance [openai/gpt-oss-20b]:

Based on the official university academic guidelines and project documentation:

1. **3. External Examiner Viva Voce Expectations**: External examiners evaluate each individual team member on:
2. **3. External Examiner Viva Voce Expectations**: Identifying exactly which files and modules the student wrote personally.
3. **3. External Examiner Viva Voce Expectations**: Explaining how failures, network timeouts, and model hallucinations are mitigated.
4. **1. Introduction and Objectives**: The Final-Year Capstone Project is the culminating academic requirement for Bachelor of Engineering (B.E./B.Tech) students. The objective is to design, develop, test, and demonstrate an innovative engineering solution addressing real-world problems.
5. **3. External Examiner Viva Voce Expectations**: Explaining time and space complexity of custom algorithms.
6. **3. External Examiner Viva Voce Expectations**: Justifying why a particular database (e.g. ChromaDB vs PostgreSQL) or model was selected over alternatives.
7. **Q4: How do you measure and mitigate model hallucinations?**: Answer**: We implement a Hallucination Detector service that parses the claims in the generated response and computes semantic entailment against the retrieved reference chunks. If an LLM assertion cannot be mapped to the retrieved context chunks with a minimum threshold (>0.60), it is flagged as an unsupported claim.

**Actionable Next Steps**:
- Verify deliverables against the official university project rubrics.
- Ensure code test coverage meets or exceeds standard evaluation thresholds (>80%).
- Document all architectural decisions and API specifications in your project report.

### Comparison without RAG:
### AI Project Mentor Guidance [openai/gpt-oss-20b]:

For your final-year project inquiry, follow these standard steps:
1. **Requirements & Scope**: Define clear input-output specifications with strict validation schemas.
2. **Architecture**: Decouple business logic, vector storage, and API routing microservices.
3. **Quantitative Metrics**: Measure latency (P95/P99), accuracy, and resource utilization (RAM/CPU).
4. **Verification**: Implement comprehensive Pytest unit and integration test suites for every component.

### Analytical Finding:
LLM injected additional generic statements not present in retrieved context.

---

