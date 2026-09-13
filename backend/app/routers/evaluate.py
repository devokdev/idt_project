import json
from pathlib import Path
from fastapi import APIRouter, HTTPException
from backend.app.schemas.pydantic_models import EvaluateRequest, EvaluationResponse
from evaluation.evaluator import model_evaluator
from backend.app.config import BASE_DIR

router = APIRouter(prefix="", tags=["Evaluation & Benchmarking"])

EVAL_OUTPUTS_DIR = BASE_DIR / "evaluation" / "outputs"
EVAL_DATASETS_DIR = BASE_DIR / "evaluation" / "datasets"

@router.get("/evaluation/dataset")
async def get_evaluation_dataset():
    """Returns the curated 30-question evaluation dataset with ground truth."""
    dataset_file = EVAL_DATASETS_DIR / "evaluation_30_questions.json"
    if not dataset_file.exists():
        raise HTTPException(status_code=404, detail="Evaluation dataset not found.")
    with open(dataset_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return {"total": len(data), "questions": data}

@router.get("/evaluation/metrics-summary")
async def get_metrics_summary():
    """Returns the precomputed quantitative IR, quality, and hardware metrics for all 3 models."""
    summary_file = EVAL_OUTPUTS_DIR / "model_summaries.json"
    if not summary_file.exists():
        raise HTTPException(status_code=404, detail="Model summaries file not found.")
    with open(summary_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return {"models": data}

@router.get("/evaluation/rag-audit")
async def get_rag_audit_cases():
    """Returns the 10-case RAG diagnostic ablation audit."""
    audit_file = EVAL_OUTPUTS_DIR / "rag_pipeline_10_question_analysis.md"
    if not audit_file.exists():
        raise HTTPException(status_code=404, detail="RAG audit file not found.")
    with open(audit_file, "r", encoding="utf-8") as f:
        content = f.read()
    return {"audit_markdown": content}

@router.post("/evaluate", response_model=EvaluationResponse)
async def evaluate_models_endpoint(request: EvaluateRequest):
    """
    Executes multi-model evaluation across dataset questions, calculating
    Precision@K, Recall@K, MRR, Correctness, Relevance, Hallucination Rate, and Latency.
    """
    models_to_test = request.models or ["openai/gpt-oss-20b", "openai/gpt-oss-120b", "qwen/qwen3.8-27b"]
    results = model_evaluator.run_benchmark(
        models=models_to_test,
        sample_size=request.sample_size or 30,
        save_results=request.save_results
    )
    return results
