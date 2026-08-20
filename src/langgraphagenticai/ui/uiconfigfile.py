from configparser import ConfigParser
from pathlib import Path


class Config:
    def __init__(self, config_file=None):
        if config_file is None:
            config_file = Path(__file__).with_name("uiconfigfile.ini")

        self.config = ConfigParser()
        self.config.read(config_file, encoding="utf-8")

    def _get_default(self, key, default=""):
        return self.config["DEFAULT"].get(key, default)

    def get_llm_options(self):
        value = self._get_default("LLM_OPTIONS", "")
        return [item.strip() for item in value.split(",") if item.strip()] if value else []

    def get_usecase_options(self):
        value = self._get_default("USECASE_OPTIONS", "")
        return [item.strip() for item in value.split(",") if item.strip()] if value else []

    def get_groq_model_options(self):
        value = self._get_default("GROQ_MODEL_OPTIONS", "")
        return [item.strip() for item in value.split(",") if item.strip()] if value else []

    def get_page_title(self):
        return self._get_default("PAGE_TITLE", "LangGraph Agentic AI")