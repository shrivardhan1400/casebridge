"""Provenance utilities that keep CaseBridge summaries reviewable."""
from __future__ import annotations

from typing import Dict, Iterable, List

from backend.models.case import ProvenancedField, SourceType
from backend.models.document import CaseDocument


SOURCE_LABELS: Dict[SourceType, str] = {
    SourceType.USER_PROVIDED: "USER PROVIDED",
    SourceType.DOCUMENT: "DOCUMENT-DERIVED",
    SourceType.AI_EXTRACTED: "AI-EXTRACTED",
    SourceType.CONFIRMED: "CONFIRMED BY YOU",
}


def source_label(source: SourceType) -> str:
    """Return the UI-safe provenance label for a structured field."""
    return SOURCE_LABELS[source]


def map_document_fields(document: CaseDocument) -> List[ProvenancedField]:
    """Map prototype-extracted document values to their visible source file."""
    return [
        ProvenancedField(
            key=key,
            value=value,
            source=SourceType.DOCUMENT,
            source_reference=document.filename,
            confidence=document.confidence,
        )
        for key, value in document.extracted_fields.items()
    ]


def build_source_map(fields: Iterable[ProvenancedField]) -> List[Dict[str, str]]:
    """Serialize fields for a review UI without discarding provenance."""
    return [
        {
            "field": field.key,
            "value": field.value,
            "source": source_label(field.source),
            "reference": field.source_reference,
        }
        for field in fields
    ]
