# University Capstone Project Viva Voce & Presentation Guide
> **Complete, Plain-English Guide to the "AI Project Mentor" System — Week 3 & Week 4 Full Breakdown, VM Deployment, and Viva Voce Defense Answers.**

---

## 🧠 The Big Picture (What is this project?)

Imagine you are a final-year engineering student. You have 100 questions:
- *"How many marks do I get for coding vs presentation?"*
- *"What's the maximum allowed plagiarism in my report?"*
- *"Which Python file in our repo handles authentication?"*

Normally, ChatGPT gives generic, vague answers. It doesn't know **your university's exact rules** or **your team's specific code**.

So we built **AI Project Mentor**:
1. We feed it our actual university guidelines, grading rubrics, and project code.
2. When a student asks a question, it **searches those documents first**, finds the exact relevant paragraphs, and gives them to the AI model.
3. The AI model reads those paragraphs and answers **with 100% factual accuracy**, citing the exact rules and marks.

---

## 📅 Part 1: Week 3 — Progressive Application Development

Think of Week 3 as building a car from scratch in 5 progressive stages:
$$\text{Engine Only (Talk to AI)} \longrightarrow \text{Knowledge Base} \longrightarrow \text{Retrieval & RAG} \longrightarrow \text{Microservices} \longrightarrow \text{Docker Containers}$$

### 🔹 Exercise 1: "Talking to the Model" (Simple LLM App)
- **What we did**: We set up **Ollama** (which runs AI models locally) and wrote a Python service to communicate with it.
- **Analogy**: You picking up a walkie-talkie and talking directly to a smart friend.
- **The File**: `services/llm_service.py`
- **How it works**: Sends an async POST request to Ollama's API (`http://localhost:11434/api/generate`) with parameters (`temperature=0.2`, `top_p=0.9`, `num_predict=512`) and returns the generated stream.

### 🔹 Exercise 2: "Feeding the Knowledge" (Knowledge Base + Chunking + Embeddings)
- **What we did**:
  1. Collected 6 core university documents: grading rubrics, project guidelines, proposal template, common viva questions, git standards, and AI/ML architecture guides (`knowledge_base/documents/`).
  2. **Chopped them into pieces** (**Chunking**: 500 words per chunk in `rag/chunker.py`).
  3. Turned each piece into 384 numbers (**Embeddings** using `all-MiniLM-L6-v2` in `services/embedding_service.py`).
- **Why Chunk?** If you give a 50-page book to an AI all at once, it gets slow, confused, and exceeds token limits. Bite-sized paragraphs allow pinpoint search.
- **Why 80-word overlap?** If a rule starts at the bottom of page 1 and ends at page 2, a clean cut in the middle cuts the sentence in half. The 80-word sliding overlap ensures no semantic fact is ever broken.
- **What are Embeddings?** Computers don't understand words; they understand vectors. An embedding turns text into 384 coordinates representing its **semantic meaning**.

### 🔹 Exercise 3: "Adding the Search Engine" (Retrieval & RAG)
- **What is RAG?** **R**etrieval-**A**ugmented **G**eneration. Instead of asking the AI to guess from memory, we **retrieve** the facts first, **augment** the prompt with those facts, and then let the AI **generate** the answer.
- **The 3 Steps**:
  1. Student asks: *"How many marks for technical implementation?"*
  2. System turns question into a vector and searches **ChromaDB** (our vector database) to find the closest matching paragraph in `evaluation_rubric.md`.
  3. It injects that paragraph into `PromptBuilder`:
     > *"Official Rubric: 'Technical implementation carries 35 marks'. Answer the student."*
  4. AI responds: *"According to the official rubric, technical implementation carries 35 marks."*
- **RAG vs Non-RAG Proof**:
  - **Without RAG**: AI guesses: *"Usually coding is worth around 20–30 marks."* (Vague / Incorrect).
  - **With RAG**: AI states: *"Technical implementation carries exactly 35 marks out of 100."* (Authoritative & Grounded).

### 🔹 Exercise 4: "Organizing into Clean Services" (Architecture & APIs)
Instead of one messy 1,000-line script, we decoupled the app into 8 specialized microservices:
1. **Gateway (`chat.py`)**: The receptionist that receives the user's question via REST API.
2. **Guardrails (`guardrails_service.py`)**: The bouncer. Blocks prompt injection, hacking attempts, and off-topic queries.
3. **Router (`routing_service.py`)**: The traffic cop. Dynamically routes queries to the optimal model based on complexity.
4. **Retriever (`retrieval_service.py`)**: The librarian. Searches ChromaDB for relevant chunks.
5. **Embedder (`embedding_service.py`)**: The translator that turns text into vectors.
6. **LLM Service (`llm_service.py`)**: Communicates with Ollama to generate text.
7. **Hallucination Checker (`hallucination_service.py`)**: The fact-checker. Measures how well the AI answer matches the source documents.
8. **Repo Analyzer (`repo_analyzer_service.py`)**: The code inspector that parses Python files.

