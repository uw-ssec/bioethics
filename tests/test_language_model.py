import logging
from core.generator.language_model import LanguageModel

# Set logging level
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def test_language_model() -> None:
    logging.info("🚀 Starting LanguageModel Debugging...")

    model_name = "llama3.2"

    # Initialize model
    try:
        logging.info("🟡 Initializing LanguageModel...")
        model = LanguageModel(
            model_name=model_name,
            generation_config={"max_new_tokens": 512, "temperature": 0.7}
        )
        logging.info("✅ LanguageModel initialized successfully.")
    except Exception as e:
        logging.error(f"❌ Error initializing LanguageModel: {e}")
        return

    # Load model with quantization
    try:
        logging.info("🟡 Loading language model...")
        model.load()
        logging.info("✅ Model loaded successfully.")
    except Exception as e:
        logging.error(f"❌ Error loading model: {e}")
        return

    # Run inference test
    prompt = "Tell me a fun fact about space."
    try:
        logging.info(f"🟡 Running inference on prompt: {prompt}")
        response = model.inference(prompt)
        logging.info(f"✅ Inference completed successfully.\nResponse: {response}")
    except Exception as e:
        logging.error(f"❌ Error during inference: {e}")
        return

if __name__ == "__main__":
    test_language_model()
