"""Contextual, safety-bounded explanations for the Ask CaseBridge panel."""
from __future__ import annotations

from typing import Iterable

from backend.models.case import Case
from backend.models.clarification import Clarification
from backend.services.journey_service import next_step

LEGAL_BOUNDARY = (
    "I can help organize and explain the information in your CaseBridge journey, but I can’t "
    "determine legal rights or provide legal advice. A qualified legal professional or legal-aid "
    "service can advise you on that."
)


def contextual_answer(case: Case, clarifications: Iterable[Clarification], question: str) -> str:
    """Answer supported quick actions using only present CaseBridge state."""
    lowered = question.lower()
    if any(word in lowered for word in ("legal advice", "rights", "win", "sue", "legal action")):
        return LEGAL_BOUNDARY
    if "document" in lowered:
        return "Documents may help organize or clarify information you provided. They are not automatically verified or legally required."
    if "missing" in lowered or "why are you asking" in lowered:
        return "Information that may still need clarification: " + (", ".join(case.missing_information) or "none currently identified") + "."
    if "clarif" in lowered:
        open_count = sum(item.status == "open" for item in clarifications)
        return f"There are {open_count} items that may need clarification. You decide how to describe any difference."
    action = next_step(case, any(item.status == "open" for item in clarifications))["action"]
    return f"Your next step is {action}. This step helps prepare user-provided and document-derived information for human review."
