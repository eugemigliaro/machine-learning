"""Genera la narración con Piper, un WAV por segmento del guion.

Se ejecuta con el intérprete donde está instalado piper-tts, por ejemplo:

    ~/.local/share/uv/tools/piper-tts/bin/python generar_audio.py

Escribe `build/audio/<clave>.wav` y `build/audio/duraciones.json`, con la
duración de cada segmento, el inicio de cada oración (para sincronizar las
animaciones) y la fuente que se muestra en pantalla. Solo regenera los
segmentos cuyo texto cambió.
"""

import hashlib
import json
import os
import sys
import wave
from pathlib import Path

import numpy as np
from piper import PiperVoice, SynthesisConfig

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
from narracion import segmentos, texto_hablado  # noqa: E402

VOZ = Path(os.environ.get("VOZ_PIPER", Path.home() / ".local/share/piper/voces/es_AR-daniela-high.onnx"))
SALIDA = Path(os.environ.get("VIDEO_BUILD", AQUI / "build")) / "audio"
PAUSA_ORACION = 0.28  # segundos de silencio entre oraciones
PAUSA_FINAL = 0.35  # silencio al final de cada segmento
VELOCIDAD = 1.0  # length_scale de Piper: mayor es más lento


def main() -> None:
    SALIDA.mkdir(parents=True, exist_ok=True)
    indice_path = SALIDA / "duraciones.json"
    indice = json.loads(indice_path.read_text()) if indice_path.exists() else {}
    voz = None
    config = SynthesisConfig(length_scale=VELOCIDAD)

    nuevo = {}
    for escena, clave, texto, fuente in segmentos():
        hablado = texto_hablado(texto)
        firma = hashlib.sha256(f"{VOZ.name}|{VELOCIDAD}|{hablado}".encode()).hexdigest()[:16]
        wav_path = SALIDA / f"{clave}.wav"
        previo = indice.get(clave)
        if previo and previo.get("firma") == firma and wav_path.exists():
            previo.update(escena=escena, fuente=fuente)
            nuevo[clave] = previo
            continue

        if voz is None:
            voz = PiperVoice.load(str(VOZ))
        partes, inicios, t = [], [], 0.0
        tasa = voz.config.sample_rate
        for chunk in voz.synthesize(hablado, config):
            inicios.append(round(t, 3))
            audio = chunk.audio_int16_array
            partes.append(audio)
            t += len(audio) / tasa
            silencio = np.zeros(int(PAUSA_ORACION * tasa), dtype=np.int16)
            partes.append(silencio)
            t += len(silencio) / tasa
        partes[-1] = np.zeros(int(PAUSA_FINAL * tasa), dtype=np.int16)
        audio = np.concatenate(partes)
        with wave.open(str(wav_path), "wb") as wav:
            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(tasa)
            wav.writeframes(audio.tobytes())
        nuevo[clave] = {
            "escena": escena,
            "fuente": fuente,
            "duracion": round(len(audio) / tasa, 3),
            "oraciones": inicios,
            "firma": firma,
        }
        print(f"{clave:>4}  {nuevo[clave]['duracion']:6.1f} s  {len(inicios)} oraciones")

    indice_path.write_text(json.dumps(nuevo, indent=1, ensure_ascii=False))
    total = sum(v["duracion"] for v in nuevo.values())
    por_escena = {}
    for v in nuevo.values():
        por_escena[v["escena"]] = por_escena.get(v["escena"], 0) + v["duracion"]
    for escena, dur in por_escena.items():
        print(f"{escena:<14} {dur / 60:5.2f} min")
    print(f"Total de narración: {total / 60:.2f} min")


if __name__ == "__main__":
    main()
