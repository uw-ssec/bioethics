from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Literal

from langchain_community.llms import HuggingFacePipeline
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, pipeline


class LanguageModel:
    def __init__(self, model_name, generation_config=None):
        if generation_config is None:
            generation_config = {}
        self.model_name = model_name
        self.generation_config = generation_config or {}

        self.cache_path = Path(__file__).parent.parent.parent / "models"
        self.cache_path.mkdir(exist_ok=True)
        self.model_path = str(self.cache_path / self.model_name.replace("/", "_"))

        self.llm = None
        self.tokenizer = None
        self.hg_pipeline = None

    def load_language_model(self, quantization: Literal["8bit", "4bit", None] = None):
        # Define the quantization config
        if quantization == "8bit":
            quantization_config = BitsAndBytesConfig(load_in_8bit=True)
        elif quantization == "4bit":
            quantization_config = BitsAndBytesConfig(load_in_4bit=True)
        else:
            quantization_config = None

        hf_token = os.getenv("HF_TOKEN")

        # Load tokenizer
        tokenizer = AutoTokenizer.from_pretrained(
            self.model_name, cache_dir=self.model_path, token=hf_token
        )

        # Load model with quantization
        model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            cache_dir=self.model_path,
            device_map="auto",
            quantization_config=quantization_config,
            token=hf_token,
        )
        self.llm = model
        self.tokenizer = tokenizer

    def load_hg_pipeline(self):
        if self.llm and self.tokenizer:
            pipe = pipeline(
                "text-generation",
                model=self.llm,
                tokenizer=self.tokenizer,
                max_new_tokens=self.generation_config.get("max_new_tokens", 512),
                temperature=self.generation_config.get("temperature", 0.8),
                do_sample=self.generation_config.get("do_sample", True),
                return_full_text=self.generation_config.get("return_full_text", False),
            )
            self.hg_pipeline = HuggingFacePipeline(pipeline=pipe)
        else:
            logging.error("Model and tokenizer not loaded. Cannot create pipeline.")
            return

    def inference(self, prompt):
        if self.hg_pipeline:
            return self.hg_pipeline.invoke(prompt)
        logging.info("Model and tokenizer not loaded. Cannot create pipeline.")
        return None
