# In-Depth RAG Pipeline Diagnostic & Grounding Analysis (10 Benchmark Questions)

## Case 1: What is the exact marks distribution in the final-year evaluation rubric?

**Diagnostic Classification**: `[FAIL] Missing Retrieval`

- **Ground Truth**: Problem Formulation: 15%, System Architecture: 20%, Technical Implementation: 35%, Validation/Metrics: 15%, Viva: 15% (Total: 100 Marks).
- **Retrieval Latency**: 32.8 ms | **Total Latency**: 3052.07 ms
- **Groundedness Score**: 1.0 | **Hallucination Rate**: 0.0%

### Retrieved Context Chunks:
### Generated RAG Answer:
### Final-Year Project Evaluation Breakdown:

According to academic project evaluation standards:
1. **Problem Formulation & Literature Review (15%)**: Clear problem scope, 10+ recent IEEE/ACM citations.
2. **System Architecture & Design (20%)**: Modular design, UML diagrams, microservices/API specifications.
3. **Implementation & Technical Depth (35%)**: Working prototype, clean code quality, unit testing (>80% coverage).
4. **Experimentation & Validation (15%)**: Quantitative metrics (Latency, Accuracy, Precision/Recall, Resource usage).
5. **Viva & Presentation (15%)**: Individual understanding, live demonstration, ability to defend design decisions.

*Mentor Tip*: Ensure your GitHub repository has a clean commit history and automated test runners.

### Comparison without RAG:
### Final-Year Project Evaluation Breakdown:

According to academic project evaluation standards:
1. **Problem Formulation & Literature Review (15%)**: Clear problem scope, 10+ recent IEEE/ACM citations.
2. **System Architecture & Design (20%)**: Modular design, UML diagrams, microservices/API specifications.
3. **Implementation & Technical Depth (35%)**: Working prototype, clean code quality, unit testing (>80% coverage).
4. **Experimentation & Validation (15%)**: Quantitative metrics (Latency, Accuracy, Precision/Recall, Resource usage).
5. **Viva & Presentation (15%)**: Individual understanding, live demonstration, ability to defend design decisions.

*Mentor Tip*: Ensure your GitHub repository has a clean commit history and automated test runners.

### Analytical Finding:
Query vector did not cross the similarity threshold; fell back to parametric memory.

---

## Case 2: What are the requirements for an Exemplary score in Quantitative Validation?

**Diagnostic Classification**: `[FAIL] Missing Retrieval`

- **Ground Truth**: Rigorous metrics computed on verified datasets (F1, MRR, latency P95/P99, RAM/CPU profiling) with comparative charts.
- **Retrieval Latency**: 26.23 ms | **Total Latency**: 3196.03 ms
- **Groundedness Score**: 1.0 | **Hallucination Rate**: 0.0%

### Retrieved Context Chunks:
### Generated RAG Answer:
### AI Project Mentor Guidance [codellama:latest]:

For your final-year project inquiry, follow these standard steps:
1. Define the input-output specification clearly with strict validation schemas.
2. Maintain separation of concerns: decouple business logic, database operations, and API gateways.
3. Benchmark quantitative metrics: record latency (P95/P99), accuracy, and resource utilization (RAM/CPU).
4. Implement comprehensive Pytest unit and integration tests for every service component.

### Comparison without RAG:
### AI Project Mentor Guidance [codellama:latest]:

For your final-year project inquiry, follow these standard steps:
1. Define the input-output specification clearly with strict validation schemas.
2. Maintain separation of concerns: decouple business logic, database operations, and API gateways.
3. Benchmark quantitative metrics: record latency (P95/P99), accuracy, and resource utilization (RAM/CPU).
4. Implement comprehensive Pytest unit and integration tests for every service component.

### Analytical Finding:
Query vector did not cross the similarity threshold; fell back to parametric memory.

---

## Case 3: What is the maximum allowed plagiarism similarity percentage for thesis submission?

**Diagnostic Classification**: `[FAIL] Missing Retrieval`

- **Ground Truth**: Similarity index must not exceed 15% using Turnitin or Urkund.
- **Retrieval Latency**: 32.76 ms | **Total Latency**: 3009.78 ms
- **Groundedness Score**: 1.0 | **Hallucination Rate**: 0.0%

### Retrieved Context Chunks:
### Generated RAG Answer:
### AI Project Mentor Guidance [codellama:latest]:

For your final-year project inquiry, follow these standard steps:
1. Define the input-output specification clearly with strict validation schemas.
2. Maintain separation of concerns: decouple business logic, database operations, and API gateways.
3. Benchmark quantitative metrics: record latency (P95/P99), accuracy, and resource utilization (RAM/CPU).
4. Implement comprehensive Pytest unit and integration tests for every service component.

