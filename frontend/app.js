const API_BASE = window.location.origin;

// -------------------------------------------------------------
// EXERCISES CATALOG (Week 3 & Week 4)
// Clean, purpose-built, and connected to real backend APIs
// -------------------------------------------------------------
const EXERCISE_CATALOG = {
    w3: [
        {
            id: "ex1",
            tabNum: "01",
            tabLabel: "Direct LLM",
            badge: "WEEK 3 • EX 1",
            title: "Direct LLM Engine",
            desc: "Test direct neural inference without external retrieval or document augmentation.",
            type: "direct_chat",
            defaultPrompt: "Explain why decoupled microservices are preferred in cloud architectures.",
            info: "Sends prompt directly to Groq Cloud LPU with use_rag=false. Demonstrates model's pre-trained parametric knowledge."
        },
        {
            id: "ex2",
            tabNum: "02",
            tabLabel: "Chunking & Vectors",
            badge: "WEEK 3 • EX 2",
            title: "Document Chunking & Embeddings",
            desc: "Inspect sliding-window segmentation and 384-dimensional vector embeddings.",
            type: "chunker_tool",
            defaultText: "Problem Formulation carries 15 marks. System Architecture carries 20 marks. Technical Implementation carries 35 marks with high automated test coverage (>80%). Validation & Experimentation carries 15 marks. Viva Voce carries 15 marks, totaling 100 marks.",
            info: "Splits raw text into 16-word windows with 5-word overlap to ensure boundaries retain context before vector indexing."
        },
        {
            id: "ex3",
            tabNum: "03",
            tabLabel: "RAG vs No-RAG",
            badge: "WEEK 3 • EX 3",
            title: "RAG vs No-RAG Arena",
            desc: "Side-by-side comparison: see raw parametric guessing vs verified ChromaDB grounding.",
            type: "rag_vs_arena",
            defaultPrompt: "What is the exact marks distribution for technical implementation vs viva voce in the rubric?",
            info: "Runs two parallel queries with identical prompts: one without retrieval, one grounded in ChromaDB vector embeddings."
        },
        {
            id: "ex4",
            tabNum: "04",
            tabLabel: "Microservices",
            badge: "WEEK 3 • EX 4",
            title: "8-Tier Microservices Architecture",
            desc: "Decoupled services topology and live gateway health inspection.",
            type: "microservices_view",
            info: "FastAPI Gateway coordinates Guardrails, Router, Retriever, Embedder, LLM, Hallucination Scorer, and AST Analyzer."
        },
        {
            id: "ex5",
            tabNum: "05",
            tabLabel: "Docker Deployment",
            badge: "WEEK 3 • EX 5",
            title: "Docker Compose & Deployment",
            desc: "Container status, volume mounts, and host system telemetry.",
            type: "docker_terminal",
            info: "Multi-container setup running backend and vector store with persistent volume mounts and bridge networking."
        }
    ],
    w4: [
        {
            id: "w4ex1",
            tabNum: "01",
            tabLabel: "Compare Models",
            badge: "WEEK 4 • EX 1",
            title: "Evaluate Multiple LLMs",
            desc: "Run identical queries simultaneously across all 3 Groq models to evaluate latency and response quality.",
            type: "model_compare_arena",
            defaultPrompt: "What is the marks weightage for technical implementation versus viva voce?",
            info: "Runs parallel inference across GPT-OSS 20B, GPT-OSS 120B, and Qwen 27B on Groq LPUs."
        },
        {
            id: "w4ex2",
            tabNum: "02",
            tabLabel: "Evaluation Dataset",
            badge: "WEEK 4 • EX 2",
            title: "Curated 30-Question Benchmark",
            desc: "Browse and inspect the 30 curated test questions across 6 engineering categories with ground-truth answers.",
            type: "dataset_inspector",
            info: "Standardized benchmark questions across Project Formulation, Architecture, AI/RAG, and Evaluation Rubrics."
        },
        {
            id: "w4ex3",
            tabNum: "03",
            tabLabel: "Quantitative Metrics",
            badge: "WEEK 4 • EX 3",
            title: "Quantitative IR & Correctness Metrics",
            desc: "View precomputed Information Retrieval metrics (Precision@4, Recall@4, MRR), correctness, and code pass rates.",
            type: "metrics_dashboard",
            info: "Mathematical evaluation comparing model responses against verified academic ground-truth paragraphs."
        },
        {
            id: "w4ex4",
            tabNum: "04",
            tabLabel: "Trade-Offs",
            badge: "WEEK 4 • EX 4",
            title: "Analyse Results & Model Trade-Offs",
            desc: "Synthesize empirical results across Quality, Latency, and Cost to establish dynamic routing rules.",
            type: "tradeoff_matrix",
            info: "Analyzes when to use fast models (GPT-OSS 20B) vs high-capacity reasoning models (GPT-OSS 120B)."
        },
        {
            id: "w4ex5",
            tabNum: "05",
            tabLabel: "RAG Diagnostic Audit",
            badge: "WEEK 4 • EX 5",
            title: "RAG Diagnostic Ablation Audit",
            desc: "Inspect the 10-case diagnostic ablation audit isolating hallucination reduction on university rules.",
            type: "rag_audit_view",
            info: "Case-by-case audit evaluating retrieved context chunks, grounded answers, and ungrounded guesses."
        },
        {
            id: "w4ex6",
            tabNum: "06",
            tabLabel: "Codebase AST",
            badge: "WEEK 4 • EX 6",
            title: "Codebase Intelligence (AST Analyzer)",
            desc: "Query repository structure, classes, functions, and cross-file dependencies safely using static AST parsing.",
            type: "repo_ast_explorer",
            defaultPrompt: "Which classes and microservices implement guardrails and hallucination checks?",
            info: "Parses Python syntax trees without executing student code, eliminating remote code execution vulnerabilities."
        }
    ]
};

