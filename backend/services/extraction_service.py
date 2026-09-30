"""Deterministic prototype extraction; replaceable by a future AI provider."""
from __future__ import annotations
import re
from typing import List
from backend.models.case import Case, CaseCategory, ProvenancedField, SourceType


class BaseExtractor:
    """Protocol-like base for extraction providers."""
    def extract(self, case: Case, story: str) -> Case:
        raise NotImplementedError


class LocalDemoExtractor(BaseExtractor):
    """Local pattern-based extraction with no external model or hidden claims."""
    CATEGORY_TERMS = {
        CaseCategory.RENTAL: ("rent", "rental", "landlord", "tenant", "deposit", "apartment"),
        CaseCategory.EMPLOYMENT: ("salary", "employer", "employment", "offer letter", "attendance"),
        CaseCategory.PURCHASE: ("invoice", "seller", "warranty", "purchased", "purchase"),
        CaseCategory.ONLINE_TRANSACTION: ("upi", "online", "transaction", "wallet", "transfer"),
        CaseCategory.PROPERTY_DAMAGE: ("damage", "repair", "property", "photograph"),
    }

    def extract(self, case: Case, story: str) -> Case:
        """Classify and extract amounts/dates from user-provided story text."""
        lowered = story.lower()
        case.story = story.strip()
        case.category = max(self.CATEGORY_TERMS, key=lambda c: sum(term in lowered for term in self.CATEGORY_TERMS[c]), default=CaseCategory.GENERAL)
        if not any(term in lowered for terms in self.CATEGORY_TERMS.values() for term in terms):
            case.category = CaseCategory.GENERAL
        case.amounts = [ProvenancedField(key="amount", value=f"₹{m.replace(',', '')}", source=SourceType.USER_PROVIDED, source_reference="User statement") for m in re.findall(r"(?:₹|rs\.?\s*)([\d,]+)", story, re.I)]
        date_pattern = r"\b(?:\d{1,2}\s+(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{4}|(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{4})\b"
        case.dates = [ProvenancedField(key="date", value=d, source=SourceType.USER_PROVIDED, source_reference="User statement") for d in re.findall(date_pattern, story, re.I)]
        return case
