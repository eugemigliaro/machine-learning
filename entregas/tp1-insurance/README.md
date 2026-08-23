# TP1 — Insurance Charges

Resolución del TP1 de regresión y evaluación con el dataset Insurance Charges.

## Fuente

El dataset está registrado como `[D01]` y se lee sin modificar desde:

```text
../../material/externo/datasets/insurance.csv
```

La consigna oficial está registrada como `[P01]`.

## Entorno

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
jupyter lab
```

Abrir `tp1_insurance.ipynb`. El notebook fija semillas aleatorias, valida el esquema del CSV y reserva test antes del EDA utilizado para tomar decisiones.

El notebook fue verificado con Python 3.14.4 y las dependencias globales documentadas en `requirements.txt`.

## Estado

- Dataset elegido y registrado.
- Proporción de test decidida: 10 %.
- Inspección de integridad preparada.
- Una de las dos filas exactamente duplicadas se elimina de la copia de trabajo; `[D01]` permanece intacto.
- Split reproducible ejecutado y verificado: 1.203 casos de desarrollo y 134 de test.
- EDA de desarrollo ejecutado: calidad, distribuciones, relaciones, IQR global e IQR separado por `smoker`.
- Decisiones de outliers, características y preprocesamiento confirmadas.
- Regresión lineal evaluada con 10-fold CV: RMSE medio 6.135,04 en train y 6.157,57 en validación.
- Grados polinómicos 2 y 3 comparados: grado 2 obtiene el menor RMSE de validación, 4.908,79.
- Pendiente: evaluar regularización L1 sobre el candidato de grado 2.