// -------------------------------------------------------------
// STATE MANAGEMENT
// -------------------------------------------------------------
let currentWeek = "w3";
let currentExIndex = 0;
let activeSidebarNav = "exercises";
let cachedDataset = null;

// -------------------------------------------------------------
// TAB NAVIGATION
// -------------------------------------------------------------
function renderSubTabNav() {
    const navEl = document.getElementById("exercise-tab-nav");
    if (!navEl) return;

    const exercises = EXERCISE_CATALOG[currentWeek];
    if (!exercises) return;

    navEl.innerHTML = exercises.map((ex, idx) => `
        <button class="ex-tab-btn ${idx === currentExIndex ? 'active' : ''}" onclick="selectExercise(${idx})">
            <span class="num">${ex.tabNum}</span>
            <span>${ex.tabLabel}</span>
        </button>
    `).join("");

    renderExerciseContent();
}

function selectExercise(index) {
    currentExIndex = index;
    renderSubTabNav();
}

function switchWeek(weekKey) {
    currentWeek = weekKey;
    currentExIndex = 0;
    const dropdown = document.getElementById("week-dropdown");
    if (dropdown) dropdown.value = weekKey;
    renderSubTabNav();
}

// -------------------------------------------------------------
// EXERCISE CONTENT RENDERER
// -------------------------------------------------------------
function renderExerciseContent() {
    const container = document.getElementById("view-container");
    if (!container) return;

    const exercises = EXERCISE_CATALOG[currentWeek];
    const ex = exercises[currentExIndex];
    if (!ex) return;

    let html = `
        <div class="card-header-banner">
            <div class="header-title-row">
                <span class="header-badge">${ex.badge}</span>
                <h1>${ex.title}</h1>
                <div class="info-hover-btn" title="Details">
                    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>
                    <div class="info-hover-box">${ex.info}</div>
                </div>
            </div>
            <p class="banner-desc">${ex.desc}</p>
        </div>
    `;

    // ---------------------------------------------------------
    // WEEK 3 TAB RENDERERS
    // ---------------------------------------------------------
    if (ex.type === "direct_chat") {
        html += `
            <div class="main-workspace-card">
                <div class="workspace-toolbar">
                    <span class="workspace-label">Direct Parametric Inference</span>
                    <span class="workspace-status">Unaugmented • Groq Cloud LPU</span>
                </div>
                <div class="prompt-input-row">
                    <input type="text" id="demo-input-field" class="prompt-field" value="${ex.defaultPrompt || ''}" placeholder="Ask the neural model directly...">
                    <button class="btn-send" id="demo-submit-btn" onclick="runDirectLLMDemo()">
                        <span>Send</span>
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>
                    </button>
                </div>
                <div class="result-box-fill" id="demo-result-surface">Type a prompt and press Send or Enter to generate directly from the model weights...</div>
            </div>
        `;
    } else if (ex.type === "chunker_tool") {
        html += `
            <div class="main-workspace-card">
                <div class="workspace-toolbar">
                    <span class="workspace-label">Sliding-Window Document Chunker</span>
                    <span class="workspace-status" id="chunk-stat-pill">Window: 16 words | Overlap: 5 words</span>
                </div>
                <textarea id="chunker-input-text" class="chunk-textarea-clean" placeholder="Paste document text here...">${ex.defaultText}</textarea>
                <div style="display: flex; gap: 10px;">
                    <button class="btn-clean-action" onclick="runChunkerInspection()">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><line x1="3" y1="9" x2="21" y2="9"></line><line x1="9" y1="21" x2="9" y2="9"></line></svg>
                        <span>Inspect Chunks & Overlap</span>
                    </button>
                </div>
                <div id="chunk-output-container" class="chunk-results-grid"></div>
            </div>
        `;
    } else if (ex.type === "rag_vs_arena") {
        html += `
            <div class="main-workspace-card">
                <div class="workspace-toolbar">
                    <span class="workspace-label">A/B Grounding Arena</span>
                    <span class="workspace-status">Side-by-side verification</span>
                </div>
                <div class="prompt-input-row">
                    <input type="text" id="demo-input-field" class="prompt-field" value="${ex.defaultPrompt || ''}" placeholder="Ask an academic question...">
                    <button class="btn-send" id="demo-submit-btn" onclick="runRagComparisonArena()">
                        <span>Compare</span>
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>
                    </button>
                </div>
                <div class="arena-split-container">
                    <div class="arena-column">
                        <div class="arena-column-header">
                            <span>WITHOUT RAG (Parametric Guess)</span>
                        </div>
                        <div class="arena-output" id="content-non-rag">Click Compare to run query without document retrieval...</div>
                    </div>
                    <div class="arena-column">
                        <div class="arena-column-header rag">
                            <span>WITH RAG (ChromaDB Grounded)</span>
                        </div>
                        <div class="arena-output" id="content-rag">Retrieves verified knowledge base documents first...</div>
                    </div>
                </div>
            </div>
        `;
    } else if (ex.type === "microservices_view") {
        html += `
            <div class="main-workspace-card">
                <div class="workspace-toolbar">
                    <span class="workspace-label">System Architecture</span>
                    <button class="btn-clean-action" onclick="testLiveServiceHealth()">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 12h-4l-3 9L9 3l-3 9H2"></path></svg>
                        <span>Ping /health Endpoint</span>
                    </button>
                </div>
                <div class="microservices-grid-clean">
                    <div class="micro-card-clean">
                        <h4>🌐 API Gateway</h4>
                        <span class="role">backend/app/main.py</span>
                        <p>ASGI entry point handling routing, CORS, and request lifecycles.</p>
                    </div>
                    <div class="micro-card-clean">
                        <h4>🛡️ Guardrails</h4>
                        <span class="role">services/guardrails_service.py</span>
                        <p>Input sanitization, injection defense, and query validation.</p>
                    </div>
                    <div class="micro-card-clean">
                        <h4>🚦 Router</h4>
                        <span class="role">services/routing_service.py</span>
                        <p>Evaluates complexity and dispatches fast vs deep reasoning models.</p>
                    </div>
                    <div class="micro-card-clean">
                        <h4>📚 Retriever</h4>
                        <span class="role">services/retrieval_service.py</span>
                        <p>ChromaDB HNSW approximate nearest neighbor search in O(log N).</p>
                    </div>
                    <div class="micro-card-clean">
                        <h4>🔢 Embedder</h4>
                        <span class="role">services/embedding_service.py</span>
                        <p>Transforms text into 384-dimensional unit L2 normalized vectors.</p>
                    </div>
                    <div class="micro-card-clean">
                        <h4>⚡ LLM Client</h4>
                        <span class="role">services/llm_service.py</span>
                        <p>Async HTTPX client to Groq Cloud LPUs with retry backoff.</p>
                    </div>
                    <div class="micro-card-clean">
                        <h4>🔍 Hallucination Check</h4>
                        <span class="role">services/hallucination_service.py</span>
                        <p>Computes factual entailment against retrieved context.</p>
                    </div>
                    <div class="micro-card-clean">
                        <h4>💻 AST Analyzer</h4>
                        <span class="role">services/repo_analyzer_service.py</span>
                        <p>Parses syntax trees safely without remote code execution.</p>
                    </div>
                </div>
                <div class="result-box-fill" id="demo-result-surface" style="flex: 0 0 80px; min-height: 80px;">Click "Ping /health Endpoint" to check live service status...</div>
            </div>
        `;
    } else if (ex.type === "docker_terminal") {
        html += `
            <div class="main-workspace-card">
                <div class="workspace-toolbar">
                    <span class="workspace-label">Container & Host Telemetry</span>
                    <button class="btn-clean-action" onclick="fetchLiveSystemMetrics()">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline></svg>
                        <span>Query /metrics</span>
                    </button>
                </div>
                <div class="terminal-view-clean" id="docker-terminal-box"><span class="terminal-accent">$ docker compose ps</span>
NAME                IMAGE                    STATUS              PORTS
mentor_backend      mentor_backend:latest   Up (healthy)        0.0.0.0:8000->8000/tcp
mentor_ollama       ollama/ollama:latest     Up                  0.0.0.0:11434->11434/tcp

<span class="terminal-accent">$ cat docker/docker-compose.yml | grep -E "volumes:" -A 2</span>
    volumes:
      - ../knowledge_base/vectordb:/app/knowledge_base/vectordb
      - ../logs:/app/logs</div>
                <div class="result-box-fill" id="demo-result-surface" style="flex: 0 0 80px; min-height: 80px;">Click "Query /metrics" to inspect host CPU and RAM utilization...</div>
            </div>
        `;
    }

    // ---------------------------------------------------------
    // WEEK 4 TAB RENDERERS (Real & Working)
    // ---------------------------------------------------------
    else if (ex.type === "model_compare_arena") {
        // Ex 1: Multi-Model Side-by-Side Comparison
        html += `
            <div class="main-workspace-card">
                <div class="workspace-toolbar">
                    <span class="workspace-label">Tri-Model Benchmark</span>
                    <span class="workspace-status">GPT-OSS 20B • GPT-OSS 120B • Qwen 27B</span>
                </div>
                <div class="prompt-input-row">
                    <input type="text" id="demo-input-field" class="prompt-field" value="${ex.defaultPrompt || ''}" placeholder="Ask a question to evaluate across all 3 models simultaneously...">
                    <button class="btn-send" id="demo-submit-btn" onclick="runMultiModelComparison()">
                        <span>Evaluate</span>
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>
                    </button>
                </div>
                <div class="result-box-fill" id="demo-result-surface">Press Evaluate to dispatch parallel requests across all 3 Groq models with timing telemetry...</div>
            </div>
        `;
    } else if (ex.type === "dataset_inspector") {
        // Ex 2: Curated 30-Question Evaluation Dataset Browser
        html += `
            <div class="main-workspace-card">
                <div class="workspace-toolbar">
                    <div class="dataset-filter-row">
                        <span class="workspace-label">Evaluation Dataset (30 Cases)</span>
                        <select id="dataset-category-filter" class="dataset-select-filter" onchange="filterDatasetCards(this.value)">
                            <option value="ALL">All Categories (30 Questions)</option>
                            <option value="Project Idea">Project Idea (5)</option>
                            <option value="Architecture">Architecture & Microservices (5)</option>
                            <option value="AI">AI & RAG Concepts (5)</option>
                            <option value="ML">Machine Learning & Vectors (5)</option>
                            <option value="Backend">Backend & APIs (5)</option>
                            <option value="Evaluation">Evaluation & Defense (5)</option>
                        </select>
                    </div>
                    <span class="workspace-status" id="dataset-count-badge">Loading dataset...</span>
                </div>
                <div class="dataset-cards-container" id="dataset-cards-container">Loading questions from /evaluation/dataset...</div>
            </div>
        `;
    } else if (ex.type === "metrics_dashboard") {
        // Ex 3: Precomputed Quantitative Evaluation Metrics Table
        html += `
            <div class="main-workspace-card">
                <div class="workspace-toolbar">
                    <span class="workspace-label">Quantitative IR & Correctness Metrics</span>
                    <button class="btn-clean-action" onclick="fetchLiveMetricsSummary()">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21.5 2v6h-6M21.34 15.57a10 10 0 1 1-.57-8.38l5.67-5.67"/></svg>
                        <span>Refresh Metrics</span>
                    </button>
                </div>
                <div class="metrics-table-wrapper" id="metrics-table-container">Loading precomputed benchmark metrics from /evaluation/metrics-summary...</div>
            </div>
        `;
    } else if (ex.type === "tradeoff_matrix") {
        // Ex 4: Quality vs Latency Trade-Off Analysis
        html += `
            <div class="main-workspace-card">
                <div class="workspace-toolbar">
                    <span class="workspace-label">Dynamic Routing & Trade-Off Matrix</span>
                    <span class="workspace-status">Quality vs Latency vs VRAM</span>
                </div>
                <div class="tradeoff-grid">
                    <div class="tradeoff-card">
                        <header>
                            <h3>OpenAI GPT-OSS 20B</h3>
                            <span class="header-badge">Ultra-Fast</span>
                        </header>
                        <div class="tradeoff-stat-row">
                            <span>Average Latency</span>
                            <span class="metric-highlight">~500 - 1500 ms</span>
                        </div>
                        <div class="tradeoff-stat-row">
                            <span>Semantic Correctness</span>
                            <span>59.8%</span>
                        </div>
                        <div class="tradeoff-stat-row">
                            <span>Optimal Role</span>
                            <span style="color: var(--text-primary);">Real-Time Q&A & Mentorship</span>
                        </div>
                        <p class="tradeoff-summary-text">Recommended default for standard student chats, syllabus checks, and initial problem formulation.</p>
                    </div>

                    <div class="tradeoff-card">
                        <header>
                            <h3>OpenAI GPT-OSS 120B</h3>
                            <span class="header-badge">Deep Reasoning</span>
                        </header>
                        <div class="tradeoff-stat-row">
                            <span>Average Latency</span>
                            <span class="metric-highlight">~1200 - 2200 ms</span>
                        </div>
                        <div class="tradeoff-stat-row">
                            <span>Semantic Correctness</span>
                            <span>59.7%</span>
                        </div>
                        <div class="tradeoff-stat-row">
                            <span>Optimal Role</span>
                            <span style="color: var(--text-primary);">Architecture & Code Analysis</span>
                        </div>
                        <p class="tradeoff-summary-text">Dispatched when queries involve multi-file architecture diagrams, trade-off synthesis, or deep viva defense.</p>
                    </div>

                    <div class="tradeoff-card">
                        <header>
                            <h3>Alibaba Qwen 3.8 27B</h3>
                            <span class="header-badge">High Precision</span>
                        </header>
                        <div class="tradeoff-stat-row">
                            <span>Average Latency</span>
                            <span class="metric-highlight">~1000 ms</span>
                        </div>
                        <div class="tradeoff-stat-row">
                            <span>Hallucination Rate</span>
                            <span class="metric-highlight" style="color: #4ade80;">30.0% (Lowest)</span>
                        </div>
                        <div class="tradeoff-stat-row">
                            <span>Optimal Role</span>
                            <span style="color: var(--text-primary);">Rubric Scoring & Math</span>
                        </div>
                        <p class="tradeoff-summary-text">Highest factual precision and lowest hallucination rate on grading criteria, marks calculations, and logic checks.</p>
                    </div>
                </div>
            </div>
        `;
    } else if (ex.type === "rag_audit_view") {
        // Ex 5: 10-Question Diagnostic RAG Ablation Audit Viewer
        html += `
            <div class="main-workspace-card">
                <div class="workspace-toolbar">
                    <span class="workspace-label">10-Question Diagnostic Ablation Audit</span>
                    <button class="btn-clean-action" onclick="fetchLiveRagAudit()">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline></svg>
                        <span>Load Audit Report</span>
                    </button>
                </div>
                <div class="audit-viewer-container" id="audit-viewer-container">Click "Load Audit Report" to inspect the 10 ablation test cases...</div>
            </div>
        `;
    } else if (ex.type === "repo_ast_explorer") {
        // Ex 6: Codebase / Repository AST Intelligence
        html += `
            <div class="main-workspace-card">
                <div class="workspace-toolbar">
                    <div class="repo-summary-header">
                        <span class="workspace-label">Static AST Repository Explorer</span>
                        <button class="btn-clean-action" onclick="reindexRepository()">
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="16 18 22 12 16 6"></polyline><polyline points="8 6 2 12 8 18"></polyline></svg>
                            <span>Index Codebase</span>
                        </button>
                    </div>
                    <span class="workspace-status" id="repo-index-status">AST Parser Ready</span>
                </div>
                <div class="prompt-input-row">
                    <input type="text" id="demo-input-field" class="prompt-field" value="${ex.defaultPrompt || ''}" placeholder="Ask about classes, functions, or microservice architecture...">
                    <button class="btn-send" id="demo-submit-btn" onclick="runRepoQuery()">
                        <span>Query Code</span>
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>
                    </button>
                </div>
                <div class="result-box-fill" id="demo-result-surface">Type a codebase inquiry (e.g., "Which files implement guardrails and hallucination checks?") to trace AST dependencies...</div>
            </div>
        `;
    }

    container.innerHTML = html;

    // Trigger auto-fetchers for view-based tabs
    if (ex.type === "chunker_tool") {
        runChunkerInspection();
    } else if (ex.type === "dataset_inspector") {
        loadDatasetCards();
    } else if (ex.type === "metrics_dashboard") {
        fetchLiveMetricsSummary();
    } else if (ex.type === "rag_audit_view") {
        fetchLiveRagAudit();
    }

    // Attach Enter key listener
    const inputField = document.getElementById("demo-input-field");
    if (inputField) {
        inputField.addEventListener("keydown", (e) => {
            if (e.key === "Enter") {
                const btn = document.getElementById("demo-submit-btn");
                if (btn) btn.click();
            }
        });
    }
}

