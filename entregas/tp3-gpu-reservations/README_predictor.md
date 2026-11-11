# Predictor del Grupo 11 — TP3, cancelación de reservas de GPU

Predice `canceled_job` (1 = la reserva se cancela, 0 = se ejecuta) a partir de filas del CSV `gpu_resource_reservations`.

## Contenido

- `predictor_v1_Grupo_11.py`: funciones `predictor_v1_Grupo_11(X)` y `predictor_v1_Grupo_11_proba(X)`.
- `predictor_v1_Grupo_11.joblib`: modelo entrenado. Tiene que estar en la misma carpeta que el `.py`.
- `requirements.txt`: versiones exactas con que se entrenó el modelo.

## Instalación

Requiere Python 3.11 o posterior.

```bash
pip install -r requirements.txt
```

## Uso desde Python

```python
import pandas as pd
from predictor_v1_Grupo_11 import predictor_v1_Grupo_11, predictor_v1_Grupo_11_proba

X = pd.read_csv('datos.csv')
y_pred = predictor_v1_Grupo_11(X)          # array de 0 y 1, una predicción por fila
p_cancel = predictor_v1_Grupo_11_proba(X)  # probabilidad de cancelación
```

`X` puede ser:

- un DataFrame con las columnas del CSV; las que sobran, incluida `canceled_job`, se ignoran;
- un array con las 33 columnas del CSV sin `canceled_job`, en el orden del CSV;
- un array con las 34 columnas del CSV completo; la primera, `canceled_job`, se ignora;
- una sola fila, como array o como `pandas.Series`.

Los faltantes pueden venir como `NaN`, igual que en el CSV.

## Uso desde la terminal

```bash
python predictor_v1_Grupo_11.py predecir datos.csv predicciones.csv
```

## Si el modelo no carga

Un modelo guardado de scikit-learn puede no cargar con otra versión de la librería. En ese caso, conviene instalar las versiones de `requirements.txt` o regenerar el `.joblib` con la misma receta, en un minuto aproximadamente:

```bash
python predictor_v1_Grupo_11.py entrenar gpu_resource_reservations.csv
```

## Modelo

- **Algoritmo:** promedio de las probabilidades de un Random Forest de 100 árboles y un modelo de gradient boosting (`HistGradientBoostingClassifier`). Predice que la reserva se cancela si esa probabilidad es de 0,40 o más, el umbral que maximiza la balanced accuracy.
- **Entrenamiento:** las 47.842 filas del CSV.
- **Columnas que no se usan:**
  - `execution_status` y `execution_status_date` describen el resultado de la reserva;
  - `assigned_gpu_type` y `queue_wait_time` se conocen recién cuando se asignan los recursos;
  - `high_value_client` no está documentada;
  - `total_processes` y `total_gpu_hours` son sumas de otras columnas.

  Pueden venir o no en `X`.
- **Rendimiento esperado:** estimado en la sección 12 del notebook del grupo. Depende de cuántas reservas del conjunto evaluado tengan una copia idéntica en el CSV de entrenamiento:
  - con reservas del mismo conjunto que el CSV, AUC de alrededor de 0,96 y balanced accuracy de alrededor de 0,89 (en un test reservado del 20 %: 0,960 y 0,888);
  - con reservas nuevas, sin copias en el entrenamiento, AUC de alrededor de 0,94 y balanced accuracy de alrededor de 0,86 (validación cruzada agrupada);
  - con reservas individuales, sin copias ni lotes, AUC de alrededor de 0,89 y balanced accuracy de alrededor de 0,79.
