from __future__ import annotations

import re
from typing import Optional

import pandas as pd
import regex as uni_regex

_whitespace_re = re.compile(r"\s+")
_control_chars_re = uni_regex.compile(r"[\p{C}]+")

def normalize_text(s: Optional[str]) -> str:
    if s is None:
        return ""
    s = str(s)
    s = _control_chars_re.sub(" ", s)
    s = s.replace("\u00a0", " ")  # non-breaking space
    s = s.strip()
    s = _whitespace_re.sub(" ", s)
    return s

def make_text_field(title: str, abstract: str) -> str:
    title_n = normalize_text(title)
    abstract_n = normalize_text(abstract)
    if title_n and abstract_n:
        return f"{title_n}. {abstract_n}"
    return title_n or abstract_n

def basic_quality_filter(df: pd.DataFrame) -> pd.DataFrame:
    """
    Drop rows missing title/abstract; keep minimal text length.
    """
    df = df.copy()
    df["title"] = df["title"].map(normalize_text)
    df["abstract"] = df["abstract"].map(normalize_text)
    df["categories"] = df["categories"].map(normalize_text)

    df = df[(df["title"].str.len() > 3) & (df["abstract"].str.len() > 20)]
    return df

def deduplicate(df: pd.DataFrame) -> pd.DataFrame:
    """
    Deduplicate using (title, abstract) exact match after normalization.
    """
    df = df.copy()
    df = df.drop_duplicates(subset=["title", "abstract"], keep="first")
    return df
