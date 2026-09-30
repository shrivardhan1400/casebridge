from backend.models.case import Case
from backend.services.journey_service import detect_missing_information, next_step


def test_next_step_progression_and_completion() -> None:
    case = Case()
    assert next_step(case)["action"] == "Tell Your Story"
    case.story = "A general situation"
    detect_missing_information(case)
    assert next_step(case)["action"] == "Complete Important Information"
    case.missing_information = []
    case.document_ids = ["document"]
    case.precautions_reviewed = True
    case.prepared_for_review = True
    assert next_step(case)["action"] == "Complete Workflow"
    case.status = "completed"
    assert next_step(case)["action"] == "Reopen / View Completed Case"
