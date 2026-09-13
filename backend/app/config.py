import os
import yaml
from pathlib import Path
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent.parent
CONFIG_PATH = BASE_DIR / "configs" / "config.yaml"

try:
    from dotenv import load_dotenv
    load_dotenv(BASE_DIR / ".env")
    load_dotenv(BASE_DIR / "docker" / ".env")
except ImportError:
    pass

def load_yaml_config():
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    return {}

yaml_cfg = load_yaml_config()

class Settings(BaseSettings):
    PROJECT_NAME: str = yaml_cfg.get("app", {}).get("name", "AI Project Mentor for Final-Year Students")
    VERSION: str = yaml_cfg.get("app", {}).get("version", "1.0.0")
    ENV: str = os.getenv("APP_ENV", yaml_cfg.get("app", {}).get("environment", "development"))
    HOST: str = os.getenv("HOST", yaml_cfg.get("app", {}).get("host", "0.0.0.0"))
    PORT: int = int(os.getenv("PORT", yaml_cfg.get("app", {}).get("port", 8000)))
    
    # LLM Settings
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", yaml_cfg.get("llm", {}).get("provider", "groq"))
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", yaml_cfg.get("llm", {}).get("groq_api_key", ""))
    GROQ_BASE_URL: str = os.getenv("GROQ_BASE_URL", yaml_cfg.get("llm", {}).get("groq_base_url", "https://api.groq.com/openai/v1"))
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", yaml_cfg.get("llm", {}).get("ollama_base_url", "http://localhost:11434"))
    DEFAULT_MODEL: str = os.getenv("DEFAULT_MODEL", yaml_cfg.get("llm", {}).get("default_model", "openai/gpt-oss-20b"))
    SUPPORTED_MODELS: list = yaml_cfg.get("llm", {}).get("supported_models", [
        "openai/gpt-oss-20b", "openai/gpt-oss-120b", "qwen/qwen3.8-27b"
    ])
    LLM_TIMEOUT: int = int(os.getenv("LLM_TIMEOUT", yaml_cfg.get("llm", {}).get("timeout_seconds", 60)))
    MAX_RETRIES: int = int(os.getenv("MAX_RETRIES", yaml_cfg.get("llm", {}).get("max_retries", 2)))
    
    # RAG Settings
    EMBEDDING_MODEL_NAME: str = yaml_cfg.get("rag", {}).get("embedding_model_name", "all-MiniLM-L6-v2")
    CHROMA_DB_DIR: str = str(BASE_DIR / yaml_cfg.get("rag", {}).get("chroma_db_dir", "knowledge_base/vectordb"))
    COLLECTION_NAME: str = yaml_cfg.get("rag", {}).get("collection_name", "project_mentor_kb")
    CODE_COLLECTION_NAME: str = yaml_cfg.get("rag", {}).get("code_collection_name", "repository_code_kb")
    TOP_K: int = int(yaml_cfg.get("rag", {}).get("top_k", 4))
    SIMILARITY_THRESHOLD: float = float(yaml_cfg.get("rag", {}).get("similarity_threshold", 0.35))
    CHUNK_SIZE: int = int(yaml_cfg.get("rag", {}).get("chunk_size", 500))
    CHUNK_OVERLAP: int = int(yaml_cfg.get("rag", {}).get("chunk_overlap", 80))
    
    # Directories
    DOCUMENTS_DIR: str = str(BASE_DIR / "knowledge_base" / "documents")
    EVALUATION_DATASETS_DIR: str = str(BASE_DIR / "evaluation" / "datasets")
    EVALUATION_OUTPUT_DIR: str = str(BASE_DIR / "evaluation" / "outputs")
    LOGS_DIR: str = str(BASE_DIR / "logs")

settings = Settings()

# Ensure critical directories exist
for p in [settings.CHROMA_DB_DIR, settings.DOCUMENTS_DIR, settings.EVALUATION_DATASETS_DIR, settings.EVALUATION_OUTPUT_DIR, settings.LOGS_DIR]:
    os.makedirs(p, exist_ok=True)
