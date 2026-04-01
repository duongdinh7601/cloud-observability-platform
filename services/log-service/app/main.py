from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine
from app.settings import CORS_ORIGINS
from app import models
from app.routes import router as logs_router
from app.health import router as health_router

app = FastAPI(title="Log Service")

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

@app.on_event("startup")
def create_tables():
    # This keeps local development simple by creating missing tables automatically.
    # In a more mature deployment flow, schema changes would usually be handled by migrations.
    models.Base.metadata.create_all(bind=engine)
