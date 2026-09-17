import logging
import os
import time
import uuid
from typing import List

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .agent import run_suspecting_agent
from .retrieval import load_records
from .vector_retrieval import vector_retrieve

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("clinical-ai")

app = FastAPI(title="Clinical AI Suspecting API", version="0.3.0", description="Synthetic clinical RAG and agentic AI portfolio project")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])


class Suspect(BaseModel):
    condition: str
    evidence: List[str]
    confidence: float
    rationale: str
    generation_mode: str


class SuspectResponse(BaseModel):
    request_id: str
    patient_id: str
    suspects: List[Suspect]


class SearchResponse(BaseModel):
    patient_id: str
    query: str
    retrieval_mode: str
    documents: List[str]


@app.middleware("http")
async def request_observability(request: Request, call_next):
    request_id = request.headers.get("x-request-id", str(uuid.uuid4()))
    started = time.perf_counter()
    response = await call_next(request)
    duration_ms = round((time.perf_counter() - started) * 1000, 2)
    response.headers["x-request-id"] = request_id
    logger.info("request_id=%s method=%s path=%s status=%s duration_ms=%s", request_id, request.method, request.url.path, response.status_code, duration_ms)
    return response


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "clinical-ai-suspecting-api", "llm_configured": bool(os.getenv("LLM_API_KEY"))}


@app.get("/api/v1/patients")
def patients() -> list[dict]:
    return [{"patient_id": record["patient_id"]} for record in load_records()]


@app.get("/api/v1/patients/{patient_id}/search", response_model=SearchResponse)
def search_patient(patient_id: str, q: str) -> SearchResponse:
    documents = vector_retrieve(patient_id, q)
    if not documents:
        raise HTTPException(status_code=404, detail="Synthetic patient not found")
    return SearchResponse(patient_id=patient_id, query=q, retrieval_mode="local-vector", documents=documents)


@app.post("/api/v1/patients/{patient_id}/suspects", response_model=SuspectResponse)
def create_suspects(patient_id: str) -> SuspectResponse:
    if not any(record["patient_id"] == patient_id for record in load_records()):
        raise HTTPException(status_code=404, detail="Synthetic patient not found")
    results = run_suspecting_agent(patient_id)
    return SuspectResponse(
        request_id=str(uuid.uuid4()), patient_id=patient_id,
        suspects=[Suspect(condition=r.condition, evidence=r.evidence, confidence=r.confidence, rationale=r.rationale, generation_mode=r.generation_mode) for r in results],
    )