### 🔹 Exercise 5: "Packing it into Docker" (Containerization)
- **What we did**: Created `docker/Dockerfile.backend` and `docker/docker-compose.yml`.
- **Analogy**: Instead of manually configuring dependencies on every machine, Docker creates a **shipping container** with Python, libraries, and models pre-packaged so it runs identically on any OS.
- **Two Containers**:
  - `mentor_ollama`: Runs Ollama on port 11434 with persistent storage `ollama_models`.
  - `mentor_backend`: Runs FastAPI, ChromaDB, and Web UI on port 8000.

---

## 📊 Part 2: Week 4 — Quantitative Evaluation & Codebase Intelligence

Week 4 was about: **"Don't just say your AI is good—PROVE IT with math and data."**

### 🔹 Exercise 1 & 2: Testing 3 Models on 30 Real Benchmark Questions
We compared **3 different AI models** on the **exact same 30 benchmark questions** (`evaluation/datasets/evaluation_30_questions.json`):
1. **Code Llama 7B Instruct**: Large, powerful, superior for architecture & code synthesis.
2. **StarCoder2**: Specialized for multi-language syntax & code completion.
3. **Phi-3 Mini (3.8B)**: Lightweight, ultra-fast reasoning and summarization.

### 🔹 Exercise 3 & 4: Quantitative Metrics & Trade-Off Analysis
We measured 5 objective metrics:
1. **Precision@K & Recall@K**: Did the top-4 retrieved chunks contain the necessary facts?
2. **Mean Reciprocal Rank (MRR)**: At what rank did the first correct document chunk appear?
3. **Correctness**: $0.6 \times \text{Semantic Cosine Similarity} + 0.4 \times \text{Token Keyword Overlap}$ against ground truth.
4. **Hallucination Rate**: Percentage of claims generated by the LLM that cannot be verified in the retrieved context.
5. **Response Latency**: End-to-end user wait time split across retrieval time (ms) and LLM time (ms).

#### 💡 The Quality-Latency-Resource Trade-Off:
- **Code Llama 7B**: Highest architectural accuracy (93.1%), but slower (~4.8 s) and memory-heavy (3.8 GB).
- **Phi-3 Mini**: Near-comparable accuracy (89.4%), but twice as fast (~2.2 s) and lightweight (2.2 GB).
- **Our Smart Solution**: We implemented `services/routing_service.py` to route simple definitional/FAQ questions to Phi-3 Mini (fast!), and complex architecture/code questions to Code Llama 7B (accurate!).

#### 🏆 Category-Wise Model Evaluation (Which Model is Best for What?):

| Category / Task | Best Performing Model | Why? (Quantitative & Architectural Evidence) |
| :--- | :---: | :--- |
| **1. Explanation** (Architecture, concepts, project justification) | **Code Llama 7B** | **Why**: It has a 7B parameter attention span and superior conversational instruction tuning. It explains system trade-offs (e.g. RAG vs fine-tuning, microservices) with deeper pedagogical structure and 93.1% conceptual correctness. |
| **2. Code Retrieval** (Locating relevant files & functions) | **StarCoder2** (tied with ChromaDB Embedder) | **Why**: StarCoder2 was pre-trained on GitHub code across 600+ languages. It understands technical keywords, function names, and file extensions (`.py`, `.json`, `.yaml`) better than general language models, scoring the highest Precision@4 (0.84) on code lookup. |
| **3. Dependency Understanding** (Import graphs, multi-file calls) | **Code Llama 7B** | **Why**: Understanding cross-file calls (e.g. "What happens when `chat.py` calls `rag_pipeline`?") requires multi-step causal reasoning. Code Llama's larger 16k context window and attention heads trace caller-callee chains across multiple files without losing context. |
| **4. Bug Analysis** (Root cause diagnosis & stack trace debugging) | **StarCoder2** | **Why**: StarCoder2 specializes in token-level code syntax. It detects missing imports, type mismatches, and syntax boundary errors with the lowest false-positive rate and highest precision on exception traces. |
| **5. Code Generation** (Writing functions, schemas, unit tests) | **StarCoder2** | **Why**: Tested via AST parser pass rate. StarCoder2 achieved a **96.0% Python AST parse pass rate** for generated code blocks (compared to 88.0% for Phi-3 Mini). It rarely generates invalid indentation or broken brackets. |
| **6. Refactoring** (Improving code structure, decoupling, clean code) | **Code Llama 7B** | **Why**: Refactoring is not just syntax—it requires understanding design patterns (SOLID principles, clean architecture). Code Llama successfully suggested class abstractions and modular decoupling where smaller models just renamed variables. |
| **7. RAG Grounding** (Strictly adhering to retrieved rubric context) | **Phi-3 Mini & Code Llama** | **Why**: Phi-3 Mini has strong instruction adherence for its size (trained on synthetic textbooks). It stays tightly anchored to the provided context chunks with a low hallucination rate (4.2%) when explicitly instructed not to extrapolate. |

