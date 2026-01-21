"""
Gemini 3 Flash Handler.
Simple function that processes input using Google Gemini API.
"""

from google import genai
from google.genai import types
from pathlib import Path

import sys
sys.path.append(str(Path(__file__).parent.parent))

from config import config

# Hardcoded model for this handler
MODEL = "gemini-3-flash-preview"

# Paths
PROMPTS_DIR = Path(__file__).parent.parent / "prompts" / "gemini_3_flash"


def process(user_input: str, **kwargs) -> str:
    """
    Process input using Gemini API.
    """
    # Load system prompt
    system_file = PROMPTS_DIR / "system.txt"
    system_prompt = system_file.read_text(encoding="utf-8").strip() if system_file.exists() else None
    
    # Load user prompt template and format with input
    user_file = PROMPTS_DIR / "user.txt"
    if user_file.exists():
        user_template = user_file.read_text(encoding="utf-8").strip()
        user_prompt = user_template.replace("{input}", user_input)
    else:
        user_prompt = user_input
    
    # Call API
    client = genai.Client(api_key=config.GEMINI_API_KEY)
    
    response = client.models.generate_content(
        model=MODEL,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
        ),
        contents=user_prompt
    )
    
    return response.text
