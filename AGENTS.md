# AGENTS.md — blok-api

> Lee primero `../AGENTS.md` (el harness compartido en `blok-app`) para las
> reglas de proyecto: convenciones de commits, una feature a la vez, dónde
> viven los specs. Este archivo cubre solo lo específico de este repo.

## Reglas específicas de FastAPI / SQLAlchemy

- Usa dependency injection (`Depends`) para servicios y sesión de DB — no instancies servicios directamente en el handler.
- Sin acceso a la base de datos dentro de los route handlers: el handler llama al `service`, el `service` usa el `repository`/sesión.
- Un módulo nuevo sigue la estructura de `app/modules/<nombre>/`: `models.py`, `schemas.py`, `service.py`, `router.py`.
- Registro de routers manual en `app/main.py` vía `include_router` — no autodiscovery (decisión ya tomada, revisar solo si hay 4-5 módulos y se vuelve doloroso).
- Validación de ownership de recursos: devuelve 404, no 403, para no revelar existencia del recurso a quien no es dueño.
- Todo endpoint nuevo necesita al menos un test en `tests/` antes de considerarse terminado.
- No agregues valores default a settings sensibles (`database_url`, `secret_key`) en `app/core/config.py` — deben venir de `.env` obligatoriamente vía Pydantic.

## Si te bloqueas

Documenta el bloqueo en `../progress/current.md` (harness compartido) y para la sesión.
