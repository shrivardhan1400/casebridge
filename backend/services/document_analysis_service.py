"""Safe deterministic analysis of user-supplied visible document text."""
from __future__ import annotations

import re
from typing import Dict, List

from backend.models.document import CaseDocument

DATE_PATTERN = re.compile(
    r"\b(?:\d{1,2}\s+(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{4})\b",
    re.IGNORECASE,
)
AMOUNT_PATTERN = re.compile(r"(?:₹|rs\.?\s*)([\d,]+)", re.IGNORECASE)


def analyze_visible_text(filename: str, text: str) -> CaseDocument:
    """Extract visible dates and amounts only; never authenticate a document."""
    fields: Dict[str, str] = {}
    for index, amount in enumerate(AMOUNT_PATTERN.findall(text), start=1):
        fields[f"amount_{index}"] = f"₹{amount.replace(',', '')}"
    for index, date in enumerate(DATE_PATTERN.findall(text), start=1):
        fields[f"date_{index}"] = date
    return CaseDocument(
        filename=filename,
        type="text/plain",
        category="document-analysis",
        extraction_status="prototype-extracted",
        confidence=0.0 if not fields else 0.75,
        extracted_fields=fields,
        source_fields={key: filename for key in fields},
        review_status="needs-user-review",
    )


def document_analysis_notice(document: CaseDocument) -> str:
    """Describe extraction status without presenting it as verification."""
    return (
        f"Prototype extraction identified {len(document.extracted_fields)} visible fields from "
        f"{document.filename}. Please review every AI-extracted value against the original record."
    )
