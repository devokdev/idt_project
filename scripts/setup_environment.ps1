# PowerShell Environment Setup Script for AI Project Mentor (Windows)
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "Setting up AI Project Mentor Environment (Python 3.11)" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

if (-Not (Test-Path "venv")) {
    Write-Host "Creating Python virtual environment 'venv'..." -ForegroundColor Yellow
    python -m venv venv
}

Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

Write-Host "Installing requirements..." -ForegroundColor Yellow
pip install --upgrade pip
pip install -r requirements.txt

Write-Host "Ingesting Knowledge Base documents into ChromaDB..." -ForegroundColor Yellow
python scripts\ingest_knowledge_base.py

Write-Host "==========================================================" -ForegroundColor Green
Write-Host "Setup Completed Successfully!" -ForegroundColor Green
Write-Host "Start server with: uvicorn backend.app.main:app --reload --port 8000" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Green
