from __future__ import annotations

from dataclasses import dataclass

REQUIRED_COLUMNS = ["title", "abstract", "categories"]

@dataclass(frozen=True)
class CleanRecord:
    paper_id: str
    title: str
    abstract: str
    categories: str
    text: str  # title + abstract (normalized)
