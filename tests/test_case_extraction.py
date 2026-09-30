from backend.models.case import Case, CaseCategory
from backend.services.extraction_service import LocalDemoExtractor


def test_rental_story_classification_and_amounts() -> None:
    case = LocalDemoExtractor().extract(Case(), "I rented an apartment and paid ₹30,000 deposit. ₹25,000 was returned on 30 June 2026.")
    assert case.category == CaseCategory.RENTAL
    assert [amount.value for amount in case.amounts] == ["₹30000", "₹25000"]
    assert case.dates[0].value == "30 June 2026"
