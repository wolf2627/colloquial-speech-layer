"""
Configuration loader for the API.
Loads environment variables from .env file.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file from the api directory
env_path = Path(__file__).parent / ".env"
load_dotenv(env_path)


class Config:
    """Application configuration loaded from environment variables."""
    
    # API Keys
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    
    # Server Settings
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # Model Defaults
    DEFAULT_MODEL: str = os.getenv("DEFAULT_MODEL", "openai/gpt-oss-120b")
    DEFAULT_TEMPERATURE: float = float(os.getenv("DEFAULT_TEMPERATURE", "1"))
    DEFAULT_MAX_TOKENS: int = int(os.getenv("DEFAULT_MAX_TOKENS", "8192"))
    
    # Paths
    BASE_DIR: Path = Path(__file__).parent
    SRC_DIR: Path = BASE_DIR / "src"
    PROMPTS_DIR: Path = BASE_DIR / "prompts"


config = Config()
