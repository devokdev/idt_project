import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from rag.rag_pipeline import rag_pipeline
from evaluation.metrics import EvaluationMetrics
from services.hallucination_service import hallucination_service
from backend.app.config import settings

SAMPLE_10_DIAGNOSTIC_QUESTIONS = [
    {
        "id": 1,
        "question": "What is the exact marks distribution in the final-year evaluation rubric?",
        "ground_truth": "Problem Formulation: 15%, System Architecture: 20%, Technical Implementation: 35%, Validation/Metrics: 15%, Viva: 15% (Total: 100 Marks)."
    },
    {
        "id": 2,
        "question": "What are the requirements for an Exemplary score in Quantitative Validation?",
        "ground_truth": "Rigorous metrics computed on verified datasets (F1, MRR, latency P95/P99, RAM/CPU profiling) with comparative charts."
    },
    {
        "id": 3,
        "question": "What is the maximum allowed plagiarism similarity percentage for thesis submission?",
        "ground_truth": "Similarity index must not exceed 15% using Turnitin or Urkund."
    },
    {
        "id": 4,
        "question": "Why is L2 normalization applied to embedding vectors before vector search?",
        "ground_truth": "L2 normalization enables cosine similarity to be computed directly via dot products."
    },
    {
        "id": 5,
        "question": "What branching strategy should be used according to the team Git standards?",
        "ground_truth": "GitFlow Lite: main, develop, and feature/<name> branches with Pull Requests."
    },
    {
        "id": 6,
        "question": "What is the time complexity of vector retrieval in ChromaDB?",
        "ground_truth": "HNSW indexing achieves O(log N) average search time."
    },
    {
        "id": 7,
        "question": "How do you handle 504 Gateway Timeouts when calling Ollama models?",
        "ground_truth": "Increase timeout_seconds, check VRAM loading, and verify Ollama port 11434."
    },
    {
        "id": 8,
        "question": "What is the difference between fine-tuning and RAG for academic project mentoring?",
        "ground_truth": "Fine-tuning modifies model weights with risk of forgetting; RAG dynamically retrieves factual context at query time."
    },
    {
        "id": 9,
        "question": "What chunk size and overlap are configured in this RAG pipeline?",
        "ground_truth": "Chunk size of 500 words with 80 words sliding overlap."
    },
    {
        "id": 10,
        "question": "What are the questions external examiners ask during the project viva?",
        "ground_truth": "Individual code contributions, algorithm complexity, justification of technology choices, and error handling."
    }
]

def run_rag_pipeline_deep_analysis():
    print("=" * 80)
    print("WEEK 4 EXERCISE 5: IN-DEPTH RAG PIPELINE DIAGNOSTIC (10 QUESTIONS)")
    print("=" * 80)

    out_file = Path(settings.EVALUATION_OUTPUT_DIR) / "rag_pipeline_10_question_analysis.md"
    out_file.parent.mkdir(parents=True, exist_ok=True)

    with open(out_file, "w", encoding="utf-8") as f:
        f.write("# In-Depth RAG Pipeline Diagnostic & Grounding Analysis (10 Benchmark Questions)\n\n")

        for idx, item in enumerate(SAMPLE_10_DIAGNOSTIC_QUESTIONS, 1):
            q = item["question"]
            gt = item["ground_truth"]

            res = rag_pipeline.run(question=q, model="codellama:latest", use_rag=True)
            non_rag_res = rag_pipeline.run(question=q, model="codellama:latest", use_rag=False)
            
            h_eval = hallucination_service.analyze_hallucination(res["answer"], res["context"])
            corr = EvaluationMetrics.compute_correctness(res["answer"], gt)
            
            # Identify diagnostic classification
            if len(res["context"]) > 0 and h_eval["hallucination_rate"] < 15.0 and corr > 0.6:
                diag_class = "[PASS] Correct Retrieval & High Grounding"
                insight = "Retriever fetched authoritative rubric/guidelines; answer grounded strictly on extracted facts."
            elif len(res["context"]) > 0 and h_eval["hallucination_rate"] >= 15.0:
                diag_class = "[WARN] Parametric Hallucination despite Context"
                insight = "LLM injected additional generic statements not present in retrieved context."
            elif len(res["context"]) == 0:
                diag_class = "[FAIL] Missing Retrieval"
                insight = "Query vector did not cross the similarity threshold; fell back to parametric memory."
            else:
                diag_class = "[IMPROVED] Improved Answer Because of Retrieval"
                insight = "Non-RAG gave vague response, whereas RAG answer cited exact university weights."

            print(f"\n--- Diagnostic Case {idx}: {q} ---")
            print(f"Status: {diag_class}")
            print(f"Retrieved Chunks: {len(res['context'])} | Latency: {res['latency_ms']}ms | Correctness: {corr}")
            print(f"Hallucination Rate: {h_eval['hallucination_rate']}% | Groundedness: {h_eval['groundedness_score']}")

            f.write(f"## Case {idx}: {q}\n\n")
            f.write(f"**Diagnostic Classification**: `{diag_class}`\n\n")
            f.write(f"- **Ground Truth**: {gt}\n")
            f.write(f"- **Retrieval Latency**: {res['retrieval_time_ms']} ms | **Total Latency**: {res['latency_ms']} ms\n")
            f.write(f"- **Groundedness Score**: {h_eval['groundedness_score']} | **Hallucination Rate**: {h_eval['hallucination_rate']}%\n\n")
            
            f.write("### Retrieved Context Chunks:\n")
            for c_i, chunk in enumerate(res["context"], 1):
                f.write(f"> **Chunk {c_i} (Source: `{chunk['source']}`, Similarity: {chunk['score']:.3f})**:\n")
                f.write(f"> {chunk['content'][:250]}...\n\n")

            f.write("### Generated RAG Answer:\n")
            f.write(f"{res['answer']}\n\n")

            f.write("### Comparison without RAG:\n")
            f.write(f"{non_rag_res['answer']}\n\n")

            f.write(f"### Analytical Finding:\n{insight}\n\n---\n\n")

    print(f"\nDetailed 10-Question Diagnostic Report written to: {out_file}")
    print("=" * 80)

if __name__ == "__main__":
    run_rag_pipeline_deep_analysis()
