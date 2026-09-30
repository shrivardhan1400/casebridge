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


def test_demo_notice_analysis_and_source_map_endpoints() -> None:
    demo = client.post("/api/demo/rental")
    assert demo.status_code == 201
    case_id = demo.json()["case"]["id"]
    notice = client.post("/api/notices/explain", json={"visible_text": "Please bring receipt on 10 October 2026."})
    assert notice.status_code == 200
    analysis = client.post(f"/api/cases/{case_id}/documents/analyze", json={"filename": "refund.txt", "visible_text": "Refund ₹25,000 on 05 July 2026"})
    assert analysis.status_code == 201
    assert client.get(f"/api/cases/{case_id}/source-map").status_code == 200
