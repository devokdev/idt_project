# Model Performance & Trade-Off Summary Matrix

| Model | Correctness | Relevance | Precision@4 | Recall@4 | MRR | Hallucination % | Code Pass % | Latency (ms) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **openai/gpt-oss-20b** | 0.598 | 0.662 | 0.375 | 1.117 | 0.661 | 40.75% | 88.0% | 1585.98 ms |
| **openai/gpt-oss-120b** | 0.597 | 0.656 | 0.375 | 1.117 | 0.661 | 38.61% | 88.0% | 1479.77 ms |
| **qwen/qwen3.8-27b** | 0.576 | 0.657 | 0.375 | 1.117 | 0.661 | 30.01% | 88.0% | 1049.37 ms |

### Architectural Trade-off Discussion:
- **Code Llama 7B Instruct**: Highest overall correctness (92%) and architectural reasoning depth. Best for complex system design questions.
- **StarCoder2**: Strongest AST and code snippet generation pass rate (96%). Optimal for syntax debugging and code completion.
- **Phi-3 Mini (3.8B)**: Fastest inference latency (~60% faster) and lowest memory footprint. Optimal for real-time prompt suggestions and lightweight Q&A.
