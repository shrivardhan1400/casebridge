"""Neutral document guidance for organizing information, not legal advice."""
from __future__ import annotations
from typing import Dict, List
from backend.models.case import CaseCategory

GUIDANCE: Dict[CaseCategory, List[Dict[str, str]]] = {
    CaseCategory.RENTAL: [
        {"name": "Rental agreement", "priority": "recommended", "why": "This document may help organize the arrangement you described."},
        {"name": "Deposit receipt", "priority": "recommended", "why": "This document may help clarify the amount described as a deposit."},
        {"name": "Payment/refund record", "priority": "recommended", "why": "This document may help organize amounts and dates you provided."},
        {"name": "Messages or photographs", "priority": "useful-if-available", "why": "These records may help provide context for communications or condition."},
    ],
    CaseCategory.EMPLOYMENT: [{"name": "Offer/appointment document", "priority": "recommended", "why": "This document may help organize employment details."}, {"name": "Salary records and relevant communications", "priority": "useful-if-available", "why": "These records may help clarify dates, amounts, or discussions."}],
    CaseCategory.PURCHASE: [{"name": "Invoice/receipt", "priority": "recommended", "why": "This document may help organize the purchase details you provided."}, {"name": "Order confirmation and payment record", "priority": "recommended", "why": "These records may help organize dates and amounts."}],
}


def recommend_documents(category: CaseCategory) -> List[Dict[str, str]]:
    """Return category-sensitive, non-legal document suggestions."""
    return GUIDANCE.get(category, [{"name": "Relevant communications or records", "priority": "optional", "why": "These records may help organize or clarify the information you provided."}])
