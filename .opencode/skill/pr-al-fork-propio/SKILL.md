---
name: pr-al-fork-propio
description: Use when creating pull requests, PRs, merging branches, pushing, or syncing this fork of jdepoix/youtube-transcript-api. PRs must target base repository = HectorOrlando/youtube-transcript-api (the user's own fork), NEVER jdepoix/youtube-transcript-api (upstream).
---

# Pull Requests siempre al fork propio

## Contexto de este repositorio

Este repo es un FORK. Hay dos remotos con roles distintos:

| Remoto | Apunta a | Rol |
|---|---|---|
| `origin` | `git@github.com:HectorOrlando/youtube-transcript-api.git` | EL fork del usuario (aqui viven sus ramas y PRs) |
| `upstream` | `https://github.com/jdepoix/youtube-transcript-api.git` | Repo original del autor (solo lectura para recibir mejoras) |

El usuario NO tiene permiso de escritura en `jdepoix/...`. Todo su trabajo
(pushes, merges, pull requests) debe quedar en `HectorOrlando/...`.

## La leccion (ocurrio el 2026-08-21)

Al crear un PR desde la web, GitHub dirigio el PR #615 al repo del autor
(`jdepoix/...`) en vez de al fork del usuario. Motivo: cuando trabajas desde
un fork, el formulario del PR propone POR DEFECTO `base repository` =
upstream. Hubo que cerrarlo y rehacerlo bien.

Antes de crear CUALQUIER pull request, verificar los 4 selectores del
formulario web (o los flags del comando). El destino correcto es:

```
base repository: HectorOrlando/youtube-transcript-api   ← SIEMPRE este
base: master
head repository: HectorOrlando/youtube-transcript-api
compare: <la rama de trabajo>
```

Si `base repository` dice `jdepoix/...`: NO crear el PR; avisar al usuario y
corregir el destino (desplegable "compare across forks").

## Comandos seguros

```powershell
# Crear un PR DENTRO del fork, sin ambiguedad:
gh pr create --repo HectorOrlando/youtube-transcript-api --base master --head <rama>

# Listar PRs del fork:
gh pr list --repo HectorOrlando/youtube-transcript-api

# Si un PR quedo por error en upstream, cerrarlo asi:
gh pr close <numero> --repo jdepoix/youtube-transcript-api --comment "Closing this pull request - it was opened by mistake..."

# Push de una rama de trabajo (siempre a origin):
git push -u origin <rama>
```

## Reglas de oro

1. `commit` y `merge` son locales: no salen del PC.
2. `push` sube al remoto indicado: aqui siempre `origin`.
3. Un Pull Request viaja al repo escrito en `base repository`: ese campo manda.
4. Nunca se opera contra `upstream` sin orden explicita del usuario.

Historia completa documentada en `LECCIONES.md`, leccion 1.
