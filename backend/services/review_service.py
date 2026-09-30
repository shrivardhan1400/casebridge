"""Human-review package builder preserving source and uncertainty."""
from __future__ import annotations
from typing import Dict, List
from backend.models.case import Case
from backend.models.clarification import Clarification
from backend.models.document import CaseDocument
from backend.models.timeline import TimelineEntry


def build_timeline(case: Case, documents: List[CaseDocument]) -> List[TimelineEntry]:
    """Combine user and document dates into an explicitly sourced timeline."""
    entries = [TimelineEntry(date=d.value, description="Date mentioned in user story", source=d.source, source_reference=d.source_reference) for d in case.dates]
    for document in documents:
        for key, value in document.extracted_fields.items():
            if "date" in key.lower():
                entries.append(TimelineEntry(date=value, description=f"Date extracted from {document.filename}", source="document-derived", source_reference=document.filename))
    return entries


def review_package(case: Case, documents: List[CaseDocument], clarifications: List[Clarification]) -> Dict[str, object]:
    """Create a neutral package for human review, never a legal conclusion."""
    return {"original_user_story": case.story, "situation_category": case.category.value, "people": case.people, "timeline": build_timeline(case, documents), "amounts": case.amounts, "structured_information": case.fields, "uploaded_documents": documents, "source_mapping": [*case.amounts, *case.dates], "clarifications": clarifications, "missing_information": case.missing_information, "precautions_reviewed": case.precautions_reviewed, "follow_up_items": case.follow_up_items, "review_status": case.human_review_status, "notice": "Prepared from user-provided information — requires human/legal review before filing."}
