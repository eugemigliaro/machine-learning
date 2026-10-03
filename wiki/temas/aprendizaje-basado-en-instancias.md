# Aprendizaje basado en instancias (kNN)

## Idea

Los métodos basados en vecinos basan su estimación o clasificación en las propiedades de los valores cercanos. [T09, p. 8] Suponen **continuidad local**: instancias cercanas en el espacio de características deberían tener propiedades similares. [T09, p. 9]

### Aprendizaje perezoso

Estos métodos no construyen un modelo explícito a partir de los datos. Siguen una estrategia **perezosa** (*lazy learning*): posponen el cómputo hasta el momento de la predicción. Ante un dato nuevo, consultan los datos de entrenamiento para identificar instancias cercanas e inferir la salida. [T09, p. 10] [T09, p. 11]

| | Basado en instancias | Basado en modelos |
|---|---|---|
| Qué hace | Literalmente "aprende de memoria". | A partir de los datos, crea un modelo que los representa. |
| Cómo predice | Usa los datos: busca cuál es el dato más parecido y cómo es. | Usa el modelo para generalizar a datos nuevos. |
| Qué hay que definir | Cómo se mide la similitud entre datos. | Cómo construir el modelo a partir de los datos. |

Fuente de la tabla: [T09, p. 13]. Es la misma tabla de la clase 1. [T01, p. 43] Ver [Fundamentos](fundamentos.md).

Implicaciones: [T09, p. 14]

- La fase de entrenamiento es prácticamente inexistente.
- La complejidad se traslada a la inferencia.
- La calidad de la predicción depende mucho de los datos y de elegir bien los hiperparámetros y la métrica de distancia.

## k vecinos más cercanos (kNN)

kNN es el algoritmo más característico de esta familia. Dada una instancia nueva, identifica sus `k` vecinos más cercanos en el conjunto de entrenamiento y le asigna la clase más frecuente entre ellos. `k`, la cantidad de vecinos que se miran, es un hiperparámetro. El algoritmo es simple, pero muy competitivo y capaz de captar estructuras complejas. [T09, p. 16]

Implementación: [T09, p. 18] [T09, p. 19]

1. Calcular la distancia de la instancia nueva a cada dato de entrenamiento.
2. Ordenar las instancias de entrenamiento por distancia y quedarse con las `k` más cercanas.
3. Asignar la clase más frecuente entre esos `k` vecinos.

## Métricas de distancia

Hay que definir una métrica de distancia. Esa métrica determina la geometría del espacio de características y, por lo tanto, qué instancias se consideran vecinas. [T09, p. 20] Cuál conviene depende del espacio en el que viven los datos. [T09, p. 22]

| Métrica | Fórmula | Cuándo usarla |
|---|---|---|
| Euclídea | `d(x, y) = √(Σᵢ (xᵢ − yᵢ)²)` | Medidas físicas: dimensiones con una interpretación geométrica comparable. [T09, p. 23] |
| Manhattan | `d(x, y) = Σᵢ \|xᵢ − yᵢ\|` | Datos dispersos o conteos: cuando interesa acumular diferencias coordenada por coordenada. [T09, p. 24] |
| Similitud coseno | `cos(θ) = (x · y) / (‖x‖ ‖y‖)` | Embeddings: cuando importa más la dirección o el patrón del vector que su magnitud. [T09, p. 25] |

Fuente de las fórmulas: [T09, p. 21]. La diapositiva ilustra la diferencia con un mapa: la distancia euclídea es la línea recta entre dos puntos y la de Manhattan sigue las calles. [T09, p. 20]

**Conocimiento general:** la similitud coseno no es una distancia, porque crece cuando los vectores se parecen. Para usarla en kNN se toma la *distancia coseno* `1 − cos(θ)`. Ver [Dudas y conflictos](../dudas-y-conflictos.md).

### La métrica y la representación

La métrica puede tratarse como un hiperparámetro más del modelo. [T09, p. 26] A veces, en lugar de cambiar la distancia, conviene cambiar la representación de los datos para que la distancia euclídea sea más informativa. Por ejemplo, una variable cíclica como "día del año" puede codificarse con seno y coseno. Así, valores cercanos en el ciclo también quedan cercanos en distancia euclídea. [T09, p. 26]

**Inferencia:** con período `P`, cada valor `t` se representa como `(sin(2πt/P), cos(2πt/P))`. Con `t` sin transformar, el 31 de diciembre y el 1 de enero quedan a distancia 364. Con la codificación cíclica, quedan contiguos. Ver [Datos y preprocesamiento](datos-y-preprocesamiento.md).

## Escalado

