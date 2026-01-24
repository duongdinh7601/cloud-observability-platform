from fastapi import FastAPI
from app.database import engine
from app import models
from app.routes import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Log Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

# Create tables in PostgreSQL based on models
@app.on_event("startup")
def create_tables():
    models.Base.metadata.create_all(bind=engine)

@app.get("/")
def health_check():
    return {"status": "yerrttt"}