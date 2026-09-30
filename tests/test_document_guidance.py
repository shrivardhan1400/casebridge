from backend.models.case import CaseCategory
from backend.services.document_guidance import recommend_documents


def test_rental_guidance_is_specific_and_neutral() -> None:
    guidance = recommend_documents(CaseCategory.RENTAL)
    assert any(item["name"] == "Rental agreement" for item in guidance)
    assert all("legal" not in item["why"].lower() for item in guidance)
