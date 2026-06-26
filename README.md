# Startup CTO Agent

An AI-powered multi-agent system that analyzes startup ideas and generates comprehensive CTO-level strategies — covering feasibility, market analysis, growth planning, and hiring roadmaps.

## How It Works

```
  ┌─────────────────────────────────────────────────────┐
  │                  User submits idea                  │
  │         (idea, budget, team size, timeline)         │
  └──────────────────────┬──────────────────────────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │     Planner Agent   │◄── web search, trends
              │  Analyzes idea &    │
              │  selects agents     │
              └─────────┬───────────┘
                        │
                        ▼
          ┌─────────────────────────────┐
          │       Reviewer validates    │──── retry on failure
          └─────────────┬───────────────┘
                        │
                        ▼
   ┌──────────┬─────────┼─────────┬──────────┐
   ▼          ▼         ▼         ▼          ▼
┌────────┐┌────────┐┌────────┐┌────────┐┌────────┐
│Feasib- ││Market  ││Growth  ││Hiring  ││ (more  │
│ility   ││Analysis││Strategy││Plan    ││agents) │
└───┬────┘└───┬────┘└───┬────┘└───┬────┘└───┬────┘
    │         │         │         │         │
    └─────────┴─────────┼─────────┴─────────┘
                        │
                        ▼
          ┌─────────────────────────────┐
          │     Reviewer validates      │──── retry on failure
          │     each agent output       │──── gap analysis on skip
          └─────────────┬───────────────┘
                        │
                        ▼
              ┌─────────────────────┐
              │   Results saved &   │
              │   displayed in real │
              │   time (SSE stream) │
              └─────────────────────┘
```

## Tech Stack

| Layer | Tech |
|-------|------|
| Frontend | React 19, Vite, Tailwind CSS 4, Framer Motion |
| Backend | Python 3.12, FastAPI, Uvicorn |
| AI/Agents | LangGraph, LangChain, Google Gemini / OpenAI |
| Database | MongoDB (Motor async driver) |
| Research Tools | DuckDuckGo Search, Reddit API, Google Trends |
| Export | jsPDF, html2canvas |

## Project Structure

```
├── backend/
│   ├── app/
│   │   ├── agents/        # AI agent definitions (planner, feasibility, market, growth, hiring, reviewer)
│   │   ├── api/           # FastAPI routes (strategies CRUD + generate-cto streaming endpoint)
│   │   ├── core/          # Logging, shared utilities
│   │   ├── db/            # MongoDB client, models, repositories
│   │   ├── tools/         # Web search, Reddit, Google Trends integrations
│   │   ├── config.py      # Settings via pydantic-settings
│   │   └── main.py        # FastAPI app entry point
│   ├── tests/
│   └── pyproject.toml
├── frontend/
│   ├── src/
│   │   ├── components/    # Layout, InputArea, AgentProgress, ReportView, LinksPanel, Sidebar
│   │   ├── pages/         # Home, Chat
│   │   ├── lib/           # API client, utilities
│   │   ├── App.jsx        # Main app with SSE streaming orchestration
│   │   └── main.jsx
│   └── package.json
├── scripts/               # Server run/setup/stop scripts
└── docker-compose.yml
```

## Getting Started

### Prerequisites

- Python 3.12+
- Node.js 18+
- MongoDB instance

### Backend

```bash
cd backend
cp .env.example .env      # configure API keys and MongoDB URI
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev               # runs on http://localhost:5173
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Health check |
| `POST` | `/v1/strategies` | Create a new strategy |
| `GET` | `/v1/strategies` | List all strategies |
| `GET` | `/v1/strategies/:id` | Get strategy by ID |
| `DELETE` | `/v1/strategies/:id` | Delete a strategy |
| `POST` | `/v1/strategies/:id/generate-cto` | Stream CTO strategy generation (SSE) |
