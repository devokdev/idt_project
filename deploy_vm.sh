#!/usr/bin/env bash
# ==============================================================================
# AI Project Mentor - Automated 1-Click VM Deployment Script
# Target OS: Ubuntu 24.04 / 25.04 (LinuxLab)
# ==============================================================================

set -e

echo "=========================================================="
echo "🚀 [1/5] Updating packages & Installing Docker on Ubuntu..."
echo "=========================================================="
sudo apt-get update -y
sudo apt-get install -y ca-certificates curl gnupg lsb-release git

# Install Docker and Docker Compose plugin if not present
if ! command -v docker &> /dev/null; then
    echo "Installing Docker Engine..."
    sudo apt-get install -y docker.io docker-compose-v2
    sudo systemctl enable --now docker
    sudo usermod -aG docker $USER || true
else
    echo "✅ Docker is already installed."
fi

echo "=========================================================="
echo "📂 [2/5] Navigating to Project Directory..."
echo "=========================================================="
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================================="
echo "🐳 [3/5] Starting Docker Containers (Backend + Ollama)..."
echo "=========================================================="
sudo docker compose -f docker/docker-compose.yml down --remove-orphans || true
sudo docker compose -f docker/docker-compose.yml up -d --build

echo "=========================================================="
echo "🧠 [4/5] Downloading Neural Model (phi3:mini) in Ollama..."
echo "=========================================================="
echo "Waiting 5 seconds for Ollama daemon to initialize..."
sleep 5
sudo docker exec mentor_ollama ollama pull phi3:mini

echo "=========================================================="
echo "🌐 [5/5] Re-indexing Vector Database in Container..."
echo "=========================================================="
sudo docker exec mentor_backend python scripts/ingest_knowledge_base.py

# Get VM IP address
HOST_IP=$(hostname -I | awk '{print $1}')

echo ""
echo "=========================================================="
echo "🎉 SUCCESS! AI Project Mentor is Live on your Ubuntu VM!"
echo "=========================================================="
echo "👉 Web Dashboard UI:  http://${HOST_IP}:8000/ui"
echo "👉 Interactive API:   http://${HOST_IP}:8000/docs"
echo "👉 Health Status:     http://${HOST_IP}:8000/health"
echo "=========================================================="
