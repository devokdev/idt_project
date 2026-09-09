import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from backend.app.config import settings, BASE_DIR
from backend.app.routers import chat, retrieve, models, health, repo, evaluate
from services.retrieval_service import retrieval_service

logger = logging.getLogger("main_app")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup sequence
    logger.info(f"Starting {settings.PROJECT_NAME} v{settings.VERSION}")
    stats = retrieval_service.get_stats()
    logger.info(f"Vector Database connected: {stats['default_collection_count']} documents indexed.")
    yield
    # Shutdown sequence
    logger.info("Application shutting down.")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Production-grade AI Project Mentor for final-year engineering students with RAG and Multi-Model Evaluation.",
    lifespan=lifespan
)

# Enable CORS for all frontend clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers
app.include_router(chat.router)
app.include_router(retrieve.router)
app.include_router(models.router)
app.include_router(health.router)
app.include_router(repo.router)
app.include_router(evaluate.router)

# Mount frontend static directory if exists
frontend_path = BASE_DIR / "frontend"
if frontend_path.exists():
    app.mount("/ui", StaticFiles(directory=str(frontend_path), html=True), name="frontend")

@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.PROJECT_NAME}",
        "version": settings.VERSION,
        "docs_url": "/docs",
        "ui_url": "/ui"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host=settings.HOST, port=settings.PORT, reload=True)
