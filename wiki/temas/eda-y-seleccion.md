# EDA y selección de características

## Análisis exploratorio

EDA examina y visualiza los datos para comprender su estructura antes de modelar. Busca detectar distribuciones, valores faltantes o anómalos, inconsistencias y relaciones entre variables. [T03, p. 32] [T03, p. 34] [T03, p. 56]

En problemas supervisados interesa estudiar cada característica respecto de `y` y también las relaciones entre características. Pearson mide asociación lineal, pero correlación no implica causalidad y una correlación baja no descarta relaciones no lineales. [T03, p. 48] [T03, p. 49] [T03, p. 51] [T03, p. 64]

## Dimensionalidad

Agregar variables irrelevantes aumenta grados de libertad y ruido, y puede elevar el riesgo de overfitting. En alta dimensión los datos se vuelven más dispersos, hacen falta más ejemplos y las distancias pierden capacidad discriminativa. [T03, p. 45] [T03, p. 58] [T03, p. 59]

Ese último punto golpea especialmente a [kNN](aprendizaje-basado-en-instancias.md): las distancias tienden a parecerse, la noción de "vecino cercano" pierde significado y todas las features entran en la distancia, incluso las poco informativas. [T09, p. 39] La clase 9 recomienda reducir dimensiones: elegir features por la separabilidad entre clases que aportan, revisar correlaciones o proyectar con PCA o autoencoders. [T09, p. 42] Los árboles sufren menos, porque cada split mira una sola feature. [T09, p. 39]

Dos respuestas diferentes:

- **Feature selection:** conservar un subconjunto interpretable de las variables originales.
- **Feature projection:** combinar variables para crear una representación más compacta cuando no conviene descartarlas. [T03, p. 61] [T03, p. 78]

LDA ofrece una proyección *supervisada*: busca la dirección que maximiza la separación entre clases, mientras que PCA maximiza la varianza total sin usar etiquetas. [T06, p. 27] [T06, p. 28] Ver [GDA y Naive Bayes](gda-y-naive-bayes.md).

## Familias de selección

| Familia | Idea | Ventaja | Límite | Ejemplos |
|---|---|---|---|---|
| Filtro | Evalúa variables con un criterio independiente del modelo. | Rápido y escalable. | No capta interacciones. | Pearson, información mutua, ANOVA, Chi². |
| Wrapper | Entrena un modelo sobre distintos subconjuntos. | Puede captar interacciones. | Alto costo y sin garantía de óptimo global. | Forward/backward selection, RFE. |
| Embedded | Selecciona dentro del entrenamiento. | Compromiso entre costo y ajuste al modelo. | Depende del modelo y puede sesgar la selección. | Importancia de Random Forest, Lasso, Elastic Net. |

La clasificación y sus compromisos provienen del resumen de la cátedra. [T03, p. 62] [T03, p. 79]

### Elección de filtros

- Pearson: relación lineal entre variables numéricas continuas. [T03, p. 64]
- Información mutua: dependencia lineal o no lineal, para clasificación o regresión. [T03, p. 66]
- ANOVA F-test: feature numérica frente a target categórico, bajo supuestos de normalidad y varianzas similares. [T03, p. 68]
- Chi²: dependencia entre feature y target categóricos. [T03, p. 69]

RFE elimina iterativamente la característica menos importante y puede combinarse con validación cruzada para elegir cuántas conservar. [T03, p. 72]

La importancia de Random Forest, citada como método embedded, suma la reducción de impureza que produce cada variable en los cortes donde se usa. La clase 7 agrega filtros por varianza, correlación y capacidad discriminante, y la eliminación de variables correlacionadas entre sí. [T07, p. 71] [T07, p. 72] Ver [Árboles de decisión](arboles-de-decision.md#importancia-de-características).

Toda selección debe aprenderse dentro de train o de cada fold, no antes de la separación. [T02, p. 94] [T02, p. 96]