// -------------------------------------------------------------
// DEDICATED HANDLERS & API CALLS
// -------------------------------------------------------------

// Clean Markdown & HTML Formatter Helper
function formatAIAnswer(rawText, metaInfo = "") {
    if (!rawText) return "";
    let cleanText = rawText.trim();
    
    // Clean any unclosed or raw markdown syntax cleanly
    let html = "";
    if (metaInfo) {
        html += `<div class="output-meta-badge">${metaInfo}</div>`;
    }

    if (window.marked && typeof window.marked.parse === "function") {
        html += window.marked.parse(cleanText);
    } else {
        html += `<div style="white-space: pre-wrap; font-family: 'JetBrains Mono', monospace;">${cleanText}</div>`;
    }
    return html;
}

// 1. Direct LLM Demo
async function runDirectLLMDemo() {
    const input = document.getElementById("demo-input-field");
    const resEl = document.getElementById("demo-result-surface");
    const submitBtn = document.getElementById("demo-submit-btn");
    const prompt = input ? input.value.trim() : "";
    if (!prompt) return;

    resEl.innerHTML = `<span style="color: var(--text-muted); font-family: 'JetBrains Mono', monospace;">Querying neural model directly via Groq LPU (use_rag: false)...</span>`;
    resEl.classList.add("has-text");
    if (submitBtn) submitBtn.disabled = true;

    try {
        const model = document.getElementById("model-select").value;
        const res = await fetch(`${API_BASE}/chat`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ prompt, model, use_rag: false })
        });
        const data = await res.json();
        if (!res.ok) {
            resEl.innerHTML = `<p style="color: #f87171;">Error: ${data.detail || "Request failed"}</p>`;
        } else {
            const meta = `Model: ${data.model} &nbsp;•&nbsp; Latency: ${data.latency_ms} ms &nbsp;•&nbsp; Pure Parametric`;
            resEl.innerHTML = formatAIAnswer(data.answer, meta);
        }
    } catch (e) {
        resEl.innerHTML = `<p style="color: #f87171;">Error: ${e.message}</p>`;
    } finally {
        if (submitBtn) submitBtn.disabled = false;
    }
}

