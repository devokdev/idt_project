from fastapi import APIRouter
from backend.app.schemas.pydantic_models import EvaluateRequest, EvaluationResponse
from evaluation.evaluator import model_evaluator

router = APIRouter(prefix="", tags=["Evaluation & Benchmarking"])

@router.post("/evaluate", response_model=EvaluationResponse)
async def evaluate_models_endpoint(request: EvaluateRequest):
    """
    Executes multi-model evaluation across dataset questions, calculating
    Precision@K, Recall@K, MRR, Correctness, Relevance, Hallucination Rate, and Latency.
    """
    models_to_test = request.models or ["codellama:latest", "starcoder2:latest", "phi3:latest"]
    results = model_evaluator.run_benchmark(
        models=models_to_test,
        sample_size=request.sample_size or 30,
        save_results=request.save_results
    )
    return results
