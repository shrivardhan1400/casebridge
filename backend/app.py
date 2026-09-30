"""FastAPI application for the deployable CaseBridge prototype."""
from __future__ import annotations
import re
from typing import Dict, List
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from backend.models.case import Case, FollowUpItem
from backend.models.clarification import Clarification
from backend.models.document import CaseDocument
from backend.services.clarification_service import detect_amount_differences
from backend.services.assistant_service import contextual_answer
from backend.services.demo_service import create_rental_demo
from backend.services.document_analysis_service import analyze_visible_text, document_analysis_notice
from backend.services.document_guidance import recommend_documents
from backend.services.extraction_service import LocalDemoExtractor
from backend.services.follow_up_service import mark_follow_up_complete, reopen_journey
from backend.services.journey_service import detect_missing_information, next_step
from backend.services.notice_service import explain_court_notice
from backend.services.review_service import review_package
from backend.services.source_mapping_service import build_source_map, map_document_fields

app = FastAPI(title="CaseBridge API", version="1.0.0")
CASES: Dict[str, Case] = {}
DOCUMENTS: Dict[str, List[CaseDocument]] = {}
CLARIFICATIONS: Dict[str, List[Clarification]] = {}
extractor = LocalDemoExtractor()
ALLOWED_TYPES = {"application/pdf", "image/jpeg", "image/png", "text/plain"}


class StoryRequest(BaseModel):
    story: str


class DocumentRequest(BaseModel):
    filename: str
    content_type: str
    size_bytes: int
    extracted_fields: Dict[str, str] = {}


class ClarificationRequest(BaseModel):
    clarification_id: str
    resolution: str
    explanation: str | None = None


class AssistantRequest(BaseModel):
    case_id: str
    question: str


class VisibleTextRequest(BaseModel):
    filename: str
    visible_text: str


class NoticeRequest(BaseModel):
    visible_text: str


class FollowUpCompletionRequest(BaseModel):
    notes: str | None = None


def get_case(case_id: str) -> Case:
    """Fetch a case or return the API's normal missing-resource response."""
    if case_id not in CASES:
        raise HTTPException(status_code=404, detail="Case not found")
    return CASES[case_id]


@app.get("/api/health")
def health() -> Dict[str, str]:
    """Return a small deployment health signal."""
    return {"status": "ok", "service": "CaseBridge"}


@app.post("/api/cases", status_code=201)
def create_case() -> Case:
    """Start an empty user-controlled CaseBridge journey."""
    case = Case()
    CASES[case.id], DOCUMENTS[case.id], CLARIFICATIONS[case.id] = case, [], []
    return case


@app.get("/api/cases/{case_id}")
def read_case(case_id: str) -> Case:
    return get_case(case_id)


@app.post("/api/cases/{case_id}/story")
def add_story(case_id: str, payload: StoryRequest) -> Case:
    case = get_case(case_id)
    if len(payload.story.strip()) < 20:
        raise HTTPException(status_code=422, detail="Please provide enough detail to organize the situation.")
    extractor.extract(case, payload.story)
    detect_missing_information(case)
    CLARIFICATIONS[case_id] = detect_amount_differences(case.amounts)
    return case


@app.post("/api/cases/{case_id}/documents", status_code=201)
def add_document(case_id: str, payload: DocumentRequest) -> CaseDocument:
    case = get_case(case_id)
    filename = re.sub(r"[^A-Za-z0-9._ -]", "_", payload.filename).strip(" .")
    if not filename or payload.content_type not in ALLOWED_TYPES or payload.size_bytes > 10 * 1024 * 1024:
        raise HTTPException(status_code=422, detail="Unsupported filename, type, or file size. Maximum size is 10 MB.")
    document = CaseDocument(filename=filename, type=payload.content_type, extraction_status="prototype-extracted" if payload.extracted_fields else "not-analyzed", extracted_fields=payload.extracted_fields, source_fields={k: filename for k in payload.extracted_fields})
    DOCUMENTS[case_id].append(document)
    case.document_ids.append(document.id)
    return document


@app.post("/api/cases/{case_id}/documents/analyze", status_code=201)
def analyze_document_text(case_id: str, payload: VisibleTextRequest) -> Dict[str, object]:
    """Analyze user-supplied visible text without executing or authenticating a file."""
    case = get_case(case_id)
    if len(payload.visible_text) > 100_000:
        raise HTTPException(status_code=422, detail="Visible text is too large for prototype analysis.")
    document = analyze_visible_text(payload.filename, payload.visible_text)
    DOCUMENTS[case_id].append(document)
    case.document_ids.append(document.id)
    mapped = map_document_fields(document)
    case.amounts.extend(field for field in mapped if field.key.startswith("amount_"))
    CLARIFICATIONS[case_id] = detect_amount_differences(case.amounts)
    return {"document": document, "source_mapping": build_source_map(mapped), "notice": document_analysis_notice(document)}


