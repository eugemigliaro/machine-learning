# Clustering: K-means y DBSCAN

## Aprendizaje no supervisado

En el aprendizaje supervisado, el modelo se apoya en una variable respuesta conocida. En el no supervisado esa respuesta es desconocida: el modelo trabaja con las relaciones entre las variables observadas, sin datos anotados. [T14, p. 3] Es la misma distinción que planteó la clase 1. [T01, p. 28] El programa ubica estos métodos en el módulo 4, "No supervisado y feature engineering": clustering y reducción de dimensionalidad. [T01, p. 48]

Aplicaciones típicas: [T14, p. 4]

- **Segmentación de usuarios**, por ejemplo de compradores online para campañas de marketing.
- **Sistemas de recomendación**, como los de las plataformas de streaming.
- **Detección de anomalías.**

La clase distingue tres usos comunes: [T14, p. 5]

| Uso | Idea | Ejemplo de la clase |
|---|---|---|
| **Agrupamiento** | Agrupar por similitudes. | Dividir pacientes por síndromes. |
| **Reducción de dimensiones** | Identificar dependencias ocultas y aprovechar las características para crear mejores modelos. | Ver [Reducción de dimensionalidad](reduccion-de-dimensionalidad.md). |
| **Asociación** | Reglas del tipo si/entonces. | Algoritmo Apriori. |

La asociación solo se nombra; la clase no la desarrolla. [T14, p. 5] **Conocimiento general:** Apriori busca conjuntos de ítems que aparecen juntos con frecuencia, como productos de una misma compra, y deriva reglas del tipo "si compra A, compra B".

## Qué es el clustering

El clustering agrupa las observaciones según algún criterio para encontrar subgrupos (*clusters*) en los datos. Busca que la similitud entre los miembros de un mismo cluster sea lo más fuerte posible. [T14, p. 6] En términos de distancia: [T14, p. 7]

- **minimizar la distancia intra-cluster**: las observaciones de un mismo cluster son similares;
- **maximizar la distancia inter-cluster**: las de clusters distintos no lo son.

**No hay una única forma correcta de agrupar.** El ejemplo de la clase usa los mismos cinco personajes de dibujos animados. Se pueden agrupar como niños y adultos, o según si van o no a la primaria. La mejor agrupación depende del objetivo. [T14, p. 8] [T14, p. 9] [T14, p. 10]

### Familias de métodos

Hay muchos métodos de clustering y distintos criterios para clasificarlos. Un diagrama de la clase los cruza en tres ejes: *hard* frente a *soft*, basados en prototipos frente a basados en densidad, y particionales frente a jerárquicos. [T14, p. 11]

| Criterio | Opción A | Opción B |
|---|---|---|
| Estructura | **Partición:** divide el espacio y encuentra todos los clusters a la vez. | **Jerárquico:** genera una jerarquía de clusters anidados (un dendrograma). [T14, p. 11] |
| Qué define un cluster | **Prototipo:** K-means. | **Densidad:** DBSCAN. |
| Pertenencia | **Hard:** cada punto, un solo cluster. | **Soft:** grado de pertenencia a cada cluster. |

Las definiciones de *hard* y *soft* son **conocimiento general**: la clase solo las nombra en el diagrama. Tampoco desarrolla métodos jerárquicos ni *soft*.

### Clusters basados en prototipos

En un cluster basado en prototipos, cada objeto está más cerca del prototipo de su cluster que del prototipo de cualquier otro. [T14, p. 12]

- Con atributos **continuos**, el prototipo puede ser el **centroide**.
- Con atributos **categóricos**, es el objeto más representativo del cluster. [T14, p. 12]

**Conocimiento general:** esa segunda variante corresponde a K-medoids, que usa como prototipo un punto real del cluster, o a K-modes, que usa la moda de cada atributo.

## K-means

### Definición

K-means (k medias) genera una **partición** de `n` observaciones en `k` grupos. Cada grupo está representado por el promedio de sus puntos: el **centroide**. El valor de `k`, es decir el número de clusters, se fija **a priori**. [T14, p. 14]

Formalmente, dadas observaciones `x₁, …, xₙ ∈ ℝᵖ`, K-means construye una partición `S = {S₁, …, S_K}` (con `K ≤ n`) que minimiza la distancia de los elementos dentro de cada grupo: [T14, p. 15]

```text
argmin_S  Σ_{i=1..K}  Σ_{x ∈ S_i}  ‖x − μ_i‖²        μ_i = centroide de S_i
```

Los conjuntos de índices `C₁, …, C_K` son una partición en sentido estricto: [T14, p. 16]

