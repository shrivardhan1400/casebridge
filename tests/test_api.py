from fastapi.testclient import TestClient
from backend.app import app


client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_story_document_and_completion_flow() -> None:
    case_id = client.post("/api/cases").json()["id"]
    story = "I rented an apartment in Hyderabad in January 2026 and paid ₹30,000. ₹25,000 was returned after I moved out on 30 June 2026."
    assert client.post(f"/api/cases/{case_id}/story", json={"story": story}).status_code == 200
    assert client.post(f"/api/cases/{case_id}/documents", json={"filename": "refund.pdf", "content_type": "application/pdf", "size_bytes": 123}).status_code == 201
    assert client.post(f"/api/cases/{case_id}/complete").json()["message"] == "Marked as complete by you."
    assert client.post(f"/api/cases/{case_id}/reopen").json()["status"] == "active"
