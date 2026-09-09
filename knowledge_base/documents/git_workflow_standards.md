# Git Workflow & Version Control Standards for Engineering Projects

## 1. Git Branching Strategy (GitFlow Lite)
For team collaboration in academic and production environments, use the following branching model:

```
  main (production releases, tags v1.0.0)
   ↑
  develop (integration branch)
   ↑ 
  feature/rag-retriever  feature/api-gateway  feature/eval-metrics
```

- **`main`**: Protected branch. Only fully tested and reviewed releases are merged here.
- **`develop`**: Central integration branch for ongoing development.
- **`feature/<name>`**: Feature branches branched from `develop` and merged via Pull Requests.
- **`hotfix/<name>`**: Urgent fixes branched directly from `main`.

---

## 2. Conventional Commit Message Standards
Every commit must follow the Conventional Commits specification:
- `feat: add ChromaDB persistent vector retrieval service`
- `fix: handle HTTP 504 timeout when Ollama is loading model weights`
- `docs: update evaluation rubric documentation and guidelines`
- `test: add end-to-end integration tests for /chat endpoint`
- `refactor: optimize token chunking with sliding window overlap`
- `perf: implement caching for sentence transformer embeddings`

---

## 3. Pull Request (PR) & Code Review Rules
1. Every PR must have a clear description explaining what was changed and how it was tested.
2. At least one teammate must approve the PR before merging.
3. Automated test suite (`pytest`) must pass completely in CI.
4. Never commit sensitive credentials, API keys, or `.env` files. Include `.gitignore` for `.env`, `__pycache__`, `*.pyc`, `venv/`, and `vectordb/`.