- cada observación pertenece a alguno: `C₁ ∪ C₂ ∪ … ∪ C_K = {1, …, n}`;
- ninguna pertenece a dos: `C_i ∩ C_j = ∅` para todo `i ≠ j`.

La clase muestra dos figuras. En una, los grupos no se superponen: es una partición y puede venir de K-means. En la otra, las elipses se solapan: no es una partición y no puede ser un resultado de K-means. [T14, p. 17]

### La variación dentro del cluster

Un buen agrupamiento tiene **poca variación dentro de cada cluster**. [T14, p. 18] La variación del cluster `C_k` se mide con distancias euclídeas al cuadrado: [T14, p. 19] [T14, p. 20]

```text
W(C_k) = (1 / |C_k|) · Σ_{i,j ∈ C_k} Σ_{l=1..p} (x_il − x_jl)²
```

- `|C_k|` es la cantidad de puntos del cluster.
- La primera suma recorre todos los pares de puntos `i, j` del cluster; la segunda, las `p` dimensiones.
- `x_il` y `x_jl` son las coordenadas de los puntos `i` y `j` en la dimensión `l`.

El objetivo es minimizar la variación total: [T14, p. 21]

```text
min_{C₁,…,C_K}  Σ_{k=1..K}  W(C_k)
```

Esta **suma de cuadrados dentro de los clusters** (WCSS, *within-cluster sum of squares*) mide la compacidad del agrupamiento, y se quiere lo más chica posible. K-means es un algoritmo para optimizar esta función objetivo. [T14, p. 21]

**Inferencia:** la fórmula por pares y la de la diapositiva 15, por distancia al centroide, tienen el mismo minimizador. La clase usa las dos y dice que `W` es la suma de distancias "entre los elementos y su respectivo centroide". [T14, p. 19] La identidad que las une es:

```text
(1/|C_k|) · Σ_{i,j ∈ C_k} ‖x_i − x_j‖²  =  2 · Σ_{i ∈ C_k} ‖x_i − μ_k‖²
```

Es decir, la versión por pares vale el doble de la suma de distancias al centroide. Ver [Dudas y conflictos](../dudas-y-conflictos.md).

### El algoritmo

Dado `K`: [T14, p. 22]

1. **Inicialización:** asignar al azar un número de 1 a `K` a cada observación.
2. Repetir hasta que la asignación no cambie de una iteración a la siguiente:
   1. **Actualizar:** calcular el centroide de cada cluster, que es el promedio de sus observaciones en cada variable.
   2. **Asignar:** pasar cada observación al cluster cuyo centroide esté más cerca, en distancia euclídea.

La diapositiva animada resume el ciclo como inicialización, asignación, actualización y repetición. [T14, p. 23]

Propiedades: [T14, p. 24]

- El método cambia una asignación solo si mejora el objetivo, así que **siempre converge**.
- Cuando un paso no produce cambios, se llegó a un **mínimo local**, no necesariamente al global.

**Conocimiento general:** la convergencia está garantizada porque ningún paso aumenta la WCSS y el número de particiones posibles es finito. El paso de actualización usa la media porque es el punto que minimiza la suma de distancias al cuadrado de un grupo.

### Dependencia de la inicialización

El resultado final **depende fuertemente de la asignación inicial**. [T14, p. 26] La figura de la clase corre seis veces el mismo modelo sobre los mismos datos. El valor del objetivo da 320,9, cuatro veces 235,8 y una vez 310,9. Solo cuatro corridas llegan al mejor agrupamiento encontrado. [T14, p. 26]

Para mitigarlo: [T14, p. 27]

- aplicar el método **varias veces**, con distintas inicializaciones;
- quedarse con el agrupamiento que **minimiza `Σ_k W(C_k)`**.

**Conocimiento general:** scikit-learn (`KMeans`) lo hace con el parámetro `n_init`. Además, por defecto inicializa con *k-means++*, que elige centroides iniciales alejados entre sí.

### Elección de `k`

Al aumentar `K`, la variabilidad dentro de los clusters disminuye, pero se corre el riesgo de **sobresegmentar** los datos. Hay que buscar un `k` que dé una segmentación útil y representativa. [T14, p. 28]

**Inferencia:** por eso no se puede elegir `k` minimizando la WCSS. Con `K = n`, cada punto es su propio cluster y la WCSS vale 0.

Elegir `k` no es trivial en la mayoría de los datasets reales, y **ningún método funciona siempre**. [T14, p. 30] La clase presenta dos:

