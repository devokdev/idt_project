from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

# Chat Schemas
class ChatRequest(BaseModel):
    prompt: str = Field(..., description="Student query or question", min_length=1)
    model: Optional[str] = Field("codellama:latest", description="LLM to use (codellama, starcoder2, phi3)")
    use_rag: bool = Field(True, description="Enable Retrieval-Augmented Generation")
    top_k: int = Field(4, ge=1, le=10, description="Number of context chunks to retrieve")
    stream: bool = Field(False, description="Whether to stream response")
    temperature: Optional[float] = Field(0.2, ge=0.0, le=1.0)

class ContextChunk(BaseModel):
    content: str
    source: str
    score: float
    chunk_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class ChatResponse(BaseModel):
    answer: str
    model: str
    latency_ms: float
    retrieval_time_ms: float = 0.0
    llm_time_ms: float = 0.0
    used_rag: bool
    context: List[ContextChunk] = []
    guardrail_status: str = "passed"
    confidence_score: Optional[float] = None

# Retrieval Schemas
class RetrieveRequest(BaseModel):
    query: str
    top_k: int = 4
    collection: Optional[str] = None
    min_score: Optional[float] = 0.2

class RetrieveResponse(BaseModel):
    query: str
    results: List[ContextChunk]
    total_retrieved: int
    latency_ms: float

# Embedding Schemas
class EmbedRequest(BaseModel):
    texts: List[str]

class EmbedResponse(BaseModel):
    embeddings: List[List[float]]
    dimension: int
    count: int

# Model Management Schemas
class ModelInfo(BaseModel):
    name: str
    description: str
    size: str
    status: str
    is_available: bool

class ModelsListResponse(BaseModel):
    models: List[ModelInfo]
    current_default: str

# Evaluation Schemas
class EvaluateRequest(BaseModel):
    models: Optional[List[str]] = None
    sample_size: Optional[int] = 30
    save_results: bool = True

class MetricScores(BaseModel):
    correctness: float
    relevance: float
    precision_at_k: float
    recall_at_k: float
    mrr: float
    hallucination_rate: float
    code_pass_rate: float
    avg_latency_ms: float
    prompt_tokens: int
    completion_tokens: int

class ModelEvaluationSummary(BaseModel):
    model_name: str
    metrics: MetricScores
    hardware_stats: Dict[str, Any]

class EvaluationResponse(BaseModel):
    evaluations: List[ModelEvaluationSummary]
    summary_chart_path: Optional[str] = None
    csv_results_path: Optional[str] = None

# Repository Intelligence Schemas
class RepoQuestionRequest(BaseModel):
    question: str
    project_path: Optional[str] = None
    top_k: int = 5

class RepoQuestionResponse(BaseModel):
    question: str
    answer: str
    referenced_files: List[str]
    context_chunks: List[ContextChunk]
    latency_ms: float

# Suggestion Schema
class SuggestionResponse(BaseModel):
    query_prefix: str
    suggestions: List[str]
