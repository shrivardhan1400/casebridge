"""Find cross-source differences without deciding what is correct."""
from __future__ import annotations
from typing import Iterable, List
from backend.models.case import ProvenancedField
from backend.models.clarification import Clarification


def detect_amount_differences(amounts: Iterable[ProvenancedField]) -> List[Clarification]:
    """Create an open clarification when two distinct amount values are present."""
    values = list(amounts)
    unique = []
    for amount in values:
        if amount.value not in [a.value for a in unique]:
            unique.append(amount)
    if len(unique) < 2:
        return []
    first, second = unique[0], unique[1]
    return [Clarification(field="amount", source_a=f"{first.value} — {first.source_reference}", source_b=f"{second.value} — {second.source_reference}", description="Two different amounts may need clarification. CaseBridge cannot determine which value is correct or explain any difference.")]
