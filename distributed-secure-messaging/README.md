# Distributed Secure Messaging Platform

A distributed real-time messaging portfolio project demonstrating Python backend engineering, WebSockets, event-driven design, authentication, persistence, containerization, and production-oriented observability.

## Goals
- Build a FastAPI-based messaging backend
- Support real-time communication with WebSockets
- Separate API, messaging, and persistence concerns
- Add event-driven processing and delivery acknowledgements
- Provide a React + TypeScript client
- Containerize services with Docker
- Add logging, health checks, tests, and failure handling

## Architecture

```text
React + TypeScript Client
       | REST / WebSocket
       v
FastAPI Gateway
       |
       +--> Authentication
       +--> Messaging Service
       +--> Connection Manager
       +--> Event / Delivery Pipeline
       |
       v
Persistence Layer
```

## Planned Features
- User registration/login
- JWT authentication
- WebSocket chat
- Conversation history
- Delivery/read status
- Event-driven message processing
- Structured logging and request tracing
- Dockerized local deployment
- Automated API tests

## Tech Stack
Python, FastAPI, WebSockets, React, TypeScript, PostgreSQL/MongoDB, Docker, REST APIs, pytest

## Security Note
This is an educational portfolio implementation. Production-grade end-to-end encryption requires established, audited cryptographic protocols and key-management practices rather than custom cryptography.
