# Árboles de decisión

## Idea

Un árbol de decisión llega a una predicción mediante una sucesión de preguntas de respuesta binaria. [T07, p. 3] Divide el espacio de características con reglas condicionales simples organizadas jerárquicamente. Cada decisión lleva a una rama, hasta llegar a una hoja con la predicción final, y las regiones resultantes son cada vez más homogéneas. [T07, p. 4] Para predecir, se recorre el árbol desde la raíz respondiendo cada pregunta hasta llegar a una hoja. [T07, p. 24] [T07, p. 25]

## Cómo elegir un corte

1. Calcular la impureza de cada corte posible, para cada característica.
2. Elegir el corte de menor impureza. [T07, p. 6]

```text
Impureza del split = (n_izq / n) · Impureza_izq + (n_der / n) · Impureza_der
```

Con **error de clasificación** (proporción de elementos que no pertenecen a la clase mayoritaria del lado), el ejemplo compara tres cortes con impureza total 0,11, 0,17 y 0,13. Se elige el primero. [T07, p. 7] [T07, p. 8] [T07, p. 9] Algunos valores están mal redondeados, pero el orden no cambia; ver [Dudas y conflictos](../dudas-y-conflictos.md).

Problemas del error de clasificación: [T07, p. 11]

- Es poco sensible a cambios dentro de nodos impuros. Por ejemplo, 65/35 y 55/45 dan errores parecidos (0,35 y 0,45), aunque 55/45 es mucho peor.
- Muchos cortes pueden empatar aunque sus distribuciones internas sean muy distintas.
- Produce árboles menos estables y precisos, porque no capta cuán mezcladas están las clases.

## Gini y entropía

Con `pᵢ` la proporción de la clase `i` en el nodo: [T07, p. 12] [T07, p. 13] [T07, p. 14]

- **Entropía (Shannon, 1948):** `H = −Σ pᵢ log₂(pᵢ)`. Mide la incertidumbre promedio y es muy sensible a proporciones bajas por su forma logarítmica.
- **Impureza de Gini (Corrado Gini, 1912):** viene de medir la desigualdad en economía. Penaliza la mezcla de clases aun cuando una domina.

> **Atención — fórmula de Gini.** Las diapositivas escriben `Gini = Σ pᵢ²`. [T07, p. 12] [T07, p. 13] Esa expresión mide *pureza*: vale 1 en un nodo puro. **Conocimiento general:** la impureza de Gini es `1 − Σ pᵢ²`, que vale 0 en un nodo puro y 0,5 en un nodo binario 50/50. El gráfico de la diapositiva 15 muestra justamente esa forma. [T07, p. 15] Ver [Dudas y conflictos](../dudas-y-conflictos.md).

Comparación: [T07, p. 15]

- El error de clasificación tiene pendiente constante en `p`.
- Gini y entropía penalizan más cuando hay pocas muestras de una clase. Al ser más sensibles a proporciones chicas, construyen divisiones más informativas.
- Se suele usar Gini porque es más barato de calcular: multiplicaciones en lugar de logaritmos.

El ejemplo con datos reales recorre los umbrales de una característica, grafica la Gini del split en función del umbral y elige el mínimo. [T07, p. 16] [T07, p. 17]

## Algoritmo CART

ID3 y C4.5 son propuestas históricas. Hoy el más usado es CART, que es simple y tiene soporte amplio en librerías como scikit-learn, Random Forest y XGBoost. [T07, p. 34]

Para cada nodo: [T07, p. 35] [T07, p. 36]

1. Si el nodo es puro o se cumple un criterio de parada (profundidad máxima, tamaño mínimo…), crear una hoja con la clase más frecuente.
2. Si no, calcular la impureza (Gini) de **todos** los umbrales posibles de **todas** las características.
3. Elegir la característica y el umbral de menor impureza.
4. Si se cumple un criterio de parada (por ejemplo, mejora mínima de impureza), crear la hoja. Si no, dividir en dos nodos y repetir en cada uno.

**Eficiencia:** con `n` muestras y `d` características hay `(n − 1)·d` umbrales candidatos. [T07, p. 47] Una mejora es ordenar los valores y evaluar solamente los umbrales donde cambia la clase. [T07, p. 48]

## Ventajas y desventajas

| Ventajas | Desventajas |
|---|---|
| Interpretabilidad clara. [T07, p. 26] | Propenso al sobreajuste. [T07, p. 27] |
| Maneja datos numéricos y categóricos. [T07, p. 26] | Fronteras rígidas, formadas por cortes paralelos a los ejes. [T07, p. 27] |
| No necesita normalización. [T07, p. 26] | Vulnerable a la orientación de las características: rotar los datos 45° obliga a una escalera de cortes. [T07, p. 27] |
| | Muy sensible a pequeñas variaciones de los datos. [T07, p. 27] |

**Inferencia:** "no necesita normalización" contrasta con la recomendación de escalar para otros modelos, porque un umbral sobre una variable no cambia de orden si la variable se reescala. [T03, p. 40]

