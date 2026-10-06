# TP2: clasificación supervisada

## Datos administrativos

- Ciclo: 2026 Q2.
- Defensa indicada: 07/10/2026.
- Presentación: 10 minutos y 10 minutos de preguntas.
- Envío de presentación y código: 24 horas antes de la clase de defensa. [P02, p. 1]

La duración difiere de la del TP1 (10 + 8); ver [Dudas y conflictos](../dudas-y-conflictos.md). [P01, p. 1]

## Objetivo y dataset

Se usa el dataset **Bank Marketing**, de campañas telefónicas de un banco portugués. El objetivo es predecir si un cliente contratará un depósito a plazo fijo (`y = yes/no`) a partir de datos demográficos, de campañas previas y del contexto económico. Sirve para priorizar a qué clientes llamar. [P02, p. 1]

El párrafo introductorio de la consigna habla de "modelos de regresión para predecir una variable numérica". El resto del documento describe un problema de clasificación binaria; ver [Dudas y conflictos](../dudas-y-conflictos.md). [P02, p. 1]

La consigna enlaza a su página de Kaggle. [P02, p. 1] El archivo está registrado como D02 (`bank-additional-full.csv`) y su descripción de atributos como D03. La resolución está en `entregas/tp2-bank-marketing/`, y la [guía paso a paso](../repaso/tp2-resolucion-paso-a-paso.md) la explica junto con la teoría.

## Entregables por sección

1. **Preprocesamiento y EDA.** Un análisis básico, no exhaustivo, que incluya: balance de clases, distribución de algunas variables, relación de las predictoras con el objetivo, faltantes y categorías poco frecuentes, y diferencias entre quienes aceptan y quienes no. [P02, p. 1] Cada observación del EDA debe tener alguna consecuencia sobre el preprocesamiento, la selección de variables o la interpretación. Por ejemplo: excluir variables, tratar categóricas, escalar, agrupar categorías raras, crear variables o comparar con y sin variables problemáticas. [P02, p. 1]
2. **Clasificación.** Implementar con scikit-learn **Naive Bayes, SVM, KNN y Random Forest**. [P02, p. 2] Evaluarlos con k-fold cross-validation usando solamente el conjunto de entrenamiento. [P02, p. 2] Elegir **dos métricas** vistas en clase, justificarlas y usarlas para decidir el modelo. [P02, p. 2]
3. **Ajuste de hiperparámetros.** Evaluar al menos un hiperparámetro relevante con curvas de validación: SVM (`C` o kernel), KNN (número de vecinos, ponderación…) y RF (número de árboles, profundidad máxima…). Discutir overfitting y underfitting en al menos una curva. [P02, p. 2]
4. **Modelo final.** Elegir el modelo, entrenarlo y estimar su rendimiento esperado en datos nuevos con las métricas elegidas. [P02, p. 2]
5. **Conclusiones.** Explicar qué modelos funcionaron mejor y por qué, en relación con el EDA y con cómo funciona cada algoritmo. Comentar si los datos se ajustan a los supuestos de los modelos (variables correlacionadas, distribuciones no gaussianas, escalas distintas, relaciones no lineales). Cerrar con limitaciones, errores más relevantes para el problema y mejoras posibles. [P02, p. 2]

No hace falta describir cada método en la presentación, pero sí usar su funcionamiento para interpretar los resultados. [P02, p. 2]

### Consejos de presentación

- Explicar qué datos se usan en cada etapa y por qué. [P02, p. 3]
- Preferir gráficos a tablas de números, agregando el valor sobre el gráfico si hace falta. [P02, p. 3]
- Respetar los 10 minutos e incluir los números en las diapositivas. [P02, p. 3]

## Controles conceptuales

### Separación y leakage

- Separar train y test **antes** de cualquier transformación aprendida de los datos. Escalado, imputación y codificación se ajustan solo con train, dentro del pipeline. [P02, p. 1] [T02, p. 94] [T02, p. 96]
- **Inferencia operativa:** dentro de la validación cruzada, el preprocesamiento debe reajustarse en cada fold con su porción de entrenamiento. Por eso conviene que el escalado y el encoding formen parte del pipeline que se valida, y no un paso previo sobre todo train. [P02, p. 2] [T03, p. 12] [T03, p. 15]
- La consigna pide analizar variables que serían información **no disponible antes de la llamada**, es decir, en el momento en que el modelo operaría. [P02, p. 1] La documentación del dataset advierte que `duration`, la duración de la llamada, se conoce recién al terminarla y que determina fuertemente `y`. Recomienda descartarla en un modelo predictivo realista. [D03]
- El test se usa una sola vez, para la estimación final del punto 4; nunca para elegir modelo ni hiperparámetros. [P02, p. 2] [T02, p. 89] Tras elegir, el material propone reentrenar con todos los datos de desarrollo y evaluar en test. [T02, p. 88]

