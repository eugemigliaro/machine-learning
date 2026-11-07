# Reducción de dimensionalidad: PCA y t-SNE

## Por qué reducir dimensiones

En los datasets reales los datos tienen muchas variables. Eso trae cuatro problemas: [T14, p. 44]

- **Maldición de la dimensionalidad:** a mayor dimensión, el espacio crece exponencialmente y los puntos quedan dispersos.
- **Ruido y redundancia:** muchas variables están correlacionadas y no agregan información real.
- **Costo computacional:** más dimensiones implican más tiempo de entrenamiento.
- **Visualización:** las personas solo podemos ver dos o tres dimensiones.

Hay dos objetivos distintos: **comprimir** los datos y **visualizarlos**. [T14, p. 44] PCA sirve sobre todo para lo primero y t-SNE para lo segundo.

La clase 3 distinguía *feature selection*, que conserva un subconjunto de las variables originales, de *feature projection*, que las combina en una representación más compacta. [T03, p. 61] **Inferencia:** PCA y t-SNE son métodos de proyección. La clase 9 ya recomendaba PCA o autoencoders para que kNN calcule distancias más informativas. [T09, p. 42] Ver [EDA y selección de características](eda-y-seleccion.md).

## PCA: análisis de componentes principales

### Qué es

PCA es un método **lineal** de reducción de dimensionalidad. Transforma los datos originales en un nuevo conjunto de variables, las **componentes principales**, ordenadas por la cantidad de varianza que explican. [T14, p. 45]

Propiedades: [T14, p. 45]

- Las componentes son **ortogonales** entre sí: no están correlacionadas.
- La primera componente captura la **mayor varianza posible**.
- Cada componente siguiente captura la mayor varianza restante.
- Es **no supervisado**: no usa etiquetas.

### Idea geométrica y pasos

PCA busca los ejes en los que los datos tienen mayor dispersión. Proyectar sobre esos ejes conserva la mayor cantidad de información posible. [T14, p. 46]

1. Estandarizar los datos.
2. Calcular la matriz de covarianza.
3. Obtener sus autovectores y autovalores.
4. Ordenar los autovectores por autovalor descendente: esas son las componentes principales.
5. Proyectar los datos sobre las primeras `k` componentes. [T14, p. 46]

El resultado es un **cambio de base**: de `p` variables originales a `k` componentes, con `k ≤ p`. [T14, p. 46]

**Conocimiento general:**

- El autovalor `λ_j` es la varianza de los datos proyectados sobre la componente `j`.
- La proporción de varianza explicada por esa componente es `λ_j / Σ λ`.
- La proyección es `Z = X_std · W_k`, donde las columnas de `W_k` son los primeros `k` autovectores.

### Cuántas componentes elegir

Cada componente explica una proporción de la varianza total, llamada **varianza explicada**. [T14, p. 47] Hay dos criterios comunes:

