# Máquinas de vectores de soporte (SVM)

## Idea

SVM es un algoritmo supervisado que sirve para clasificación y para regresión. Su objetivo principal es encontrar el hiperplano óptimo que mejor separa las clases. [T08, p. 10] La clase desarrolla solamente la clasificación binaria, su extensión multiclase y, muy brevemente, One-Class SVM. [T08, p. 1]

La presentación avanza en cuatro pasos, cada uno generalizando el anterior:

1. **Clasificador de margen maximal:** clases linealmente separables.
2. **Clasificador con margen tolerante:** permite violar el margen.
3. **Límites de decisión no lineales:** amplía el espacio de atributos.
4. **Máquina de vectores de soporte:** generaliza el paso anterior con núcleos (*kernels*). [T08, p. 40]

## Hiperplanos y separabilidad lineal

En un espacio de `p` dimensiones, un hiperplano es `b₀ + b₁x₁ + … + b_p x_p = 0`. En `R²` es una recta; en `R³`, un plano. [T08, p. 6] [T08, p. 11] Los puntos donde la expresión es positiva quedan de un lado; los que dan negativa, del otro. [T08, p. 11]

Con `n` ejemplos de `p` atributos y clases `yᵢ ∈ {1, −1}`, un hiperplano separa las clases si todos los ejemplos de clase 1 dan positivo y todos los de clase −1 dan negativo. Las dos condiciones se resumen en una sola: [T08, p. 12] [T08, p. 13] [T08, p. 14]

```text
yᵢ · (b₀ + b₁xᵢ,₁ + … + b_p xᵢ,p) > 0   para todo i
```

**Ejemplo:** con la recta `−2 − 4x₁ + 3x₂ = 0`, el punto `(2, 10)` de clase 1 da `1 · 20 > 0` y el punto `(6, 4)` de clase −1 da `−1 · (−14) > 0`. Ambos están bien clasificados. [T08, p. 15]

Para clasificar una observación nueva `x′` se mira el signo de `f(x′) = b₀ + b₁x′₁ + … + b_p x′_p`. El módulo `|f(x′)|` indica la cercanía al hiperplano. [T08, p. 16] Esa distancia mide la confianza: una observación lejana está bien adentro de su clase, y una cercana a 0 está cerca de la otra clase. [T08, p. 17]

**Construcción geométrica:** se toma la envolvente convexa de cada clase, se traza el segmento más corto que une ambas envolventes y se toma su perpendicular por el punto medio. [T08, p. 7] [T08, p. 8]

## Clasificador de margen maximal

Si las clases son separables, en general hay infinitos hiperplanos que las separan. [T08, p. 18] Para elegir uno:

- El **margen** de un hiperplano `H` es la distancia del ejemplo más cercano a `H`. [T08, p. 19]
- El **hiperplano de margen maximal** (o de separación óptimo) es el que tiene margen máximo. El clasificador que lo usa se llama **clasificador de margen maximal**. [T08, p. 21] [T08, p. 22]
- Quedan definidos dos hiperplanos paralelos a `H`, `H+` y `H−`, ambos a distancia `M` (el margen). [T08, p. 22]
- Los ejemplos que quedan sobre `H+` y `H−` son los **vectores de soporte**. El hiperplano óptimo depende solamente de ellos y no del resto de los ejemplos. [T08, p. 23]

Formulación: encontrar `b` que maximice `M` sujeto a [T08, p. 24]

```text
yᵢ · (b₀ + b₁xᵢ,₁ + … + b_p xᵢ,p) ≥ M      para todo i
Σⱼ bⱼ² = 1
```

**Inferencia:** la restricción `Σⱼ bⱼ² = 1` fija la escala de los coeficientes. Con esa normalización, `yᵢ · f(xᵢ)` es la distancia con signo de `xᵢ` al hiperplano. Por eso la primera restricción dice que ningún ejemplo queda a menos de `M` del hiperplano, y `|f(x′)|` funciona como distancia. [T08, p. 16] [T08, p. 24]

**Concept check:** con margen duro, si se eliminan del entrenamiento el 80 % de los datos muy alejados de la frontera y se reentrena con el 20 % restante, ¿qué le pasa al hiperplano? [T08, p. 25] **Inferencia:** no cambia, siempre que los vectores de soporte sigan en el 20 %. Los puntos eliminados están fuera del margen, así que no son vectores de soporte. [T08, p. 23]

## Clasificador con margen tolerante

El hiperplano de margen maximal no siempre conviene. Si dos clases están bien separadas y se agrega un único ejemplo cerca de la otra clase, el margen se achica mucho. Muchas observaciones que antes se clasificaban con confianza pasan a quedar cerca de la frontera. [T08, p. 26] [T08, p. 27]