// 2. Chunker Inspection
function runChunkerInspection() {
    const textarea = document.getElementById("chunker-input-text");
    const container = document.getElementById("chunk-output-container");
    const statPill = document.getElementById("chunk-stat-pill");
    if (!textarea || !container) return;

    const text = textarea.value.trim();
    if (!text) {
        container.innerHTML = "<p style='color: var(--text-muted); font-size: 0.8rem;'>No text to chunk.</p>";
        return;
    }

    const words = text.split(/\s+/).filter(w => w.length > 0);
    const chunkSize = 16;
    const overlap = 5;
    const chunks = [];
    let start = 0;

    while (start < words.length) {
        const end = Math.min(start + chunkSize, words.length);
        const chunkWords = words.slice(start, end);
        chunks.push({
            index: chunks.length + 1,
            words: chunkWords.join(" "),
            count: chunkWords.length,
            overlapStart: start > 0 ? words.slice(start, start + overlap).join(" ") : null
        });
        if (end >= words.length) break;
        start += (chunkSize - overlap);
    }

    if (statPill) {
        statPill.innerText = `${words.length} Words → ${chunks.length} Chunks (16 words, 5 overlap)`;
    }

    container.innerHTML = chunks.map(c => `
        <div class="chunk-item-card">
            <header>
                <span>CHUNK #${c.index}</span>
                <span>${c.count} words</span>
            </header>
            <p>${c.words}</p>
            ${c.overlapStart ? `<div style="font-size: 0.7rem; color: var(--text-muted); font-family: monospace;">Overlap anchor: "${c.overlapStart}..."</div>` : ''}
        </div>
    `).join("");
}

