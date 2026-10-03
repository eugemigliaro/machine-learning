# Regresión logística

## Problema: clasificación binaria

La regresión logística se presenta para resolver clasificación binaria a partir de datos anteriores: spam / no spam, tumor benigno / maligno o unidad defectuosa / correcta. Por convención, `0` es la clase negativa y `1` la positiva. [T04, p. 9] [T04, p. 10] Las características dependen del problema: frecuencia de palabras para correos, radio o textura para tumores, lecturas de sensores para semiconductores. [T04, p. 11]

## Por qué no alcanza la regresión lineal

La regresión lineal predice valores continuos y puede salirse del rango `[0, 1]`, por lo que su salida no se puede interpretar como probabilidad. La idea es "aplastar" la salida para que quede entre 0 y 1. [T04, p. 17]

Las figuras del ejemplo del tumor muestran otro problema: agregar un tumor muy grande, bien etiquetado como maligno, inclina la recta y mueve el punto donde cruza 0,5; con eso, un caso maligno pasa a clasificarse mal. [T04, p. 14] [T04, p. 15] [T04, p. 16] **Lectura de la figura:** un ejemplo "fácil" lejos de la frontera no debería mover la regla de decisión, pero en regresión lineal sí la mueve.

## Función sigmoidea

```text
P(Y = 1 | x) = 1 / (1 + e^-(w·x + b))
```

La sigmoidea tiene asíntotas en 0 y 1, convierte cualquier número real en una probabilidad y se usa para clasificación, no para regresión. Los parámetros `w` y `b` se ajustan con el conjunto de entrenamiento. [T04, p. 19] [T04, p. 20]

**Conocimiento general, fuera de T04:** la presentación no muestra la función de costo con que se entrenan `w` y `b`. Lo habitual es maximizar la verosimilitud, que es lo mismo que minimizar el log-loss o entropía cruzada. La cátedra presenta esa pérdida en la clase de árboles; ver [árboles de decisión](arboles-de-decision.md#log-loss). [T07, p. 73]

## Odds y logit

El modelo logístico es una regresión lineal sobre una escala logarítmica. [T04, p. 55]

| Magnitud | Definición | Rango |
|---|---|---|
| Probabilidad | `p` | `(0, 1)` |
| Odds | `p / (1 - p)`; por ejemplo, `p = 0,8` da odds `= 4` ("4 veces más probable que compre a que no compre") | `(0, +∞)` |
| Logit | `ln(p / (1 - p)) = β0 + β1·x` | `(-∞, +∞)` |

El modelo es lineal en `logit(p)`, no en `p`. [T04, p. 55] Si se despeja `p` a partir del logit, se obtiene la sigmoidea: `p = 1 / (1 + e^-(β0 + β1·x))`. [T04, p. 56] La notación `w, b` de la diapositiva 20 y la notación `β0, β1` de las diapositivas 55-56 describen el mismo modelo. [T04, p. 20] [T04, p. 55]

**Conocimiento general:** `β1` es el cambio en log-odds por unidad de `x`, así que `e^β1` es el factor por el que se multiplican las odds.

## De probabilidad a clase

La salida es una probabilidad. Por ejemplo, `0,7` para un tumor de 4 cm se interpreta como 70 % de probabilidad de malignidad. Para convertirla en una predicción `0/1` se aplica un **umbral**. [T04, p. 21] [T04, p. 22] Cómo se elige ese umbral se desarrolla en [métricas de clasificación](metricas-de-clasificacion.md).

## Conexiones

- [Regresión, complejidad y generalización](regresion-y-generalizacion.md)
- [Métricas de clasificación](metricas-de-clasificacion.md)
- [Probabilidad e inferencia bayesiana](probabilidad-y-bayes.md): la regresión logística es el ejemplo de modelo discriminativo. [T06, p. 3]
