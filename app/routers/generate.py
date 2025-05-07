from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.generation_service import generate_answer

router = APIRouter()


class GenerationRequest(BaseModel):  # type: ignore[misc]
    prompt: str
    generation_model: str


class GenerationResponse(BaseModel):  # type: ignore[misc]
    answer: str
    status_code: int


@router.post("/generate/", response_model=GenerationResponse)  # type: ignore[misc]
async def generate(request: GenerationRequest) -> GenerationResponse:
    try:
        result = generate_answer(request.prompt, request.generation_model)

        if result.get("status_code") != 200:
            raise HTTPException(
                status_code=result.get("status_code", 500),
                detail=result.get("error", "Unknown generation error"),
            )

        return GenerationResponse(
            answer=result.get("answer", ""), status_code=result.get("status_code", 200)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {e!s}") from e
