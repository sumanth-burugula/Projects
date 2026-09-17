import hashlib
import math
import re
from collections import Counter
from typing import List

from .retrieval import load_records


def _features(text: str, dimensions: int = 256) -> List[float]:
    """Local hashed embedding used as a zero-credential vector-search fallback."""
    vector = [0.0] * dimensions
    tokens = re.findall(r"[a-z0-9]+", text.lower())
    counts = Counter(tokens)
    for token, count in counts.items():
        digest = hashlib.sha256(token.encode()).digest()
        index = int.from_bytes(digest[:4], "big") % dimensions
        vector[index] += float(count)
    norm = math.sqrt(sum(value * value for value in vector)) or 1.0
    return [value / norm for value in vector]


def _cosine(left: List[float], right: List[float]) -> float:
    return sum(a * b for a, b in zip(left, right))


def vector_retrieve(patient_id: str, query: str, limit: int = 3) -> List[str]:
    record = next((r for r in load_records() if r["patient_id"] == patient_id), None)
    if record is None:
        return []
    query_vector = _features(query)
    ranked = [(_cosine(query_vector, _features(doc)), doc) for doc in record["documents"]]
    ranked.sort(key=lambda item: item[0], reverse=True)
    return [doc for _, doc in ranked[:limit]]