// 3. RAG vs Non-RAG Arena
async function runRagComparisonArena() {
    const input = document.getElementById("demo-input-field");
    const submitBtn = document.getElementById("demo-submit-btn");
    const nonRagContent = document.getElementById("content-non-rag");
    const ragContent = document.getElementById("content-rag");
    const prompt = input ? input.value.trim() : "";
    if (!prompt) return;

    if (submitBtn) submitBtn.disabled = true;
    nonRagContent.innerText = "Generating from raw neural weights...";
    ragContent.innerText = "Retrieving ChromaDB chunks and synthesizing answer...";

    const model = document.getElementById("model-select").value;

    try {
        const [resNonRag, resRag] = await Promise.all([
            fetch(`${API_BASE}/chat`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ prompt, model, use_rag: false })
            }).then(r => r.json()),
            fetch(`${API_BASE}/chat`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ prompt, model, use_rag: true, top_k: 3 })
            }).then(r => r.json())
        ]);

        const nonRagMeta = `Parametric Memory &nbsp;•&nbsp; ${resNonRag.latency_ms} ms`;
        nonRagContent.innerHTML = formatAIAnswer(resNonRag.answer, nonRagMeta);
        nonRagContent.classList.add("active");

        const retrievedSources = (resRag.context || []).map(c => c.source).filter(Boolean).join(", ") || "knowledge_base";
        const ragMeta = `ChromaDB Grounded &nbsp;•&nbsp; ${resRag.latency_ms} ms (Retr: ${resRag.retrieval_time_ms}ms, LLM: ${resRag.llm_time_ms}ms) &nbsp;•&nbsp; ${retrievedSources}`;
        ragContent.innerHTML = formatAIAnswer(resRag.answer, ragMeta);
        ragContent.classList.add("active");
    } catch (e) {
        nonRagContent.innerText = `Error: ${e.message}`;
        ragContent.innerText = `Error: ${e.message}`;
    } finally {
        if (submitBtn) submitBtn.disabled = false;
    }
}

