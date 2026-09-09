#!/usr/bin/env bash
# ==============================================================================
# AI Project Mentor - Ultra-Lightweight Native VM Setup (< 1.5 GB disk)
# Avoids Docker overhead entirely for low-storage VMs (~10 GB total disk).
# ==============================================================================
set -e

echo "=========================================================="
echo "⚡ Setting up AI Project Mentor (Lightweight Native Mode)..."
echo "=========================================================="

# 1. Install minimal Python environment (if missing)
if ! command -v python3 &> /dev/null || ! python3 -m venv --help &> /dev/null; then
    echo "📦 Installing minimal Python packages..."
    sudo apt-get update -y
    sudo apt-get install -y python3 python3-pip python3-venv curl
fi

# 2. Setup Python virtual environment (lightweight, ~400 MB)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if [ ! -d "venv" ]; then
    echo "🐍 Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate

echo "📦 Installing Python dependencies with no cache..."
pip install --no-cache-dir -r requirements.txt

# 3. Ingest knowledge base into ChromaDB (~10 MB)
echo "📚 Ingesting knowledge base documents into ChromaDB..."
python scripts/ingest_knowledge_base.py

# 4. Launch backend server in the background
echo "🚀 Starting FastAPI server on port 8000..."
pkill -f "uvicorn backend.app.main:app" || true
nohup python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 > server.log 2>&1 &

HOST_IP=$(hostname -I 2>/dev/null | awk '{print $1}' || echo "localhost")
sleep 2

echo ""
echo "=========================================================="
echo "🎉 SUCCESS! Server is running in the background."
echo "💾 Disk used by this setup: < 1.2 GB"
echo ""
echo "👉 Web Dashboard UI:  http://${HOST_IP}:8000/ui"
echo "👉 Interactive API:   http://${HOST_IP}:8000/docs"
echo "👉 Logs:              tail -f server.log"
echo "=========================================================="
