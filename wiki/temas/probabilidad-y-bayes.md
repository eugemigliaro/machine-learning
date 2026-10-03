# Probabilidad e inferencia bayesiana

## Modelos discriminativos y generativos

| Enfoque | Qué aprende | Qué modela | Ejemplos |
|---|---|---|---|
| Discriminativo | La frontera de decisión. | `P(y \| x)` directamente. | Regresión logística. |
| Generativo | Cómo se distribuye cada clase por separado; con eso podría generar datos nuevos. | La verosimilitud `P(x \| y)` y el prior `P(y)`. | GDA, Naive Bayes. |

Fuente de la tabla: [T06, p. 3].

## Repaso de probabilidad

- **Espacio muestral y eventos:** el espacio muestral es el conjunto de todos los resultados posibles; un evento es cualquier subconjunto de él. [T06, p. 5]
- **Frecuencia relativa:** `f_A = n_A / n` en `n` repeticiones independientes. Por ejemplo, 106 caras en 200 tiros dan 0,53, frente a una probabilidad de 0,5. [T06, p. 5] [T06, p. 6]
- **Probabilidad conjunta:** por ejemplo, `P(cara ∩ cara) = 0,25`. Es conmutativa: `P(A ∩ B) = P(B ∩ A)`. [T06, p. 7]
- **Independencia:** `P(A ∩ B) = P(A)·P(B)`. Si `A` y `B` son independientes, también lo son `A` y `Bᶜ`. Si son mutuamente excluyentes, no son independientes. [T06, p. 8] **Precisión (conocimiento general):** esto último vale cuando `P(A) > 0` y `P(B) > 0`.
- **Condicional:** `P(A | B) = P(A ∩ B) / P(B)`. Ejemplo: `P(3♦ | roja) = (1/52) / (1/2) = 1/26`. [T06, p. 11]
- **Probabilidad total:** si los `Bᵢ` particionan el espacio, `P(A) = Σ P(Bᵢ)·P(A | Bᵢ)`. [T06, p. 12]
- **Bayes:** `P(A | B) = P(A)·P(B | A) / P(B)`. [T06, p. 13]

## Bayes aplicado al aprendizaje

```text
p(H | D) = p(H) · p(D | H) / p(D)
posterior = prior · verosimilitud / evidencia
```

Nombres de cada término: [T06, p. 16]. El objetivo es encontrar la hipótesis más probable de un conjunto `H` dados los datos de entrenamiento `D`. [T06, p. 17]

- **MAP (máximo a posteriori):** `h_MAP = argmax_h P(D | h)·P(h)`. `P(D)` se descarta porque es constante entre hipótesis. [T06, p. 18]
- **ML (máxima verosimilitud):** si todas las hipótesis son equiprobables, `P(h)` también es constante y queda `h_ML = argmax_h P(D | h)`. En ese caso `h_MAP = h_ML`. [T06, p. 19]

### Chequeo conceptual: el poder del prior

Un detector de metales suena y `P(sonido | lata) ≈ P(sonido | tesoro) ≈ 1`. ¿Por qué es mucho más probable haber encontrado una lata? [T06, p. 20]

<details>
<summary>Respuesta (inferencia)</summary>

Como las verosimilitudes son casi iguales, el posterior queda dominado por el prior: en la playa hay muchísimas más latas que tesoros. Un criterio ML, que ignora el prior, no puede distinguir entre ambas hipótesis; MAP sí.

</details>

## De Bayes a un clasificador

En clasificación, las hipótesis son las clases. Se elige la clase `v` que maximiza `P(a₁, …, aₙ | v)·P(v)`, porque el denominador es constante. [T06, p. 37] Queda estimar `P(D | h)`: [T06, p. 21]

- Con atributos continuos se modela `P(x | y)` como una gaussiana por clase, lo que da la familia GDA. [T06, p. 22]
- Con atributos categóricos se estiman las probabilidades con frecuencias y se asume independencia condicional, lo que da Naive Bayes. [T06, p. 38]

Ambos casos se desarrollan en [GDA y Naive Bayes](gda-y-naive-bayes.md).

## Conexiones

- [Regresión logística](regresion-logistica.md): el modelo discriminativo de referencia.
- [GDA y Naive Bayes](gda-y-naive-bayes.md)