Como kNN se basa en distancias, es fundamental que las features estén en escalas comparables. Si no lo están, las de mayor magnitud dominan la distancia y tienen una influencia desproporcionada sobre la predicción. Las dos opciones de la clase son la normalización min-max `(x − min) / (max − min)` y la estandarización z-score `(x − media) / desvío`. [T09, p. 32] Son las mismas de la clase 3. [T03, p. 42] [T03, p. 43]

**Inferencia operativa:** los parámetros del escalado (mínimo y máximo, o media y desvío) se calculan con train y se reutilizan en validación y test. [T02, p. 94] [T02, p. 96]

## Elección de k

`k` es el principal hiperparámetro de kNN. [T09, p. 28] [T09, p. 29]

- **`k` chico:** bajo sesgo, pero alta varianza (más riesgo de sobreajuste). Con `k = 1` la frontera es muy local y flexible. [T09, p. 29] [T09, p. 30]
- **`k` grande:** más estabilidad, pero más sesgo y menos sensibilidad a las estructuras locales. [T09, p. 29]

Se elige como cualquier otro hiperparámetro, con validación cruzada. [T09, p. 31] Consideraciones adicionales: [T09, p. 31]

- **Clases desbalanceadas:** un `k` alto puede favorecer sistemáticamente a la clase mayoritaria.
- **Alta dimensionalidad:** el concepto de vecindad pierde fuerza. Puede convenir ajustar `k` junto con alguna estrategia de reducción de dimensionalidad.
- **Empates:** los valores impares de `k` reducen la posibilidad de empate. En multiclase, evitar múltiplos del número de clases puede ayudar, pero no garantiza que no haya empates.

**Inferencia:** los dos extremos muestran el equilibrio de [Regresión, complejidad y generalización](regresion-y-generalizacion.md). Con `k = 1`, cada punto de train es su propio vecino más cercano, así que el error de train es nulo (salvo puntos duplicados con etiquetas distintas). Por eso el error de train no sirve para elegir `k`. Con `k = n`, el modelo predice siempre la clase mayoritaria, para cualquier punto.

## kNN ponderado

El kNN convencional da la misma importancia a todos los vecinos dentro de los `k`, sin importar cuán cerca estén. En la **ponderación por distancia**, al contar la clase más presente, cada vecino pesa la inversa de su distancia al punto. [T09, p. 34]

**Inferencia (formalización):** con `wᵢ = 1 / d(x, xᵢ)`, se predice la clase `c` que maximiza `Σ wᵢ`, sumando sobre los vecinos de clase `c`.

**Ejemplo (inferencia, no está en el material):** con `k = 3`, un vecino de clase A a distancia 1 y dos de clase B a distancia 3. Con voto uniforme gana B, 2 a 1. Con ponderación, A suma 1 y B suma `1/3 + 1/3 ≈ 0,67`, así que gana A.

Reducir `k` y ponderar dan más importancia a los vecinos más cercanos, pero **no son equivalentes**: [T09, p. 36]

- Un `k` muy chico es más inestable y susceptible al ruido o a los outliers.
- Un `k` moderado (10 a 20) combinado con ponderación suele dar un sistema más estable y robusto.

Esa combinación es especialmente útil en regiones de alta variabilidad, como las cercanas a las fronteras de decisión, en espacios con densidad heterogénea y con datos ruidosos. [T09, p. 36]

**Conocimiento general:** si el punto nuevo coincide con uno de entrenamiento, `d = 0` y el peso no está definido. scikit-learn (`weights="distance"`) resuelve ese caso asignándole directamente la etiqueta de los puntos que coinciden.

## Limitaciones

1. **Costo computacional elevado**, sobre todo al predecir: para clasificar o estimar un punto nuevo hay que calcular su distancia a todos los puntos de entrenamiento. [T09, p. 38]
2. **Distancias poco discriminativas en alta dimensionalidad:** al aumentar las dimensiones, las distancias entre puntos tienden a parecerse y la noción de "vecino cercano" pierde significado. Además, todas las features entran en la distancia, incluso las poco informativas. [T09, p. 39] Es el mismo fenómeno descripto en [EDA y selección de características](eda-y-seleccion.md). [T03, p. 59]

El segundo problema suele afectar menos a los [árboles](arboles-de-decision.md), porque cada split evalúa una sola feature por vez. [T09, p. 39]

**Conocimiento general:** la búsqueda exhaustiva cuesta `O(n · d)` por consulta, con `n` ejemplos de entrenamiento y `d` features.

## Eficiencia

### Reducción de dimensionalidad

Reducir dimensiones baja el costo y además hace más informativo el cálculo de distancias. Hay que asegurarse de que todas las dimensiones aporten información relevante. Opciones: [T09, p. 42]

- estudiar cuánta separabilidad entre clases aporta cada feature y quedarse con las de mayor valor;
- evaluar la correlación entre features;
- proyectar a un espacio nuevo con PCA o autoencoders.

Ver [EDA y selección de características](eda-y-seleccion.md).

