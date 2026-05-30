import json
import logging
import time

from fastapi import FastAPI, Request

request_logger = logging.getLogger("log_service.request")

# Set log level for now until service-wide logging configuration is added
request_logger.setLevel(logging.INFO)

# Local JSON log handler until service-wide logging configuration is added
if not request_logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(message)s"))
    request_logger.addHandler(handler)

request_logger.propagate = False


HEALTH_PATHS = {"/health/live", "/health/ready"}


def add_request_logging_middleware(app: FastAPI) -> None:
    @app.middleware("http")
    async def request_logging_middleware(request: Request, call_next):
        if request.url.path in HEALTH_PATHS:
            return await call_next(request)

        start_time = time.perf_counter()

        try:
            response = await call_next(request)
        except Exception as exc:
            duration_ms = round((time.perf_counter() - start_time) * 1000, 2)

            error_log_record = {
                "event": "http_request_error",
                "method": request.method,
                "path": request.url.path,
                "status_code": 500,
                "duration_ms": duration_ms,
                "error_type": type(exc).__name__,
                "error": str(exc),
            }

            request_logger.exception(json.dumps(error_log_record, sort_keys=True))

            raise

        duration_ms = round((time.perf_counter() - start_time) * 1000, 2)

        log_record = {
            "event": "http_request",
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "duration_ms": duration_ms,
        }

        request_logger.info(json.dumps(log_record, sort_keys=True))

        return response
