# Métricas de clasificación

## Accuracy y sus límites

`Accuracy = predicciones correctas / total de predicciones`. En el ejemplo, acertar 8 de 10 diagnósticos da 80 %. [T04, p. 25] [T04, p. 26]

La accuracy no dice qué tipo de error se cometió. Hay tres modelos con 80 % sobre los mismos 10 pacientes: uno comete 2 falsos negativos, otro 2 falsos positivos y el tercero uno de cada tipo. [T04, p. 26] [T04, p. 27]

**Conocimiento general:** con clases desbalanceadas, un modelo que siempre predice la clase mayoritaria puede tener accuracy alta sin detectar ningún positivo. El plan de la clase anuncia "métricas con clases desbalanceadas", pero ninguna diapositiva desarrolla el tema; ver [Dudas y conflictos](../dudas-y-conflictos.md). [T04, p. 1]

## Matriz de confusión

La matriz de confusión cruza la predicción con el valor real (ground truth). [T04, p. 28] [T04, p. 29]

| | Real + | Real − |
|---|---|---|
| **Predicho +** | TP: maligno predicho maligno | FP: benigno predicho maligno |
| **Predicho −** | FN: maligno predicho benigno | TN: benigno predicho benigno |

En el diagnóstico de tumores, el FN es "el error más grave". [T04, p. 29] La presentación incluye además una matriz multiclase de 5 × 5, pero sin desarrollarla. [T04, p. 28]

## Métricas derivadas

| Métrica | Fórmula | Pregunta que responde |
|---|---|---|
| Precisión | `TP / (TP + FP)` | ¿Qué tan exactas son las predicciones positivas? [T04, p. 31] |
| Recall / sensibilidad / TPR | `TP / (TP + FN)` | ¿Qué proporción de los positivos reales encuentra el modelo? [T04, p. 31] [T04, p. 37] [T04, p. 45] |
| Especificidad | `TN / (TN + FP)` | ¿Qué proporción de los negativos reales encuentra el modelo? [T04, p. 35] [T04, p. 36] |
| Valor predictivo negativo | `TN / (TN + FN)` | ¿Qué tan exactas son las predicciones negativas? [T04, p. 33] [T04, p. 34] |
| FPR | `FP / (FP + TN)` | ¿Qué proporción de los negativos reales se marca como positiva? [T04, p. 45] |
| Accuracy | `(TP + TN) / (TP + FP + TN + FN)` | ¿Qué proporción total acierta el modelo? [T04, p. 31] |

`FPR = 1 − especificidad`, como indica el eje horizontal de la curva ROC de ejemplo. [T04, p. 50]

**Regla para recordar (inferencia):** precisión y valor predictivo negativo se leen por fila, porque parten de lo que *dijo* el modelo. Recall, especificidad y FPR se leen por columna, porque parten de lo que *es* realmente.

F1 aparece en la lista de métricas pero no se define en la presentación. [T04, p. 24] **Conocimiento general:** `F1 = 2·P·R / (P + R)`, la media armónica entre precisión y recall.

## El umbral y su trade-off

La regresión logística devuelve una probabilidad, y el umbral que la convierte en 0/1 lo elegimos nosotros. [T04, p. 38]

- **Bajar el umbral:** se marcan más positivos, sube el recall y baja la precisión (más falsas alarmas). [T04, p. 39]
- **Subir el umbral:** se marcan menos positivos, sube la precisión y baja el recall (se escapan positivos). [T04, p. 40]

La elección depende del costo de cada error. En diagnóstico de cáncer conviene un umbral bajo (recall alto), porque es peor dejar pasar un maligno. En un filtro de spam conviene un umbral alto (precisión alta), porque es peor perder un correo importante. No existe un umbral correcto universal. [T04, p. 41] [T04, p. 42] [T04, p. 43] [T04, p. 44]

## Curva ROC

La curva ROC no fija un único umbral: recorre todos los posibles. Para cada uno calcula `TPR` y `FPR` y grafica los puntos `(FPR, TPR)` mientras el umbral baja de 1 a 0. [T04, p. 45]

Ejemplo de recorrido: [T04, p. 46] [T04, p. 47] [T04, p. 48]

| Umbral | TP | FP | FN | TN | Punto (FPR, TPR) |
|---|---|---|---|---|---|
| Por encima de todos los scores | 0 | 0 | — | — | (0, 0) |
| Intermedio | 35 | 5 | 6 | 37 | (0,11; 0,85) |
| Por debajo de todos los scores | 45 | 45 | 0 | 0 | (1, 1) |

Las cantidades totales del ejemplo intermedio no coinciden con las del extremo; ver [Dudas y conflictos](../dudas-y-conflictos.md).

## AUC

El área bajo la curva resume el desempeño del clasificador para todos los umbrales: `AUC = 1` corresponde al clasificador ideal, que pasa por el punto (0, 1), y `AUC = 0,5` a un clasificador aleatorio, que queda sobre la diagonal. [T04, p. 50] [T04, p. 51] La figura también muestra un "mal" clasificador con `AUC < 0,5`. [T04, p. 51]

**Conocimiento general:** el AUC es la probabilidad de que un positivo elegido al azar reciba un score mayor que un negativo elegido al azar. Un `AUC < 0,5` indica un ranking invertido.

## Elegir el umbral

Un criterio práctico es elegir el umbral cuyo punto `(FPR, TPR)` quede más cerca del ideal `(0, 1)`: [T04, p. 52]

1. Definir un rango de umbrales.
2. Para cada umbral, clasificar, calcular `FPR` y `TPR` y medir la distancia a `(0, 1)`.
3. Quedarse con el de distancia mínima.

**Inferencia operativa:** el umbral es una decisión del pipeline. Por eso se elige con dev o con validación cruzada, nunca mirando test. [T02, p. 89] [T03, p. 9]

## Conexiones

- [Regresión logística](regresion-logistica.md)
- [Evaluación y validación](evaluacion-y-validacion.md)
- [Árboles de decisión](arboles-de-decision.md): usa accuracy de train y validación para diagnosticar sobreajuste. [T07, p. 49] [T07, p. 50]
