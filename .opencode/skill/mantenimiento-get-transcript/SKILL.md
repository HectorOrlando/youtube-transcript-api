---
name: mantenimiento-get-transcript
description: Use when modifying, fixing, extending, or testing get_transcript.py, its transcript output formats, folder/filename logic, or the YouTube oEmbed title lookup. Contains code conventions and the piped-stdin testing recipe.
---

# Mantenimiento de get_transcript.py

## Arquitectura (flujo principal)

```
URL pegada → extract_video_id() → ytt_api.fetch(video_id, languages=["es","en"])
→ TextFormatter → choose_output_dir() [menu 1/2/3] → get_video_title() [oEmbed]
→ prompt "Guardar como [...] (Enter=aceptar)" → sanitize_name()
→ guardar UTF-8 en transcripts/<subcarpeta>/<nombre>.txt
```

Funciones y su responsabilidad:

| Funcion | Hace |
|---|---|
| `extract_video_id(url)` | Regex para watch?v=, youtu.be/, shorts/, embed/, /v/, ?v= y &v= |
| `sanitize_name(nombre)` | `\ / : * ? " < > \|` → `_`; colapsa espacios; recorta a 200; quita puntos/espacios finales |
| `get_video_title(video_id)` | GET `https://www.youtube.com/oembed` con requests, timeout 10s; devuelve None si falla (fallback: ID del video) |
| `choose_output_dir()` | Menu interactivo: `[1]` transcripts/ por defecto, `[2]` crear subcarpeta, `[3]` listar subcarpetas existentes |
| `main()` | Orquesta todo + manejo especifico de errores |

Errores importados desde
`youtube_transcript_api._errors`: NoTranscriptFound, TranscriptsDisabled,
VideoUnavailable, VideoUnplayable, AgeRestricted, RequestBlocked,
CouldNotRetrieveTranscript. Hay ademas un `except Exception` generico con
traceback al final.

## Convenciones obligatorias

1. **Consola cp1252**: nada de emojis ni Unicode especial en `print()`.
   Marcadores ASCII: `[OK]`, `[-]`, `[INFO]`.
2. **Texto sin tildes** en los mensajes de consola (estilo del archivo).
3. El script arranca con `sys.stdout/stderr.reconfigure(errors="replace")`
   para no crashear si un titulo trae caracteres fuera de cp1252. NO quitarlo.
4. Archivos de salida SIEMPRE en UTF-8 (`open(..., encoding="utf-8")`).
5. La salida vive dentro de `transcripts/` (o su subcarpeta elegida), jamas
   en la raiz del repo.
6. `requests` ya es dependencia del proyecto: usarla, no agregar librerias.

## Receta de pruebas (entrada canalizada)

El script usa `input()`; en pruebas se le alimenta stdin canalizado desde
PowerShell 5.1. Cada linea entre comillas es una respuesta consecutiva.

```powershell
# Flujo completo: URL + opcion [1] (carpeta por defecto) + Enter (aceptar nombre)
"https://www.youtube.com/watch?v=MTnrsUa1VA4`n1`n`n" | python get_transcript.py

# Opcion [2]: crear subcarpeta "test_auto" y nombre personalizado
"https://...watch?v=<ID>`n2`ntest_auto`nmi_nombre`n" | python get_transcript.py

# Opcion [3]: elegir la subcarpeta numero 1 de la lista
"https://...watch?v=<ID>`n3`n1`n`n" | python get_transcript.py
```

Verificar el resultado:

```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
Get-ChildItem transcripts -Recurse -File | Select-Object FullName
Get-Content "<archivo generado>" -Encoding UTF8 -TotalCount 3   # sin -Encoding se ve mojibake en PS 5.1
```

LIMPIAR los artefactos de prueba despues (borrar subcarpetas/archivos
creados solo para el test). Cada ejecucion consume red real (transcripcion +
oEmbed): no abusar de corridas.

## Acuerdo de documentacion

Cualquier cambio de comportamiento visible (mensajes, menu, nombres de
archivo, carpeta de salida) exige actualizar tambien `COMO_USAR.md`, que es
el manual para humanos.
