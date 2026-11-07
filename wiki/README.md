# Wiki de la materia

Este es el índice del conocimiento canónico compilado. Agregá una entrada por tema en `temas/` y mantené enlaces entre conceptos relacionados.

## Navegación

- [Glosario](glosario.md)
- [Dudas y conflictos](dudas-y-conflictos.md)
- [Preguntas de repaso](repaso/preguntas.md)
- [TP2 paso a paso](repaso/tp2-resolucion-paso-a-paso.md): guía de estudio de la resolución para preparar la defensa.

## Temas

- [Fundamentos del aprendizaje automático](temas/fundamentos.md): definición, paradigmas y estructura general de un proyecto.
- [Datos y preprocesamiento](temas/datos-y-preprocesamiento.md): tipos de variables, codificación, limpieza, outliers y escalado.
- [Regresión, complejidad y generalización](temas/regresion-y-generalizacion.md): regresión lineal y polinómica, underfitting y overfitting.
- [Evaluación y validación](temas/evaluacion-y-validacion.md): train/dev/test, validación cruzada (estratificada, por grupos y temporal), leakage y métricas de regresión.
- [EDA y selección de características](temas/eda-y-seleccion.md): exploración, dimensionalidad y familias de métodos de selección.
- [Regularización](temas/regularizacion.md): L1, L2 y Elastic Net.
- [TP1: regresión y evaluación](temas/tp1-regresion.md): mapa de la consigna, entregables y controles conceptuales.
- [TP2: clasificación supervisada](temas/tp2-clasificacion.md): Bank Marketing, entregables, leakage, métricas y supuestos de Naive Bayes, SVM, KNN y RF.
- [TP3: optimización de modelos y competencia](temas/tp3-optimizacion.md): reservas GPU, reglas de la competencia, perfil del dataset, columnas con leakage, entregables y predictor.

### Clasificación

- [Regresión logística](temas/regresion-logistica.md): sigmoidea, odds, logit y umbral de decisión.
- [Métricas de clasificación](temas/metricas-de-clasificacion.md): matriz de confusión, precisión, recall, especificidad, ROC y AUC.
- [Probabilidad e inferencia bayesiana](temas/probabilidad-y-bayes.md): modelos discriminativos frente a generativos, Bayes, MAP y ML.
- [GDA y Naive Bayes](temas/gda-y-naive-bayes.md): LDA, QDA, Gaussian Naive Bayes, Naive Bayes categórico y Laplace.
- [Árboles de decisión](temas/arboles-de-decision.md): impureza, Gini, entropía, CART, poda e hiperparámetros.
- [Ensambles y Random Forest](temas/ensambles-random-forest.md): bootstrap, Random Forest, Extra Trees, bagging y stacking.
- [Máquinas de vectores de soporte (SVM)](temas/svm.md): margen maximal, margen tolerante, kernels, multiclase y One-Class SVM.
- [Gradient boosting y combinación de modelos](temas/gradient-boosting-y-combinacion.md): gradient boosting, XGBoost, LightGBM, CatBoost, bagging frente a boosting, stacking con predicciones out-of-fold y blending.

### Métodos basados en vecinos

- [Aprendizaje basado en instancias (kNN)](temas/aprendizaje-basado-en-instancias.md): lazy learning, distancias, elección de `k`, kNN ponderado, KD-Trees, LSH, HNSW, FAISS y kNN, árboles y Random Forest como regresores.

### Diagnóstico, datos y producción

