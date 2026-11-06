from fastapi import FastAPI

app = FastAPI(
    title="fast-api-auth",
    version="0.1.0",
)


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Welcome to fast-api-auth"}


@app.get("/health")
def read_health() -> dict[str, str]:
    return {"status": "healthy"}
