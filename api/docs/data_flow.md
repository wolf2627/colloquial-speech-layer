# Data Flow Guide

This document explains how data travels from the frontend through the API to the model handler.

## Complete Request Flow

```
USER INPUT
    │
    ▼
┌──────────────────────────────────────────────────────────────┐
│  STEP 1: Frontend (app.js)                                   │
│  ──────────────────────────────────────────────────────────  │
│                                                              │
│  User fills form:                                            │
│    - Selects model: "groq_compound"                          │
│    - Enters input: "Your blood sugar is high"                │
│    - Sets temperature: 1.0                                   │
│    - Sets max_tokens: 8192                                   │
│                                                              │
│  app.js builds request:                                      │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ fetch('http://localhost:8000/api/groq_compound', {     │  │
│  │   method: 'POST',                                      │  │
│  │   headers: { 'Content-Type': 'application/json' },     │  │
│  │   body: JSON.stringify({                               │  │
│  │     input: "Your blood sugar is high",                 │  │
│  │     temperature: 1.0,                                  │  │
│  │     max_tokens: 8192,                                  │  │
│  │     stream: false                                      │  │
│  │   })                                                   │  │
│  │ })                                                     │  │
│  └────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
    │
    │ HTTP POST
    ▼
┌──────────────────────────────────────────────────────────────┐
│  STEP 2: FastAPI Entry (main.py)                             │
│  ──────────────────────────────────────────────────────────  │
│                                                              │
│  1. Request hits http://localhost:8000/api/groq_compound     │
│  2. CORS middleware allows the request                       │
│  3. Request is routed to /api router                         │
│                                                              │
└──────────────────────────────────────────────────────────────┘
    │
    ▼
┌──────────────────────────────────────────────────────────────┐
│  STEP 3: Dynamic Router (router.py)                          │
│  ──────────────────────────────────────────────────────────  │
│                                                              │
│  @router.post("/{endpoint}")                                 │
│  async def process_request(endpoint: str, payload):          │
│                                                              │
│  1. endpoint = "groq_compound"                               │
│  2. payload = RequestPayload(                                │
│       input="Your blood sugar is high",                      │
│       temperature=1.0,                                       │
│       max_tokens=8192,                                       │
│       stream=False                                           │
│     )                                                        │
│                                                              │
│  3. discover_modules() → scans /src → finds "groq_compound"  │
│  4. get_handler("groq_compound") → loads module              │
│  5. Calls handler.process(...)                               │
│                                                              │
└──────────────────────────────────────────────────────────────┘
    │
    ▼
┌──────────────────────────────────────────────────────────────┐
│  STEP 4: Handler (src/groq_compound.py)                      │
│  ──────────────────────────────────────────────────────────  │
│                                                              │
│  class GroqCompoundHandler(BaseModel):                       │
│                                                              │
│  def process(self, user_input, model, temperature, ...):     │
│                                                              │
│  1. Load system prompt from /prompts/groq_compound/system.txt│
│     → "You are a Tamil-speaking medical assistant..."        │
│                                                              │
│  2. Load user prompt from /prompts/groq_compound/user.txt    │
│     → Template with {input} placeholder                      │
│                                                              │
│  3. Replace {input} with actual user input                   │
│     → "Convert the following... Your blood sugar is high"    │
│                                                              │
│  4. Build messages array:                                    │
│     messages = [                                             │
│       {"role": "system", "content": system_prompt},          │
│       {"role": "user", "content": formatted_user_prompt}     │
│     ]                                                        │
│                                                              │
│  5. Apply defaults (model, temperature, max_tokens)          │
│                                                              │
│  6. Call Groq API:                                           │
│     self.client.chat.completions.create(                     │
│       model=model,                                           │
│       messages=messages,                                     │
│       temperature=temperature,                               │
│       max_completion_tokens=max_tokens                       │
│     )                                                        │
│                                                              │
└──────────────────────────────────────────────────────────────┘
    │
    │ API Call
    ▼
┌──────────────────────────────────────────────────────────────┐
│  STEP 5: External AI (Groq API)                              │
│  ──────────────────────────────────────────────────────────  │
│                                                              │
│  Groq processes the request and returns:                     │
│  "Unga sugar level konjam high-a irukku..."                  │
│                                                              │
└──────────────────────────────────────────────────────────────┘
    │
    │ Response
    ▼
┌──────────────────────────────────────────────────────────────┐
│  STEP 6: Response Flow (back up the chain)                   │
│  ──────────────────────────────────────────────────────────  │
│                                                              │
│  Handler returns: "Unga sugar level konjam high-a irukku..." │
│                        │                                     │
│                        ▼                                     │
│  Router wraps in ResponsePayload:                            │
│  {                                                           │
│    "output": "Unga sugar level konjam high-a irukku...",     │
│    "model": "openai/gpt-oss-120b",                           │
│    "endpoint": "groq_compound"                               │
│  }                                                           │
│                        │                                     │
│                        ▼                                     │
│  Frontend (app.js) receives and displays in output-content   │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## Key Files in the Flow

| Step | File | Function |
|------|------|----------|
| 1 | `frontend/js/app.js` | `handleSubmit()` - builds and sends request |
| 2 | `api/main.py` | FastAPI app receives request |
| 3 | `api/router.py` | `process_request()` - routes to handler |
| 4 | `api/src/groq_compound.py` | `process()` - calls AI API |
| 4 | `api/src/base_model.py` | `load_system_prompt()`, `load_user_prompt()` |
| 4 | `api/prompts/groq_compound/*.txt` | Prompt templates |
| 6 | `frontend/js/app.js` | `showOutput()` - displays response |

## Code Walkthrough

### Frontend Request (app.js)
```javascript
// User clicks Submit
async function handleSubmit() {
    const endpoint = modelSelect.value;           // "groq_compound"
    const input = userInput.value;                // User's text
    
    const response = await fetch(`${API_BASE_URL}/api/${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            input: input,
            temperature: parseFloat(temperatureInput.value),
            max_tokens: parseInt(maxTokensInput.value),
            stream: false
        })
    });
    
    const data = await response.json();
    showOutput(data);  // Display result
}
```

### Router Processing (router.py)
```python
@router.post("/{endpoint}")
async def process_request(endpoint: str, payload: RequestPayload):
    # 1. Validate endpoint exists
    modules = discover_modules()  # ["groq_compound", "gemini_3_flash"]
    if endpoint not in modules:
        raise HTTPException(404, f"Endpoint not found")
    
    # 2. Load handler class
    handler = get_handler(endpoint)  # GroqCompoundHandler()
    
    # 3. Process request
    result = handler.process(
        user_input=payload.input,
        model=payload.model,
        temperature=payload.temperature,
        max_tokens=payload.max_tokens,
        stream=payload.stream
    )
    
    # 4. Return response
    return ResponsePayload(output=result, model=..., endpoint=endpoint)
```

### Handler Processing (groq_compound.py)
```python
def process(self, user_input, model, temperature, max_tokens, stream, **kwargs):
    # 1. Load prompts from /prompts/groq_compound/
    system_prompt = self.load_system_prompt()     # From system.txt
    user_prompt = self.load_user_prompt(user_input)  # From user.txt with {input} replaced
    
    # 2. Build messages
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    
    # 3. Apply defaults
    model = model or config.DEFAULT_MODEL
    
    # 4. Call API
    completion = self.client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_completion_tokens=max_tokens
    )
    
    # 5. Return result
    return completion.choices[0].message.content
```

## Prompt Loading Detail

The `BaseModel` class provides these methods:

```python
def load_system_prompt(self) -> str:
    """Loads /prompts/{module_name}/system.txt"""
    system_file = self.prompts_dir / "system.txt"
    return system_file.read_text() if system_file.exists() else ""

def load_user_prompt(self, user_input: str) -> str:
    """Loads /prompts/{module_name}/user.txt and replaces {input}"""
    user_file = self.prompts_dir / "user.txt"
    template = user_file.read_text() if user_file.exists() else "{input}"
    return template.replace("{input}", user_input)
```
