# Final-Year Project Evaluation Rubric and Grading Criteria

## 1. Overall Grade Distribution (Total: 100 Marks)

| Evaluation Component | Weightage | Description |
| :--- | :--- | :--- |
| **1. Problem Formulation & Literature Survey** | **15 Marks** | Clear problem statement, novelty, review of 10+ recent IEEE/ACM publications (last 3-5 years), benchmark comparisons. |
| **2. Architectural Design & Methodology** | **20 Marks** | Robust system architecture, C4 architectural models, modularity, database normalization, API contract definitions. |
| **3. Technical Implementation & Quality** | **35 Marks** | Quality of code, error handling, design patterns, separation of concerns, concurrency, automated test coverage (>80%). |
| **4. Validation, Metrics & Experimentation** | **15 Marks** | Quantitative evaluation: precision/recall, latency, throughput, confusion matrix, ablation studies, baseline comparisons. |
| **5. Defense, Presentation & Viva Voce** | **15 Marks** | Individual student technical competence, ability to explain architectural decisions, live system demo, QA handling. |

---

## 2. Detailed Performance Level Rubric

### Component 1: Technical Implementation (35 Marks)
- **Exemplary (30 - 35 Marks)**: Production-grade code, end-to-end working system, zero critical bugs during demo, clean Docker Compose setup, comprehensive unit and API integration tests passing in CI.
- **Proficient (22 - 29 Marks)**: Functional prototype with minor edge-case glitches, adequate code structure, basic unit tests, dockerized backend.
- **Developing (15 - 21 Marks)**: Incomplete modules, UI/backend desynchronization, no automated tests, hardcoded credentials.
- **Unacceptable (0 - 14 Marks)**: Non-functional system, plagiarized codebase, failure to demonstrate working API.

### Component 2: Quantitative Validation (15 Marks)
- **Exemplary (13 - 15 Marks)**: Rigorous metrics computed on verified datasets (F1-score, MRR, latency distributions P95/P99, memory/CPU profiling) with clear comparative charts.
- **Proficient (10 - 12 Marks)**: Standard metrics computed, simple accuracy plots, basic comparison with single baseline.
- **Developing (6 - 9 Marks)**: Superficial metrics without benchmark datasets or statistical significance.
- **Unacceptable (0 - 5 Marks)**: No quantitative evaluation; qualitative subjective claims only.

---

## 3. External Examiner Viva Voce Expectations
External examiners evaluate each individual team member on:
1. Identifying exactly which files and modules the student wrote personally.
2. Explaining time and space complexity of custom algorithms.
3. Justifying why a particular database (e.g. ChromaDB vs PostgreSQL) or model was selected over alternatives.
4. Explaining how failures, network timeouts, and model hallucinations are mitigated.
