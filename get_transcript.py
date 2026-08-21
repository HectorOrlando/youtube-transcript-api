import re
import sys

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

        # Guardar en archivo .txt
        safe_id = video_id.replace("/", "_")
        output_path = f"transcript_{safe_id}.txt"
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