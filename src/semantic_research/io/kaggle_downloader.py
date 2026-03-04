from __future__ import annotations

import os
import shutil
import zipfile
from pathlib import Path
from typing import Optional

from kaggle.api.kaggle_api_extended import KaggleApi


def _configure_kaggle_env_from_vars() -> None:
    """
    Kaggle API typically uses ~/.kaggle/kaggle.json.
    For CI/containers, allow env vars KAGGLE_USERNAME/KAGGLE_KEY.
    """
    username = os.getenv("KAGGLE_USERNAME")
    key = os.getenv("KAGGLE_KEY")
    if username and key:
        os.environ["KAGGLE_USERNAME"] = username
        os.environ["KAGGLE_KEY"] = key


def download_dataset(dataset_slug: str, dest_dir: Path, *, force: bool = False) -> Path:
    """
    Downloads and unzips a Kaggle dataset to dest_dir/<dataset_slug_sanitized>/.
    Returns the folder containing extracted files.
    """
    _configure_kaggle_env_from_vars()

    safe_name = dataset_slug.replace("/", "__")
    extract_dir = dest_dir / safe_name
    zip_path = dest_dir / f"{safe_name}.zip"

    if extract_dir.exists() and any(extract_dir.iterdir()) and not force:
        return extract_dir

    dest_dir.mkdir(parents=True, exist_ok=True)
    if extract_dir.exists() and force:
        shutil.rmtree(extract_dir)

    api = KaggleApi()
    api.authenticate()

    api.dataset_download_files(dataset_slug, path=str(dest_dir), quiet=False, unzip=False)

    # Kaggle uses dataset name zip; normalize to our zip_path if needed
    found_zip: Optional[Path] = None
    for p in dest_dir.glob("*.zip"):
        # take the most recent-looking zip if multiple
        found_zip = p
        break

    if found_zip is None:
        raise FileNotFoundError(f"No zip downloaded into {dest_dir}")

    if found_zip != zip_path:
        try:
            found_zip.rename(zip_path)
        except Exception:
            zip_path = found_zip

    extract_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(extract_dir)

    return extract_dir
