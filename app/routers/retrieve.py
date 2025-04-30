from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.retrieval_service import perform_retrieval

router = APIRouter()


class RetrieveRequest(BaseModel):  # type: ignore[misc]
    documents: list[dict[str, Any]] | None = []
    query: str
    existing_collection: str | None = None
    existing_qdrant_path: str | None = None
    embedding_model: str


class RetrievalResponse(BaseModel):  # type: ignore[misc]
    results: list[dict[str, Any]]
    status: str = "success"


@router.post("/retrieve/", response_model=RetrievalResponse)  # type: ignore[misc]
async def retrieve(request: RetrieveRequest) -> RetrievalResponse:
    try:
        results = perform_retrieval(  # type: ignore[no-untyped-call]
            request.documents,
            request.query,
            request.existing_collection,
            request.existing_qdrant_path,
            request.embedding_model,
        )
        return RetrievalResponse(results=results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