El clasificador con margen tolerante (*soft margin*) busca: [T08, p. 29]

- clasificar cada observación con robustez, sin que su distancia al hiperplano sea crítica;
- clasificar mejor a la mayoría de los ejemplos, incluso cuando las clases no son linealmente separables.

Formulación: encontrar `b` y `ε₁, …, εₙ` que maximicen `M` sujeto a [T08, p. 30]

```text
yᵢ · (b₀ + b₁xᵢ,₁ + … + b_p xᵢ,p) ≥ M · (1 − εᵢ)   para todo i
Σⱼ bⱼ² = 1
εᵢ ≥ 0   y   Σᵢ εᵢ ≤ C
```

Cada **variable de holgura** `εᵢ` permite que `xᵢ` quede en un lugar erróneo: [T08, p. 30] [T08, p. 31]

| Valor de `εᵢ` | Posición de `xᵢ` |
|---|---|
| `εᵢ = 0` | Del lado correcto del margen. |
| `εᵢ > 0` | Del lado incorrecto del margen. |
| `εᵢ > 1` | Del lado incorrecto del hiperplano: mal clasificado. |

`C` es un parámetro de ajuste. Si `C = 0`, se vuelve al clasificador de margen maximal. Se puede elegir con validación cruzada. [T08, p. 30] [T08, p. 32] **Inferencia:** como cada error de clasificación aporta `εᵢ > 1` y la suma no puede superar `C`, en esta formulación hay a lo sumo `C` ejemplos de entrenamiento mal clasificados. [T08, p. 30] [T08, p. 31]

> **Atención — dos sentidos de `C`.** En esta formulación, `C` es un *presupuesto* de violaciones: más `C` significa más tolerancia. La diapositiva de kernels RBF usa `C` como *costo* de violar el margen: más `C` significa menos tolerancia y menos regularización. [T08, p. 49] Las dos lecturas van en direcciones opuestas. Ver [Dudas y conflictos](../dudas-y-conflictos.md).

## Límites de decisión no lineales

Los clasificadores anteriores funcionan bien cuando la separación entre clases es lineal, pero no en casos no lineales. [T08, p. 33]

**Ejemplo:** [T08, p. 34] [T08, p. 35]

- En `R²`, los puntos `(±2, ±2)` son de clase −1 y los `(±1, ±1)` son de clase 1. No hay recta que los separe.
- Si cada punto se representa en `R³` como `(x₁, x₂, x₁²)`, la tercera coordenada vale 4 en la clase −1 y 1 en la clase 1. Ahora sí existe un hiperplano de separación.
- **Inferencia:** por ejemplo, el plano `x₃ = 2,5`.

En general, los `p` atributos se pueden representar en `2p` dimensiones como `xᵢ₁, xᵢ₁², …, xᵢp, xᵢp²`, donde podría existir un hiperplano de dimensión `2p − 1` que los separe. [T08, p. 36] El problema es el mismo del margen tolerante, con coeficientes `bⱼ₁` para cada `xᵢⱼ` y `bⱼ₂` para cada `xᵢⱼ²`. [T08, p. 37] Se puede usar otro grado u otra función. La separabilidad lineal en el espacio ampliado equivale a una separabilidad no lineal en el espacio original, con el costo de aumentar la dimensión. [T08, p. 38] [T08, p. 39]

## Núcleos (kernels)

Como el clasificador de margen maximal depende solamente de los vectores de soporte, existen `α₁, …, α_k` tales que [T08, p. 41] [T08, p. 42]

```text
f(x) = b₀ + Σᵢ αᵢ · K(x, xᵢ)      (suma sobre los vectores de soporte)
```

donde `K(x, xᵢ) = ⟨x, xᵢ⟩` es el **núcleo** (*kernel*). Si se cambia el núcleo, la formulación del problema no cambia y `f(x)` se sigue calculando igual. [T08, p. 50]

| Núcleo | Fórmula | Comportamiento |
|---|---|---|
| Lineal | `K(x, x′) = x · x′` | Equivale a `f(x) = b₀ + b₁x₁ + … + b_p x_p`. [T08, p. 43] |
| Polinómico | `K(x′, xᵢ) = (1 + Σⱼ xᵢⱼ x′ⱼ)^d` | Con `d` mayor hay más flexibilidad para encontrar una separación lineal en el espacio ampliado. [T08, p. 44] [T08, p. 45] |
| Radial (RBF) | `K(x′, xᵢ) = exp(−γ Σⱼ (xᵢⱼ − x′ⱼ)²)`, con `γ > 0` | Produce fronteras cerradas y locales alrededor de grupos de puntos. [T08, p. 46] [T08, p. 47] |

