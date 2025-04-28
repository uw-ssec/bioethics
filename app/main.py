from __future__ import annotations

from app.routers import generate, retrieve
from fastapi import FastAPI

app = FastAPI(title="RAG Application")

app.include_router(retrieve.router, prefix="/api")
app.include_router(generate.router, prefix="/api")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