- **Método del codo:** se grafica la WCSS en función de `k` y se busca el "codo", donde la disminución de la variabilidad se estabiliza. [T14, p. 29] En el ejemplo de la diapositiva 29, el codo está en `k = 5`. En el de la 30, la curva de SSE tiene el codo en `k = 3`. [T14, p. 29] [T14, p. 30]
- **Coeficiente de silhouette:** [T14, p. 30]

  ```text
  s(i) = (b(i) − a(i)) / max(a(i), b(i))
  ```

  En el ejemplo, el silhouette es máximo (≈ 0,59) en `k = 3`, lo que coincide con el codo. [T14, p. 30]

**Conocimiento general:** la clase no define `a(i)` ni `b(i)`.

- `a(i)` es la distancia promedio de `i` a los demás puntos de su cluster.
- `b(i)` es la menor distancia promedio de `i` a los puntos de otro cluster.
- `s(i)` va de −1 a 1. Cerca de 1, el punto está bien asignado; cerca de 0, está en la frontera; si es negativo, probablemente está en el cluster equivocado.
- Se elige el `k` que maximiza el silhouette promedio.

### Limitaciones

K-means asume clusters **esféricos** y de **densidad uniforme**. Por eso le cuesta identificar grupos con densidades diferentes, como las distintas partes de una media luna. [T14, p. 31]

La diapositiva 31 lo muestra con dos medias lunas entrelazadas. K-means las corta mal, mezclando la punta de una con la otra, y obtiene un silhouette de 0,5. DBSCAN separa correctamente cada media luna, pero su silhouette es 0,38. En la otra figura de la diapositiva, dos círculos concéntricos quedan divididos por una línea en lugar de separarse en círculo interior y exterior. [T14, p. 31]

**Inferencia:** el ejemplo muestra que un silhouette más alto no garantiza un mejor agrupamiento cuando los clusters no son convexos. La métrica premia grupos compactos y separados, la misma forma que asume K-means.

### Pros y contras

| Ventajas | Desventajas |
|---|---|
| Simple y fácil de implementar. | Depende de la inicialización. |
| Su orden es lineal. | Tiende a caer en un mínimo local. |
| | Sensible a outliers. |
| | Los clusters tienen que ser esféricos. |
| | No se puede aplicar a datos categóricos. |

[T14, p. 32]

**Inferencia y conocimiento general:**

- **Outliers:** el centroide es una media y el objetivo eleva las distancias al cuadrado, así que un punto extremo arrastra a su centroide.
- **Costo lineal:** cada iteración cuesta `O(n · K · p)`.
- **Escala:** como usa distancia euclídea, las variables con mayor escala dominan la distancia. Conviene escalarlas, igual que en kNN. [T09, p. 32]

### Usos de K-means

**Compresión de imágenes:** reduce el tamaño de un archivo de imagen sin reducir significativamente su calidad. El ejemplo pasa de 16,77 millones de colores a 16. [T14, p. 33] **Conocimiento general:** cada píxel es un punto en el espacio RGB. K-means agrupa los colores y reemplaza cada píxel por el centroide de su cluster. Así basta guardar `k` colores más un índice por píxel. 16,77 millones es `2²⁴`, la cantidad de colores de 24 bits.

Una segunda figura muestra una imagen original junto a reconstrucciones con `k = 5, 10, 70, 100` y `200`: cuanto mayor es `k`, más se parece al original. La diapositiva no explica cómo se construyeron. [T14, p. 34]

## DBSCAN

*Density-Based Spatial Clustering of Applications with Noise*. [T14, p. 35]

DBSCAN agrupa puntos según su **densidad local**. Los puntos con suficientes vecinos cercanos forman un grupo, y los aislados se consideran **ruido o anomalías**. [T14, p. 36]

### Hiperparámetros

- **`ε` (epsilon):** radio de vecindad; define qué tan cerca deben estar dos puntos para ser vecinos.
- **`minPts`:** número mínimo de vecinos dentro del radio `ε` para que un punto sea **núcleo**. [T14, p. 37]

### Tipos de puntos

| Tipo | Definición |
|---|---|
| **Núcleo** (*core point*) | Tiene al menos `minPts` puntos, incluido él mismo, dentro del radio `ε`. |
| **Alcanzable o frontera** (*border point*) | Está dentro del radio `ε` de un punto núcleo, pero no tiene suficientes vecinos para ser núcleo. |
| **Ruido** (*noise point*) | No pertenece a ningún grupo ni está cerca de un punto núcleo. |

[T14, p. 38] La figura de la clase usa `minPts = 3`. [T14, p. 37]

### Algoritmo

[T14, p. 39]