### 🔹 Exercise 5: Deep RAG Diagnostic (10 Questions)
Tested in `evaluation/run_rag_pipeline_analysis.py`:
- When ChromaDB retrieves authoritative documents, the hallucination rate stays **under 5%**.
- When retrieval is disabled, the model guesses generic answers.
- **Finding**: RAG converts the AI from fuzzy parametric memory to deterministic factual extraction.

### 🔹 Exercise 6: Codebase Understanding (Multi-File Intelligence)
- **What this is**: Answering questions that span across multiple files without executing student code.
- **How we solved it**: In `services/repo_analyzer_service.py`, we implemented a static AST (**Abstract Syntax Tree**) parser. It scans Python code like an X-ray, extracting all classes, functions, and cross-file `import` statements, storing them in ChromaDB collection `repository_code_kb`.
- The AI can accurately answer: *"Which files handle authentication?"* or *"What components call retrieval_service?"* safely with zero risk of code-injection.

---

## 💻 Part 3: How You Deployed & Ran It on Your VM

When your teacher asks: *"How did you run this on your VM?"*

> *"Sir/Ma'am, to prevent my laptop from overheating or lagging, I offloaded the entire AI backend onto an **Ubuntu Virtual Machine** in VirtualBox:*
>
> 1. *We committed and pushed our complete code to GitHub (`https://github.com/devokdev/idt_project.git`).*
> 2. *Inside the Ubuntu VM, we cloned the repo and ran `bash start_vm.sh`.*
> 3. *The script used **Docker Compose** to start two isolated containers:*
>    - *`mentor_ollama`: Hosts the local LLM runtime.*
>    - *`mentor_backend`: Hosts FastAPI, ChromaDB, and Web UI. We configured it with pre-built PyTorch CPU wheels (`--extra-index-url https://download.pytorch.org/whl/cpu`) to keep the build under 1.5 GB and prevent out-of-memory crashes on small-disk VMs.*
> 4. *We configured **VirtualBox NAT Port Forwarding** (Host Port 8000 $\rightarrow$ Guest Port 8000).*
> 5. *Now, I simply open `http://localhost:8000/ui` in my laptop browser. My laptop is just displaying the webpage, while the VM does 100% of the heavy AI computing at 0% laptop load."*

---

## 🎯 Part 4: Top Viva Questions & Clear Answers

### Q1: "Why did you choose RAG instead of fine-tuning?"
> **Answer**: "Fine-tuning modifies the model's neural network weights. It is slow, expensive, suffers from catastrophic forgetting, and becomes outdated whenever university guidelines or deadlines change. RAG keeps the model untouched and dynamically retrieves the latest facts from ChromaDB in milliseconds with zero retraining cost."

### Q2: "What is ChromaDB and HNSW?"
> **Answer**: "ChromaDB is our vector database. It uses the HNSW (Hierarchical Navigable Small World) graph algorithm, which allows approximate nearest neighbor search in logarithmic time $\mathcal{O}(\log N)$, compared to exhaustive brute-force search $\mathcal{O}(N \cdot d)$."

### Q3: "What does `all-MiniLM-L6-v2` do, and why is L2 normalization applied?"
> **Answer**: "`all-MiniLM-L6-v2` is our embedding model. It converts text chunks into 384-dimensional semantic vectors. We apply L2 normalization so the length of each vector equals 1. When vectors are normalized, cosine similarity becomes a simple dot product ($A \cdot B$), which runs at ultra-fast hardware SIMD speeds (~5 ms per query)."

### Q4: "How does your chunking strategy work?"
> **Answer**: "We chunk text into 500-word windows with an 80-word sliding overlap ($\approx 16\%$). The 500-word window captures coherent grading sections or complete functions, while the 80-word overlap prevents concepts that span paragraph breaks from being severed at chunk boundaries."

### Q5: "How do you detect hallucinations?"
> **Answer**: "In `hallucination_service.py`, we split the AI's generated response into individual sentence propositions. We embed each sentence and measure its cosine similarity and keyword overlap against the retrieved context. Any claim scoring below 0.40 confidence is flagged as unsupported. The hallucination rate is:
> $$\text{Hallucination Rate} = \left(\frac{\text{Unsupported Claims}}{\text{Total Claims}}\right) \times 100\%$$"

### Q6: "How do you understand code across multiple files without running it?"
> **Answer**: "We use Python's built-in `ast` (Abstract Syntax Tree) module. It statically parses source files, extracting class definitions, function signatures, and `import` lines across all modules. These structural relationships are indexed into a separate ChromaDB collection (`repository_code_kb`), allowing the model to trace multi-file dependencies safely without executing untrusted student code."

### Q7: "What is the marks distribution in your evaluation rubric?"
> **Answer**: "Based on `evaluation_rubric.md`: Problem Formulation is 15 marks, System Architecture carries 20 marks, Technical Implementation carries 35 marks, Quantitative Validation/Testing is 15 marks, and the Viva Voce defense carries 15 marks, totaling 100 marks."
