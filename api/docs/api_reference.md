# API Reference

## Base URL
```
http://localhost:8000
```

---

## Endpoints

### Health Check

#### `GET /`
Check if the API is running.

**Response:**
```json
{
  "status": "ok",
  "message": "API is running"
}
```

#### `GET /health`
Alias for health check.

**Response:**
```json
{
  "status": "healthy"
}
```

---

### Models

#### `GET /api/models`
List all available model endpoints.

**Response:**
```json
{
  "models": ["groq_compound", "gemini_3_flash"],
  "count": 2
}
```

---

### Process Request

#### `POST /api/{endpoint}`
Send input to a specific model handler.

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `endpoint` | string | Handler name (e.g., `groq_compound`) |

**Request Body:**
```json
{
  "input": "Your text here",
  "model": "openai/gpt-oss-120b",
  "temperature": 1.0,
  "max_tokens": 8192,
  "stream": false
}
```

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `input` | string | Yes | - | User input text |
| `model` | string | No | From config | Model identifier |
| `temperature` | float | No | 1.0 | Sampling temperature (0-2) |
| `max_tokens` | int | No | 8192 | Maximum tokens in response |
| `stream` | bool | No | false | Enable streaming (collected) |

**Success Response:**
```json
{
  "output": "Model response text...",
  "model": "openai/gpt-oss-120b",
  "endpoint": "groq_compound"
}
```

**Error Responses:**

*404 - Endpoint Not Found:*
```json
{
  "detail": "Endpoint 'unknown' not found. Available: ['groq_compound']"
}
```

*500 - Processing Error:*
```json
{
  "detail": "Error message from handler"
}
```

---

## Examples

### cURL

```bash
# Health check
curl http://localhost:8000/

# List models
curl http://localhost:8000/api/models

# Process request
curl -X POST http://localhost:8000/api/groq_compound \
  -H "Content-Type: application/json" \
  -d '{
    "input": "Your blood sugar is high",
    "temperature": 1.0,
    "max_tokens": 1000
  }'
```

### Python

```python
import requests

# Process request
response = requests.post(
    "http://localhost:8000/api/groq_compound",
    json={
        "input": "Your blood sugar is high",
        "temperature": 1.0,
        "max_tokens": 1000
    }
)
data = response.json()
print(data["output"])
```

### JavaScript

```javascript
const response = await fetch('http://localhost:8000/api/groq_compound', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        input: 'Your blood sugar is high',
        temperature: 1.0,
        max_tokens: 1000
    })
});
const data = await response.json();
console.log(data.output);
```

---

## OpenAPI / Swagger

FastAPI automatically generates OpenAPI documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json
