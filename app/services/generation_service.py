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
                model_name=generation_model, generation_config={"max_new_tokens": 1024}
            )  # type: ignore[no-untyped-call]
            # TODO: https://github.com/uw-ssec/bioethics/issues/5
            MODEL_INSTANCES[generation_model].load_language_model()
            MODEL_INSTANCES[generation_model].load_hg_pipeline()  # type: ignore[no-untyped-call]
        return MODEL_INSTANCES[generation_model]
    except Exception as e:
        error_message = f"Failed to initialize model: {e!s}"
        raise Exception(error_message) from e


def generate_answer(prompt: str, generation_model: str) -> dict[str, Any]:
    try:
        model = get_model(generation_model)

        if not model.hg_pipeline:
            logger.error("HuggingFace pipeline not initialized properly")
            return {
                "answer": "Model initialization failed",
                "error": "Pipeline not available",
                "status_code": 500,
            }

        response = model.inference(prompt)  # type: ignore[no-untyped-call]
        logger.info("Successfully generated response")
        return {"answer": response, "status_code": 200}
    except Exception as e:
        return {"answer": "Failed to generate response", "error": str(e), "status_code": 500}
