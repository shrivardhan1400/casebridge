"""Clarification records deliberately preserve uncertainty."""
from __future__ import annotations
from typing import Optional
from uuid import uuid4
from pydantic import BaseModel, Field


class Clarification(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    field: str
    source_a: str
    source_b: str
    description: str
    status: str = "open"
    user_resolution: Optional[str] = None
    explanation: Optional[str] = None
