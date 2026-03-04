from prometheus_client import Counter, Histogram, start_http_server

INGEST_ROWS_TOTAL = Counter(
    "ingest_rows_total",
    "Total rows read from raw source"
)

CLEAN_ROWS_TOTAL = Counter(
    "clean_rows_total",
    "Total rows after cleaning/dedup"
)

PIPELINE_RUNS_TOTAL = Counter(
    "pipeline_runs_total",
    "Number of ingestion pipeline runs"
)

STEP_LATENCY_SECONDS = Histogram(
    "pipeline_step_latency_seconds",
    "Latency of pipeline steps",
    labelnames=["step"]
)

def start_metrics_server(port: int) -> None:
    start_http_server(port)