### Vecinos más cercanos aproximados (ANN)

La familia más usada para buscar vecinos de forma eficiente es la de los **Approximate Nearest Neighbours (ANN)**. Encuentran vecinos aproximados en lugar de exactos, pero mucho más rápido, sobre todo en alta dimensión o con grandes volúmenes de datos. [T09, p. 43] Funcionamiento: [T09, p. 43]

1. Preprocesar los datos para crear una estructura que divida el espacio de características en subespacios.
2. Calcular distancias solo con los puntos que pertenecen al mismo subespacio que el punto a evaluar.

Sacrifican un poco de precisión en los vecinos a cambio de muchísima velocidad. [T09, p. 43]

> **Atención — sigla.** En esta clase, ANN significa *Approximate Nearest Neighbours*. [T09, p. 1] [T09, p. 43] **Conocimiento general:** en la bibliografía de ML, ANN suele significar *Artificial Neural Network*.

### KD-Trees

Un KD-Tree usa un árbol para dividir el espacio de características. En cada nodo divide el subespacio en dos partes según el **valor mediano** de una dimensión, y la dimensión usada cambia en cada nodo. El espacio queda dividido en regiones rectangulares con menos puntos cada una. [T09, p. 45] [T09, p. 47]

**Inferencia:** la diapositiva habla de "árboles de decisión", pero el corte no es el de CART (ver [Árboles de decisión](arboles-de-decision.md)): no usa etiquetas ni minimiza impureza, sino que parte por la mediana para repartir los puntos. [T07, p. 35] [T09, p. 45]

La división falla cuando el punto queda demasiado cerca de un corte: su vecino real puede estar del otro lado. [T09, p. 50] Por eso la búsqueda hace *backtracking*: [T09, p. 51]

1. Dividir el espacio de características con el árbol.
2. Para evaluar un punto, recorrer el árbol hasta la hoja que lo contiene.
3. Calcular distancias dentro de esa hoja y tomar la distancia `d` a los vecinos más cercanos.
4. Recorrer el árbol hacia arriba evaluando si la distancia del punto al corte de cada nodo es menor que `d`. Si lo es, bajar por la otra rama y calcular distancias en las hojas cuyo corte esté a menos de `d`.
5. Entre todos esos candidatos, quedarse con los más cercanos.

Con muchas dimensiones (más de 20), los KD-Trees pierden efectividad, porque las distancias son cada vez menos informativas. [T09, p. 67]

**Conocimiento general:** con backtracking completo, la búsqueda en un KD-Tree es *exacta*; se vuelve aproximada solo si se limita cuántas ramas se revisan. El título de la sección también menciona Ball Trees, pero no se desarrollan. [T09, p. 41]

### Locality-Sensitive Hashing (LSH)

LSH busca una división (*hashing*, "picar en trozos") del espacio que conserve la cercanía (*locality*). [T09, p. 52] Pasos: [T09, p. 58]

1. Generar `k` hiperplanos aleatorios y ver de qué lado de cada uno queda cada punto. Eso da un **vector hash** por punto, por ejemplo `h(x) = (1, 0, 0, 0, 1, 0)`.
2. Para clasificar un punto, calcular a qué **bucket** pertenece: el de los puntos con el mismo `h(x)`. Se pueden crear varios `h(x)` con distintos grupos de hiperplanos. En ese caso se calcula el bucket del punto en cada espacio hash y se marcan los puntos que compartieron bucket al menos una vez.
3. Sobre esos candidatos, calcular la distancia en el **espacio original** (no en el hash) y aplicar kNN.

El ejemplo muestra un hiperplano aleatorio que divide el espacio en 0 y 1 alrededor del punto consultado. [T09, p. 57]

LSH tiene tres hiperparámetros: [T09, p. 59] [T09, p. 60]

| Hiperparámetro | Efecto al aumentarlo |
|---|---|
| Número de hiperplanos aleatorios `k` (longitud del vector hash) | Buckets más chicos: más rápido, pero menos preciso. |
| Cantidad de proyecciones hash `L` (grupos de `k` hiperplanos) | Menos riesgo de no evaluar los mejores vecinos, pero más costo. |
| Cantidad de vecinos más cercanos | El `k` típico de kNN. |

La diapositiva llama "cantidad de buckets" a `L` y usa `k` tanto para los hiperplanos como para los vecinos. Ver [Dudas y conflictos](../dudas-y-conflictos.md). **Conocimiento general:** `k` hiperplanos generan hasta `2ᵏ` buckets por proyección.

### Caso real: ANNOY (Spotify)

ANNOY (*Approximate Nearest Neighbors Oh Yeah*) se creó para un contexto muy concreto: recomendar en tiempo real canciones similares, dentro de una base de millones de canciones, a millones de usuarios. [T09, p. 61] Ese contexto impone: [T09, p. 61]

