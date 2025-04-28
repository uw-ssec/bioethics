from __future__ import annotations

from typing import Any

from app.services.retrieval_service import perform_retrieval
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()


class RetrieveRequest(BaseModel):
    documents: list[dict[str, Any]] | None = []
    query: str
    existing_collection: str | None = None
    existing_qdrant_path: str | None = None
    embedding_model: str


@router.post("/retrieve/")
async def retrieve(request: RetrieveRequest):
    try:
        return perform_retrieval(
            request.documents,
            request.query,
            request.existing_collection,
            request.existing_qdrant_path,
            request.embedding_model,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
