from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.generation_service import generate_answer
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

class GenerationRequest(BaseModel):
    prompt: str
    generation_model: str

@router.post("/generate/")
async def generate(request: GenerationRequest):
    try:
        logger.info(f"Generation request for model: {request.generation_model}")
        result = generate_answer(request.prompt, request.generation_model)
        
        if result.get("status_code") != 200:
            logger.error(f"Generation error: {result.get('error', 'Unknown error')}")
            raise HTTPException(status_code=result.get("status_code", 500), 
                              detail=result.get("error", "Unknown generation error"))
        
        return result
    except Exception as e:
        logger.error(f"Unhandled exception in generate endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")