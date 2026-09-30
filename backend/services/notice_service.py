"""Court notice explainer that simplifies text without legal conclusions."""
from __future__ import annotations

import re
from typing import Dict, List

from backend.services.document_analysis_service import DATE_PATTERN

DOCUMENT_TERMS = ("document", "notice", "receipt", "agreement", "identity", "record", "annexure")
INSTRUCTION_TERMS = ("bring", "submit", "appear", "attend", "provide", "reply")


def explain_court_notice(visible_text: str) -> Dict[str, object]:
    """Organize visible notice content for human review; not legal advice."""
    lines = [line.strip() for line in re.split(r"[\n.!?]", visible_text) if line.strip()]
    instructions = [line for line in lines if any(term in line.lower() for term in INSTRUCTION_TERMS)]
    mentioned_documents = [line for line in lines if any(term in line.lower() for term in DOCUMENT_TERMS)]
    dates = DATE_PATTERN.findall(visible_text)
    return {
        "simple_explanation": "This prototype lists visible dates, instructions, and document references so you can review them with a human.",
        "dates_mentioned": dates,
        "instructions_mentioned": instructions,
        "documents_mentioned": mentioned_documents,
        "source_reference": "User-provided notice text",
        "safety_notice": "This is not legal advice and does not determine authenticity, obligations, deadlines, or outcomes.",
    }