- [Diagnóstico de modelos](temas/diagnostico-de-ml.md): fuentes de error, HLP, árbol de diagnóstico, curvas de validación y de aprendizaje, y qué hacer en cada caso.
- [Diseño centrado en datos y análisis de errores](temas/data-centric-y-analisis-de-errores.md): model-centric frente a data-centric, tags, priorización, data augmentation y buenos datos.
- [MLOps, despliegue y monitoreo](temas/mlops-y-despliegue.md): ciclo de vida, data y concept drift, patrones de despliegue, función predictora y monitoreo.
- La validación cruzada estratificada, por grupos y temporal está en [Evaluación y validación](temas/evaluacion-y-validacion.md#validación-cruzada-avanzada).

### Aprendizaje no supervisado

- [Clustering: K-means y DBSCAN](temas/clustering.md): supervisado frente a no supervisado, aplicaciones, familias de métodos, WCSS, inicialización, codo y silhouette, puntos núcleo, frontera y ruido.
- [Reducción de dimensionalidad: PCA y t-SNE](temas/reduccion-de-dimensionalidad.md): maldición de la dimensionalidad, componentes principales, varianza explicada, perplejidad y cuándo usar cada método.

## Fuentes incorporadas

| ID | Fuente | Alcance |
|---|---|---|
| T01 | Introducción al Aprendizaje Automático | Fundamentos, tipos de aprendizaje, proyecto y desafíos. |
| T02 | Datos, variables, overfitting y métricas | Preparación de datos, regresión y particiones. |
| T03 | EDA, feature selection, regularización y métricas | Flujo de proyecto, selección, regularización y evaluación. |
| P01 | TP1: Regresión e introducción a la evaluación de modelos | Consigna práctica vigente del ciclo 2026. |
| D01 | Insurance Charges | Dataset externo elegido para resolver el TP1. |
| T04 | Regresión logística y métricas de evaluación | Clasificación binaria, sigmoidea, matriz de confusión, ROC y AUC. |
| T06 | GDA y Naive Bayes | Modelos generativos, Bayes, MAP/ML, LDA, QDA y Naive Bayes. El archivo está marcado como "WIP". |
| T07 | Árboles de decisión y Random Forest | Impureza, CART, poda, grid search, bootstrap y ensambles. |
| T08 | Máquinas de vectores de soporte (SVM) | Margen maximal y tolerante, kernels, `C` y `γ`, multiclase, escalado y One-Class SVM. |
| T09 | Aprendizaje basado en instancias | Repaso de árboles y RF, kNN, métricas de distancia, kNN ponderado, ANN (KD-Trees, LSH, ANNOY) y kNN, árboles y RF como regresores. |
| P02 | TP2: Clasificación supervisada | Consigna práctica vigente del ciclo 2026: Bank Marketing con Naive Bayes, SVM, KNN y RF. |
| T11 | Diagnóstico de ML | Sesgo, varianza y error irreducible, HLP, curvas de aprendizaje, diseño centrado en datos, análisis de errores, data augmentation y validación cruzada estratificada, por grupos y temporal. |
| T12 | Algoritmos avanzados y MLOps | Reglas de la competencia del TP3, gradient boosting, ANN (HNSW, FAISS), bagging, boosting, stacking y blending, MLOps, despliegue, monitoreo y mantenimiento. |
| P03 | TP3: Optimización de modelos de Machine Learning | Consigna del ciclo 2026: clasificación de cancelaciones de reservas GPU, análisis de errores, enfoque data-centered, optimización y predictor. |
| P04 | TP3: anuncio de la competencia (Campus) | Anuncio en HTML de la cátedra: entregables, fechas de submission, Competition Score y premios. El texto buscable está en `material/extraido/P04.txt`. |
| D04 | GPU Resource Reservations | Dataset de la competencia del TP3, provisto por la cátedra (`material/catedra/datasets/`). |
| T14 | Aprendizaje no supervisado | Aplicaciones, clustering particional, K-means (WCSS, inicialización, codo y silhouette), DBSCAN, PCA y t-SNE. |

No existe T05 a propósito: en la fecha de la clase 5 no hubo material teórico nuevo. Tampoco existe T10: la clase 11 indica que la sesión anterior fue el TP2 [T11, p. 1] y no se recibió material teórico con número 10. Tampoco existe T13: el repaso de la clase 14 remite a temas de las clases 11 y 12 [T14, p. 1] y no se recibió material teórico con número 13. Los IDs de teoría conservan el número de clase.
