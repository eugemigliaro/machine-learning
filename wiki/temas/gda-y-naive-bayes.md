# GDA y Naive Bayes

Estos son los clasificadores generativos de la clase 6: modelan `P(x | y)` y `P(y)`, y clasifican con Bayes. Ver [probabilidad e inferencia bayesiana](probabilidad-y-bayes.md). [T06, p. 3]

## Gaussiana multivariada por clase

Para atributos continuos, cada clase `k` se modela con una campana de Gauss multivariada, definida por dos parámetros: [T06, p. 22]

- **Media `μₖ`:** dónde está centrado el grupo; es el punto de máxima densidad.
- **Covarianza `Σₖ`:** la forma, el estiramiento y la orientación de la nube de puntos.

```text
f(x) = 1 / ((2π)^(d/2) |Σ|^(1/2)) · exp(−½ (x − μ)ᵀ Σ⁻¹ (x − μ))
```

## LDA: análisis discriminante lineal

**Supuestos:** distribución normal en cada clase y la misma matriz de covarianza para todas. [T06, p. 24]

Derivación de la presentación: [T06, p. 25] [T06, p. 26]

1. Score en logaritmos: `Score(k) = ln P(x | Cₖ) + ln P(Cₖ)`. El logaritmo no cambia el argmax.
2. Se reemplaza la gaussiana y se expande `(x − μₖ)ᵀ Σ⁻¹ (x − μₖ)`. Aparecen un término cuadrático `−½ xᵀ Σ⁻¹ x`, uno lineal y uno constante.
3. Como `Σ` es compartida, el término cuadrático es idéntico en todas las clases y se cancela al compararlas.
4. Queda la función discriminante lineal `δₖ(x) = xᵀ Σ⁻¹ μₖ − ½ μₖᵀ Σ⁻¹ μₖ + ln P(Cₖ) = wₖᵀ x + bₖ`.

La frontera entre dos clases es un hiperplano (en 2D, una recta) con normal `w ∝ Σ⁻¹ (μ₁ − μ₀)`, que coincide con el criterio de Fisher: maximizar la distancia entre centros en relación con cuán apretada está cada clase. [T06, p. 26] [T06, p. 27]

**Reducción de dimensionalidad:** proyectar sobre la dirección de LDA maximiza la separación *entre clases*. PCA, en cambio, maximiza la *varianza total* sin mirar las etiquetas. [T06, p. 27] [T06, p. 28] **Inferencia:** LDA es una forma supervisada de *feature projection*; ver [EDA y selección](eda-y-seleccion.md). [T03, p. 61]

**Ejercicio propuesto por la cátedra:** generar puntos en `[0,1] × [0,1]` con 3 clases, separar 70/30, graficar, mostrar la proyección LDA a una dimensión y clasificar test con LDA. [T06, p. 29]

## QDA y la familia GDA

Si una clase es un círculo chico y otra un óvalo enorme, forzar una única `Σ` produce una mala frontera, con mucho sesgo. QDA le da a cada clase su propia `Σₖ`. Así los términos `xᵀ Σₖ⁻¹ x` ya no se cancelan y la frontera es cuadrática. QDA es más flexible, pero estima muchos más parámetros. La familia completa se llama *Gaussian Discriminant Analysis* (GDA). [T06, p. 30]

| Modelo | Covarianza | Frontera | Parámetros de covarianza (inferencia, `d` atributos, `K` clases) |
|---|---|---|---|
| LDA | Una sola, compartida | Lineal | `d(d+1)/2` |
| QDA | Una por clase | Cuadrática | `K·d(d+1)/2` |
| Gaussian Naive Bayes | Diagonal: sin correlaciones dentro de cada clase | Lineal o cuadrática simple | `K·d` varianzas |

Las tres primeras columnas vienen de [T06, p. 32] y [T06, p. 33]. La última es un conteo propio.

### Chequeo conceptual: ¿LDA o QDA?

Hay 200 pacientes, 500 características y sospecha de dispersiones algo distintas entre clases. [T06, p. 31]

<details>
<summary>Respuesta razonada (inferencia)</summary>

Con 500 atributos, cada `Σₖ` de QDA tiene `500·501/2 = 125 250` parámetros, y cada clase aporta alrededor de 100 ejemplos. La matriz no se puede estimar de forma confiable (queda singular), así que la varianza sería enorme. Conviene LDA, o incluso Gaussian Naive Bayes: se acepta algo de sesgo por compartir o simplificar `Σ` a cambio de un modelo estimable. Es el mismo trade-off sesgo-varianza del [overfitting](regresion-y-generalizacion.md). [T06, p. 30] [T06, p. 32]

</details>

## Naive Bayes

### Independencia condicional

`X` es condicionalmente independiente de `Y` dado `Z` si `P(X | Y, Z) = P(X | Z)`. Equivale a `P(X, Y | Z) = P(X | Z)·P(Y | Z)`. [T06, p. 35]

Naive Bayes ("ingenuo") asume que los atributos son independientes entre sí dado el valor de la clase: [T06, p. 38]

```text
P(a₁, …, aₙ | vⱼ) = Πᵢ P(aᵢ | vⱼ)
v_NB = argmax_vⱼ P(vⱼ) · Πᵢ P(aᵢ | vⱼ)
```

