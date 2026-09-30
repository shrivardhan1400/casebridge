from backend.models.case import ProvenancedField
from backend.services.clarification_service import detect_amount_differences


def test_different_amounts_create_open_clarification() -> None:
    items = detect_amount_differences([ProvenancedField(key="amount", value="₹30000"), ProvenancedField(key="amount", value="₹25000", source_reference="Refund record")])
    assert len(items) == 1
    assert items[0].status == "open"
    assert "cannot determine" in items[0].description
