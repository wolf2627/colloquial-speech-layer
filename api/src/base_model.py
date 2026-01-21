"""
Base Model Class.
Abstract base class that all model handlers must extend.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class BaseModel(ABC):
    """
    Abstract base class for all model handlers.
    
    Each handler should:
    1. Extend this class
    2. Implement the process() method
    3. Have corresponding prompts in /prompts/{module_name}/
    """
    
    def __init__(self):
        self.name = self.__class__.__module__.split('.')[-1]
        self.prompts_dir = Path(__file__).parent.parent / "prompts" / self.name
    
    def load_system_prompt(self) -> str:
        """Load the system prompt from prompts/{module_name}/system.txt"""
        system_file = self.prompts_dir / "system.txt"
        if system_file.exists():
            return system_file.read_text(encoding="utf-8").strip()
        return ""
    
    def load_user_prompt(self, user_input: str) -> str:
        """
        Load and format the user prompt from prompts/{module_name}/user.txt
        Replaces {input} placeholder with the actual user input.
        """
        user_file = self.prompts_dir / "user.txt"
        if user_file.exists():
            template = user_file.read_text(encoding="utf-8").strip()
            return template.replace("{input}", user_input)
        return user_input
    
    @abstractmethod
    def process(
        self,
        user_input: str,
        model: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
        stream: bool = False,
        **kwargs: Any
    ) -> str:
        """
        Process the user input and return the model response.
        
        Args:
            user_input: The user's input text
            model: Optional model override
            temperature: Optional temperature override
            max_tokens: Optional max tokens override
            stream: Whether to stream the response
            **kwargs: Additional model-specific parameters
            
        Returns:
            The model's response as a string
        """
        pass
