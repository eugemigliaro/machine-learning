# Regresión, complejidad y generalización

## Regresión

La regresión supervisada predice una variable numérica continua y aprende una función que relaciona entradas con el objetivo. [T02, p. 46] [T02, p. 48]

En una variable, la regresión lineal usa `ŷ = β0 + β1x`; durante el entrenamiento ajusta intercepto y pendiente para minimizar el error, generalmente MSE en la presentación. En varias variables, la misma idea se extiende a una combinación lineal de características. [T02, p. 49] [T02, p. 50] [T02, p. 51]

La regresión polinómica agrega transformaciones de mayor grado para representar relaciones no lineales. Aumentar el grado incrementa la capacidad y también la complejidad. [T02, p. 52]

## Underfitting y overfitting

- **Underfitting / alto sesgo:** el modelo es demasiado simple para capturar la relación relevante.
- **Buen ajuste:** la complejidad alcanza para modelar la señal sin perseguir peculiaridades del conjunto.
- **Overfitting / alta varianza:** el modelo se ajusta excesivamente a train y generaliza peor. [T02, p. 53]

El error de train, por sí solo, no estima la generalización. Si el modelo aprende ruido particular de train, aparece una brecha respecto del error en datos independientes. [T02, p. 76] [T02, p. 77]

## Controles de complejidad

El material propone aumentar datos cuando sea posible, reducir características, regularizar y evaluar con particiones independientes. [T02, p. 57] [T02, p. 64] La selección de características reduce grados de libertad; la regularización penaliza coeficientes; dev permite elegir estas decisiones sin contaminar test. [T03, p. 9] [T03, p. 61] [T03, p. 85]

## Conexiones

- [Evaluación y validación](evaluacion-y-validacion.md)
- [Regularización](regularizacion.md)
- [Trabajo práctico 1](tp1-regresion.md)
