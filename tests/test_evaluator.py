import pytest
from evaluation.metrics import EvaluationMetrics
from evaluation.evaluator import model_evaluator

def test_evaluation_metrics_precision_recall_mrr():
    retrieved = ["project_guidelines.md", "evaluation_rubric.md", "common_viva_questions.md"]
    expected = ["evaluation_rubric.md", "project_guidelines.md"]
    
    p = EvaluationMetrics.precision_at_k(retrieved, expected, k=2)
    r = EvaluationMetrics.recall_at_k(retrieved, expected, k=2)
    mrr = EvaluationMetrics.mean_reciprocal_rank(retrieved, expected)
    
    assert p == 1.0
    assert r == 1.0
    assert mrr == 1.0

def test_semantic_correctness():
    gen = "The final evaluation gives 35 marks for implementation."
    gt = "Technical implementation carries 35 marks in the rubric."
    corr = EvaluationMetrics.compute_correctness(gen, gt)
    assert corr > 0.5

def test_benchmark_runner_sample():
    eval_res = model_evaluator.run_benchmark(models=["phi3:latest"], sample_size=2, save_results=False)
    assert "evaluations" in eval_res
    assert len(eval_res["evaluations"]) == 1
    assert "metrics" in eval_res["evaluations"][0]
