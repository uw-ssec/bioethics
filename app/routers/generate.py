from __future__ import annotations

from app.services.generation_service import generate_answer
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()


class GenerationRequest(BaseModel):
    prompt: str
    generation_model: str


@router.post("/generate/")
async def generate(request: GenerationRequest):
    try:
        result = generate_answer(request.prompt, request.generation_model)

        if result.get("status_code") != 200:
            raise HTTPException(
                status_code=result.get("status_code", 500),
                detail=result.get("error", "Unknown generation error"),
            )

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {e!s}") from e
