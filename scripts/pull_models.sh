#!/usr/bin/env bash
# Ollama Model Pull & Verification Script (Linux/macOS)

echo "=========================================================="
echo "Pulling Required LLM Models via Ollama"
echo "=========================================================="

# Check if Ollama is running
curl -s http://localhost:11434/api/tags > /dev/null || {
    echo "Warning: Ollama is not running on port 11434."
    echo "Start Ollama with: ollama serve &"
}

echo "Pulling Code Llama (codellama:latest)..."
ollama pull codellama:latest

echo "Pulling StarCoder2 (starcoder2:latest)..."
ollama pull starcoder2:latest

echo "Pulling Phi-3 Mini (phi3:latest)..."
ollama pull phi3:latest

echo "----------------------------------------------------------"
echo "Installed Models in Ollama:"
ollama list
echo "=========================================================="
