# CaseBridge

## Overview

CaseBridge is an AI-assisted guided case journey that helps people organize complex situations for human review. **AI doesn’t decide what happened. It helps people explain what happened.** This is an independent hackathon prototype and is not affiliated with or endorsed by the Government of India. Demo records are synthetic.

## Problem Statement

People often have a story, messages, documents, and unanswered questions but lack a neutral way to organize them before speaking to a human reviewer.

## Solution and Key Features

The retained premium frontend provides story intake, bilingual/voice interactions, source mapping, document guidance and upload, document analysis, clarification, dashboard, notice explainer, precautions, contextual assistant, court-filing draft, print support, follow-up, and completion/reopen. The FastAPI backend adds structured Case, Document, Clarification, provenance, timeline, and state-based journey logic.

## Guided Case Journey

Tell Your Story → Understand Situation → Complete Information → Find Documents → Review & Clarify → Preserve Information → Prepare for Human Review → Follow-up → Complete or Reopen. Progress is computed from case state by `journey_service.next_step`.

## Architecture

See [architecture](docs/architecture.md). The backend is intentionally modular: extraction, guidance, clarification, journey, and review package services are separate, typed modules.

## Innovation and SDG 9 Alignment

CaseBridge is a modular civic-tech information infrastructure: a source-aware case model, cross-source clarification engine, state-driven journey engine, deterministic demo extractor, notice explainer, and human-review package builder. It advances **SDG 9: Industry, Innovation and Infrastructure** by making complex information organization reproducible, reviewable, and deployable without automating legal decisions. See the executable feature map in [evaluation alignment](docs/evaluation-alignment.md).

## AI Role, Document Intelligence, and Human-in-the-Loop

The default `LocalDemoExtractor` is a deterministic **Prototype extraction engine**, not a real LLM. It can be replaced behind `BaseExtractor`. Recommendations explain what may help without claiming legal necessity or authenticity. Conflicts remain open until a user clarifies them; packages are labeled for human review.

## Court Notice Explainer

The frontend retains its notice-explainer flow. It simplifies visible content and identifies mentioned information without giving legal advice, determining authenticity, or telling a user what legal action to take.

## Technology Stack

HTML/CSS/JavaScript, Python, FastAPI, Pydantic, and pytest.

## Project Structure

`frontend/` retained UI; `backend/models/` typed domain state; `backend/services/` algorithms; `tests/` API/domain tests; `fixtures/` demo data; `docs/` deployment and safety documentation.

## Installation and Running Locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn backend.app:app --reload
```

Open `http://127.0.0.1:8000`. For deployment, set production environment variables from `.env.example` and run `uvicorn backend.app:app --host 0.0.0.0 --port 8000`; use a process manager/reverse proxy and add authenticated encrypted storage before handling real data.

## Running Tests

```powershell
pytest -q
```

## Publish to GitHub

GitHub Pages can publish static sites, but it cannot run this FastAPI backend. Push this repository to GitHub to get automated tests through `.github/workflows/tests.yml`, then deploy the same GitHub repository to a Python host such as Render, Railway, or Fly.io. Use the build command `pip install -r requirements.txt` and start command `uvicorn backend.app:app --host 0.0.0.0 --port $PORT`. Configure `CASEBRIDGE_AI_PROVIDER=local-demo` and `MAX_UPLOAD_BYTES=10485760` in that host's environment settings; do not add a `.env` file to GitHub.

### Vercel

Vercel can detect the root `app.py` entry point directly; it imports `backend.app:app`. The same custom entry point and runtime dependencies are declared in `pyproject.toml`. After pushing both root files to GitHub, open the failed Vercel deployment and select **Redeploy**.

## API Endpoints

See [API documentation](docs/api.md). Health: `GET /api/health`; additional live flows include `POST /api/demo/rental`, `POST /api/notices/explain`, document-text analysis, source maps, review-package retrieval, and follow-up completion.

## Demo Case

See [demo instructions](docs/demo.md). It models a synthetic Hyderabad rental journey and a ₹30,000 versus ₹25,000 clarification.

## Privacy, Safety Boundaries, Limitations, Future Work

This prototype holds API data in memory; do not submit sensitive production material. It provides no legal advice or legal conclusions. Future work includes consent-based persistence, authentication, encrypted document storage, accessibility audit, and a provider-integrated extractor with evaluation controls.
