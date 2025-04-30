from __future__ import annotations

import logging
import os
from typing import Any

from langchain_community.llms.ollama import Ollama


class LanguageModel:
    def __init__(self, model_name: str, generation_config: dict[str, Any] | None) -> None:
        if generation_config is None:
            generation_config = {}
        self.model_name = model_name
        self.generation_config = generation_config
        self.base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.llm = None

    def load(self) -> None:
        try:
            self.llm = Ollama(
                model=self.model_name,
                base_url=self.base_url,
                temperature=self.generation_config.get("temperature", 0.8),
                num_predict=self.generation_config.get("max_new_tokens", 128),
            )
        except Exception as e:
            logging.error("Error loading model via Ollama: %s", e)
            raise

    def inference(self, prompt: str) -> str:
        try:
            return self.llm.invoke(prompt)  # type: ignore[no-any-return,attr-defined]
        except Exception as e:
            return f"Error: {e!s}"
