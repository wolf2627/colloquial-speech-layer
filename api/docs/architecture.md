# Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              FRONTEND (Port 3000)                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────────────────┐  │
│  │ index.html  │  │  style.css  │  │              app.js                 │  │
│  │  (UI View)  │  │  (Styling)  │  │  (API calls, DOM manipulation)      │  │
│  └─────────────┘  └─────────────┘  └─────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      │ HTTP POST /api/{endpoint}
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              API BACKEND (Port 8000)                        │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                           main.py                                    │   │
│  │  • FastAPI application entry point                                   │   │
│  │  • CORS middleware (allows frontend access)                          │   │
│  │  • Mounts /api router                                                │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                      │                                      │
│                                      ▼                                      │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                          router.py                                   │   │
│  │  • Dynamic endpoint routing                                          │   │
│  │  • Auto-discovers modules in /src                                    │   │
│  │  • Routes POST /api/{endpoint} to handler                            │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                      │                                      │
│                                      ▼                                      │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                      /src/base_model.py                              │   │
│  │  • Abstract base class for all handlers                              │   │
│  │  • Provides prompt loading utilities                                 │   │
│  │  • Defines process() method signature                                │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                      │                                      │
│                        ┌─────────────┴─────────────┐                       │
│                        ▼                           ▼                        │
│  ┌──────────────────────────────┐  ┌──────────────────────────────┐        │
│  │  /src/groq_compound.py       │  │  /src/gemini_3_flash.py      │        │
│  │  • Extends BaseModel         │  │  • Extends BaseModel         │        │
│  │  • Implements process()      │  │  • Implements process()      │        │
│  │  • Uses Groq API             │  │  • Uses Gemini API           │        │
│  └──────────────────────────────┘  └──────────────────────────────┘        │
│                        │                           │                        │
│                        ▼                           ▼                        │
│  ┌──────────────────────────────┐  ┌──────────────────────────────┐        │
│  │ /prompts/groq_compound/      │  │ /prompts/gemini_3_flash/     │        │
│  │  • system.txt (role)         │  │  • system.txt                │        │
│  │  • user.txt (template)       │  │  • user.txt                  │        │
│  └──────────────────────────────┘  └──────────────────────────────┘        │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
                          ┌───────────────────────┐
                          │   External AI APIs    │
                          │  (Groq, Gemini, etc)  │
                          └───────────────────────┘
```

## Component Responsibilities

### main.py
- Entry point for the FastAPI application
- Configures CORS to allow frontend requests
- Includes the router with `/api` prefix
- Provides health check endpoints

### config.py
- Loads environment variables from `.env`
- Provides typed configuration access
- Centralizes all configurable values

### router.py
- Scans `/src` directory for handler modules
- Dynamically creates POST endpoints
- Validates requests and routes to handlers
- Returns standardized response format

### base_model.py
- Abstract base class all handlers must extend
- Provides `load_system_prompt()` method
- Provides `load_user_prompt(input)` method
- Defines `process()` method signature

### Handler Files (/src/*.py)
- Each file = one API endpoint
- Must have a class extending BaseModel
- Must implement `process()` method
- Connects to specific AI service
