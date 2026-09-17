# Clinical AI Suspecting Platform

A portfolio project inspired by value-based care workflows. The system ingests synthetic clinical-style data, retrieves relevant patient context, and generates structured AI-assisted suspect suggestions with traceable evidence.

## Goals
- Demonstrate Python/FastAPI backend development
- Build a simple RAG workflow for clinical-style records
- Model agentic/tool-driven workflows with deterministic validation
- Provide a React + TypeScript frontend
- Run locally with Docker
- Emphasize observability, explainability, and safe synthetic data

## Architecture

```text
React + TypeScript UI
        |
        v
FastAPI API Layer
        |
        +--> Patient/Encounter Service
        +--> Retrieval Service
        +--> Suspecting Agent
        +--> Validation / Guardrails
        +--> Audit + Observability
        |
        v
Synthetic Clinical Data + Vector/Keyword Retrieval
```

## Planned Features
- Synthetic patient and encounter ingestion
- Clinical text search and retrieval
- AI-assisted suspect generation
- Structured JSON outputs
- Evidence and confidence display
- Deterministic validation rules
- Audit trail and request IDs
- Health and readiness endpoints
- Dockerized local deployment

## Tech Stack
Python, FastAPI, Pydantic, React, TypeScript, Docker, REST APIs, pytest

## Important
This project uses only synthetic/demo data and is not intended for clinical decision-making.
