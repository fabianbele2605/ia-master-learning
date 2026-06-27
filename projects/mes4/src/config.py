"""
Configuration - Mes 4

Variables de configuración centralizadas
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ============ LLM CONFIG ============

# Ollama (local)
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen3:8b")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# OpenAI (opcional)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

# ============ AGENT CONFIG ============

# Temperature (0 = determinístico, 1 = creativo)
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))

# Max iterations (prevenir loops infinitos)
MAX_ITERATIONS = int(os.getenv("MAX_ITERATIONS", "10"))

# ============ LOGGING ============

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# ============ ENVIRONMENT ============

ENV = os.getenv("ENV", "development")
DEBUG = ENV == "development"
