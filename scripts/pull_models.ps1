# Ollama Model Pull Script (Windows PowerShell)
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "Pulling Required LLM Models via Ollama" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

try {
    Write-Host "Pulling Code Llama..." -ForegroundColor Yellow
    ollama pull codellama:latest

    Write-Host "Pulling StarCoder2..." -ForegroundColor Yellow
    ollama pull starcoder2:latest

    Write-Host "Pulling Phi-3 Mini..." -ForegroundColor Yellow
    ollama pull phi3:latest

    Write-Host "Available Models:" -ForegroundColor Green
    ollama list
} catch {
    Write-Host "Ollama command error. Ensure Ollama for Windows is installed and running." -ForegroundColor Red
}
