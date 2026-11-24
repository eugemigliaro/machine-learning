# Video: la teoría del TP3 contada con nuestra resolución

Video de unos 15 minutos, al estilo de 3Blue1Brown, que explica la teoría nueva de las clases 11 y 12 a alguien que llegó hasta el TP2. Cada concepto se aplica enseguida a nuestra resolución del TP3 (Grupo 11). Está pensado para repasar antes de la defensa.

El video no se versiona porque se regenera desde estos archivos; ver [Cómo regenerarlo](#cómo-regenerarlo). Al generarlo queda en `tp3-teoria-y-resolucion.mp4`, en esta carpeta, con un capítulo por paso.

## Capítulos

| Capítulo | Teoría | Nuestra resolución |
|---|---|---|
| 0. El problema | Qué cambia del TP2 al TP3: de elegir un modelo a entender por qué se equivoca. [P03, p. 2] [P03, p. 3] | 47.842 reservas, 41,7 % canceladas. [D04] |
| 1. Validar según el uso | La relación train–validación debe ser la misma que train–uso [T11, p. 71] [T11, p. 72]; k-fold estratificada [T11, p. 74]; grupos y leakage indirecto [T11, p. 76] [T11, p. 78]. | El 33 % de las filas son copias: reservas en lote. Validación principal al azar y control agrupado: AUC 0,956 contra 0,937. |
| 2. Diagnosticar | Sesgo, varianza y error irreducible [T11, p. 5]; árbol de diagnóstico [T11, p. 11]; curvas de validación [T11, p. 19] y de aprendizaje [T11, p. 21] [T11, p. 22] [T11, p. 23]. | 79 grupos idénticos con etiquetas distintas; la brecha crece con la profundidad (0,006 a 0,018); la curva agrupada se aplana: el límite es la información. |
| 3. Analizar errores | Centrado en el modelo frente a centrado en datos [T11, p. 31] [T11, p. 43]; tags y las dos proporciones [T11, p. 34]; brecha por frecuencia [T11, p. 35]; data augmentation [T11, p. 56] [T11, p. 60]. | Las reservas únicas de `cloud_marketplace`: 41 % de las filas y 77 % de los errores; efecto de composición en `basic` y `GPU_T4`; datos a adquirir. |
| 4. Optimizar | Bagging frente a boosting [T12, p. 20] [T12, p. 21]; gradient boosting [T12, p. 4] [T12, p. 5] [T12, p. 6]; implementaciones [T12, p. 10]; stacking y correlación [T12, p. 24] [T12, p. 25] [T12, p. 26]. | Regla de adopción fija; se adoptan `max_features = 0,2`, el promedio con gradient boosting y 100 árboles; +0,0018 de AUC, concentrado en las cohortes difíciles. |
| 5. Modelo final y producción | La validación elige una receta [T11, p. 68]; del POC a producción [T12, p. 34]; la función predictora [T12, p. 49]; data y concept drift [T12, p. 40] [T12, p. 41]. | La competencia mide balanced accuracy: umbral 0,40; test: AUC 0,960 y balanced accuracy 0,888; tres escenarios de rendimiento y la pista del leaderboard; el predictor empaquetado. |

Los números salen de `entregas/tp3-gpu-reservations/tp3_gpu_reservations.ipynb` y `entregas/tp3-gpu-reservations/decisiones.md`, en su estado del 11/11, que ya incluye la actualización posterior al leaderboard: balanced accuracy y umbral 0,40. Cada segmento muestra su fuente en la esquina inferior derecha, y las inferencias propias están marcadas como tales.

**Para tener en cuenta:**

- La animación de boosting usa datos de juguete, no los del TP.
- Las distribuciones de probabilidad del capítulo 3, los folds del capítulo 4 y las probabilidades del ejemplo de combinación son esquemas, y lo dicen en pantalla.
- La fórmula del umbral según los costos es conocimiento general, no está en las clases.

## Archivos

| Archivo | Qué hace |
|---|---|
| `narracion.py` | Guion narrado, segmento por segmento, con la fuente de cada uno, y el mapa de pronunciación de los términos en inglés. |
| `generar_audio.py` | Genera la voz con Piper (`es_AR-daniela-high`) y guarda la duración de cada oración para sincronizar las animaciones. |
| `base.py` | Estilo común (colores, fuentes) y la clase `Escena`, que reproduce cada segmento y espera a que termine. |
| `c0_intro.py` a `c5_final.py` | Las escenas de Manim, una por capítulo. |
| `construir_video.py` | Renderiza las escenas en paralelo y las une con ffmpeg, con capítulos. |
| `hoja.py` | Arma una hoja de cuadros de un video para revisarlo sin verlo entero. |

## Cómo regenerarlo

Requisitos:

- Manim Community 0.22 (no necesita LaTeX);
- ffmpeg;
- Piper con la voz `es_AR-daniela-high` en `~/.local/share/piper/voces/`;
- la fuente P052, que viene con las fuentes URW de Ghostscript.

```bash
cd wiki/repaso/video-tp3
~/.local/share/uv/tools/piper-tts/bin/python generar_audio.py   # narración (solo los segmentos que cambiaron)
python3 construir_video.py --borrador                           # 480p para revisar
python3 construir_video.py                                      # 1080p final
```

Para cambiar el texto, se edita `narracion.py` y se vuelve a ejecutar todo. Las animaciones se sincronizan con el inicio de cada oración, así que conviene no cambiar la cantidad de oraciones de un segmento sin revisar la escena correspondiente.

Los archivos intermedios quedan en `build/`, que tampoco se versiona.

`construir_video.py` renderiza siempre sin la caché de Manim. Cuando Manim reutiliza una animación de la caché, descarta el sonido que se agrega justo después, y se pierde la narración de ese segmento. Al terminar, el script revisa que cada escena tenga todo el audio y ningún silencio de más de 3 segundos.