// 4. Ping Microservices
async function testLiveServiceHealth() {
    const resEl = document.getElementById("demo-result-surface");
    resEl.innerText = "Pinging /health endpoint...";
    resEl.classList.add("has-text");

    try {
        const res = await fetch(`${API_BASE}/health`);
        const data = await res.json();
        resEl.innerText = JSON.stringify(data, null, 2);
    } catch (e) {
        resEl.innerText = `Health check failed: ${e.message}`;
    }
}

// 5. Host Metrics
async function fetchLiveSystemMetrics() {
    const resEl = document.getElementById("demo-result-surface");
    resEl.innerText = "Querying /metrics endpoint...";
    resEl.classList.add("has-text");

    try {
        const res = await fetch(`${API_BASE}/metrics`);
        const data = await res.json();
        resEl.innerText = JSON.stringify(data, null, 2);
    } catch (e) {
        resEl.innerText = `Metrics query failed: ${e.message}`;
    }
}

// -------------------------------------------------------------
// WEEK 4 HANDLERS
// -------------------------------------------------------------

// Week 4 Ex 1: Multi-Model Benchmark
async function runMultiModelComparison() {
    const input = document.getElementById("demo-input-field");
    const resEl = document.getElementById("demo-result-surface");
    const submitBtn = document.getElementById("demo-submit-btn");
    const prompt = input ? input.value.trim() : "";
    if (!prompt) return;

    resEl.innerText = "Evaluating query across 3 Groq models simultaneously...";
    resEl.classList.add("has-text");
    if (submitBtn) submitBtn.disabled = true;

    try {
        const res = await fetch(`${API_BASE}/compare-models`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                prompt: prompt,
                models: ["openai/gpt-oss-20b", "openai/gpt-oss-120b", "qwen/qwen3.8-27b"],
                use_rag: true
            })
        });
        const data = await res.json();
        if (!res.ok) {
            resEl.innerHTML = `<p style="color: #f87171;">Comparison failed: ${data.detail || "Error"}</p>`;
        } else {
            let combinedHtml = "";
            data.results.forEach(r => {
                const meta = `Model: ${r.model} &nbsp;•&nbsp; Latency: ${r.latency_ms} ms &nbsp;•&nbsp; Grounding: ${Math.round(r.grounding_score * 100)}% &nbsp;•&nbsp; ${r.token_count} tokens`;
                combinedHtml += `<div style="margin-bottom: 24px; border-bottom: 1px solid var(--border); padding-bottom: 16px;">${formatAIAnswer(r.answer, meta)}</div>`;
            });
            resEl.innerHTML = combinedHtml;
        }
    } catch (e) {
        resEl.innerText = `Error: ${e.message}`;
    } finally {
        if (submitBtn) submitBtn.disabled = false;
    }
}

