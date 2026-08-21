# TP1: regresión e introducción a la evaluación

## Datos administrativos

- Ciclo: 2026 Q2.
- Defensa indicada: 26/08/2026.
- Presentación: 10 minutos y 8 minutos de preguntas.
- Envío de presentación y código: 24 horas antes de la clase de defensa. [P01, p. 1]

Hay variantes incompatibles de duración en la clase introductoria; ver [Dudas y conflictos](../dudas-y-conflictos.md).

## Objetivo y alcance

El TP pide elegir uno de tres datasets (Bike Sharing, Insurance Charges o Wine Quality) y mantenerlo durante todo el trabajo para predecir una variable numérica. [P01, p. 1]

La entrega debe cubrir:

1. Una explicación breve de train/validación/test.
2. Identificación y tratamiento justificado de variables categóricas, faltantes y outliers.
3. Selección de características y escalado cuando corresponda.
4. Separación de train y test.
5. K-fold cross-validation usando solamente train.
6. Regresión lineal con error de train y validación.
7. Regresión polinómica para grados justificados y, opcionalmente, regularización L1 con algunos valores de `λ`.
8. Comparación mediante RMSE por grado y `λ`, elección del modelo y estimación de su rendimiento en datos nuevos. [P01, p. 1] [P01, p. 2] [P01, p. 3]

## Controles conceptuales

- No ajustar limpieza, encoding, escalado ni transformación polinómica con test. [T02, p. 94] [T02, p. 96]
- **Inferencia operativa:** en cada fold, ajustar el preprocesamiento solamente con la porción de entrenamiento del fold. Esto mantiene la separación que exige la consigna. [P01, p. 2] [T03, p. 12] [T03, p. 15]
- Elegir grado y `λ` por validación; usar test solamente para el RMSE final esperado en datos nuevos. [P01, p. 2] [P01, p. 3] [T02, p. 89]
- Reportar claramente errores de train y validación para diagnosticar complejidad, no solamente el mejor número. [P01, p. 2] [T02, p. 53] [T02, p. 77]

## Punto pendiente de confirmación

La consigna alterna “RMS” y “RMSE”; la teoría define la métrica como RMSE. [P01, p. 2], [T03, p. 87]
