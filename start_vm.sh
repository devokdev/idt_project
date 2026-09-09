#!/usr/bin/env bash
# ==============================================================================
# AI Project Mentor - Ultra Zero-Effort 1-Liner VM Setup
# ==============================================================================
set -e

echo "🚀 Setting up AI Project Mentor on VM..."

# 1. Install Docker if missing
if ! command -v docker &> /dev/null; then
    echo "Installing Docker..."
    curl -fsSL https://get.docker.com | sh
    sudo usermod -aG docker $USER || true
fi

# 2. Start Containers (Ollama + FastAPI + Web UI)
echo "🐳 Starting Containers..."
sudo docker compose -f docker/docker-compose.yml up -d --build

# 3. Pull lightweight model in container
echo "🧠 Loading AI Model (phi3:mini)..."
sleep 5
sudo docker exec mentor_ollama ollama pull phi3:mini

# 4. Ingest knowledge base
echo "📚 Ingesting Knowledge Base into ChromaDB..."
sudo docker exec mentor_backend python scripts/ingest_knowledge_base.py

# 5. Done!
HOST_IP=$(hostname -I 2>/dev/null | awk '{print $1}' || echo "localhost")
echo ""
echo "=========================================================="
echo "✅ READY! Open this in your laptop browser:"
echo "👉 http://${HOST_IP}:8000/ui"
echo "=========================================================="
