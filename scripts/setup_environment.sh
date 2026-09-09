# Python Environment Setup Script for AI Project Mentor (Linux / macOS)
set -e

echo "=========================================================="
echo "Setting up AI Project Mentor Environment (Python 3.11)"
echo "=========================================================="

# Check Python version
python3 --version || { echo "Python 3 is required."; exit 1; }

# Create virtual environment if not existing
if [ ! -d "venv" ]; then
    echo "Creating virtual environment 'venv'..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Upgrade pip and install dependencies
echo "Installing dependencies from requirements.txt..."
pip install --upgrade pip
pip install -r requirements.txt

# Ingest initial knowledge base into ChromaDB
echo "Ingesting Knowledge Base documents into ChromaDB..."
python scripts/ingest_knowledge_base.py

echo "=========================================================="
echo "Environment setup complete! To start the FastAPI server:"
echo "source venv/bin/activate && uvicorn backend.app.main:app --reload --port 8000"
echo "=========================================================="
