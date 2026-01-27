import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from app.database import engine
from app import models
from app.routes import router

load_dotenv()

app = FastAPI(title="Log Service")

cors_origins = os.getenv("CORS_ORIGINS", "")
allow_origins = [
    origin.strip()
    for origin in cors_origins.split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.on_event("startup")
def create_tables():
    models.Base.metadata.create_all(bind=engine)

@app.get("/")
def health_check():
    return {"status": "yerrttt"}
