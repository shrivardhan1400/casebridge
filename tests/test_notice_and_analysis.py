from backend.services.document_analysis_service import analyze_visible_text
from backend.services.notice_service import explain_court_notice
from backend.services.source_mapping_service import build_source_map, map_document_fields


def test_notice_explainer_preserves_dates_and_safety_boundary() -> None:
    result = explain_court_notice("Please bring the agreement on 10 October 2026. Submit the receipt.")
    assert result["dates_mentioned"] == ["10 October 2026"]
    assert "bring" in result["instructions_mentioned"][0].lower()
    assert "not legal advice" in result["safety_notice"].lower()


def test_document_analysis_maps_document_provenance() -> None:
    document = analyze_visible_text("refund.pdf", "Refund amount ₹25,000 dated 05 July 2026")
    mapped = build_source_map(map_document_fields(document))
    assert document.extraction_status == "prototype-extracted"
    assert mapped[0]["source"] == "DOCUMENT-DERIVED"
    assert all(item["reference"] == "refund.pdf" for item in mapped)