1. **Inicialización:** marcar todos los puntos como no visitados y crear una lista vacía de clusters.
2. **Selección:** elegir un punto `p` no visitado y marcarlo como visitado.
3. **Búsqueda de vecinos:** encontrar todos los puntos dentro del radio `ε` de `p`.
   - Si son menos de `minPts`, marcar `p` como ruido **por ahora**.
   - Si son `minPts` o más, crear un cluster nuevo con `p`.
4. **Expansión:** agregar al cluster todos los vecinos `q` de `p`. Para cada `q`:
   - si no fue visitado, marcarlo como visitado;
   - si tiene al menos `minPts` vecinos, agregar esos vecinos al cluster, de forma recursiva;
   - si tiene menos de `minPts` vecinos, marcarlo como punto frontera y no expandir desde él.
5. **Repetir** hasta visitar todos los puntos.

La diapositiva dice "si `q` *no tiene menos* de `minPts` vecinos" para el caso frontera; se lee "tiene menos". Ver [Dudas y conflictos](../dudas-y-conflictos.md).

**Inferencia:** el "por ahora" del paso 3 importa. Un punto marcado como ruido puede caer después dentro del radio `ε` de un núcleo de otro cluster; en ese caso se incorpora como punto frontera.

La animación de la diapositiva 40 muestra cómo crece un cluster a lo largo de un anillo de puntos, con `ε = 1,00` y `minPoints = 4`. [T14, p. 40]

### Ventajas y desventajas

| Ventajas | Desventajas |
|---|---|
| No requiere el número de grupos como hiperparámetro. | Hay que definir `ε` y `minPts`. |
| Identifica outliers. | No es resistente a grupos con distintas densidades. |
| Identifica clusters con formas variadas. | Es menos eficiente en datasets grandes o de alta dimensionalidad. |

[T14, p. 41]

**Inferencia:** el problema de las densidades distintas viene de que `ε` y `minPts` son globales. Un `ε` adecuado para un grupo denso deja como ruido los puntos de un grupo disperso; uno adecuado para el disperso puede fusionar los grupos densos. En alta dimensionalidad, además, las distancias pierden capacidad de discriminar, lo que dificulta elegir `ε`. [T09, p. 39]

**Conocimiento general:**

- **`minPts`:** suele tomarse al menos `p + 1`, y es común `2 · p`, con `p` features.
- **`ε`:** se elige con el gráfico de *k-distancias*. Se ordena la distancia de cada punto a su `minPts`-ésimo vecino y se busca el codo de la curva.

## K-means frente a DBSCAN

| Aspecto | K-means | DBSCAN |
|---|---|---|
| Familia | Prototipos (centroide). [T14, p. 12] | Densidad. [T14, p. 36] |
| Hiperparámetros | `k`, fijado a priori. [T14, p. 14] | `ε` y `minPts`; no requiere `k`. [T14, p. 37] [T14, p. 41] |
| Forma de los clusters | Esférica. [T14, p. 31] [T14, p. 32] | Variada. [T14, p. 41] |
| Outliers | Sensible: los asigna a algún cluster. [T14, p. 16] [T14, p. 32] | Los identifica como ruido. [T14, p. 36] [T14, p. 41] |
| Densidades distintas | Dificultades. [T14, p. 31] | No es resistente. [T14, p. 41] |
| Inicialización | Aleatoria; el resultado depende de ella. [T14, p. 26] | **Conocimiento general:** núcleos y ruido no dependen del orden; un punto frontera alcanzable desde dos clusters puede quedar en cualquiera. |
| Costo | Lineal. [T14, p. 32] | Menos eficiente con muchos datos o dimensiones. [T14, p. 41] |

**Inferencia:** las dos dependen de una distancia, así que heredan los problemas de escala y de dimensionalidad de [kNN](aprendizaje-basado-en-instancias.md). Una práctica común es escalar y, si hay muchas variables, reducir dimensiones antes de agrupar. Ver [Reducción de dimensionalidad](reduccion-de-dimensionalidad.md).

## Conexiones

- [Fundamentos](fundamentos.md): paradigmas de aprendizaje.
- [Reducción de dimensionalidad](reduccion-de-dimensionalidad.md): el otro bloque de la clase 14, con PCA y t-SNE.
- [Aprendizaje basado en instancias (kNN)](aprendizaje-basado-en-instancias.md): distancias, escalado y búsqueda de vecinos.
- [Máquinas de vectores de soporte](svm.md): One-Class SVM, otro enfoque para detectar anomalías.
- [Datos y preprocesamiento](datos-y-preprocesamiento.md): escalado y outliers.
