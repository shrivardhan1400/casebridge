"""User-controlled follow-up and completion helpers."""
from __future__ import annotations

from backend.models.case import Case, FollowUpItem


def mark_follow_up_complete(case: Case, follow_up_id: str, notes: str | None = None) -> FollowUpItem:
    """Mark an existing follow-up complete without declaring the situation resolved."""
    item = next((value for value in case.follow_up_items if value.id == follow_up_id), None)
    if item is None:
        raise ValueError("Follow-up item not found")
    item.status = "completed"
    if notes:
        item.notes = notes
    return item


def reopen_journey(case: Case) -> Case:
    """Return a completed journey to active user control."""
    case.status = "active"
    return case
