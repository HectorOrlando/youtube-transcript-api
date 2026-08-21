import re
import sys

from pathlib import Path

import requests

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from youtube_transcript_api._errors import (
    NoTranscriptFound,
    TranscriptsDisabled,
    VideoUnavailable,
    VideoUnplayable,
    AgeRestricted,
    RequestBlocked,
    CouldNotRetrieveTranscript,
)

CARPETA_BASE = Path("transcripts")

# Evita que print() falle si un titulo trae caracteres fuera de la codepage cp1252
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(errors="replace")
    sys.stderr.reconfigure(errors="replace")


def extract_video_id(url: str) -> str | None:
    """Extrae el ID del video de diversas formas de URL de YouTube."""
    url = url.strip()

    # youtube.com/watch?v=VIDEO_ID (o &xx=... despues)
    m = re.search(r"(?:v=|\/vi\/)([0-9A-Za-z_-]{11})", url)
    if m:
        return m.group(1)

    # youtu.be/VIDEO_ID (shortened)
    m = re.search(r"youtu\.be\/([0-9A-Za-z_-]{11})", url)
    if m:
        return m.group(1)

    # /embed/VIDEO_ID
    m = re.search(r"\/embed\/([0-9A-Za-z_-]{11})", url)
    if m:
        return m.group(1)

    # /v/VIDEO_ID (old format)
    m = re.search(r"\/v\/([0-9A-Za-z_-]{11})", url)
    if m:
        return m.group(1)

    # YouTube Shorts: /shorts/VIDEO_ID
    m = re.search(r"\/shorts\/([0-9A-Za-z_-]{11})", url)
    if m:
        return m.group(1)

    # Estructura de URL con ?v= o &v=
    m = re.search("[?&]v=([0-9A-Za-z_-]{11})", url)
    if m:
        return m.group(1)

    return None


def sanitize_name(nombre: str) -> str:
    """Convierte un texto en nombre valido de archivo/carpeta para Windows."""
    limpio = re.sub(r'[\\/:*?"<>|]', "_", nombre.strip())
    limpio = re.sub(r"\s+", " ", limpio)
    return limpio[:200].rstrip(" .")


def get_video_title(video_id: str) -> str | None:
    """Consulta el titulo publico del video via oEmbed (sin API key)."""
    try:
        resp = requests.get(
            "https://www.youtube.com/oembed",
            params={
                "url": f"https://www.youtube.com/watch?v={video_id}",
                "format": "json",
            },
            timeout=10,
        )
        if resp.ok:
            titulo = resp.json().get("title")
            if titulo and titulo.strip():
                return titulo.strip()
    except (requests.RequestException, ValueError):
        pass
    return None


def choose_output_dir() -> Path:
    """Pregunta al usuario donde guardar y devuelve la carpeta elegida."""
    while True:
        print("\nDonde guardar la transcripcion?")
        print("  [1] Carpeta por defecto (transcripts)")
        print("  [2] Crear una subcarpeta dentro de transcripts")
        print("  [3] Usar una subcarpeta existente de transcripts")
        opcion = input("Opcion: ").strip()

        if opcion == "1":
            CARPETA_BASE.mkdir(exist_ok=True)
            return CARPETA_BASE

        if opcion == "2":
            nombre = sanitize_name(input("Nombre de la nueva carpeta: "))
            if not nombre:
                print("[-] Nombre invalido, intenta de nuevo.")
                continue
            destino = CARPETA_BASE / nombre
            destino.mkdir(parents=True, exist_ok=True)
            return destino

        if opcion == "3":
            if not CARPETA_BASE.is_dir():
                print("[-] La carpeta 'transcripts' aun no existe.")
                continue
            subcarpetas = sorted(c.name for c in CARPETA_BASE.iterdir() if c.is_dir())
            if not subcarpetas:
                print("[-] Todavia no hay subcarpetas dentro de 'transcripts'.")
                continue
            print()
            for indice, carpeta in enumerate(subcarpetas, start=1):
                print(f"  [{indice}] {carpeta}")
            eleccion = input("Numero de carpeta: ").strip()
            if eleccion.isdigit() and 1 <= int(eleccion) <= len(subcarpetas):
                return CARPETA_BASE / subcarpetas[int(eleccion) - 1]
            print("[-] Numero invalido, intenta de nuevo.")
            continue

        print("[-] Opcion invalida, elige 1, 2 o 3.")


def main() -> None:
    url = input("Pega la URL del video de YouTube: ").strip()
    video_id = extract_video_id(url)

    if not video_id:
        print("[-] No pude extraer el ID del video de la URL. Formatos compatibles:")
        print("    - https://www.youtube.com/watch?v=VIDEO_ID")
        print("    - https://youtu.be/VIDEO_ID")
        print("    - https://www.youtube.com/shorts/VIDEO_ID")
        print("    - https://www.youtube.com/embed/VIDEO_ID")
        sys.exit(1)

    print(f"\n[INFO] Obteniendo transcripcion para video ID: {video_id} ...")

    try:
        ytt_api = YouTubeTranscriptApi()
        fetched = ytt_api.fetch(video_id, languages=["es", "en"])

        # Convertir a texto plano usando TextFormatter
        formatter = TextFormatter()
        text_output = formatter.format_transcript(fetched)

        carpeta_destino = choose_output_dir()

        titulo = get_video_title(video_id)
        if titulo:
            sugerido = sanitize_name(titulo) or video_id
            print(f"\n[INFO] Titulo detectado: {titulo}")
        else:
            sugerido = video_id
            print("\n[INFO] No se pudo detectar el titulo del video.")

        respuesta = input(f"Guardar como [{sugerido}] (Enter=aceptar): ").strip()
        base_nombre = sanitize_name(respuesta) or sugerido

        output_path = carpeta_destino / f"{base_nombre}.txt"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text_output)

        print(f"\n[OK] Transcripcion guardada en: {output_path}")
        print(f"    ( {len(fetched.snippets)} fragmentos )")

    except NoTranscriptFound as e:
        print(f"\n[-] No se encontraron subtitulos/transcripciones para este video.")
        print(f"    Causa: {e.cause}")
    except TranscriptsDisabled:
        print("\n[-] Las transcripciones estan deshabilitadas para este video.")
    except VideoUnavailable:
        print("\n[-] El video ya no está disponible.")
    except VideoUnplayable as e:
        print(f"\n[-] El video es inplayable: {e.reason}")
        if e.sub_reasons:
            for sr in e.sub_reasons:
                print(f"     - {sr}")
    except AgeRestricted:
        print("\n[-] El video es restringido por edad. No se puede acceder sin autenticacion.")
    except RequestBlocked as e:
        print("\n[-] Tu IP ha sido bloqueada por YouTube.")
        print("    Causa:", e.cause.strip())
        print("    Solucion: usa proxies residenciales (Webshare) o ejecuta desde otra red/IP.")
    except CouldNotRetrieveTranscript as e:
        print(f"\n[-] No se pudo recuperar la transcripcion.")
        print(f"    Causa: {e.cause}")
    except Exception as e:
        print(f"\n[-] Error inesperado: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
