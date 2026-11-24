"""Renderiza las escenas con Manim y las une en un solo video con capítulos.

Uso (desde esta carpeta, después de `generar_audio.py`):

    python3 construir_video.py            # 1080p, 30 cuadros por segundo
    python3 construir_video.py --borrador # 480p, 15 cuadros por segundo
    python3 construir_video.py --solo-unir # une las escenas ya renderizadas

El resultado queda en `tp3-teoria-y-resolucion.mp4` (o `-borrador.mp4`).
"""

import argparse
import json
import os
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

AQUI = Path(__file__).resolve().parent
BUILD = Path(os.environ.get("VIDEO_BUILD", AQUI / "build"))

ESCENAS = [
    ("c0_intro.py", "Intro", "0. El problema"),
    ("c1_validacion.py", "Validacion", "1. Validar según el uso"),
    ("c2_diagnostico.py", "Diagnostico", "2. Diagnosticar"),
    ("c3_errores.py", "Errores", "3. Analizar errores"),
    ("c4_optimizacion.py", "Optimizacion", "4. Optimizar"),
    ("c5_final.py", "Final", "5. Modelo final y producción"),
]


def ruta(archivo, escena, borrador):
    carpeta = "480p15" if borrador else "1080p30"
    return BUILD / "media" / "videos" / Path(archivo).stem / carpeta / f"{escena}.mp4"


def renderizar(archivo, escena, borrador):
    # Sin caché: cuando Manim reutiliza una animación cacheada, descarta el sonido que se agrega
    # justo después, y la narración de ese segmento se pierde.
    calidad = ["-ql"] if borrador else ["-r", "1920,1080", "--fps", "30"]
    log = BUILD / f"log_{escena}.txt"
    with log.open("w") as salida:
        subprocess.run(["manim", *calidad, "--disable_caching", "--media_dir", str(BUILD / "media"), archivo, escena],
                       cwd=AQUI, stdout=salida, stderr=subprocess.STDOUT, check=True)
    return ruta(archivo, escena, borrador)


def duracion(video, flujo=None):
    opciones = ["-show_entries", "format=duration"] if flujo is None else \
        ["-select_streams", flujo, "-show_entries", "stream=duration"]
    salida = subprocess.run(["ffprobe", "-v", "error", *opciones, "-of", "csv=p=0", str(video)],
                            capture_output=True, text=True, check=True)
    return float(salida.stdout.strip())


def problemas_de_audio(video, escena):
    """Detecta narración perdida: audio más corto que el guion o silencios de más de 3 segundos."""
    narracion = json.loads((BUILD / "audio" / "duraciones.json").read_text())
    esperado = sum(v["duracion"] for v in narracion.values() if v["escena"] == escena)
    problemas = []
    if duracion(video, "a") < esperado - 1.0:
        problemas.append(f"audio de {duracion(video, 'a'):.1f} s para {esperado:.1f} s de narración")
    salida = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(video), "-map", "0:a",
                             "-af", "silencedetect=noise=-35dB:d=3", "-f", "null", "-"],
                            capture_output=True, text=True).stderr
    problemas += [linea.split("]")[-1].strip() for linea in salida.splitlines() if "silence_start" in linea]
    return problemas


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--borrador", action="store_true")
    parser.add_argument("--procesos", type=int, default=3)
    parser.add_argument("--solo-unir", action="store_true")
    args = parser.parse_args()
    if not (BUILD / "audio" / "duraciones.json").exists():
        raise SystemExit("Falta la narración: ejecutá primero generar_audio.py con el Python de piper-tts.")

    if args.solo_unir:
        videos = [ruta(a, e, args.borrador) for a, e, _ in ESCENAS]
    else:
        with ThreadPoolExecutor(args.procesos) as pool:
            videos = list(pool.map(lambda e: renderizar(e[0], e[1], args.borrador), ESCENAS))
    for (_, escena, _), video in zip(ESCENAS, videos):
        problemas = problemas_de_audio(video, escena)
        if problemas:
            raise SystemExit(f"{escena}: posible narración perdida: {problemas}")

    lista = BUILD / "concat.txt"
    lista.write_text("".join(f"file '{v}'\n" for v in videos))
    metadatos = [";FFMETADATA1"]
    inicio = 0.0
    for video, (_, _, titulo) in zip(videos, ESCENAS):
        fin = inicio + duracion(video)
        metadatos += ["[CHAPTER]", "TIMEBASE=1/1000", f"START={int(inicio * 1000)}", f"END={int(fin * 1000)}",
                      f"title={titulo}"]
        print(f"{int(inicio // 60):02d}:{int(inicio % 60):02d}  {titulo}")
        inicio = fin
    (BUILD / "capitulos.txt").write_text("\n".join(metadatos) + "\n")

    nombre = "tp3-teoria-y-resolucion-borrador.mp4" if args.borrador else "tp3-teoria-y-resolucion.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lista),
                    "-i", str(BUILD / "capitulos.txt"), "-map_metadata", "1", "-map", "0", "-c", "copy",
                    "-movflags", "+faststart", str(AQUI / nombre)], check=True)
    print(f"Listo: {AQUI / nombre} ({inicio / 60:.1f} min)")


if __name__ == "__main__":
    main()
