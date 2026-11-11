# TP3 — Reservas de GPU (Grupo 11)

Resolución del TP3 de optimización de modelos: predecir si una reserva de infraestructura GPU se cancelará antes de su ejecución. La consigna oficial está registrada como `[P03]` y el anuncio de la competencia como `[P04]`.

## Fuente

El dataset está registrado como `[D04]`. El notebook lo lee como `gpu_resource_reservations.csv`, en su misma carpeta, para que la copia entregada no dependa de la estructura del repositorio. En el repo ese archivo es un enlace simbólico al original, que no se modifica:

```text
gpu_resource_reservations.csv -> ../../material/catedra/datasets/gpu_resource_reservations.csv
```

Los entregables (notebook, predictor y diapositivas) no citan la wiki, el catálogo de fuentes ni otros archivos del repo: tienen que entenderse solos. Las citas `[P03]`, `[T11, p. N]`, etc. quedan sólo en este README, en `decisiones.md` y en el guion.

## Entorno

Se usan las mismas dependencias que en el TP2. En Ubuntu 26.04 se instalan con `apt`:

```bash
sudo apt install python3-sklearn python3-pandas python3-matplotlib python3-seaborn \
  jupyter-notebook python3-ipykernel python3-nbconvert
```

`requirements.txt` documenta los rangos de versión equivalentes para instalar con `pip` dentro de un entorno virtual. Para ejecutar el notebook completo sin interfaz:

```bash
python3 -m nbconvert --to notebook --execute --inplace tp3_gpu_reservations.ipynb
```

La primera ejecución completa tarda más de una hora, sobre todo por Random Forest y la búsqueda de hiperparámetros de gradient boosting. Los resultados de la validación cruzada quedan en `cache/` (no versionado) y las ejecuciones siguientes tardan un par de minutos. Si se modifica `prepare_features` o la definición de los folds, hay que borrar `cache/`.

Verificado con Python 3.14.4, scikit-learn 1.7.2, pandas 2.3.3, matplotlib 3.10.7 y seaborn 0.13.2.

## Predictor

`predictor_v1_Grupo_11.py` tiene las transformaciones fijas, la receta del modelo final y las funciones `predictor_v1_Grupo_11(X)` y `predictor_v1_Grupo_11_proba(X)`. Al ejecutar el notebook, la sección 12.6:

- entrena el modelo con todo el CSV y lo guarda en `predictor_v1_Grupo_11.joblib`;
- arma `predictor_v1_Grupo_11.zip` con el `.py`, el `.joblib`, `requirements_predictor.txt` (como `requirements.txt`) y `README_predictor.md` (como `README.md`);
- prueba el paquete descomprimido en un proceso nuevo.

El `.zip` es lo que se envía por mail. El `.joblib` y el `.zip` no se versionan (están en `.gitignore`): pesan 36 MB y se regeneran en cada ejecución del notebook o con `python predictor_v1_Grupo_11.py entrenar <dataset.csv>`. La sección 12.1 verifica que reentrenar reproduce las mismas predicciones.

Para comprobar que un `.zip` es el mismo que el generado el 09/11 (scikit-learn 1.7.2), su SHA-256 es:

```
07629fc333423bc0ec4271a0e44edc7d6b70e7d56e6d432536e1756db9dce0f2  predictor_v1_Grupo_11.zip
```

Guardá fuera del repositorio una copia del `.zip` exacto que se envíe, porque el `.joblib` depende de las versiones de `requirements_predictor.txt`.

## Presentación

- **Diapositivas:** [artifact de Slides](https://claude.ai/artifact/RTKkJodPsGvyJakUPFCy26), 13 diapositivas. Se presentan y se exportan a PDF o PowerPoint desde el artifact. El link es privado hasta que se comparte desde el menú del artifact.
- **Fuente versionada:** `presentacion/project/`. El índice es `deck.json` (título, orden y secciones) y cada diapositiva es un HTML en `slides/`. El artifact se publica desde esos archivos, así que el repositorio guarda exactamente lo que muestra.
- **Cambios:** se editan los archivos y se vuelven a publicar en el mismo artifact. Si alguien edita las diapositivas en la web, hay que bajar esos archivos del artifact a `presentacion/project/` antes de commitear, para que no queden desfasados.
- **Guion:** `guion_defensa.md` tiene el reparto entre oradores, qué decir en cada diapositiva y las preguntas probables con sus respuestas.

## Entregables y fechas

- Defensa: 11/11/2026. La presentación, el predictor y el código se envían 24 horas antes. [P03, p. 1]
- Predictor: `predictor_v1_Grupo_11(X)`, enviado por mail. [P03, p. 3] La versión que se envíe antes de la defensa cuenta para el leaderboard del 11/11. Si en la defensa cambia algún supuesto, se puede enviar una nueva versión antes del 18/11 a las 16:00. [P04]

## Estado

- [x] Paso 0: carpeta, decisiones previas y notebook.
- [x] Paso 1: integridad, leakage, duplicados, reserva de test y EDA de desarrollo (secciones 1 a 4 del notebook).
- [x] Paso 2: métricas, validación cruzada y baseline (punto 2 de la consigna, secciones 5 y 6 del notebook).
- [x] Paso 3: análisis de errores, curvas de aprendizaje, estrategia data-centered y adquisición de datos (punto 3, secciones 7 a 10 del notebook).
- [x] Paso 4: feature engineering, selección de modelos, búsqueda de hiperparámetros y combinación (punto 4, sección 11 del notebook).
- [x] Paso 5: modelo final, evaluación en test y predictor (punto 5, sección 12 del notebook).
- [x] Paso 6: presentación y guion de defensa.
