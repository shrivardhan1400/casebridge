"""Document models with explicit provenance and safe upload metadata."""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Dict, Optional
from uuid import uuid4
from pydantic import BaseModel, Field


class CaseDocument(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    filename: str
    type: str
    category: str = "supporting-record"
    uploaded_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    extraction_status: str = "not-analyzed"
    confidence: Optional[float] = None
    extracted_fields: Dict[str, str] = Field(default_factory=dict)
    source_fields: Dict[str, str] = Field(default_factory=dict)
    review_status: str = "needs-user-review"
