"""FastAPI application entry point. Mounts routers and defines health endpoint."""

from fastapi import FastAPI

from app.config import settings
from app.api.router import api_router

app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG)
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


@app.get("/health")
def health_check():
    return {"status": "ok"}
