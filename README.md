# Blok API

Backend modular para la app de gestión personal **Blok**. Un solo API REST con JWT sirve a los clientes web (React) y Android (Kotlin/Compose).

## Stack

- FastAPI + PostgreSQL + SQLAlchemy + Alembic
- Auth JWT (`/auth/register`, `/auth/login`, `/auth/me`)
- Arquitectura *modular monolith*: `core/` + `modules/<nombre>/`

## Estructura

```
app/
├── core/                 # config, DB, security, auth, registry
├── modules/
│   └── notas/            # router, models, schemas, service
└── main.py
```

## Cómo añadir un módulo nuevo

1. Crear `app/modules/<nombre>/` con `models.py`, `schemas.py`, `service.py`, `router.py`
2. Importar el modelo en `alembic/env.py` y generar migración
3. Registrar el router en `app/core/registry.py` con `include_router`
4. Añadir tests en `tests/modules/<nombre>/`
5. Documentar el recurso en este README

## Endpoints (MVP)

| Método | Ruta | Auth | Descripción |
|--------|------|------|-------------|
| GET | `/health` | No | Healthcheck |
| POST | `/auth/register` | No | Crear usuario |
| POST | `/auth/login` | No | Obtener JWT |
| GET | `/auth/me` | Sí | Usuario actual |
| GET | `/notas` | Sí | Listar notas del usuario |
| POST | `/notas` | Sí | Crear nota |
| GET | `/notas/{id}` | Sí | Obtener nota |
| PATCH | `/notas/{id}` | Sí | Actualizar nota |
| DELETE | `/notas/{id}` | Sí | Eliminar nota |

## Arranque local

```bash
cp .env.example .env
docker compose up --build
```

API: http://localhost:8000  
Docs: http://localhost:8000/docs

Migraciones: las aplica el contenedor `api` al arrancar (`alembic upgrade head`).  
En Windows, preferí `postgresql+psycopg` (psycopg3). Postgres del compose se publica en **5434** para no chocar con otros Postgres locales (`5432` / `5433`).

### Sin Docker (solo tests / desarrollo)

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# pytest usa SQLite en memoria (no necesita Postgres)
pytest
```

## Tests

```bash
pytest -q
```

Los tests de integración usan SQLite en memoria y override de `get_db`.