### Métricas

- Las métricas disponibles en la teoría son accuracy, precisión, recall, especificidad, valor predictivo negativo, FPR, curva ROC y AUC. [T04, p. 31] [T04, p. 35] [T04, p. 45] [T04, p. 50] F1 se nombra pero no se define. [T04, p. 24] Ver [Métricas de clasificación](metricas-de-clasificacion.md).
- La accuracy no distingue el tipo de error. [T04, p. 26] [T04, p. 27] **Inferencia:** si el EDA muestra clases desbalanceadas, la accuracy sola puede ser engañosa. Como la consigna pide justificar las métricas y nombrar los errores más relevantes, conviene que ambas decisiones salgan del costo de cada error en una campaña de marketing. [P02, p. 1] [P02, p. 2] [T04, p. 41]
- AUC resume el desempeño para todos los umbrales; precisión y recall dependen del umbral elegido. [T04, p. 39] [T04, p. 40] [T04, p. 51] **Inferencia operativa:** si se ajusta el umbral, se elige con validación, no con test. [T04, p. 52] [T02, p. 89]

### Curvas de validación

Una curva de validación grafica el rendimiento en train y en validación en función de un hiperparámetro. Un gap grande indica sobreajuste; un gap chico con rendimiento bajo, subajuste. [T07, p. 50] La clase 9 muestra ejemplos con la profundidad y el tamaño mínimo de split de un árbol. [T09, p. 4]

### Qué mirar de cada modelo

| Modelo | Hiperparámetro de la consigna | Supuestos y advertencias del material |
|---|---|---|
| Naive Bayes | (no se pide ajustar) | Asume atributos independientes dado la clase. [T06, p. 38] La versión gaussiana modela cada atributo continuo con una normal por clase y covarianza diagonal. [T06, p. 22] [T06, p. 32] [T06, p. 33] Para atributos categóricos se estiman frecuencias por clase. [T06, p. 34] [T06, p. 38] Ver [GDA y Naive Bayes](gda-y-naive-bayes.md). |
| SVM | `C` o kernel | Necesita escalar los atributos. [T08, p. 54] `C` y `γ` del kernel RBF se ajustan con validación cruzada. [T08, p. 49] Hay dos lecturas opuestas de `C` en la clase; ver [Dudas y conflictos](../dudas-y-conflictos.md). Ver [Máquinas de vectores de soporte](svm.md). |
| KNN | `k`, ponderación | Escalado imprescindible. [T09, p. 32] Un `k` chico tiene alta varianza; uno grande, más sesgo. [T09, p. 29] Con clases desbalanceadas, un `k` alto puede favorecer a la mayoritaria. [T09, p. 31] Es costoso al predecir y pierde capacidad discriminativa en alta dimensionalidad. [T09, p. 38] [T09, p. 39] Ver [kNN](aprendizaje-basado-en-instancias.md). |
| Random Forest | `n_estimators`, `max_depth` | Como sus árboles, no necesita normalización y maneja datos numéricos y categóricos. [T07, p. 26] Más árboles dan más estabilidad, hasta cierto punto. [T07, p. 61] Ver [Ensambles y Random Forest](ensambles-random-forest.md). |

**Inferencia:** el one-hot de muchas categóricas aumenta la dimensionalidad. [T02, p. 18] Eso afecta más a KNN, por la pérdida de discriminación de las distancias, que a Random Forest, que evalúa una feature por split. [T09, p. 39] **Conocimiento general:** el costo de entrenar un SVM con kernel crece más que linealmente con la cantidad de ejemplos. Con decenas de miles de filas, una búsqueda amplia de hiperparámetros puede ser lenta.

## Relación con el TP1

El flujo se mantiene: EDA con decisiones, separación temprana de test, k-fold solo con train, elección por validación y una estimación final en test. Cambian el tipo de problema (clasificación en vez de regresión), las métricas y los modelos. [P02, p. 1] [P02, p. 2] Ver [TP1: regresión y evaluación](tp1-regresion.md).
