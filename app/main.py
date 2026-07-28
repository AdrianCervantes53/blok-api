from fastapi import FastAPI

from app.core.registry import register_modules

app = FastAPI(
    title="Blok API",
    description="Modular personal management API — shared backend for web and Android.",
    version="0.1.0",
)

register_modules(app)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
