# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a LangChain Agent Web MVP with a Vue 3 frontend and FastAPI backend. The agent uses LangGraph for orchestration with OpenAI models and includes built-in tools for calculations and time queries.

## Project Structure

```
langchanproject/
├── backend/           # Python FastAPI backend
│   ├── main.py        # FastAPI app with chat endpoint
│   ├── agent.py       # LangGraph agent setup with tools
│   ├── tools.py       # Tool definitions (calculator, time)
│   ├── pyproject.toml # Python dependencies (uv-based)
│   └── .env.example   # Environment variable template
└── frontend/          # Vue 3 frontend
    ├── src/
    │   ├── App.vue    # Main chat component
    │   └── main.js    # Vue app entry point
    ├── package.json   # Node dependencies
    └── vite.config.js # Vite config with proxy to backend
```

## Development Commands

### Backend (Python)

The backend uses `uv` for dependency management.

```bash
# Navigate to backend
cd backend

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate     # On Windows
uv pip install -e .

# Run the backend server (default: http://localhost:8000)
python main.py
# or with uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend (Vue 3)

The frontend uses Vite for development and building.

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Run development server (default: http://localhost:5173)
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Architecture

### Backend

- **FastAPI** provides REST API endpoints
- **LangGraph** (`create_react_agent`) creates the agent orchestration
- **LangChain** integrates with OpenAI Chat models
- Tools are defined using `@tool` decorator from `langchain_core.tools`

Key endpoint: `POST /chat` - Receives `{message: string}` and returns `{response: string}`

The agent app is initialized at startup and reused for requests to maintain conversation state in the message flow.

### Frontend

- **Vue 3** with Composition API (`<script setup>`)
- **Axios** for HTTP requests to backend
- **Vite proxy** forwards `/api/*` requests to `http://localhost:8100` (note: backend default is 8000, may need adjustment)

### Communication Flow

1. Frontend sends message to `/api/chat` (proxied to backend)
2. Backend invokes LangGraph agent with message
3. Agent decides whether to call tools or respond directly
4. Response returned to frontend and displayed in chat UI

## Environment Variables

Create `backend/.env` from `backend/.env.example`:

```env
OPENAI_API_KEY=your_actual_key_here
OPENAI_MODEL=gpt-4o
```

## Notes

- The backend uses Python 3.10 (required by pyproject.toml)
- Tools defined in `tools.py` should be imported into `agent.py` for use
- CORS is enabled for all origins (configure for production)
- Frontend proxy target (8100) differs from backend default (8000) - update as needed
