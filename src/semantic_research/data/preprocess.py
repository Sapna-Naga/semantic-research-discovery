from __future__ import annotations

from pathlib import Path
from typing import Iterable, Optional

import pandas as pd

from semantic_research.data.cleaning import basic_quality_filter, deduplicate, make_text_field
from semantic_research.data.schema import REQUIRED_COLUMNS


def _find_candidate_files(extract_dir: Path) -> list[Path]:
    candidates = []
    for ext in ("*.csv", "*.json", "*.jsonl", "*.parquet"):
        candidates.extend(sorted(extract_dir.rglob(ext)))
    return candidates


def load_raw_dataframe(extract_dir: Path, *, row_limit: int = 0) -> pd.DataFrame:
    """
    Loads the dataset into a DataFrame.
    Supports CSV/JSON/JSONL/Parquet. Chooses the first file that contains required columns.
    """
    candidates = _find_candidate_files(extract_dir)
    if not candidates:
        raise FileNotFoundError(f"No dataset files found under {extract_dir}")

    last_err: Optional[Exception] = None
    for path in candidates:
        try:
            if path.suffix.lower() == ".csv":
                df = pd.read_csv(path)
            elif path.suffix.lower() == ".parquet":
                df = pd.read_parquet(path)
            elif path.suffix.lower() == ".json":
                df = pd.read_json(path)
            elif path.suffix.lower() == ".jsonl":
                df = pd.read_json(path, lines=True)
            else:
                continue

            cols = set(map(str.lower, df.columns))
            if all(c in cols for c in REQUIRED_COLUMNS):
                # normalize columns to expected names
                rename = {c: c.lower() for c in df.columns}
                df = df.rename(columns=rename)
                df = df[REQUIRED_COLUMNS + [c for c in df.columns if c not in REQUIRED_COLUMNS]]

                if row_limit and row_limit > 0:
                    df = df.head(row_limit)
                return df

        except Exception as e:
            last_err = e
            continue

    raise RuntimeError(
        f"Could not find a file with required columns {REQUIRED_COLUMNS} under {extract_dir}. "
        f"Last error: {last_err}"
    )


def clean_and_store(df: pd.DataFrame, out_path: Path) -> pd.DataFrame:
    """
    Clean + dedup + create `text` field; store to Parquet.
    """
    df = df.copy()
    df = basic_quality_filter(df)
    df["text"] = df.apply(lambda r: make_text_field(r["title"], r["abstract"]), axis=1)
    df = deduplicate(df)

    # stable id for downstream reproducibility (hash title+abstract)
    df["paper_id"] = pd.util.hash_pandas_object(df[["title", "abstract"]], index=False).astype("uint64").astype(str)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    df[["paper_id", "title", "abstract", "categories", "text"]].to_parquet(out_path, index=False)
    return df
