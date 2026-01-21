# Adding New Models

This guide explains how to add a new AI model handler to the API.

## Quick Steps

1. Create handler file: `/api/src/your_model.py`
2. Create prompt folder: `/api/prompts/your_model/`
3. Add prompts: `system.txt` and `user.txt`
4. Update `.env` with any required API keys
5. Restart server → endpoint auto-created at `/api/your_model`

---

## Step 1: Create Handler File

Create a new file in `/api/src/` named after your endpoint.

**File**: `/api/src/your_model.py`

```python
"""
Your Model Handler.
Implements chat completion using Your API.
"""

from typing import Any
import sys
sys.path.append(str(__file__).rsplit('\\', 2)[0])

from config import config
from src.base_model import BaseModel

# Import your API client
from your_api import YourClient


class YourModelHandler(BaseModel):
    """Handler for Your API."""
    
    def __init__(self):
        super().__init__()
        # Initialize your client with API key from config
        self.client = YourClient(api_key=config.YOUR_API_KEY)
    
    def process(
        self,
        user_input: str,
        model: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
        stream: bool = False,
        **kwargs: Any
    ) -> str:
        """Process input and return model response."""
        
        # Load prompts (provided by BaseModel)
        system_prompt = self.load_system_prompt()
        user_prompt = self.load_user_prompt(user_input)
        
        # Apply defaults
        model = model or config.DEFAULT_MODEL
        temperature = temperature if temperature is not None else config.DEFAULT_TEMPERATURE
        max_tokens = max_tokens if max_tokens is not None else config.DEFAULT_MAX_TOKENS
        
        # Call your API
        response = self.client.generate(
            model=model,
            system=system_prompt,
            prompt=user_prompt,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        return response.text
```

---

## Step 2: Create Prompts Folder

Create a folder matching your handler name:

```
/api/prompts/your_model/
├── system.txt
└── user.txt
```

---

## Step 3: Write Prompts

**system.txt** - Defines the AI's role/personality:
```
You are a helpful assistant specialized in [your domain].

Your responsibilities:
- [Responsibility 1]
- [Responsibility 2]

Rules:
- [Rule 1]
- [Rule 2]
```

**user.txt** - Template for user messages (use `{input}` placeholder):
```
Please process the following request:

{input}

Provide a clear and helpful response.
```

---

## Step 4: Update Configuration

Add any required API keys to `/api/.env`:

```env
# Existing keys
GROQ_API_KEY=your_groq_key

# New keys for your model
YOUR_API_KEY=your_new_api_key
```

Update `/api/config.py` to load the new key:

```python
class Config:
    # Existing
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    
    # Add new
    YOUR_API_KEY: str = os.getenv("YOUR_API_KEY", "")
```

---

## Step 5: Restart and Test

```bash
# Restart the server
python -m uvicorn main:app --reload

# Test the new endpoint
curl http://localhost:8000/api/models
# Should now include "your_model"

curl -X POST http://localhost:8000/api/your_model \
  -H "Content-Type: application/json" \
  -d '{"input": "Test message"}'
```

---

## Example: Adding OpenAI GPT-4

### 1. Handler (`/api/src/openai_gpt4.py`)
```python
from typing import Any
from openai import OpenAI
import sys
sys.path.append(str(__file__).rsplit('\\', 2)[0])

from config import config
from src.base_model import BaseModel


class OpenAIGPT4Handler(BaseModel):
    def __init__(self):
        super().__init__()
        self.client = OpenAI(api_key=config.OPENAI_API_KEY)
    
    def process(self, user_input: str, model: str | None = None, 
                temperature: float | None = None, max_tokens: int | None = None,
                stream: bool = False, **kwargs: Any) -> str:
        
        system_prompt = self.load_system_prompt()
        user_prompt = self.load_user_prompt(user_input)
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": user_prompt})
        
        response = self.client.chat.completions.create(
            model=model or "gpt-4",
            messages=messages,
            temperature=temperature or 1.0,
            max_tokens=max_tokens or 4096
        )
        
        return response.choices[0].message.content
```

### 2. Prompts
**`/api/prompts/openai_gpt4/system.txt`**:
```
You are a helpful AI assistant powered by GPT-4.
```

**`/api/prompts/openai_gpt4/user.txt`**:
```
{input}
```

### 3. Config
Add to `.env`:
```
OPENAI_API_KEY=sk-your-key-here
```

Add to `config.py`:
```python
OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
```

---

## BaseModel Methods

Your handler inherits these methods from `BaseModel`:

| Method | Description |
|--------|-------------|
| `load_system_prompt()` | Loads `/prompts/{handler}/system.txt` |
| `load_user_prompt(input)` | Loads `/prompts/{handler}/user.txt` and replaces `{input}` |
| `self.name` | Handler name (filename without .py) |
| `self.prompts_dir` | Path to prompts folder |

---

## Naming Conventions

| Item | Convention | Example |
|------|------------|---------|
| Handler file | `snake_case.py` | `groq_compound.py` |
| Handler class | `PascalCaseHandler` | `GroqCompoundHandler` |
| Prompts folder | Same as file | `groq_compound/` |
| Endpoint | Same as file | `/api/groq_compound` |
