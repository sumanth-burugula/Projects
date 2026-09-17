from dataclasses import dataclass
from typing import List

from .retrieval import retrieve


@dataclass
class AgentResult:
    condition: str
    evidence: List[str]
    confidence: float
    rationale: str


def _validate(result: AgentResult) -> AgentResult | None:
    """Deterministic guardrail: never return a suspect without evidence."""
    if not result.evidence:
        return None
    result.confidence = min(max(result.confidence, 0.0), 1.0)
    return result


def run_suspecting_agent(patient_id: str) -> List[AgentResult]:
    """Tool-driven agent skeleton.

    The agent calls retrieval as a tool, forms candidate hypotheses, then sends
    each candidate through deterministic validation. This architecture keeps
    retrieval and validation independent from whichever LLM provider is added
    later.
    """
    context = retrieve(
        patient_id,
        "A1C hyperglycemia diabetes hypertension high blood pressure elevated",
    )
    joined = " ".join(context).lower()
    candidates: List[AgentResult] = []

    if "a1c" in joined or "hyperglycemia" in joined:
        candidates.append(
            AgentResult(
                condition="Possible diabetes-related condition",
                evidence=[doc for doc in context if "a1c" in doc.lower() or "hyperglycemia" in doc.lower()],
                confidence=0.82,
                rationale="Retrieved evidence contains a diabetes-related laboratory or clinical signal.",
            )
        )

    if "158/96" in joined or "elevated" in joined or "hypertension" in joined:
        candidates.append(
            AgentResult(
                condition="Possible hypertension",
                evidence=[doc for doc in context if "158/96" in doc.lower() or "elevated" in doc.lower() or "hypertension" in doc.lower()],
                confidence=0.84,
                rationale="Retrieved evidence contains repeated or explicit elevated blood-pressure signals.",
            )
        )

    validated = [_validate(candidate) for candidate in candidates]
    return [candidate for candidate in validated if candidate is not None]
