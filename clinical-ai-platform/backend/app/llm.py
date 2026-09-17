import json
import os
from dataclasses import dataclass
from typing import List

import httpx


@dataclass
class GeneratedCandidate:
    condition: str
    evidence: List[str]
    confidence: float
    rationale: str


SYSTEM_PROMPT = """You are a software demonstration component analyzing synthetic clinical-style text.
Return only JSON. Do not make treatment recommendations. Identify only potential documentation gaps supported directly by the supplied evidence.
Expected schema: {"suspects":[{"condition":"string","evidence":["exact supplied evidence"],"confidence":0.0,"rationale":"string"}]}.
If evidence is insufficient, return {"suspects":[]}.
"""


def _parse_candidates(payload: str, allowed_evidence: List[str]) -> List[GeneratedCandidate]:
    data = json.loads(payload)
    allowed = set(allowed_evidence)
    results: List[GeneratedCandidate] = []
    for item in data.get("suspects", []):
        evidence = [text for text in item.get("evidence", []) if text in allowed]
        if not evidence:
            continue
        results.append(GeneratedCandidate(
            condition=str(item.get("condition", "Potential documentation gap")),
            evidence=evidence,
            confidence=min(max(float(item.get("confidence", 0.5)), 0.0), 1.0),
            rationale=str(item.get("rationale", "Supported by retrieved synthetic evidence.")),
        ))
    return results


def generate_with_llm(patient_id: str, evidence: List[str]) -> List[GeneratedCandidate] | None:
    """Optional provider-backed generation using an OpenAI-compatible chat endpoint.

    Configure LLM_API_KEY to enable it. LLM_BASE_URL and LLM_MODEL can point to
    another OpenAI-compatible provider. Returns None when no provider is configured,
    allowing the application to use its deterministic fallback.
    """
    api_key = os.getenv("LLM_API_KEY")
    if not api_key:
        return None

    base_url = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")
    model = os.getenv("LLM_MODEL", "gpt-4.1-mini")
    user_prompt = json.dumps({"patient_id": patient_id, "retrieved_evidence": evidence})

    response = httpx.post(
        f"{base_url.rstrip('/')}/chat/completions",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={
            "model": model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0,
        },
        timeout=30.0,
    )
    response.raise_for_status()
    content = response.json()["choices"][0]["message"]["content"]
    return _parse_candidates(content, evidence)
