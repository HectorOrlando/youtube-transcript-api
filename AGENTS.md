# AGENTS.md — Contexto para IAs en este repositorio

## Que es este proyecto

Fork de uso personal de `jdepoix/youtube-transcript-api` (libreria Python
MIT que obtiene transcripciones de YouTube sin API key). El dueno es Hector.
Responder siempre en espanol.

## Remotos (regla critica)

| Remoto | Apunta a | Rol |
|---|---|---|
| `origin` | `git@github.com:HectorOrlando/youtube-transcript-api.git` | Fork de Hector: aqui viven pushes, ramas y pull requests |
| `upstream` | `https://github.com/jdepoix/youtube-transcript-api.git` | Repo original del autor: SOLO lectura (fetch/pull de mejoras) |

Los pull requests se crean SIEMPRE con `base repository:
HectorOrlando/youtube-transcript-api`, nunca contra jdepoix. Historia
completa en `LECCIONES.md`. Detalles operativos en
`.opencode/skill/pr-al-fork-propio/SKILL.md`.

## Archivos personales (no existen upstream)

- `get_transcript.py` — script interactivo de transcripciones (ver skill
  `mantenimiento-get-transcript` antes de modificarlo o probarlo)
- `COMO_USAR.md` — manual de uso del script para humanos
- `LECCIONES.md` — lecciones aprendidas git/GitHub
- `.opencode/` — skill y agente propios del usuario
- `transcripts/` — salida generada, organizada en subcarpetas tematicas

## Entorno

- Windows 11, PowerShell 5.1: NO usar `&&`; encadenar con `;` o
  `if ($?) { ... }`
- Consola cp1252: no imprimir emojis ni caracteres Unicode especiales;
  usar marcadores ASCII como `[OK]`, `[-]`, `[INFO]`
- Python 3.11.9 (Microsoft Store); dependencias: `requests`, `defusedxml`
- gh CLI autenticado como `HectorOrlando`

## Flujo tipico de actualizacion

```
git pull upstream master    # traer mejoras del autor original
git push origin master      # respaldar en el fork
```
