"""V1 API router. All endpoint modules are included here."""

from fastapi import APIRouter

api_router = APIRouter()


@api_router.get("/")
def root():
    return {"message": "Welcome to Startup CTO Agent API"}
