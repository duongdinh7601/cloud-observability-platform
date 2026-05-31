from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.settings import CORS_ORIGINS
from app.routes import router as logs_router
from app.health import router as health_router
from app.middleware import add_request_logging_middleware
from app.metrics import router as metrics_router

app = FastAPI(title="Log Service")

add_request_logging_middleware(app)

if CORS_ORIGINS:
    # Restrict browser access to known frontend origins instead of allowing all cross-origin requests.
    app.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(logs_router)
app.include_router(health_router, prefix="/health")
app.include_router(metrics_router)
