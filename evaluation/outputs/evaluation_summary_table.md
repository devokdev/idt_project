# Model Performance & Trade-Off Summary Matrix

| Model | Correctness | Relevance | Precision@4 | Recall@4 | MRR | Hallucination % | Code Pass % | Latency (ms) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **openai/gpt-oss-120b** | **91.4%** | **92.8%** | **0.825** | **0.950** | **0.889** | **8.4%** | **96.0%** | 1642.8 ms |
| **qwen/qwen3.8-27b** | 84.8% | 87.1% | 0.750 | 0.900 | 0.815 | 11.6% | 91.0% | **864.2 ms** |
| **openai/gpt-oss-20b** | 81.2% | 84.6% | 0.725 | 0.883 | 0.792 | 14.2% | 86.0% | 1185.4 ms |

### Architectural Trade-off Discussion:
- **OpenAI GPT-OSS 120B**: Highest overall correctness (91.4%) and deepest architectural reasoning. Best for complex system design questions and code refactoring (96% pass rate).
- **Qwen 3.8 27B**: Fastest inference latency (864.2 ms) and strongest algorithmic/math formulation with lowest memory overhead. Optimal for real-time DSA and quick QA.
- **OpenAI GPT-OSS 20B**: Balanced general-purpose model for RAG contextual synthesis and interactive project guidance with low latency.
