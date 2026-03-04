import pandas as pd

from semantic_research.data.cleaning import normalize_text, deduplicate, basic_quality_filter, make_text_field

def test_normalize_text_collapses_whitespace():
    s = " hello \n  world\t\t"
    assert normalize_text(s) == "hello world"

def test_make_text_field():
    assert make_text_field("Title", "Abstract") == "Title. Abstract"

def test_basic_quality_filter_drops_short():
    df = pd.DataFrame(
        {
            "title": ["a", "Good Title"],
            "abstract": ["short", "This is a sufficiently long abstract for filtering."],
            "categories": ["cs.AI", "cs.CL"],
        }
    )
    out = basic_quality_filter(df)
    assert len(out) == 1

def test_deduplicate():
    df = pd.DataFrame(
        {"title": ["t", "t"], "abstract": ["a", "a"], "categories": ["c", "c"]}
    )
    out = deduplicate(df)
    assert len(out) == 1