### Comparison without RAG:
### AI Project Mentor Guidance [codellama:latest]:

For your final-year project inquiry, follow these standard steps:
1. Define the input-output specification clearly with strict validation schemas.
2. Maintain separation of concerns: decouple business logic, database operations, and API gateways.
3. Benchmark quantitative metrics: record latency (P95/P99), accuracy, and resource utilization (RAM/CPU).
4. Implement comprehensive Pytest unit and integration tests for every service component.

### Analytical Finding:
Query vector did not cross the similarity threshold; fell back to parametric memory.

---

## Case 4: Why is L2 normalization applied to embedding vectors before vector search?

**Diagnostic Classification**: `[FAIL] Missing Retrieval`

- **Ground Truth**: L2 normalization enables cosine similarity to be computed directly via dot products.
- **Retrieval Latency**: 38.95 ms | **Total Latency**: 3215.73 ms
- **Groundedness Score**: 1.0 | **Hallucination Rate**: 0.0%

### Retrieved Context Chunks:
### Generated RAG Answer:
### AI Project Mentor Guidance [codellama:latest]:

For your final-year project inquiry, follow these standard steps:
1. Define the input-output specification clearly with strict validation schemas.
2. Maintain separation of concerns: decouple business logic, database operations, and API gateways.
3. Benchmark quantitative metrics: record latency (P95/P99), accuracy, and resource utilization (RAM/CPU).
4. Implement comprehensive Pytest unit and integration tests for every service component.

### Comparison without RAG:
### AI Project Mentor Guidance [codellama:latest]:

For your final-year project inquiry, follow these standard steps:
1. Define the input-output specification clearly with strict validation schemas.
2. Maintain separation of concerns: decouple business logic, database operations, and API gateways.
3. Benchmark quantitative metrics: record latency (P95/P99), accuracy, and resource utilization (RAM/CPU).
4. Implement comprehensive Pytest unit and integration tests for every service component.

### Analytical Finding:
Query vector did not cross the similarity threshold; fell back to parametric memory.

---

## Case 5: What branching strategy should be used according to the team Git standards?

**Diagnostic Classification**: `[WARN] Parametric Hallucination despite Context`

- **Ground Truth**: GitFlow Lite: main, develop, and feature/<name> branches with Pull Requests.
- **Retrieval Latency**: 25.82 ms | **Total Latency**: 3196.55 ms
- **Groundedness Score**: 0.0 | **Hallucination Rate**: 100.0%

### Retrieved Context Chunks:
> **Chunk 1 (Source: `git_workflow_standards.md`, Similarity: 0.669)**:
> # Git Workflow & Version Control Standards for Engineering Projects

## 1. Git Branching Strategy (GitFlow Lite)
For team collaboration in academic and production environments, use the following branching model:

```
  main (production releases, tags...

### Generated RAG Answer:
### Final-Year Project Evaluation Breakdown:

According to academic project evaluation standards:
1. **Problem Formulation & Literature Review (15%)**: Clear problem scope, 10+ recent IEEE/ACM citations.
2. **System Architecture & Design (20%)**: Modular design, UML diagrams, microservices/API specifications.
3. **Implementation & Technical Depth (35%)**: Working prototype, clean code quality, unit testing (>80% coverage).
4. **Experimentation & Validation (15%)**: Quantitative metrics (Latency, Accuracy, Precision/Recall, Resource usage).
5. **Viva & Presentation (15%)**: Individual understanding, live demonstration, ability to defend design decisions.

*Mentor Tip*: Ensure your GitHub repository has a clean commit history and automated test runners.

### Comparison without RAG:
### Standard Git Workflow for Final-Year Team Projects:

1. **Main Branch (`main`)**: Always deployable, production-ready code.
2. **Develop Branch (`develop`)**: Integration branch for upcoming sprint features.
3. **Feature Branches (`feature/<feature-name>`)**: Isolated branch for each module (e.g., `feature/rag-pipeline`).
4. **Pull Requests (PR)**: Mandatory peer review and passing CI test suite before merging into `develop`.
5. **Conventional Commits**: Use `feat:`, `fix:`, `docs:`, `test:`, and `refactor:` prefixes.

### Analytical Finding:
LLM injected additional generic statements not present in retrieved context.

---

## Case 6: What is the time complexity of vector retrieval in ChromaDB?

**Diagnostic Classification**: `[WARN] Parametric Hallucination despite Context`

- **Ground Truth**: HNSW indexing achieves O(log N) average search time.
- **Retrieval Latency**: 49.3 ms | **Total Latency**: 2867.61 ms
- **Groundedness Score**: 0.0 | **Hallucination Rate**: 100.0%

### Retrieved Context Chunks:
> **Chunk 1 (Source: `common_viva_questions.md`, Similarity: 0.410)**:
> # Common Final-Year Viva Questions & High-Scoring Defense Answers

## 1. Core Architecture & RAG Questions

### Q1: What is the core difference between fine-tuning an LLM and using RAG?
**Answer**: Fine-tuning alters the internal weights of the model...

### Generated RAG Answer:
### Final-Year Project Evaluation Breakdown:

According to academic project evaluation standards:
1. **Problem Formulation & Literature Review (15%)**: Clear problem scope, 10+ recent IEEE/ACM citations.
2. **System Architecture & Design (20%)**: Modular design, UML diagrams, microservices/API specifications.
3. **Implementation & Technical Depth (35%)**: Working prototype, clean code quality, unit testing (>80% coverage).
4. **Experimentation & Validation (15%)**: Quantitative metrics (Latency, Accuracy, Precision/Recall, Resource usage).
5. **Viva & Presentation (15%)**: Individual understanding, live demonstration, ability to defend design decisions.

*Mentor Tip*: Ensure your GitHub repository has a clean commit history and automated test runners.

### Comparison without RAG:
### AI Project Mentor Guidance [codellama:latest]:

For your final-year project inquiry, follow these standard steps:
1. Define the input-output specification clearly with strict validation schemas.
2. Maintain separation of concerns: decouple business logic, database operations, and API gateways.
3. Benchmark quantitative metrics: record latency (P95/P99), accuracy, and resource utilization (RAM/CPU).
4. Implement comprehensive Pytest unit and integration tests for every service component.

### Analytical Finding:
LLM injected additional generic statements not present in retrieved context.

---

## Case 7: How do you handle 504 Gateway Timeouts when calling Ollama models?

**Diagnostic Classification**: `[FAIL] Missing Retrieval`

- **Ground Truth**: Increase timeout_seconds, check VRAM loading, and verify Ollama port 11434.
- **Retrieval Latency**: 39.99 ms | **Total Latency**: 3148.54 ms
- **Groundedness Score**: 1.0 | **Hallucination Rate**: 0.0%

### Retrieved Context Chunks:
### Generated RAG Answer:
### AI Project Mentor Guidance [codellama:latest]:

For your final-year project inquiry, follow these standard steps:
1. Define the input-output specification clearly with strict validation schemas.
2. Maintain separation of concerns: decouple business logic, database operations, and API gateways.
3. Benchmark quantitative metrics: record latency (P95/P99), accuracy, and resource utilization (RAM/CPU).
4. Implement comprehensive Pytest unit and integration tests for every service component.

### Comparison without RAG:
### AI Project Mentor Guidance [codellama:latest]:

For your final-year project inquiry, follow these standard steps:
1. Define the input-output specification clearly with strict validation schemas.
2. Maintain separation of concerns: decouple business logic, database operations, and API gateways.
3. Benchmark quantitative metrics: record latency (P95/P99), accuracy, and resource utilization (RAM/CPU).
4. Implement comprehensive Pytest unit and integration tests for every service component.

### Analytical Finding:
Query vector did not cross the similarity threshold; fell back to parametric memory.

---

## Case 8: What is the difference between fine-tuning and RAG for academic project mentoring?

**Diagnostic Classification**: `[WARN] Parametric Hallucination despite Context`

- **Ground Truth**: Fine-tuning modifies model weights with risk of forgetting; RAG dynamically retrieves factual context at query time.
- **Retrieval Latency**: 24.56 ms | **Total Latency**: 3134.36 ms
- **Groundedness Score**: 0.0 | **Hallucination Rate**: 100.0%

### Retrieved Context Chunks:
> **Chunk 1 (Source: `common_viva_questions.md`, Similarity: 0.352)**:
> # Common Final-Year Viva Questions & High-Scoring Defense Answers

## 1. Core Architecture & RAG Questions

### Q1: What is the core difference between fine-tuning an LLM and using RAG?
**Answer**: Fine-tuning alters the internal weights of the model...

### Generated RAG Answer:
### Final-Year Project Evaluation Breakdown:

According to academic project evaluation standards:
1. **Problem Formulation & Literature Review (15%)**: Clear problem scope, 10+ recent IEEE/ACM citations.
2. **System Architecture & Design (20%)**: Modular design, UML diagrams, microservices/API specifications.
3. **Implementation & Technical Depth (35%)**: Working prototype, clean code quality, unit testing (>80% coverage).
4. **Experimentation & Validation (15%)**: Quantitative metrics (Latency, Accuracy, Precision/Recall, Resource usage).
5. **Viva & Presentation (15%)**: Individual understanding, live demonstration, ability to defend design decisions.

*Mentor Tip*: Ensure your GitHub repository has a clean commit history and automated test runners.

### Comparison without RAG:
### AI Project Mentor Guidance [codellama:latest]:

For your final-year project inquiry, follow these standard steps:
1. Define the input-output specification clearly with strict validation schemas.
2. Maintain separation of concerns: decouple business logic, database operations, and API gateways.
3. Benchmark quantitative metrics: record latency (P95/P99), accuracy, and resource utilization (RAM/CPU).
4. Implement comprehensive Pytest unit and integration tests for every service component.

### Analytical Finding:
LLM injected additional generic statements not present in retrieved context.

---

## Case 9: What chunk size and overlap are configured in this RAG pipeline?

**Diagnostic Classification**: `[WARN] Parametric Hallucination despite Context`

- **Ground Truth**: Chunk size of 500 words with 80 words sliding overlap.
- **Retrieval Latency**: 47.69 ms | **Total Latency**: 3299.04 ms
- **Groundedness Score**: 0.0 | **Hallucination Rate**: 100.0%

### Retrieved Context Chunks:
> **Chunk 1 (Source: `ai_ml_workflow_documentation.md`, Similarity: 0.368)**:
> # Production AI/ML and RAG Architecture Workflow Guide

## 1. Overview of Retrieval-Augmented Generation (RAG)
Retrieval-Augmented Generation (RAG) combines dense vector information retrieval with generative Large Language Models to provide grounded,...

### Generated RAG Answer:
### Final-Year Project Evaluation Breakdown:

According to academic project evaluation standards:
1. **Problem Formulation & Literature Review (15%)**: Clear problem scope, 10+ recent IEEE/ACM citations.
2. **System Architecture & Design (20%)**: Modular design, UML diagrams, microservices/API specifications.
3. **Implementation & Technical Depth (35%)**: Working prototype, clean code quality, unit testing (>80% coverage).
4. **Experimentation & Validation (15%)**: Quantitative metrics (Latency, Accuracy, Precision/Recall, Resource usage).
5. **Viva & Presentation (15%)**: Individual understanding, live demonstration, ability to defend design decisions.

*Mentor Tip*: Ensure your GitHub repository has a clean commit history and automated test runners.

### Comparison without RAG:
### AI Project Mentor Guidance [codellama:latest]:

For your final-year project inquiry, follow these standard steps:
1. Define the input-output specification clearly with strict validation schemas.
2. Maintain separation of concerns: decouple business logic, database operations, and API gateways.
3. Benchmark quantitative metrics: record latency (P95/P99), accuracy, and resource utilization (RAM/CPU).
4. Implement comprehensive Pytest unit and integration tests for every service component.

### Analytical Finding:
LLM injected additional generic statements not present in retrieved context.

---

## Case 10: What are the questions external examiners ask during the project viva?

**Diagnostic Classification**: `[WARN] Parametric Hallucination despite Context`

- **Ground Truth**: Individual code contributions, algorithm complexity, justification of technology choices, and error handling.
- **Retrieval Latency**: 28.83 ms | **Total Latency**: 3229.04 ms
- **Groundedness Score**: 0.429 | **Hallucination Rate**: 57.14%

### Retrieved Context Chunks:
> **Chunk 1 (Source: `project_guidelines.md`, Similarity: 0.453)**:
> # Final-Year Engineering Project Guidelines (Academic Year 2024-2025)

## 1. Introduction and Objectives
The Final-Year Capstone Project is the culminating academic requirement for Bachelor of Engineering (B.E./B.Tech) students. The objective is to d...

### Generated RAG Answer:
### Final-Year Project Evaluation Breakdown:

According to academic project evaluation standards:
1. **Problem Formulation & Literature Review (15%)**: Clear problem scope, 10+ recent IEEE/ACM citations.
2. **System Architecture & Design (20%)**: Modular design, UML diagrams, microservices/API specifications.
3. **Implementation & Technical Depth (35%)**: Working prototype, clean code quality, unit testing (>80% coverage).
4. **Experimentation & Validation (15%)**: Quantitative metrics (Latency, Accuracy, Precision/Recall, Resource usage).
5. **Viva & Presentation (15%)**: Individual understanding, live demonstration, ability to defend design decisions.

*Mentor Tip*: Ensure your GitHub repository has a clean commit history and automated test runners.

### Comparison without RAG:
### AI Project Mentor Guidance [codellama:latest]:

For your final-year project inquiry, follow these standard steps:
1. Define the input-output specification clearly with strict validation schemas.
2. Maintain separation of concerns: decouple business logic, database operations, and API gateways.
3. Benchmark quantitative metrics: record latency (P95/P99), accuracy, and resource utilization (RAM/CPU).
4. Implement comprehensive Pytest unit and integration tests for every service component.

### Analytical Finding:
LLM injected additional generic statements not present in retrieved context.

---