- **Umbral de varianza acumulada:** elegir `k` tal que las primeras `k` componentes expliquen un `x %` de la varianza.
- **Gráfico de codo (*scree plot*):** graficar la varianza explicada por componente y buscar el codo, como en el método del codo de [K-means](clustering.md#elección-de-k). [T14, p. 47]

No existe un criterio universal: la elección depende del problema y del objetivo. [T14, p. 47]

El *scree plot* del ejemplo tiene estos porcentajes para las diez componentes: 41,2; 18,4; 12,4; 8,2; 7; 4,2; 3; 2,7; 1,6 y 1,2. Al lado aparece un *biplot*: los países proyectados sobre las dos primeras componentes, con flechas para las variables originales. [T14, p. 47]

**Inferencia:** según esos porcentajes, dos componentes explican el 59,6 % de la varianza, cuatro el 80,2 % y seis el 91,4 %. Con un umbral del 90 % habría que quedarse con seis.

### Ventajas y limitaciones

| Ventajas | Limitaciones |
|---|---|
| Reduce la dimensionalidad manteniendo la mayor varianza posible. | Solo captura relaciones lineales. |
| Elimina correlaciones entre variables. | Las componentes pueden ser difíciles de interpretar. |
| Es útil como preprocesamiento para otros algoritmos de ML. | Es sensible a la escala de las variables, así que requiere estandarizar. |
| Sus resultados son interpretables mediante los *loadings* de las variables. | No preserva estructuras no lineales, como clusters curvos. |
| Es computacionalmente eficiente. | |

[T14, p. 48]

**Inferencia:** la tabla lista la interpretabilidad como ventaja y como limitación. No es una contradicción. Los *loadings* (las flechas del biplot) muestran cuánto pesa cada variable original en cada componente. [T14, p. 47] Pero cada componente es una combinación de todas las variables y no siempre tiene un significado claro.

**Inferencia:** si PCA se usa como preprocesamiento de un modelo supervisado, el estandarizador y PCA se ajustan solo con train, dentro del pipeline, igual que cualquier transformación aprendida. Si no, la información de validación o test se filtra al entrenamiento. Ver [leakage](evaluacion-y-validacion.md).

### PCA frente a LDA

LDA proyecta sobre la dirección que maximiza la separación **entre clases**, usando las etiquetas. PCA maximiza la **varianza total** sin mirarlas. [T06, p. 27] [T06, p. 28] Ver [GDA y Naive Bayes](gda-y-naive-bayes.md).

## t-SNE

*t-distributed Stochastic Neighbor Embedding*. [T14, p. 49]

### Qué es

t-SNE es un método **no lineal** diseñado específicamente para **explorar y visualizar** datos de alta dimensión en 2D o 3D. [T14, p. 50]

**Idea central:** preserva las relaciones de **vecindad local**. Los puntos que estaban cerca en el espacio original tienden a quedar cerca en la proyección. [T14, p. 50]

Las tres fórmulas de la clase: [T14, p. 50]

```text
Dimensión original (gaussiana):
  p_{j|i} = exp(−‖x_i − x_j‖² / 2σ_i²) / Σ_{k≠i} exp(−‖x_i − x_k‖² / 2σ_i²)

Dimensión resultante (t de Student):
  q_ij = (1 + ‖y_i − y_j‖²)⁻¹ / Σ_{k≠l} (1 + ‖y_k − y_l‖²)⁻¹

Costo (divergencia de Kullback-Leibler):
  C = Σ_i KL(P_i ‖ Q_i)
```

### Cómo funciona

[T14, p. 51]

1. Para cada par de puntos del espacio original, calcular la probabilidad de que sean vecinos con una distribución gaussiana. Los puntos cercanos tienen probabilidad alta.
2. En el espacio de baja dimensión, inicializar los puntos al azar y calcular sus probabilidades de vecindad con una distribución t de Student.
3. Optimizar iterativamente la posición de los puntos para que las dos distribuciones se parezcan lo más posible, es decir, minimizar la divergencia KL.

La diapositiva incluye el pseudocódigo del paper original: [T14, p. 51]

- **Entradas:** los datos, la perplejidad, la cantidad de iteraciones `T`, la tasa de aprendizaje `η` y el momentum `α(t)`.
- **Probabilidades simétricas:** `p_ij = (p_{j|i} + p_{i|j}) / 2n`.
- **Inicialización:** la solución inicial se muestrea de `N(0, 10⁻⁴ I)`.
- **Iteraciones:** en cada una se calculan los `q_ij`, se calcula el gradiente y se actualizan las posiciones con un paso de gradiente más un término de momentum.

El gradiente es:

```text
∂C/∂y_i = 4 · Σ_j (p_ij − q_ij) (y_i − y_j) (1 + ‖y_i − y_j‖²)⁻¹
```

La regla de actualización de la diapositiva suma `η · ∂C/∂Y`, igual que el paper; para minimizar hay que avanzar en sentido opuesto al gradiente. Ver [Dudas y conflictos](../dudas-y-conflictos.md).

**Conocimiento general:**

- **El gradiente:** si `p_ij > q_ij`, dos puntos que eran vecinos quedaron demasiado lejos y se atraen. Si `p_ij < q_ij`, se repelen.
- **La t de Student:** tiene colas pesadas, así que en 2D los puntos moderadamente lejanos pueden ubicarse todavía más lejos. Eso alivia el *crowding problem* y separa los grupos.
- **El `σ_i` de cada punto:** se ajusta para que su distribución de vecinos tenga la perplejidad pedida.

### Perplejidad

La **perplejidad** controla el balance entre estructura local y global. Informalmente, indica cuántos vecinos cercanos considera cada punto al calcular sus probabilidades de vecindad. Los valores típicos van de 5 a 50, con 30 por defecto. [T14, p. 52]

| Perplejidad | Efecto |
|---|---|
| Baja (5–10) | Capta estructuras muy locales; puede fragmentar clusters reales. |
| Media (30) | Balance recomendado para la mayoría de los datasets. |
| Alta (50 o más) | Capta más estructura global; los clusters pueden solaparse más. |

[T14, p. 52]

**Advertencia de la clase:** las **distancias entre clusters** de un gráfico de t-SNE **no son interpretables**. Solo es significativa la cohesión interna de cada grupo. [T14, p. 52]

**Conocimiento general:**

- **Tamaño de los grupos:** tampoco es interpretable.
- **Semilla:** distintas semillas dan figuras distintas.
- **Puntos nuevos:** t-SNE no aprende una función reutilizable para proyectarlos. `TSNE` de scikit-learn no tiene `transform`.
- **Costo:** la versión exacta es cuadrática en la cantidad de puntos; la aproximación de Barnes-Hut lo baja a `O(n log n)`.

**Inferencia:** por eso t-SNE se usa para explorar, como dice la clase. [T14, p. 50] No funciona como paso de preprocesamiento de un modelo predictivo, cosa que PCA sí permite. [T14, p. 48]

### Ejemplo: MNIST

La clase aplica t-SNE al dataset MNIST de dígitos manuscritos. La proyección en 2D forma grupos bien separados, coloreados por dígito. [T14, p. 53] **Inferencia:** t-SNE no usa las etiquetas; solo sirven para colorear la figura. Que cada color quede en su propio grupo indica que los dígitos ya forman vecindades distintas en el espacio de píxeles.

En la comparación con el mismo dataset, PCA a 2D produce una sola nube donde los dígitos se superponen. t-SNE separa los diez grupos. [T14, p. 54]

## PCA frente a t-SNE

| Aspecto | PCA | t-SNE |
|---|---|---|
| Tipo | Lineal. [T14, p. 45] | No lineal. [T14, p. 50] |
| Qué preserva | La varianza: las direcciones de mayor dispersión. [T14, p. 45] [T14, p. 46] | Las vecindades locales. [T14, p. 50] |
| Uso principal | Comprimir y preprocesar para otros modelos. [T14, p. 44] [T14, p. 48] | Explorar y visualizar en 2D o 3D. [T14, p. 50] |
| Hiperparámetro | Cantidad de componentes `k`. [T14, p. 47] | Perplejidad. [T14, p. 52] |
| Interpretación | *Loadings* de las variables. [T14, p. 48] | Las distancias entre clusters no se interpretan. [T14, p. 52] |
| Inicialización | **Conocimiento general:** determinista, salvo el signo de las componentes. | Aleatoria. [T14, p. 51] |
| MNIST en 2D | Clases superpuestas. [T14, p. 54] | Grupos separados. [T14, p. 54] |

## Conexiones

- [Clustering: K-means y DBSCAN](clustering.md): el otro bloque de la clase 14 y el método del codo.
- [EDA y selección de características](eda-y-seleccion.md): dimensionalidad, *feature selection* y *feature projection*.
- [Aprendizaje basado en instancias (kNN)](aprendizaje-basado-en-instancias.md): por qué la dimensionalidad perjudica a los métodos basados en distancias.
- [GDA y Naive Bayes](gda-y-naive-bayes.md): LDA como proyección supervisada.
- [Datos y preprocesamiento](datos-y-preprocesamiento.md): estandarización.
