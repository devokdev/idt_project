import os
import json
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path

logger = logging.getLogger("document_loader")

class DocumentLoader:
    """
    Multi-format document loader supporting Markdown, TXT, JSON, PDF, and Code files.
    """
    @staticmethod
    def load_file(file_path: str) -> List[Dict[str, Any]]:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        ext = path.suffix.lower()
        if ext in [".md", ".markdown"]:
            return DocumentLoader._load_text(path, doc_type="markdown")
        elif ext in [".txt", ".rst"]:
            return DocumentLoader._load_text(path, doc_type="text")
        elif ext in [".json"]:
            return DocumentLoader._load_json(path)
        elif ext in [".py", ".js", ".ts", ".html", ".css", ".yaml", ".yml", ".sh"]:
            return DocumentLoader._load_text(path, doc_type="code")
        elif ext in [".pdf"]:
            return DocumentLoader._load_pdf(path)
        else:
            return DocumentLoader._load_text(path, doc_type="unknown")

    @staticmethod
    def _load_text(path: Path, doc_type: str) -> List[Dict[str, Any]]:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        return [{
            "content": content,
            "metadata": {
                "source": path.name,
                "file_path": str(path),
                "doc_type": doc_type,
                "size_bytes": len(content.encode("utf-8"))
            }
        }]

    @staticmethod
    def _load_json(path: Path) -> List[Dict[str, Any]]:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        docs = []
        if isinstance(data, list):
            for idx, item in enumerate(data):
                docs.append({
                    "content": json.dumps(item, indent=2),
                    "metadata": {
                        "source": path.name,
                        "file_path": str(path),
                        "item_index": idx,
                        "doc_type": "json"
                    }
                })
        elif isinstance(data, dict):
            for key, val in data.items():
                docs.append({
                    "content": f"Section: {key}\n{json.dumps(val, indent=2)}",
                    "metadata": {
                        "source": path.name,
                        "file_path": str(path),
                        "section": key,
                        "doc_type": "json"
                    }
                })
        return docs

    @staticmethod
    def _load_pdf(path: Path) -> List[Dict[str, Any]]:
        docs = []
        try:
            import pypdf
            reader = pypdf.PdfReader(str(path))
            for page_num, page in enumerate(reader.pages, 1):
                text = page.extract_text() or ""
                if text.strip():
                    docs.append({
                        "content": text,
                        "metadata": {
                            "source": path.name,
                            "file_path": str(path),
                            "page_number": page_num,
                            "total_pages": len(reader.pages),
                            "doc_type": "pdf"
                        }
                    })
        except Exception as e:
            logger.warning(f"pypdf extraction failed on {path.name}: {e}. Reading as raw text stream.")
            return DocumentLoader._load_text(path, doc_type="pdf_raw")
        return docs

    @staticmethod
    def load_directory(dir_path: str, recursive: bool = True) -> List[Dict[str, Any]]:
        """Loads all documents in a directory."""
        path = Path(dir_path)
        if not path.exists() or not path.is_dir():
            logger.warning(f"Directory {dir_path} does not exist.")
            return []
        
        all_docs = []
        pattern = "**/*" if recursive else "*"
        for file in path.glob(pattern):
            if file.is_file() and not file.name.startswith("."):
                try:
                    loaded = DocumentLoader.load_file(str(file))
                    all_docs.extend(loaded)
                except Exception as e:
                    logger.error(f"Error loading {file}: {e}")
        return all_docs
