from __future__ import annotations

import logging
from typing import Any

from core.generator.language_model import LanguageModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global model instance (lazy-loaded)
MODEL_INSTANCES: dict[str, LanguageModel] = {}


def get_model(generation_model: str) -> LanguageModel:
    """
    Retrieve or create a cached instance of the language model.
    """
    try:
        if generation_model not in MODEL_INSTANCES:
            MODEL_INSTANCES[generation_model] = LanguageModel(
                model_name=generation_model,
                generation_config={"max_new_tokens": 1024, "temperature": 0.8},
            )
            MODEL_INSTANCES[generation_model].load()
        return MODEL_INSTANCES[generation_model]
    except Exception as e:
        error_message = f"Failed to initialize model: {e!s}"
        raise Exception(error_message) from e


def generate_answer(prompt: str, generation_model: str) -> dict[str, Any]:
    try:
        model = get_model(generation_model)
        response = model.inference(prompt)

        return {"answer": response, "status_code": 200}
    except Exception as e:
        return {"answer": "Failed to generate response", "error": str(e), "status_code": 500}
