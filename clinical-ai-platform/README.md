# Clinical AI Suspecting Platform

Full-stack portfolio project inspired by value-based care workflows. It uses synthetic clinical-style records, retrieval, a tool-driven suspecting workflow, deterministic guardrails, and an evidence-focused React interface.

> Educational portfolio demo using synthetic data only. It is not a medical device and is not intended for clinical decision-making.

## Current Architecture

```text
React + TypeScript UI
        |
        v
FastAPI API Layer  ---- request IDs / latency logging
        |
        +--> Retrieval Tool
        |       |
        |       v
        |   Synthetic Patient Documents
        |
        +--> Suspecting Agent
                |
                +--> candidate generation
                +--> deterministic evidence validation
                +--> structured result
```

The first working version deliberately uses dependency-free lexical retrieval and deterministic candidate generation. This makes the application runnable and testable without external API credentials. The retrieval and candidate-generation boundaries are designed so embeddings/vector search and an LLM provider can be introduced without rewriting the API.

## Implemented

- Python + FastAPI backend
- Synthetic clinical-style patient records
- Retrieval layer for patient context
- Tool-driven suspecting workflow
- Evidence-required validation guardrail
- Structured Pydantic API responses
- Request IDs, latency logging, and health endpoint
- React + TypeScript evidence review interface
- Dockerfiles and Docker Compose
- pytest API tests
- CORS configuration for local full-stack development

## Run with Docker

```bash
docker compose up --build
```

Frontend: `http://localhost:5173`

FastAPI docs: `http://localhost:8000/docs`

## Run Backend Tests

```bash
cd backend
pip install -r requirements.txt
pytest
```

## API Examples

List synthetic patients:

```text
GET /api/v1/patients
```

Retrieve context:

```text
GET /api/v1/patients/SYN-1001/search?q=A1C
```

Run the suspecting workflow:

```text
POST /api/v1/patients/SYN-1001/suspects
```

## Next Engineering Iterations

1. Add provider-agnostic LLM interface with structured outputs.
2. Add embeddings and a vector-store adapter while retaining lexical fallback.
3. Add pipeline orchestration for ingestion/evaluation jobs.
4. Add PostgreSQL persistence and audit history.
5. Add OpenTelemetry-compatible tracing and metrics.
6. Add CI workflow for backend tests and frontend build.
7. Deploy the containerized application to a cloud environment.

## Tech Stack

Python, FastAPI, Pydantic, React, TypeScript, REST APIs, Docker, Docker Compose, pytest

## Design Principles

- Evidence before generation: a finding cannot be returned without retrieved evidence.
- Provider independence: retrieval, generation, and validation are separate modules.
- Observable by default: requests carry traceable IDs and latency is logged.
- Safe demo data: no real patient information is stored in this repository.
- Deterministic fallback: core functionality works without an LLM or external credentials.
