"""V1 API router. All route modules are included here."""

from fastapi import APIRouter

from app.api.routes import strategies_router

api_router = APIRouter()
api_router.include_router(strategies_router)


@api_router.get("/")
def root():
    return {"message": "Welcome to Startup CTO Agent API"}