- miles de búsquedas por segundo;
- una construcción razonablemente rápida, porque el índice se actualiza con frecuencia;
- poder indexar ítems nuevos sin rehacer todo.

**Conocimiento general:** ANNOY construye un bosque de árboles de proyecciones aleatorias, que parten el espacio con hiperplanos, y combina la búsqueda en varios árboles. En la biblioteca pública, una vez construido el índice no se le pueden agregar ítems: hay que reconstruirlo.

## kNN como regresor

- **Clasificador:** asigna la clase más votada entre los `k` vecinos más cercanos.
- **Regresor:** predice el promedio de `y` de los `k` vecinos más cercanos, `ŷ(x) = (1/k) · Σ yᵢ`, sumando sobre los vecinos `Nₖ(x)`.
- **Regresor ponderado:** predice el promedio de `y` de los `k` vecinos, ponderado por la inversa de la distancia. [T09, p. 63]

**Inferencia (formalización):** `ŷ(x) = Σ wᵢ yᵢ / Σ wᵢ`, con `wᵢ = 1 / d(x, xᵢ)`.

Un `k` alto da una regresión más suave, pero atenúa más los máximos de la función. Igual que en clasificación, un `k` chico tiende más al sobreajuste. [T09, p. 65] El gráfico compara `k = 3` y `k = 10`: las dos curvas son escalonadas, y la de `k = 10` se aplana en los extremos del rango. [T09, p. 65] **Inferencia:** en los bordes, todos los vecinos quedan del mismo lado del punto, así que el promedio queda sesgado hacia el interior.

Características: [T09, p. 66]

- Es un modelo no paramétrico.
- No aprende una función global.
- Es muy sensible a la escala y al ruido.
- Puede modelar relaciones muy complejas.
- Igual que en clasificación, es muy costoso y escala mal con datasets grandes y con muchas features.

En la figura, kNN ponderado con `k = 10` pasa más cerca de cada punto que kNN uniforme con el mismo `k`. [T09, p. 66]

**Inferencia — "no asume nada":** la diapositiva dice que kNN "no asume nada sobre el modelo". [T09, p. 66] Pero el método sí asume continuidad local. [T09, p. 9] "No paramétrico" significa que no hay un vector fijo de parámetros: el "modelo" son los datos de entrenamiento.

Mejoras de eficiencia: [T09, p. 67]

- Los KD-Trees sirven, pero pierden efectividad con más de 20 dimensiones.
- ANN también sirve, pero la regresión se ve más afectada que la clasificación, porque se calcula un valor de `y` y no una clase.
- **Inferencia:** en clasificación, cambiar un vecino por otro de la misma clase no altera el voto. En regresión, cualquier cambio de vecino mueve el promedio.

## Comparación con árboles y Random Forest

Los árboles y los Random Forests también sirven como regresores: predicen el promedio de `y` en cada hoja. [T09, p. 69] Ver [Árboles de decisión](arboles-de-decision.md#árboles-de-regresión) y [Ensambles y Random Forest](ensambles-random-forest.md#random-forest-como-regresor).

| | kNN | Árbol de decisión | Random Forest |
|---|---|---|---|
| Entrenamiento | Prácticamente nulo. [T09, p. 14] | Construye un árbol. | Construye muchos árboles. |
| Predicción | Costosa: distancias a todo train. [T09, p. 38] | Recorre un camino del árbol. [T07, p. 24] | Recorre un camino en cada árbol. |
| Escalado | Imprescindible. [T09, p. 32] | No hace falta. [T07, p. 26] | No hace falta. |
| Alta dimensión | Las distancias pierden sentido. [T09, p. 39] | Menos afectado: una feature por split. [T09, p. 39] | Menos afectado. |
| Interpretabilidad | Baja. | Muy interpretable. [T09, p. 71] | Menos interpretable. [T09, p. 72] |
| Control de complejidad | `k`, ponderación, métrica. [T09, p. 26] [T09, p. 36] | `max_depth` y otros. [T09, p. 70] | `n_estimators`, `max_features`. [T07, p. 61] |

**Inferencia:** las filas sin cita son una síntesis propia. RF capta diferencias más globales y kNN más locales, así que probablemente cometan errores distintos. Por eso la clase 7 propone combinarlos con *blending*. [T07, p. 72] Ver [Ensambles y Random Forest](ensambles-random-forest.md).

## Conexiones

- [Fundamentos](fundamentos.md): instance-based frente a model-based.
- [Datos y preprocesamiento](datos-y-preprocesamiento.md): escalado y codificación cíclica.
- [EDA y selección de características](eda-y-seleccion.md): dimensionalidad.
- [Evaluación y validación](evaluacion-y-validacion.md): elegir `k` con validación cruzada.
- [Máquinas de vectores de soporte](svm.md): otro modelo que necesita escalado.