## Control del sobreajuste

| Pre-poda (restricciones al crecer) | Poda posterior |
|---|---|
| Limitar la profundidad. | Hacer crecer el árbol sin restricciones. |
| No crear nodos con pocos datos. | Eliminar las ramas que aportan poca mejora. |
| Exigir una mejora mínima para dividir. | |

Fuente de la tabla: [T07, p. 28]. En general se usa la pre-poda, porque es más eficiente computacionalmente. [T07, p. 29] Cuando se alcanza una restricción, se crea una hoja con la clase mayoritaria del nodo. [T07, p. 30]

En el ejemplo, un árbol sin restricciones logra accuracy 1,00 en train y 0,86 en validación. Con `max_depth = 4` y `min_samples_split = 45` pasa a 0,90 y 0,89: la brecha casi desaparece. [T07, p. 49] [T07, p. 54]

## Evaluación y ajuste de hiperparámetros

1. Calcular la métrica en train y en validación.
2. Usar validación cruzada (k-fold) para una estimación más estable.
3. Mirar el **gap de generalización**: un gap grande indica sobreajuste, y un gap chico con desempeño bajo indica subajuste.
4. Trazar **curvas de validación**: desempeño en función de un hiperparámetro de complejidad (profundidad, cantidad de nodos, mínimo de puntos por split…). [T07, p. 50] [T07, p. 51]

El repaso de la clase 9 muestra tres de esas curvas: accuracy de train y validación en función de `min_samples_split`, de `min_samples_leaf` y de la profundidad. En la curva de profundidad, validación alcanza su máximo (alrededor de 0,90) con profundidad 2 o 3 y después cae a alrededor de 0,86, mientras train sube hasta 1,0. [T09, p. 4]

**Grid search:** primero se grafica cada hiperparámetro por separado en un rango amplio. Después se elige un rango más acotado donde funcione bien, *dejando margen*, porque lo que parece sobreajuste en un hiperparámetro aislado puede compensarse con los demás. [T07, p. 52] [T07, p. 53] Ver también [Evaluación y validación](evaluacion-y-validacion.md).

## Importancia de características

Los árboles y los Random Forests indican qué variables usan más. Cada vez que se elige un umbral, la reducción de impureza que produce se suma a la variable correspondiente. El vector resultante indica qué variables son más informativas. [T07, p. 71] Es el método *embedded* que ya aparecía en la clase 3. [T03, p. 62] [T04, p. 4]

## Log-loss

Para métodos avanzados, la presentación no recomienda ni Gini ni entropía, sino log-loss: [T07, p. 73]

```text
log-loss = −[y · log(p̂) + (1 − y) · log(1 − p̂)]
```

Ventajas: es derivable, así que permite usar gradientes, y crece muy rápido ante errores cometidos con alta confianza. [T07, p. 73] **Conocimiento general:** es la misma pérdida que se minimiza al entrenar la [regresión logística](regresion-logistica.md).

## Árboles de regresión

Un árbol también puede usarse como regresor. Divide el espacio en hojas y, para un valor de `x`, predice el promedio de `y` de los ejemplos de entrenamiento que caen en esa hoja. [T09, p. 69] La diapositiva dice "la y promedio de las x de esa hoja"; se refiere a los valores de `y` de esos ejemplos.

- **Ejemplo:** con `max_depth = 2`, los cortes en `x = 3,27`, `2,48` y `3,78` dejan cuatro hojas. La predicción es una función escalonada. [T09, p. 69] [T09, p. 70]
- **`max_depth`:** una profundidad mayor permite más divisiones del espacio de features. La salida es más ruidosa y más sensible a los datos. En el gráfico, `max_depth = 5` persigue los puntos mucho más que `max_depth = 2`. [T09, p. 70] [T09, p. 71]
- **Ventajas y desventajas**, igual que en clasificación: puede capturar geometrías complejas, es muy interpretable, es propenso al sobreajuste y es inestable. [T09, p. 71]

**Conocimiento general:** en regresión, el criterio de corte no es Gini ni entropía. Se elige el split que más reduce el error cuadrático (la varianza de `y` dentro de cada hijo). Como cada hoja predice un promedio de valores vistos, el árbol no extrapola fuera del rango de `y` de entrenamiento.

Ver [Random Forest como regresor](ensambles-random-forest.md#random-forest-como-regresor) y la comparación con [kNN como regresor](aprendizaje-basado-en-instancias.md#knn-como-regresor).

## Conexiones

- [Ensambles y Random Forest](ensambles-random-forest.md)
- [Regresión, complejidad y generalización](regresion-y-generalizacion.md)
- [EDA y selección de características](eda-y-seleccion.md)
- [Aprendizaje basado en instancias (kNN)](aprendizaje-basado-en-instancias.md): los KD-Trees usan una estructura de árbol para buscar vecinos, y los árboles sufren menos en alta dimensión. [T09, p. 39] [T09, p. 45]
