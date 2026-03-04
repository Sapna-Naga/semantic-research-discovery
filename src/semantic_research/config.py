from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    kaggle_dataset_slug: str = os.getenv("KAGGLE_DATASET_SLUG", "sumitm004/arxiv-scientific-research-papers-dataset")

    data_dir: Path = Path(os.getenv("DATA_DIR", "./data"))
    raw_dir: Path = Path(os.getenv("RAW_DIR", "./data/raw"))
    interim_dir: Path = Path(os.getenv("INTERIM_DIR", "./data/interim"))
    processed_dir: Path = Path(os.getenv("PROCESSED_DIR", "./data/processed"))

    clean_parquet_name: str = os.getenv("CLEAN_PARQUET_NAME", "arxiv_clean.parquet")
    row_limit: int = int(os.getenv("ROW_LIMIT", "50000"))

    metrics_port: int = int(os.getenv("METRICS_PORT", "8001"))
    log_level: str = os.getenv("LOG_LEVEL", "INFO")

    def ensure_dirs(self) -> None:
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        self.interim_dir.mkdir(parents=True, exist_ok=True)
        self.processed_dir.mkdir(parents=True, exist_ok=True)

    @property
    def clean_parquet_path(self) -> Path:
        return self.processed_dir / self.clean_parquet_name
