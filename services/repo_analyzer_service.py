import os
import ast
import time
from pathlib import Path
from typing import List, Dict, Any, Optional
from services.retrieval_service import retrieval_service
from services.llm_service import llm_service
from rag.prompt_builder import PromptBuilder
from backend.app.config import settings

class RepoAnalyzerService:
    """
    Codebase understanding and multi-file dependency intelligence service.
    Indexes AST symbols, functions, classes, imports, and cross-file dependencies.
    """
    def __init__(self):
        self.retriever = retrieval_service
        self.llm = llm_service

    def index_repository(self, root_path: str) -> Dict[str, Any]:
        """Indexes source files and stores code chunks in Chroma code collection."""
        p = Path(root_path)
        if not p.exists():
            raise FileNotFoundError(f"Project directory not found: {root_path}")

        code_chunks = []
        extensions = [".py", ".json", ".yaml", ".yml", ".md", ".sh", ".dockerfile", "Dockerfile"]

        for file_path in p.rglob("*"):
            if file_path.is_file() and not any(part.startswith((".", "venv", "__pycache__", "vectordb")) for part in file_path.parts):
                if file_path.suffix.lower() in extensions or file_path.name.lower() in ["dockerfile"]:
                    try:
                        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                            content = f.read()

                        if not content.strip():
                            continue

                        # Extract AST summary for python files
                        ast_meta = self._parse_ast(content) if file_path.suffix == ".py" else {}
                        rel_path = str(file_path.relative_to(p))

                        code_chunks.append({
                            "content": f"# File: {rel_path}\n" + (f"# AST Functions: {ast_meta.get('functions', [])}\n" if ast_meta else "") + content,
                            "metadata": {
                                "source": rel_path,
                                "file_name": file_path.name,
                                "file_type": file_path.suffix or "dockerfile",
                                "classes": ",".join(ast_meta.get("classes", [])),
                                "functions": ",".join(ast_meta.get("functions", [])),
                                "imports": ",".join(ast_meta.get("imports", []))
                            },
                            "chunk_id": f"code_{rel_path.replace(os.sep, '_')}"
                        })
                    except Exception as e:
                        pass

        ingested_count = self.retriever.add_documents(code_chunks, collection_name=settings.CODE_COLLECTION_NAME)
        return {
            "indexed_files": len(code_chunks),
            "ingested_chunks": ingested_count,
            "collection": settings.CODE_COLLECTION_NAME
        }

    def _parse_ast(self, code_str: str) -> Dict[str, List[str]]:
        classes, functions, imports = [], [], []
        try:
            tree = ast.parse(code_str)
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    classes.append(node.name)
                elif isinstance(node, ast.FunctionDef):
                    functions.append(node.name)
                elif isinstance(node, ast.Import):
                    for n in node.names:
                        imports.append(n.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append(node.module)
        except Exception:
            pass
        return {
            "classes": classes,
            "functions": functions,
            "imports": imports
        }

    def answer_repository_query(self, question: str, top_k: int = 5) -> Dict[str, Any]:
        start = time.time()
        # Retrieve code snippets from ChromaDB code collection
        retrieved = self.retriever.retrieve(
            query=question,
            top_k=top_k,
            threshold=0.20,
            collection_name=settings.CODE_COLLECTION_NAME
        )

        prompt = PromptBuilder.build_repo_analysis_prompt(question, retrieved)
        llm_res = self.llm.generate(prompt=prompt, model="codellama:latest")
        latency = (time.time() - start) * 1000

        referenced_files = list({c.get("source", "unknown") for c in retrieved})

        return {
            "question": question,
            "answer": llm_res.get("text", ""),
            "referenced_files": referenced_files,
            "context_chunks": retrieved,
            "latency_ms": round(latency, 2)
        }

repo_analyzer_service = RepoAnalyzerService()