@app.get("/api/cases/{case_id}/documents/guidance")
def document_guidance(case_id: str) -> List[Dict[str, str]]:
    return recommend_documents(get_case(case_id).category)


@app.post("/api/cases/{case_id}/clarifications")
def resolve_clarification(case_id: str, payload: ClarificationRequest) -> Clarification:
    get_case(case_id)
    item = next((c for c in CLARIFICATIONS[case_id] if c.id == payload.clarification_id), None)
    if item is None:
        raise HTTPException(status_code=404, detail="Clarification not found")
    item.status, item.user_resolution, item.explanation = "resolved", payload.resolution, payload.explanation
    return item


@app.get("/api/cases/{case_id}/next-step")
def case_next_step(case_id: str) -> Dict[str, str]:
    case = get_case(case_id)
    return next_step(case, any(c.status == "open" for c in CLARIFICATIONS[case_id]))


@app.post("/api/cases/{case_id}/precautions-reviewed")
def mark_precautions(case_id: str) -> Case:
    case = get_case(case_id)
    case.precautions_reviewed = True
    return case


@app.post("/api/cases/{case_id}/prepare-review")
def prepare_review(case_id: str) -> Dict[str, object]:
    case = get_case(case_id)
    case.prepared_for_review, case.human_review_status = True, "prepared-for-human-review"
    return review_package(case, DOCUMENTS[case_id], CLARIFICATIONS[case_id])


@app.get("/api/cases/{case_id}/review-package")
def get_review_package(case_id: str) -> Dict[str, object]:
    """Return the current neutral human-review package without changing state."""
    case = get_case(case_id)
    return review_package(case, DOCUMENTS[case_id], CLARIFICATIONS[case_id])


@app.get("/api/cases/{case_id}/source-map")
def get_source_map(case_id: str) -> List[Dict[str, str]]:
    """Expose every available structured value with its provenance label."""
    case = get_case(case_id)
    document_fields = [field for document in DOCUMENTS[case_id] for field in map_document_fields(document)]
    return build_source_map([*case.amounts, *case.dates, *document_fields])


@app.post("/api/cases/{case_id}/follow-up", status_code=201)
def create_follow_up(case_id: str, item: FollowUpItem) -> FollowUpItem:
    get_case(case_id).follow_up_items.append(item)
    return item


@app.post("/api/cases/{case_id}/follow-up/{follow_up_id}/complete")
def complete_follow_up(case_id: str, follow_up_id: str, payload: FollowUpCompletionRequest) -> FollowUpItem:
    """Mark one user-created follow-up item complete."""
    try:
        return mark_follow_up_complete(get_case(case_id), follow_up_id, payload.notes)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.post("/api/cases/{case_id}/complete")
def complete_case(case_id: str) -> Dict[str, str]:
    case = get_case(case_id)
    case.status = "completed"
    return {"status": case.status, "message": "Marked as complete by you."}


@app.post("/api/cases/{case_id}/reopen")
def reopen_case(case_id: str) -> Case:
    return reopen_journey(get_case(case_id))


@app.post("/api/assistant")
def assistant(payload: AssistantRequest) -> Dict[str, str]:
    case = get_case(payload.case_id)
    return {"answer": contextual_answer(case, CLARIFICATIONS[payload.case_id], payload.question)}


@app.post("/api/notices/explain")
def explain_notice(payload: NoticeRequest) -> Dict[str, object]:
    """Explain visible notice text simply, preserving limits and source reference."""
    if not payload.visible_text.strip():
        raise HTTPException(status_code=422, detail="Please provide visible notice text to explain.")
    return explain_court_notice(payload.visible_text)


@app.post("/api/demo/rental", status_code=201)
def create_demo_rental() -> Dict[str, object]:
    """Create the deterministic synthetic rental demo with open clarification."""
    case, documents, clarification_count = create_rental_demo()
    CASES[case.id], DOCUMENTS[case.id] = case, documents
    CLARIFICATIONS[case.id] = detect_amount_differences(case.amounts)
    return {"case": case, "documents": documents, "open_clarifications": clarification_count}


app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
