from __future__ import annotations

from prefect import flow, task

from semantic_research.config import Settings
from semantic_research.io.kaggle_downloader import download_dataset
from semantic_research.data.preprocess import load_raw_dataframe, clean_and_store
from semantic_research.logging_config import configure_logging
from semantic_research.observability.metrics import (
    PIPELINE_RUNS_TOTAL,
    INGEST_ROWS_TOTAL,
    CLEAN_ROWS_TOTAL,
    STEP_LATENCY_SECONDS,
    start_metrics_server,
)

logger = configure_logging("INFO", logger_name="module1")


@task(retries=2, retry_delay_seconds=10)
def t_download(settings: Settings):
    with STEP_LATENCY_SECONDS.labels(step="download").time():
        extract_dir = download_dataset(settings.kaggle_dataset_slug, settings.raw_dir, force=False)
    logger.info(f"Dataset extracted to: {extract_dir}")
    return extract_dir


@task
def t_load(extract_dir, settings: Settings):
    with STEP_LATENCY_SECONDS.labels(step="load_raw").time():
        df = load_raw_dataframe(extract_dir, row_limit=settings.row_limit)
    INGEST_ROWS_TOTAL.inc(len(df))
    logger.info(f"Loaded rows: {len(df)}")
    return df


@task
def t_clean_store(df, settings: Settings):
    with STEP_LATENCY_SECONDS.labels(step="clean_store").time():
        out_df = clean_and_store(df, settings.clean_parquet_path)
    CLEAN_ROWS_TOTAL.inc(len(out_df))
    logger.info(f"Clean rows: {len(out_df)} | Saved: {settings.clean_parquet_path}")
    return str(settings.clean_parquet_path)


@flow(name="module1_ingestion_pipeline")
def module1_flow():
    settings = Settings()
    settings.ensure_dirs()

    configure_logging(settings.log_level, logger_name="module1")
    start_metrics_server(settings.metrics_port)
    PIPELINE_RUNS_TOTAL.inc()

    extract_dir = t_download(settings)
    df = t_load(extract_dir, settings)
    out_path = t_clean_store(df, settings)
    return out_path


if __name__ == "__main__":
    module1_flow()