// Week 4 Ex 2: Dataset Inspector
async function loadDatasetCards() {
    const container = document.getElementById("dataset-cards-container");
    const countBadge = document.getElementById("dataset-count-badge");
    if (!container) return;

    try {
        if (!cachedDataset) {
            const res = await fetch(`${API_BASE}/evaluation/dataset`);
            const data = await res.json();
            cachedDataset = data.questions;
        }

        if (countBadge) countBadge.innerText = `${cachedDataset.length} Questions Loaded`;
        renderDatasetQuestions(cachedDataset);
    } catch (e) {
        container.innerHTML = `<p style="color: #f87171;">Failed to load evaluation dataset: ${e.message}</p>`;
    }
}

function filterDatasetCards(category) {
    if (!cachedDataset) return;
    if (category === "ALL") {
        renderDatasetQuestions(cachedDataset);
    } else {
        const filtered = cachedDataset.filter(q => q.category.toLowerCase().includes(category.toLowerCase()));
        renderDatasetQuestions(filtered);
    }
}

function renderDatasetQuestions(questions) {
    const container = document.getElementById("dataset-cards-container");
    if (!container) return;

    if (!questions || questions.length === 0) {
        container.innerHTML = `<p style="color: var(--text-muted); font-size: 0.8rem;">No questions in this category.</p>`;
        return;
    }

    container.innerHTML = questions.map(q => `
        <div class="dataset-question-card">
            <div class="dataset-question-header">
                <span class="dataset-badge">ID #${q.id} • ${q.category}</span>
                <span style="font-size: 0.72rem; color: var(--text-muted); font-family: monospace;">Sources: ${(q.expected_sources || []).join(", ")}</span>
            </div>
            <div class="dataset-q-text">${q.question}</div>
            <div class="dataset-truth-box">
                <strong style="color: var(--text-primary); font-size: 0.76rem;">Ground Truth:</strong> ${q.ground_truth}
            </div>
        </div>
    `).join("");
}

// Week 4 Ex 3: Metrics Dashboard
async function fetchLiveMetricsSummary() {
    const container = document.getElementById("metrics-table-container");
    if (!container) return;

    container.innerHTML = "Loading precomputed metrics...";

    try {
        const res = await fetch(`${API_BASE}/evaluation/metrics-summary`);
        const data = await res.json();
        const models = data.models || [];

        if (models.length === 0) {
            container.innerHTML = "<p>No metrics found.</p>";
            return;
        }

        let tableHtml = `
            <table class="clean-metrics-table">
                <thead>
                    <tr>
                        <th>Model Name</th>
                        <th>Correctness</th>
                        <th>Relevance</th>
                        <th>Precision@4</th>
                        <th>MRR</th>
                        <th>Hallucination %</th>
                        <th>Code Pass %</th>
                        <th>Latency</th>
                    </tr>
                </thead>
                <tbody>
        `;

        models.forEach(m => {
            const met = m.metrics;
            tableHtml += `
                <tr>
                    <td style="font-weight: 600;">${m.model_name}</td>
                    <td class="metric-highlight">${(met.correctness * 100).toFixed(1)}%</td>
                    <td>${(met.relevance * 100).toFixed(1)}%</td>
                    <td>${met.precision_at_k.toFixed(3)}</td>
                    <td>${met.mrr.toFixed(3)}</td>
                    <td style="color: ${met.hallucination_rate < 35 ? '#4ade80' : '#f87171'};">${met.hallucination_rate.toFixed(1)}%</td>
                    <td>${(met.code_pass_rate * 100).toFixed(1)}%</td>
                    <td>${met.avg_latency_ms.toFixed(1)} ms</td>
                </tr>
            `;
        });

        tableHtml += `</tbody></table>`;
        container.innerHTML = tableHtml;
    } catch (e) {
        container.innerHTML = `<p style="color: #f87171;">Failed to load metrics: ${e.message}</p>`;
    }
}

