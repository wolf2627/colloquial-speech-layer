# Configuration Guide

## Environment Variables

All configuration is done via the `.env` file in the `/api` directory.

### File: `/api/.env`

```env
# API Keys
GROQ_API_KEY=your_groq_api_key_here

# Server Configuration
HOST=0.0.0.0
PORT=8000

# Default Model Settings
DEFAULT_MODEL=openai/gpt-oss-120b
DEFAULT_TEMPERATURE=1
DEFAULT_MAX_TOKENS=8192
```

---

## Configuration Options

### API Keys

| Variable | Description | Required |
|----------|-------------|----------|
| `GROQ_API_KEY` | Groq API authentication key | Yes (for groq_compound) |

### Server Settings

| Variable | Default | Description |
|----------|---------|-------------|
| `HOST` | `0.0.0.0` | Server bind address |
| `PORT` | `8000` | Server port |

### Model Defaults

| Variable | Default | Description |
|----------|---------|-------------|
| `DEFAULT_MODEL` | `openai/gpt-oss-120b` | Default model if not specified in request |
| `DEFAULT_TEMPERATURE` | `1` | Default sampling temperature (0-2) |
| `DEFAULT_MAX_TOKENS` | `8192` | Default max tokens in response |

---

## Config Class

The `/api/config.py` file loads these variables:

```python
class Config:
    # API Keys
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    
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
```

---

## Usage in Handlers

Access config values in your handlers:

```python
from config import config

# Use API key
client = Groq(api_key=config.GROQ_API_KEY)

# Use defaults
model = model or config.DEFAULT_MODEL
temperature = temperature if temperature is not None else config.DEFAULT_TEMPERATURE
```

---

## Adding New Configuration

1. Add variable to `.env`:
   ```env
   NEW_API_KEY=your_key
   ```

2. Add to `config.py`:
   ```python
   class Config:
       NEW_API_KEY: str = os.getenv("NEW_API_KEY", "")
   ```

3. Use in handler:
   ```python
   from config import config
   client = NewClient(api_key=config.NEW_API_KEY)
   ```

---

## Security Notes

- **Never commit `.env` to version control**
- Use `.env.example` as a template (included in repo)
- The `.gitignore` already excludes `.env`
