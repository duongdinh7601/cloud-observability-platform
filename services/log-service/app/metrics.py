from fastapi import APIRouter, Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

router = APIRouter(tags=["metrics"])

HTTP_REQUESTS_TOTAL = Counter(
    name="log_service_http_requests_total",
    documentation="Total HTTP requests handled by log-service.",
    labelnames=["method", "path", "status_code"],
)

HTTP_REQUEST_DURATION_SECONDS = Histogram(
    name="log_service_http_request_duration_seconds",
    documentation="HTTP request duration in seconds for log-service.",
    labelnames=["method", "path", "status_code"],
)

LOGS_INGESTED_TOTAL = Counter(
    name="log_service_logs_ingested_total",
    documentation="Total log entries successfully ingested by log-service.",
)


def record_http_request_metrics(
    method: str, path: str, status_code: int, duration_seconds: float
) -> None:
    """Record Prometheus metrics for one HTTP request."""

    status_code_label = str(status_code)

    HTTP_REQUESTS_TOTAL.labels(
        method=method,
        path=path,
        status_code=status_code_label,
    ).inc()

    HTTP_REQUEST_DURATION_SECONDS.labels(
        method=method,
        path=path,
        status_code=status_code_label,
    ).observe(duration_seconds)


def record_log_ingested() -> None:
    """Record one successfully ingested log entry."""
    LOGS_INGESTED_TOTAL.inc()


@router.get("/metrics")
def get_metrics():
    metrics_output = generate_latest()
    return Response(content=metrics_output, media_type=CONTENT_TYPE_LATEST)