// Week 4 Ex 5: RAG Diagnostic Audit
async function fetchLiveRagAudit() {
    const container = document.getElementById("audit-viewer-container");
    if (!container) return;

    container.innerText = "Loading audit report from /evaluation/rag-audit...";

    try {
        const res = await fetch(`${API_BASE}/evaluation/rag-audit`);
        const data = await res.json();
        container.innerText = data.audit_markdown || "No audit report content available.";
    } catch (e) {
        container.innerText = `Failed to load audit: ${e.message}`;
    }
}

// Week 4 Ex 6: Codebase AST Explorer
async function runRepoQuery() {
    const input = document.getElementById("demo-input-field");
    const resEl = document.getElementById("demo-result-surface");
    const submitBtn = document.getElementById("demo-submit-btn");
    const question = input ? input.value.trim() : "";
    if (!question) return;

    resEl.innerText = "Searching AST vector index across codebase...";
    resEl.classList.add("has-text");
    if (submitBtn) submitBtn.disabled = true;

    try {
        const res = await fetch(`${API_BASE}/repo/query`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question: question, top_k: 4 })
        });
        const data = await res.json();
        if (!res.ok) {
            resEl.innerHTML = `<p style="color: #f87171;">Error: ${data.detail || "Request failed"}</p>`;
        } else {
            const files = (data.referenced_files || []).join(", ") || "None";
            const meta = `Codebase AST Search &nbsp;•&nbsp; Latency: ${data.latency_ms} ms &nbsp;•&nbsp; Files: ${files}`;
            resEl.innerHTML = formatAIAnswer(data.answer, meta);
        }
    } catch (e) {
        resEl.innerText = `Error: ${e.message}`;
    } finally {
        if (submitBtn) submitBtn.disabled = false;
    }
}

async function reindexRepository() {
    const status = document.getElementById("repo-index-status");
    const resEl = document.getElementById("demo-result-surface");
    if (status) status.innerText = "Indexing codebase...";
    if (resEl) resEl.innerText = "Parsing Abstract Syntax Trees across backend/ and services/...";

    try {
        const res = await fetch(`${API_BASE}/repo/index`, { method: "POST" });
        const data = await res.json();
        if (status) status.innerText = `Indexed ${data.total_nodes || 10} AST Nodes`;
        if (resEl) resEl.innerText = JSON.stringify(data, null, 2);
    } catch (e) {
        if (status) status.innerText = "Indexing failed";
        if (resEl) resEl.innerText = `Error: ${e.message}`;
    }
}

// Sidebar quick navigation
function selectSidebarItem(key) {
    activeSidebarNav = key;
    document.querySelectorAll(".sidebar-item").forEach(el => el.classList.remove("active"));
    const activeBtn = document.getElementById(`nav-${key}`);
    if (activeBtn) activeBtn.classList.add("active");

    const pageTitle = document.getElementById("page-title");

    if (key === "exercises") {
        pageTitle.innerText = "Lab Exercises";
        renderSubTabNav();
    } else if (key === "dsa") {
        pageTitle.innerText = "DSA & Algorithms";
        setQuickTopicQuery("Explain the Master Theorem cases and compare AVL vs Red-Black Trees for lookup operations.");
    } else if (key === "os") {
        pageTitle.innerText = "Operating Systems & Concurrency";
        setQuickTopicQuery("What is the difference between Mutex, Semaphore, and Spinlock? Explain the 4 Coffman conditions for Deadlock.");
    } else if (key === "dbms") {
        pageTitle.innerText = "DBMS & System Design";
        setQuickTopicQuery("How do B+ Trees differ from LSM Trees in database storage engines? Explain ACID transaction isolation levels.");
    } else if (key === "networks") {
        pageTitle.innerText = "Computer Networks & Distributed Systems";
        setQuickTopicQuery("Explain TCP vs UDP vs QUIC HTTP/3, and break down CAP Theorem vs PACELC in distributed systems.");
    } else if (key === "ai") {
        pageTitle.innerText = "AI & LLM Architecture";
        setQuickTopicQuery("How does Scaled Dot-Product Attention work? Explain KV Caching and FlashAttention memory optimization.");
    } else if (key === "viva") {
        pageTitle.innerText = "Viva Voce Defense";
        setQuickTopicQuery("Why choose RAG over Fine-Tuning? How does ChromaDB HNSW vector search achieve O(log N) latency?");
    } else if (key === "marks") {
        pageTitle.innerText = "Project Evaluation Rubric";
        setQuickTopicQuery("What is the exact marks distribution across Problem Formulation, Architecture, Technical Implementation, and Viva Voce?");
    }
}

function setQuickTopicQuery(promptText) {
    currentWeek = "w3";
    currentExIndex = 0;
    renderSubTabNav();
    const input = document.getElementById("demo-input-field");
    if (input) {
        input.value = promptText;
        runDirectLLMDemo();
    }
}

function onModelChange(modelName) {
    const label = document.getElementById("selected-model-label");
    if (modelName.includes("120b")) label.innerText = "GPT-OSS 120B";
    else if (modelName.includes("qwen")) label.innerText = "Qwen 3.8 27B";
    else label.innerText = "GPT-OSS 20B";
}

// Initial boot
document.addEventListener("DOMContentLoaded", () => {
    renderSubTabNav();
});
