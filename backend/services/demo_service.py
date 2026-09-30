"""Deterministic synthetic rental journey for demonstrations and tests."""
from __future__ import annotations

from backend.models.case import Case, Person, ProvenancedField, SourceType
from backend.models.document import CaseDocument
from backend.services.clarification_service import detect_amount_differences
from backend.services.extraction_service import LocalDemoExtractor
from backend.services.journey_service import detect_missing_information

DEMO_STORY = (
    "I rented an apartment in Hyderabad from Rohan Kapoor in January 2026. I paid a security "
    "deposit of ₹30,000 and paid monthly rent regularly. When I moved out on 30 June 2026, the "
    "landlord returned ₹25,000. He mentioned repairs but gave no clear breakdown. I have a rental "
    "agreement, security deposit receipt, bank transaction records, refund record, photographs, "
    "and WhatsApp messages."
)


def create_rental_demo() -> tuple[Case, list[CaseDocument], int]:
    """Build the declared synthetic rental demo and its open clarification."""
    case = LocalDemoExtractor().extract(Case(), DEMO_STORY)
    case.people = [Person(name="Aarav Mehta", role="Tenant"), Person(name="Rohan Kapoor", role="Landlord")]
    case.amounts = [
        ProvenancedField(key="original_security_deposit", value="₹30000", source=SourceType.USER_PROVIDED, source_reference="User statement"),
        ProvenancedField(key="returned_amount", value="₹25000", source=SourceType.DOCUMENT, source_reference="Refund_Record_DEMO.pdf"),
    ]
    documents = [CaseDocument(filename=name, type="application/pdf" if name.endswith(".pdf") else "image/jpeg", category="demo-supporting-record") for name in ("Rental_Agreement_DEMO.pdf", "Security_Deposit_Receipt_DEMO.pdf", "Refund_Record_DEMO.pdf", "Repair_Messages_DEMO.pdf", "Bank_Transaction_DEMO.pdf", "Property_Photo_DEMO.jpg")]
    case.document_ids = [document.id for document in documents]
    detect_missing_information(case)
    return case, documents, len(detect_amount_differences(case.amounts))
