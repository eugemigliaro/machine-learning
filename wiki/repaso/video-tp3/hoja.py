"""Arma una hoja de contacto con cuadros de un video (solo para revisar)."""
import subprocess, sys
from pathlib import Path
from PIL import Image
video, salida, *tiempos = sys.argv[1:]
ims = []
for t in tiempos:
    png = Path(salida).with_suffix(f'.{t}.png')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', t, '-i', video, '-frames:v', '1', str(png)], check=True)
    ims.append(Image.open(png))
w, h = ims[0].size
cols = 3
filas = (len(ims) + cols - 1) // cols
hoja = Image.new('RGB', (w * cols, h * filas))
for i, im in enumerate(ims):
    hoja.paste(im, ((i % cols) * w, (i // cols) * h))
hoja.save(salida)
for t in tiempos:
    Path(salida).with_suffix(f'.{t}.png').unlink()