`P(vⱼ)` y `P(aᵢ | vⱼ)` se estiman con las frecuencias de los datos de entrenamiento. [T06, p. 38] [T06, p. 45]

**Chequeo conceptual:** para clasificar propiedades por `tamaño_en_m²` y `número_de_habitaciones`, ¿se cumple la independencia condicional? [T06, p. 36]

<details>
<summary>Respuesta (inferencia)</summary>

No: dentro de una misma clase, las propiedades más grandes tienden a tener más habitaciones. El supuesto se viola, y el modelo cuenta dos veces evidencia redundante. **Conocimiento general:** aun así, Naive Bayes suele clasificar razonablemente bien, aunque sus probabilidades quedan mal calibradas.

</details>

### Ejemplo: ¿Pepe juega al tenis?

Hay 14 sábados descritos por pronóstico, temperatura, humedad y viento, con la clase sí/no. Se pide clasificar `<soleado, frío, alta, fuerte>` comparando `P(sí)·P(soleado | sí)·P(frío | sí)·P(alta | sí)·P(fuerte | sí)` con el producto análogo para `no`. [T06, p. 39] [T06, p. 40] [T06, p. 41]

<details>
<summary>Resolución (calculada a partir de la tabla de la diapositiva 40)</summary>

La tabla tiene 9 días "sí" y 5 días "no".

- `sí`: `9/14 · 2/9 · 3/9 · 3/9 · 3/9 ≈ 0,0053`
- `no`: `5/14 · 3/5 · 1/5 · 4/5 · 3/5 ≈ 0,0206`

Predicción: **no juega**. Al normalizar, `P(no | x) ≈ 0,0206 / (0,0206 + 0,0053) ≈ 0,80`. Con corrección de Laplace (usando `k` = cantidad de valores de cada atributo) la decisión no cambia: `P(no | x) ≈ 0,74`.

</details>

### Probabilidades nulas y corrección de Laplace

Si un valor nunca aparece con una clase en entrenamiento (por ejemplo, humedad "baja"), su frecuencia es 0 y anula toda la productoria. [T06, p. 42] La corrección de Laplace asigna una probabilidad no nula: [T06, p. 43] [T06, p. 44]

```text
p̂ = (nᵢ + 1) / (N + k)
```

Donde `nᵢ` es la cantidad de veces que la variable toma el valor `i`, `N` es el total de observaciones de esa variable y `k` es **la cantidad de valores distintos que puede tomar la variable**. [T06, p. 44] La diapositiva 43 dice "número de clases posibles"; ver [Dudas y conflictos](../dudas-y-conflictos.md). En la figura de la diapositiva 43, cuatro valores con conteos 3, 1, 0 y 4 sobre 8 pasan de `0,375 / 0,125 / 0 / 0,5` a `0,333 / 0,167 / 0,083 / 0,417`. Esta lectura se reconstruyó de etiquetas superpuestas y confirma `k = 4` valores. [T06, p. 43]

### Ejemplo: ¿este correo es spam?

Priors iguales (½), conteos de palabras por clase (8 palabras en cada una) y Laplace con `α = 1` sobre un vocabulario de 3 palabras: `P(palabra | clase) = (conteo + 1) / (8 + 3)`. [T06, p. 46]

- Score de spam para «oferta urgente»: `½ · 5/11 · 4/11 = 10/121 ≈ 0,0826`
- Score de no spam: `½ · 2/11 · 2/11 = 2/121 ≈ 0,0165`
- Al normalizar: `P(spam | correo) = 10 / 12 ≈ 83,3 %`, así que la predicción es spam. [T06, p. 46]

### Problema: ¿inglés o escocés?

Los atributos son binarios (scones, cerveza, whiskey, avena, fútbol) y hay 6 personas inglesas y 7 escocesas. Se pide clasificar `x = (1, 0, 1, 1, 0)`. [T06, p. 48] [T06, p. 49] [T06, p. 50]

<details>
<summary>Resolución (calculada a partir de la tabla de la diapositiva 49)</summary>

Frecuencias de "1" por atributo:

| | Scones | Cerveza | Whiskey | Avena | Fútbol |
|---|---|---|---|---|---|
| Ingleses (6) | 3/6 | 3/6 | 2/6 | 3/6 | 3/6 |
| Escoceses (7) | 7/7 | 4/7 | 3/7 | 5/7 | 3/7 |

- `P(x | inglés) = 3/6 · 3/6 · 2/6 · 3/6 · 3/6 = 1/48 ≈ 0,0208` (con `x` = 0 se usa `1 − p`)
- `P(x | escocés) = 1 · 3/7 · 3/7 · 5/7 · 4/7 ≈ 0,0750`
- Con priors `6/13` y `7/13`: `P(escocés | x) ≈ 0,040 / (0,040 + 0,0096) ≈ 0,81`, así que la predicción es **escocés**.

Con Laplace (`k = 2`) queda `≈ 0,76` y la decisión es la misma. Todos los escoceses comen scones: sin Laplace, cualquier persona con `scones = 0` tendría probabilidad nula de ser escocesa, que es justamente el problema de la diapositiva 42.

</details>

## Conexiones

- [Probabilidad e inferencia bayesiana](probabilidad-y-bayes.md)
- [Regresión logística](regresion-logistica.md): el contraste discriminativo.
- [Métricas de clasificación](metricas-de-clasificacion.md)
