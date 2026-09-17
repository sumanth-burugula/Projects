import json
import re
from pathlib import Path
from typing import List

DATA_PATH = Path(__file__).parent / "data" / "synthetic_records.json"


def _tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def load_records() -> list[dict]:
    with DATA_PATH.open(encoding="utf-8") as handle:
        return json.load(handle)


def retrieve(patient_id: str, query: str, limit: int = 3) -> List[str]:
    """Small dependency-free retriever for the first working RAG version.

    It deliberately uses lexical scoring so the repository runs without an
    external vector database. A production evolution can swap this module for
    embeddings/vector search without changing the API layer.
    """
    record = next((r for r in load_records() if r["patient_id"] == patient_id), None)
    if record is None:
        return []

    query_tokens = _tokens(query)
    ranked = []
    for document in record["documents"]:
        score = len(query_tokens.intersection(_tokens(document)))
        ranked.append((score, document))

    ranked.sort(key=lambda item: item[0], reverse=True)
    return [document for score, document in ranked[:limit] if score > 0] or record["documents"][:limit]
