from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_diabetes_suspect_has_evidence():
    response = client.post("/api/v1/patients/SYN-1001/suspects")
    assert response.status_code == 200
    payload = response.json()
    assert payload["patient_id"] == "SYN-1001"
    assert payload["suspects"]
    assert payload["suspects"][0]["evidence"]


def test_unknown_patient_returns_404():
    response = client.post("/api/v1/patients/UNKNOWN/suspects")
    assert response.status_code == 404
