# CHECKPOINTS.md — blok-api

Verificaciones antes de marcar cualquier trabajo en este repo como terminado.

## Después de implementar

- [ ] `pytest` pasa (todos los tests, no solo los del módulo tocado)
- [ ] Sin `print()` de debug ni código comentado sin razón
- [ ] Migraciones de Alembic generadas si hubo cambios de modelo, y aplicadas sin error

## Antes de marcar como terminado

- [ ] El endpoint/feature tiene al menos un test que lo cubra
- [ ] `app/core/config.py` no tiene valores default para `database_url` ni `secret_key`
- [ ] Ningún secreto o credencial quedó hardcodeado en el diff
- [ ] Commit en rama propia, Conventional Commits, no directo a `master`

## Huecos conocidos (no fingir que existen)

- No hay `ruff` ni `mypy` configurados todavía — solo `pytest`. Si agregas linter/type-checker, actualiza este archivo.
