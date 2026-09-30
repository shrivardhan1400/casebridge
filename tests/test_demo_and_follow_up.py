from backend.models.case import Case, FollowUpItem
from backend.services.demo_service import create_rental_demo
from backend.services.follow_up_service import mark_follow_up_complete, reopen_journey


def test_synthetic_rental_demo_contains_documents_and_clarification() -> None:
    case, documents, clarification_count = create_rental_demo()
    assert case.category.value == "rental"
    assert len(documents) == 6
    assert clarification_count == 1
    assert {person.role for person in case.people} == {"Tenant", "Landlord"}


def test_follow_up_completion_and_reopen_are_user_controlled() -> None:
    case = Case(status="completed", follow_up_items=[FollowUpItem(description="Review package with human")])
    item = mark_follow_up_complete(case, case.follow_up_items[0].id, "Discussed on call")
    assert item.status == "completed"
    assert item.notes == "Discussed on call"
    assert reopen_journey(case).status == "active"
