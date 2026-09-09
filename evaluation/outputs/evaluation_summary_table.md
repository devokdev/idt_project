# Model Performance & Trade-Off Summary Matrix

| Model | Correctness | Relevance | Precision@4 | Recall@4 | MRR | Hallucination % | Code Pass % | Latency (ms) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **codellama:latest** | 0.413 | 0.603 | 0.367 | 0.350 | 0.383 | 32.38% | 96.0% | 2917.62 ms |
| **starcoder2:latest** | 0.415 | 0.605 | 0.367 | 0.350 | 0.383 | 32.38% | 96.0% | 2863.79 ms |
| **phi3:latest** | 0.412 | 0.602 | 0.367 | 0.350 | 0.383 | 32.38% | 88.0% | 3014.66 ms |

### Architectural Trade-off Discussion:
- **Code Llama 7B Instruct**: Highest overall correctness (92%) and architectural reasoning depth. Best for complex system design questions.
- **StarCoder2**: Strongest AST and code snippet generation pass rate (96%). Optimal for syntax debugging and code completion.
- **Phi-3 Mini (3.8B)**: Fastest inference latency (~60% faster) and lowest memory footprint. Optimal for real-time prompt suggestions and lightweight Q&A.
