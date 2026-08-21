# Instrucciones: get_transcript.py

Script para obtener la transcripcion (subtitulos) en texto plano de un video de YouTube
y guardarla automaticamente en un archivo `.txt`.

Este script usa la libreria `youtube_transcript_api` incluida en este repositorio,
la cual consulta una parte no documentada de la API web de YouTube (no requiere
API key ni navegador headless).

---

## Requisitos

- Python 3.8 o superior (probado con Python 3.11)
- Dependencias instaladas:

```
pip install requests defusedxml
```

No hace falta instalar nada mas: el paquete `youtube_transcript_api` es el propio
directorio `youtube_transcript_api/` de este repositorio, y Python lo encuentra
porque el script se ejecuta desde la raiz del repositorio.

---

## Como usarlo

1. Abre una terminal en la carpeta raiz de este repositorio:
   `C:\Users\Hector\Documents\GitHub\youtube-transcript-api`

2. Ejecuta:

```
python get_transcript.py
```

3. Cuando te lo pida, pega la URL del video y presiona Enter:

```
Pega la URL del video de YouTube: https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

4. Salida esperada:

```
[INFO] Obteniendo transcripcion para video ID: dQw4w9WgXcQ ...

[OK] Transcripcion guardada en: transcript_dQw4w9WgXcQ.txt
    ( 61 fragmentos )
```

5. El archivo generado queda en la misma carpeta donde ejecutaste el script,
   con nombre `transcript_<ID_del_video>.txt`, codificado en UTF-8.

---

## Formatos de URL compatibles

El script extrae el ID del video de cualquiera de estos formatos:

- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://www.youtube.com/shorts/VIDEO_ID`
- `https://www.youtube.com/embed/VIDEO_ID`
- URLs antiguas con `/v/VIDEO_ID`
- Cualquier URL que contenga `?v=VIDEO_ID` o `&v=VIDEO_ID`

Si pegas un texto que no contiene ninguna de esas estructuras, el script muestra
un mensaje de error y termina sin hacer nada.

---

## Idioma de la transcripcion

Por defecto el script busca **espanol** primero (`es`) y, si el video no tiene
transcripcion en espanol, intenta **ingles** (`en`).

Esto esta definido en esta linea del script (funcion `main`):

```python
fetched = ytt_api.fetch(video_id, languages=["es", "en"])
```

Para cambiar la prioridad de idiomas, edita esa lista. Ejemplos:

- Solo ingles: `languages=["en"]`
- Aleman primero, luego espanol e ingles: `languages=["de", "es", "en"]`

Nota: si YouTube solo tiene subtitulos autogenerados en un idioma distinto a los
solicitados, la busqueda fallara con `NoTranscriptFound`. En ese caso prueba
agregando ese idioma a la lista.

---

## Formato de salida

El archivo `.txt` contiene solo el texto de la transcripcion (sin marcas de tiempo),
con cada fragmento separado por saltos de linea, gracias al `TextFormatter` de la
libreria (`youtube_transcript_api/formatters.py`).

Otros formatos disponibles en la libreria, por si quieres extender el script:

| Formatter | Salida |
|---|---|
| `TextFormatter` | Texto plano (el que usa el script) |
| `JSONFormatter` | JSON con texto, inicio y duracion |
| `SRTFormatter` | Subtitulos .srt con timestamps |
| `WebVTTFormatter` | Subtitulos .vtt |
| `PrettyPrintFormatter` | Representacion legible de los datos crudos |

---

## Errores comunes y que significan

| Mensaje | Significado | Que hacer |
|---|---|---|
| `[-] No pude extraer el ID...` | La URL pegada no coincide con ningun formato conocido | Verifica que sea una URL de video de YouTube valida |
| `NoTranscriptFound` | El video no tiene transcripcion en `es` ni `en` | Prueba otros idiomas editando `languages=[...]` |
| `TranscriptsDisabled` | El autor del video desactivo los subtitulos | No hay solucion para ese video |
| `VideoUnavailable` | El video fue eliminado o es privado | Nada que hacer |
| `VideoUnplayable` | El video no se puede reproducir (region, eliminacion parcial, etc.) | Revisar los detalles que imprime el script |
| `AgeRestricted` | Video con restriccion de edad | Requeriria autenticacion con cookies, hoy no soportada por la libreria |
| `RequestBlocked` / `IpBlocked` | YouTube bloqueo tu IP (muchas peticiones, IP de nube/VPN) | Cambia de red/IP o usa proxies residenciales (ver abajo) |

### Sobre bloqueos de IP

YouTube bloquea con frecuencia las IPs de servicios cloud (AWS, GCP, Azure) y
tambien bloquea IPs que hacen demasiadas peticiones. Si te pasa esto desde tu casa,
espera un rato o reinicia el router; para uso intensivo la libreria soporta proxies
residenciales via `WebshareProxyConfig` (ver README.md, seccion "Working around IP bans").

---

## Como actualizar este repositorio

Este repositorio tiene dos remotos configurados:

| Remoto | Apunta a | Para que sirve |
|---|---|---|
| `origin` | Tu fork: https://github.com/HectorOrlando/youtube-transcript-api | Donde se guardan tus cambios (respaldo en la nube) |
| `upstream` | El repo original: https://github.com/jdepoix/youtube-transcript-api | De donde llegan las mejoras del autor |

Cuando el autor publique mejoras, recibir y respaldar es tan simple como:

```
git pull upstream master
git push origin master
```

Tus archivos personales (`get_transcript.py`, `COMO_USAR.md` y los archivos
`transcript_*.txt`) NO existen en el repositorio del autor, por lo que el `pull`
nunca generara conflictos.

Para ver si hay actualizaciones sin aplicarlas todavia:

```
git fetch upstream
git log HEAD..upstream/master --oneline
```

---

## Notas tecnicas

- El ID del video NO es la URL completa: es el codigo de 11 caracteres, ej.
  `dQw4w9WgXcQ`.
- Los archivos generados no se sobreescriben entre videos distintos (el nombre
  incluye el ID). Si corres dos veces el mismo video, el archivo se reemplaza.
- Este script depende de endpoints no documentados de YouTube: puede dejar de
  funcionar si YouTube cambia su API.
