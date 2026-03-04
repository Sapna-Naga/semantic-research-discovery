from pathlib import Path
import pandas as pd

from semantic_research.data.preprocess import clean_and_store

def test_clean_and_store_writes_parquet(tmp_path: Path):
    df = pd.DataFrame(
        {
            "title": ["Paper A", "Paper A"],
            "abstract": ["This is an abstract that is long enough to pass.", "This is an abstract that is long enough to pass."],
            "categories": ["cs.AI", "cs.AI"],
        }
    )
    out_path = tmp_path / "clean.parquet"
    out_df = clean_and_store(df, out_path)
    assert out_path.exists()
    assert set(out_df.columns) >= {"paper_id", "title", "abstract", "categories", "text"}
    assert len(out_df) == 1
