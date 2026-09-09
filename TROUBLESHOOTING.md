# Troubleshooting & Gotchas Manual
> **Diagnostic and Resolution Guide for Common Development, Runtime, VectorDB, and Ollama Multi-Model Errors.**

---

## 1. Port Conflicts (Address Already in Use)

### Symptom
```
OSError: [Errno 48] Address already in use: 0.0.0.0:8000
OSError: [Errno 10048] Only one usage of each socket address is normally permitted: 11434
```

### Root Cause
An orphaned uvicorn process, zombie Docker container, or existing background server is holding the port.

### Resolution Steps
- **Windows PowerShell**:
  ```powershell
  # Find PID occupying port 8000 or 11434
  netstat -ano | findstr :8000
  # Kill process by PID
  Stop-Process -Id <PID> -Force
  ```
- **Linux / macOS**:
  ```bash
  # Identify process
  sudo lsof -i :8000
  # Terminate process
  sudo kill -9 $(sudo lsof -t -i:8000)
  ```

---

## 2. ChromaDB SQLite Database Locks & Concurrency Issues

### Symptom
```
OperationalError: database is locked
sqlite3.OperationalError: disk I/O error
```

### Root Cause
SQLite (which powers ChromaDB persistent mode) uses file-level locking. Multiple processes (e.g., simultaneous ingestion while running evaluation tests or multiple workers in uvicorn) attempting write transactions simultaneously will trigger database lock timeouts.

### Resolution Steps
1. **Use Single Ingest Worker**: Always ensure only one process performs document writes at a time.
2. **Read-Only Concurrent Queries**: In `services/retrieval_service.py`, ChromaDB instances are instantiated using the shared `PersistentClient` singleton to reuse SQLite connections.
3. **Resetting Corrupt Vector DB**:
   ```bash
   # Remove locked ChromaDB folder
   rm -rf knowledge_base/vectordb/
   # Re-run ingestion
   python scripts/ingest_knowledge_base.py
   ```

---

## 3. Ollama HTTP 404 (Model Not Found)

### Symptom
```
HTTP Request: POST http://localhost:11434/api/generate "HTTP/1.1 404 Not Found"
WARNING:llm_service:Model 'codellama:latest' not found in local Ollama instance (HTTP 404). Falling back immediately.
```

### Root Cause
Ollama is running, but the specified model tag has not yet been pulled into the local model registry (`~/.ollama/models`).

### Resolution Steps
1. **Pull the model explicitly**:
   ```bash
   ollama pull codellama:latest
   ollama pull starcoder2:latest
   ollama pull phi3:latest
   ```
2. **Verify pulled models**:
   ```bash
   ollama list
   ```
3. **Automatic Fallback Handling**: Note that the application is architected with a deterministic self-contained inference engine in `services/llm_service.py` that catches HTTP 404s instantly without blocking or crashing the service.

---

## 4. Ollama HTTP 504 Gateway Timeout or ReadTimeout

### Symptom
```
httpx.ReadTimeout: The read operation timed out after 60.0 seconds.
```

### Root Cause
Model initialization (cold start) or heavy prompt computation on CPU systems takes longer than the standard HTTP client timeout.

### Resolution Steps
1. **Increase Timeout in `configs/config.yaml`**:
   ```yaml
   models:
     timeout_seconds: 180
   ```
2. **Pre-warm the Model in Memory**:
   ```bash
   curl http://localhost:11434/api/generate -d '{"model": "codellama:latest", "keep_alive": "24h"}'
   ```
3. **Switch to a Smaller Model for CPU-only Machines**: Select `phi3:latest` (3.8B parameters) or `phi3:mini` which processes prompts 3x faster than 7B models on standard x86 CPUs.

---

## 5. CUDA Out of Memory (OOM) Errors

### Symptom
```
torch.cuda.OutOfMemoryError: CUDA out of memory. Tried to allocate 2.40 GiB
```

### Root Cause
Hosting SentenceTransformers embeddings and multiple large LLMs simultaneously on a GPU with $\le 8\text{ GB}$ VRAM.

### Resolution Steps
1. **Force SentenceTransformers to CPU**: In `services/embedding_service.py`, pass `device="cpu"` to keep GPU VRAM 100% free for Ollama quantization weights:
   ```python
   self.model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")
   ```
2. **Use 4-bit Quantization (`Q4_K_M`) in Ollama**:
   Ollama automatically loads 4-bit quantized weights by default (~3.8 GB VRAM for 7B models), fitting comfortably inside consumer GPUs (RTX 3060/4060).

---

## 6. AST Parsing Syntax Errors on Non-Python Repositories

### Symptom
```
SyntaxError: invalid syntax at line 1 in file repository/script.sh
```

### Root Cause
Attempting to run `ast.parse()` on shell scripts, HTML templates, or non-Python source files.

### Resolution Steps
- In `services/repo_analyzer_service.py`, the file scanner explicitly filters files with `.endswith(".py")` and wraps `ast.parse` in a `try...except (SyntaxError, UnicodeDecodeError)` block to gracefully bypass non-standard or malformed Python files without halting analysis.
