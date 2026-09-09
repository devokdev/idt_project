import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from evaluation.generate_charts import generate_evaluation_visualizations
from evaluation.run_rag_pipeline_analysis import run_rag_pipeline_deep_analysis

def run_all():
    print("==========================================================")
    print("STARTING FULL EVALUATION SUITE (WEEK 4)")
    print("==========================================================")
    
    # 1. Run multi-model evaluation & chart generation
    generate_evaluation_visualizations()
    
    # 2. Run in-depth 10-question RAG diagnostic
    run_rag_pipeline_deep_analysis()
    
    print("==========================================================")
    print("ALL EVALUATIONS AND CHARTS GENERATED SUCCESSFULLY!")
    print("==========================================================")

if __name__ == "__main__":
    run_all()
