"""State-based guided journey and information checklist."""
from __future__ import annotations
from typing import Dict, List
from backend.models.case import Case, CaseCategory, JourneyStage

CHECKLIST: Dict[CaseCategory, List[str]] = {
    CaseCategory.RENTAL: ["people involved", "property location", "rental start date", "issue date", "amount paid", "amount returned", "explanation provided", "written communications", "available documents"],
    CaseCategory.EMPLOYMENT: ["people involved", "employment start date", "issue date", "relevant communications", "available documents"],
    CaseCategory.PURCHASE: ["seller or provider", "purchase date", "amount paid", "issue description", "available documents"],
}


def detect_missing_information(case: Case) -> List[str]:
    """Identify checklist concepts not visibly supplied by the user."""
    story = case.story.lower()
    terms = {"people involved": ("landlord", "tenant", "seller", "employer"), "property location": ("hyderabad", "property", "apartment"), "rental start date": ("january", "rental"), "issue date": ("moved out", "issue"), "amount paid": ("₹", "paid"), "amount returned": ("returned", "refund"), "explanation provided": ("told", "explanation", "deduct"), "written communications": ("message", "whatsapp", "email"), "available documents": ("agreement", "receipt", "record", "document")}
    missing = []
    for item in CHECKLIST.get(case.category, ["people involved", "issue date", "available documents"]):
        if not any(term in story for term in terms.get(item, ())):
            missing.append(item)
    case.missing_information = missing
    return missing


def next_step(case: Case, clarification_open: bool = False) -> Dict[str, str]:
    """Select exactly one user-controlled next step from actual case state."""
    if not case.story:
        stage, action = JourneyStage.STORY, "Tell Your Story"
    elif case.missing_information:
        stage, action = JourneyStage.COMPLETE, "Complete Important Information"
    elif not case.document_ids:
        stage, action = JourneyStage.DOCUMENTS, "Find Documents That May Help"
    elif clarification_open:
        stage, action = JourneyStage.CLARIFY, "Review & Clarify"
    elif not case.precautions_reviewed:
        stage, action = JourneyStage.PRESERVE, "Preserve Important Information"
    elif not case.prepared_for_review:
        stage, action = JourneyStage.REVIEW, "Prepare for Human Review"
    elif any(item.status == "open" for item in case.follow_up_items):
        stage, action = JourneyStage.FOLLOW_UP, "Review Follow-up"
    elif case.status != "completed":
        stage, action = JourneyStage.DONE, "Complete Workflow"
    else:
        stage, action = JourneyStage.DONE, "Reopen / View Completed Case"
    case.current_stage = stage
    return {"stage": stage.value, "action": action}