**Conocimiento general:** esto se conoce como *truco del kernel*. Como el problema solamente necesita productos internos entre ejemplos, basta calcular `K` y no hace falta construir explícitamente el espacio ampliado, cuya dimensión crece rápido. [T08, p. 38]

### Hiperparámetros del kernel RBF

| Hiperparámetro | Significado | Pequeño | Grande |
|---|---|---|---|
| `C` | Costo de violar el margen. | Más regularización. | Prioriza el ajuste. |
| `γ` | Alcance de cada observación. | Frontera suave. | Influencia local. |

Fuente de la tabla: [T08, p. 49]. `C` y `γ` se ajustan conjuntamente mediante validación cruzada. [T08, p. 49] En los ejemplos, con `γ` grande la frontera rodea cada grupo de puntos, y con `C` y `γ` grandes a la vez se vuelve muy irregular. [T08, p. 48] [T08, p. 49] **Inferencia:** es el mismo equilibrio entre subajuste y sobreajuste de [Regresión, complejidad y generalización](regresion-y-generalizacion.md). Por eso conviene buscarlos con [grid search y validación cruzada](evaluacion-y-validacion.md).

**Inferencia — matiz sobre la varianza.** La clase de ensambles ubica a SVM entre los modelos de baja varianza y alto sesgo. [T07, p. 69] Eso describe bien un SVM lineal o muy regularizado, pero un kernel RBF con `C` y `γ` grandes produce fronteras muy flexibles. [T08, p. 49]

## SVM multiclase

Con más de dos clases hay dos enfoques: [T08, p. 51]

- **Uno contra uno:** se entrena un SVM por cada par de clases (una como +1 y otra como −1), ignorando los ejemplos del resto. Para una observación nueva, cada SVM vota y gana la clase más votada. [T08, p. 52]
- **Uno contra todos:** se entrena un SVM por clase (esa clase como +1 y el resto como −1). Gana la clase cuyo SVM da el mayor `f(x′)`. [T08, p. 53]

**Conocimiento general:** con `K` clases, uno contra uno entrena `K(K − 1)/2` modelos y uno contra todos entrena `K`.

## Escalado de atributos

SVM usa productos internos y distancias, así que una variable con valores grandes puede dominar la frontera. Por eso se estandarizan los atributos. [T08, p. 54] La fórmula de la diapositiva está mal renderizada; corresponde al z-score `zⱼ = (xⱼ − μⱼ) / σⱼ` de la clase 3. [T03, p. 43] Ver [Datos y preprocesamiento](datos-y-preprocesamiento.md). **Inferencia operativa:** `μⱼ` y `σⱼ` se estiman con el conjunto de entrenamiento y se reutilizan en validación y test. [T02, p. 94] [T02, p. 96]

**Inferencia:** contrasta con los [árboles de decisión](arboles-de-decision.md), que no necesitan normalización. [T07, p. 26]

## One-Class SVM

La presentación lo anuncia en el plan de la clase, pero solo le dedica una diapositiva con figuras y sin texto. [T08, p. 1] [T08, p. 56]

- Una figura muestra una frontera cerrada que encierra los "datos normales" y deja afuera las "nuevas anomalías".
- La otra muestra un hiperplano `w · x + b = 0` que separa los datos del origen, con una brecha (*gap*) y holguras `ξ` para algunos puntos. [T08, p. 56]

**Conocimiento general:** One-Class SVM se entrena solamente con datos de una clase (los normales). Aprende una región que los contiene y marca como anomalía lo que cae afuera. En la formulación de Schölkopf, busca el hiperplano que separa los datos del origen con máximo margen en el espacio del kernel, y un parámetro `ν` acota la fracción de puntos de entrenamiento que pueden quedar afuera.

## Ejemplo de aplicación: MoodRec

La presentación muestra un "Proyecto final: MoodRec", que detecta siete emociones faciales en imágenes y videos: [T08, p. 55]

1. Detectar la cara y la región de interés.
2. Alinear la pose.
3. Pasar a escala de grises y aplicar Sobel.
4. Describir la imagen con un vector HOG.
5. Clasificar con SVM RBF.
6. Integrar en el tiempo con la moda de las predicciones.

Entrenaron con KDEF (4900 imágenes, 7 emociones) y eligieron `C = 10`, `γ = 0,01` con `GridSearchCV`. Probaron con BAUM1 (240 videos), siguiendo a cada persona por centroides. Tomar la moda reduce el efecto de predicciones instantáneas aisladas. [T08, p. 55]

## Conexiones

- [Regresión logística](regresion-logistica.md): otro clasificador lineal, pero estima probabilidades.
- [Regularización](regularizacion.md)
- [Evaluación y validación](evaluacion-y-validacion.md)
- [Ensambles y Random Forest](ensambles-random-forest.md)
