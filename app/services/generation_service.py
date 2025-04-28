import logging
import traceback
from core.generator.language_model import LanguageModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global model instance (lazy-loaded)
MODEL_INSTANCES = {}

def get_model(generation_model):
    """
    Retrieve or create a cached instance of the language model.
    """
    try:
        if generation_model not in MODEL_INSTANCES:
            logger.info(f"Initializing model: {generation_model}")
            MODEL_INSTANCES[generation_model] = LanguageModel(model_name=generation_model, generation_config={"max_new_tokens": 1024})
            MODEL_INSTANCES[generation_model].load_language_model()
            # MODEL_INSTANCES[generation_model].load_language_model(quantization="8bit")
            MODEL_INSTANCES[generation_model].load_hg_pipeline()
            logger.info(f"Model initialized successfully: {generation_model}")
        return MODEL_INSTANCES[generation_model]
    except Exception as e:
        logger.error(f"Error initializing model {generation_model}: {str(e)}")
        logger.error(traceback.format_exc())
        raise Exception(f"Failed to initialize model: {str(e)}")

def generate_answer(prompt, generation_model):
    try:
        logger.info(f"Generating answer with model: {generation_model}")
        model = get_model(generation_model)
        
        if not model.hg_pipeline:
            logger.error("HuggingFace pipeline not initialized properly")
            return {"answer": "Model initialization failed", "error": "Pipeline not available", "status_code": 500}
        
        response = model.inference(prompt)
        logger.info("Successfully generated response")
        return {"answer": response, "status_code": 200}
    except Exception as e:
        logger.error(f"Error generating answer: {str(e)}")
        logger.error(traceback.format_exc())
        return {"answer": "Failed to generate response", "error": str(e), "status_code": 500}
