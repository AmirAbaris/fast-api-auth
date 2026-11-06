from fastapi import FastAPI

from app.api.v1.api import api_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
)

# Include v1 API routes (auth, users, etc.)
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Welcome to fast-api-auth"}


@app.get("/health")
def read_health() -> dict[str, str]:
    return {"status": "healthy"}
