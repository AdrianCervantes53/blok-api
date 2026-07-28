"""Manual module registration for the modular monolith."""

from fastapi import FastAPI

from app.core.router import router as auth_router
from app.modules.notas.router import router as notas_router


def register_modules(app: FastAPI) -> None:
    app.include_router(auth_router)
    app.include_router(notas_router)
