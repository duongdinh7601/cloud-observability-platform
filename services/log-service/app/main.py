from fastapi import FastAPI
from app.database import engine
from app import models
from app.routes import router

app = FastAPI(title="Log Service")

app.include_router(router)

# Create tables in PostgreSQL based on models
@app.on_event("startup")
def create_tables():
    models.Base.metadata.create_all(bind=engine)

@app.get("/")
def health_check():
    return {"status": "yerrttt"}