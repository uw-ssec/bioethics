from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.retrieval_service import DocumentDict, perform_retrieval

router = APIRouter()


class RetrieveRequest(BaseModel):  # type: ignore[misc]
    documents: list[DocumentDict] | None = []
    query: str
    existing_collection: str | None = None
    existing_qdrant_path: str | None = None
    embedding_model: str


class RetrievalResponse(BaseModel):  # type: ignore[misc]
    docs: list[dict[str, Any]]
    status_code: int = 200


@router.post("/retrieve/", response_model=RetrievalResponse)  # type: ignore[misc]
async def retrieve(request: RetrieveRequest) -> RetrievalResponse:
    try:
        result = perform_retrieval(
            request.documents,
            request.query,
            request.existing_collection,
            request.existing_qdrant_path,
            request.embedding_model,
        )

        return RetrievalResponse(docs=result.get("results", []), status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
