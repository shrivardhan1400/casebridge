"""Case and journey models used throughout CaseBridge."""
from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional
from uuid import uuid4

from pydantic import BaseModel, Field


class CaseCategory(str, Enum):
    RENTAL = "rental"
    EMPLOYMENT = "employment"
    PURCHASE = "purchase"
    ONLINE_TRANSACTION = "online_transaction"
    PROPERTY_DAMAGE = "property_damage"
    GENERAL = "general"


class SourceType(str, Enum):
    USER_PROVIDED = "user-provided"
    DOCUMENT = "document-derived"
    AI_EXTRACTED = "ai-extracted"
    CONFIRMED = "confirmed-by-you"


class JourneyStage(str, Enum):
    STORY = "tell-your-story"
    UNDERSTAND = "understand-situation"
    COMPLETE = "complete-information"
    DOCUMENTS = "find-documents"
    CLARIFY = "review-clarify"
    PRESERVE = "preserve-information"
    REVIEW = "prepare-human-review"
    FOLLOW_UP = "human-review-follow-up"
    DONE = "complete-or-reopen"


class ProvenancedField(BaseModel):
    """A value retained with the place it came from."""
    key: str
    value: str
    source: SourceType = SourceType.USER_PROVIDED
    source_reference: str = "User statement"
    confidence: Optional[float] = None


class Person(BaseModel):
    name: str
    role: Optional[str] = None


class FollowUpItem(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    description: str
    due_date: Optional[str] = None
    status: str = "open"
    notes: Optional[str] = None


class Case(BaseModel):
    """A user-controlled guided case journey, never a legal determination."""
    id: str = Field(default_factory=lambda: str(uuid4()))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    status: str = "active"
    current_stage: JourneyStage = JourneyStage.STORY
    category: CaseCategory = CaseCategory.GENERAL
    story: str = ""
    people: List[Person] = Field(default_factory=list)
    dates: List[ProvenancedField] = Field(default_factory=list)
    events: List[ProvenancedField] = Field(default_factory=list)
    amounts: List[ProvenancedField] = Field(default_factory=list)
    fields: Dict[str, ProvenancedField] = Field(default_factory=dict)
    document_ids: List[str] = Field(default_factory=list)
    clarification_ids: List[str] = Field(default_factory=list)
    missing_information: List[str] = Field(default_factory=list)
    precautions_reviewed: bool = False
    prepared_for_review: bool = False
    follow_up_items: List[FollowUpItem] = Field(default_factory=list)
    human_review_status: str = "not-prepared"
