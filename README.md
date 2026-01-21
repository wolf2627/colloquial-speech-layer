# Colloquial Speech Layer

A modular API layer for medical text translation with a testing UI.

## Quick Start (Docker)

### 1. Set up environment
```bash
cp api/.env.example api/.env
# Edit api/.env and add your API keys
```

### 2. Build and run
```bash
docker-compose up --build
```

### 3. Access
- **Frontend UI**: http://localhost:3000
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

## Manual Setup

### API Backend
```bash
cd api
pip install -r requirements.txt
# Edit .env with your API keys
python -m uvicorn main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
python -m http.server 3000
```

---

## Project Structure

```
├── Dockerfile
├── docker-compose.yml
├── api/
│   ├── main.py
│   ├── config.py
│   ├── router.py
│   ├── .env
│   ├── src/
│   │   └── gemini_3_flash.py
│   └── prompts/
│       └── gemini_3_flash/
│           ├── system.txt
│           └── user.txt
└── frontend/
    ├── index.html
    ├── css/style.css
    └── js/app.js
```

---

## Adding New Models

1. Create `api/src/your_model.py` with a `process(user_input)` function
2. Create `api/prompts/your_model/system.txt` and `user.txt`
3. Restart the server - endpoint auto-created at `/api/your_model`
