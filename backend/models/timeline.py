"""Timeline entries retain their source rather than asserting truth."""
from __future__ import annotations
from pydantic import BaseModel
from .case import SourceType


class TimelineEntry(BaseModel):
    date: str
    description: str
    source: SourceType
    source_reference: str
