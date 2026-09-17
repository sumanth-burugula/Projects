from dataclasses import dataclass
from typing import List

from .llm import generate_with_llm
from .vector_retrieval import vector_retrieve


@dataclass
class AgentResult:
    condition: str
    evidence: List[str]
    confidence: float
    rationale: str
    generation_mode: str = "deterministic"


def _validate(result: AgentResult, retrieved_context: List[str]) -> AgentResult | None:
    """Evidence-grounding guardrail shared by LLM and deterministic paths."""
    allowed = set(retrieved_context)
    result.evidence = [item for item in result.evidence if item in allowed]
    if not result.evidence:
        return None
    result.confidence = min(max(result.confidence, 0.0), 1.0)
    return result


def _deterministic_candidates(context: List[str]) -> List[AgentResult]:
    joined = " ".join(context).lower()
    candidates: List[AgentResult] = []
    if "a1c" in joined or "hyperglycemia" in joined:
        candidates.append(AgentResult(
            condition="Possible diabetes-related condition",
            evidence=[d for d in context if "a1c" in d.lower() or "hyperglycemia" in d.lower()],
            confidence=0.82,
            rationale="Retrieved evidence contains a diabetes-related laboratory or clinical signal.",
        ))
    if "158/96" in joined or "elevated" in joined or "hypertension" in joined:
        candidates.append(AgentResult(
            condition="Possible hypertension",
            evidence=[d for d in context if "158/96" in d.lower() or "elevated" in d.lower() or "hypertension" in d.lower()],
            confidence=0.84,
            rationale="Retrieved evidence contains repeated or explicit elevated blood-pressure signals.",
        ))
    return candidates


def run_suspecting_agent(patient_id: str) -> List[AgentResult]:
    query = "potential documentation gaps involving diabetes A1C hyperglycemia hypertension elevated blood pressure"
    context = vector_retrieve(patient_id, query)

    generated = generate_with_llm(patient_id, context)
    if generated is not None:
        candidates = [AgentResult(
            condition=item.condition,
            evidence=item.evidence,
            confidence=item.confidence,
            rationale=item.rationale,
            generation_mode="llm",
        ) for item in generated]
    else:
        candidates = _deterministic_candidates(context)

    validated = [_validate(candidate, context) for candidate in candidates]
    return [candidate for candidate in validated if candidate is not None]
