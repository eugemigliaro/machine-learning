# Ensambles y Random Forest

## Bootstrap

Bootstrap es un método de muestreo con reemplazo. A partir de un dataset de tamaño `n` se generan muestras nuevas también de tamaño `n`: algunos puntos aparecen varias veces y otros no aparecen. Permite entrenar varios modelos sobre datos distintos, aunque todos derivados del mismo dataset, y es la base del bagging y de Random Forest. [T07, p. 56]

Por qué ayuda a los árboles: [T07, p. 57]

- Genera variedad entre árboles, lo que reduce la varianza del modelo.
- Cada árbol "ve" una versión algo distinta del problema, así que el ensamble es más estable y menos sensible a outliers o ruido.
- En promedio, cada muestra contiene alrededor del 63 % de los datos únicos. El 37 % restante, llamado **out-of-bag**, sirve como validación interna.
- En datasets muy grandes se usan muestras más chicas, en general submuestreos sin reemplazo.

**Conocimiento general:** la probabilidad de que un dato no salga en `n` extracciones es `(1 − 1/n)ⁿ → 1/e ≈ 0,368`. De ahí vienen el 63 % y el 37 %.

## Random Forest

Un Random Forest es un conjunto de árboles entrenados con variaciones aleatorias. Promediar árboles individualmente más débiles da una predicción más robusta. [T07, p. 58]

1. Cada árbol se entrena sobre una muestra bootstrap del mismo tamaño que el dataset original.
2. En cada división se considera solo un **subconjunto aleatorio de variables**.
3. Cada árbol clasifica por separado y vota. Gana la clase con más votos, y la probabilidad de una clase es el porcentaje de árboles que la votaron. [T07, p. 59]

**Conocimiento general:** `RandomForestClassifier.predict_proba` de scikit-learn promedia las probabilidades de cada árbol en lugar de contar votos duros. Suele dar resultados parecidos, pero no idénticos.

**¿Por qué la aleatoriedad reduce el sobreajuste?** Rompe la homogeneidad entre árboles, que entonces cometen errores distintos. Al combinarlos, esos errores se atenúan y solo sobreviven los patrones consistentes. [T07, p. 62]

### Hiperparámetros

- `n_estimators`: cantidad de árboles. Más árboles dan más estabilidad, hasta cierto punto.
- `max_features`: clave para la diversidad. Cuanto menor, más distintos son los árboles.
- Los mismos de un árbol: `max_depth`, `min_samples_split`, `min_samples_leaf`. [T07, p. 61]

## Extra Trees

Extra Trees es el caso extremo: además de sortear las variables, también sortea los umbrales. Cada árbol es aún más débil, pero si sus errores no están correlacionados, promediar muchos los diluye. [T07, p. 62] [T07, p. 63]

| | Árbol de decisión | Random Forest | Extra Trees |
|---|---|---|---|
| Features candidatas | Todas | Subconjunto aleatorio | Subconjunto aleatorio |
| Umbral | El mejor | El mejor | Uno aleatorio por feature |
| Optimiza | El mejor split global | El mejor split entre las features elegidas | El mejor entre candidatos aleatorios |

Fuente de la tabla: [T07, p. 64]. La clase 9 la repite en su repaso. [T09, p. 5]

## Árbol frente a Random Forest

| | Árbol de decisión | Random Forest |
|---|---|---|
| Ventajas | Interpretabilidad. | Precisión y robustez; maneja grandes volúmenes de datos y variables; reduce el overfitting. |
| Desventajas | Propenso al overfitting; muy sensible a los datos. | Mayor costo computacional; menos interpretable; puede sobreajustar en datasets pequeños. |

Fuente de la tabla: [T07, p. 60].

### Resultados del ejemplo (dos características)

| Modelo | Acc. train | Acc. validación |
|---|---|---|
| Árbol sin restricciones | 1,00 | 0,86 |
| Árbol `max_depth = 4`, `min_samples_split = 45` | 0,90 | 0,89 |
| Random Forest `max_depth = 4` | 0,92 | 0,89 |
| Extra Trees, 500 árboles, `max_depth = 4` | 0,87 | 0,87 |
| Random Forest con rotaciones aleatorias | 0,95 | 0,91 |

Fuentes: [T07, p. 49] [T07, p. 54] [T07, p. 65] [T07, p. 66] [T07, p. 67]. La clase 9 repite las filas del árbol restringido y de Random Forest. [T09, p. 6] Con solo dos características, Random Forest pierde parte de su potencial. [T07, p. 65] [T09, p. 6] **Inferencia:** las rotaciones aleatorias atacan la debilidad de los árboles frente a la orientación de las características. [T07, p. 27]

## Random Forest como regresor

Igual que un árbol, cada hoja predice el promedio de `y` de sus ejemplos. [T09, p. 69] [T09, p. 72] Como en clasificación, Random Forest puede capturar geometrías complejas, es menos interpretable que un árbol, es menos propenso al sobreajuste y es robusto. [T09, p. 72] En el gráfico comparativo, la curva del bosque sigue la forma de los datos con escalones más suaves que la del árbol. [T09, p. 72]

**Conocimiento general:** el regresor promedia las predicciones de los árboles en lugar de votar. Como cada árbol predice promedios de valores vistos, el bosque tampoco extrapola fuera del rango de `y` de entrenamiento.

Ver [Árboles de regresión](arboles-de-decision.md#árboles-de-regresión) y [kNN como regresor](aprendizaje-basado-en-instancias.md#knn-como-regresor).

## Bagging, stacking y blending

- **Bagging** rinde sobre todo con modelos de alta varianza como los árboles. Con modelos de baja varianza y alto sesgo, como la regresión logística o [las SVM](svm.md), aporta menos. [T07, p. 69]
- **Stacking:** un meta-modelo recibe las salidas de los modelos base. En la versión *con passthrough* recibe también las features originales, y así puede reconocer en qué regiones funciona mejor cada modelo. [T07, p. 70]
- **Blending RF + KNN:** RF capta diferencias más globales y KNN más locales, así que probablemente cometan errores distintos. Se entrena cada uno por separado y se combinan sus probabilidades con un promedio simple o ponderado. [T07, p. 72] kNN se desarrolla en [Aprendizaje basado en instancias](aprendizaje-basado-en-instancias.md).

**Inferencia operativa:** los pesos del blending o el meta-modelo del stacking son decisiones del pipeline. Deben ajustarse con predicciones que no provengan de los mismos datos con que se entrenaron los modelos base (por ejemplo, fuera de fold) y nunca con test. [T02, p. 94] [T03, p. 9]

## Mejoras de selección de características

Reducir variables puede eliminar ruido y sobreajuste. Algunas opciones: la importancia del propio RF (`feature_importances_`); filtros por varianza, correlación o capacidad discriminante (graficar la distribución de cada característica por clase); y quitar variables correlacionadas entre sí, conservando una. [T07, p. 72] Ver [EDA y selección de características](eda-y-seleccion.md).

## Conexiones

- [Árboles de decisión](arboles-de-decision.md)
- [Regresión, complejidad y generalización](regresion-y-generalizacion.md): el ensamble reduce varianza.
- [Evaluación y validación](evaluacion-y-validacion.md)
