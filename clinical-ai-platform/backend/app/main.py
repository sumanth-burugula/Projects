from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import uuid

app = FastAPI(
    title="Clinical AI Suspecting API",
    version="0.1.0",
    description="Synthetic clinical prospective suspecting portfolio project",
)


class ClinicalRecord(BaseModel):
    patient_id: str
    text: str


class Suspect(BaseModel):
    condition: str
    evidence: List[str]
    confidence: float


class SuspectResponse(BaseModel):
    request_id: str
    patient_id: str
    suspects: List[Suspect]


def generate_demo_suspects(record: ClinicalRecord) -> List[Suspect]:
    """Deterministic starter implementation.

    This will later be replaced by retrieval + LLM generation followed by
    deterministic validation. Keeping the first version deterministic makes
    the API testable without requiring external credentials.
    """
    text = record.text.lower()
    suspects: List[Suspect] = []

    if "a1c" in text or "hyperglycemia" in text:
        suspects.append(
            Suspect(
                condition="Possible diabetes-related condition",
                evidence=[record.text],
                confidence=0.70,
            )
        )

    if "hypertension" in text or "high blood pressure" in text:
        suspects.append(
            Suspect(
                condition="Possible hypertension",
                evidence=[record.text],
                confidence=0.75,
            )
        )

    return suspects


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/api/v1/suspects", response_model=SuspectResponse)
def create_suspects(record: ClinicalRecord) -> SuspectResponse:
    return SuspectResponse(
        request_id=str(uuid.uuid4()),
        patient_id=record.patient_id,
        suspects=generate_demo_suspects(record),
    )
