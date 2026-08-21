# Regularización

La regularización controla la complejidad penalizando modelos demasiado complejos durante el entrenamiento. En modelos lineales, la cátedra vincula esa complejidad con el tamaño de los coeficientes. [T03, p. 82] [T03, p. 85]

## L1, L2 y Elastic Net

- **L1 / Lasso:** `J(w) = Error(w) + λ Σ|wⱼ|`. Favorece que algunos coeficientes sean exactamente cero, por lo que también actúa como selección de variables. [T03, p. 90]
- **L2 / Ridge:** `J(w) = Error(w) + λ Σwⱼ²`. Penaliza con más fuerza coeficientes grandes y suele reducirlos sin llevarlos exactamente a cero. [T03, p. 91]
- **Elastic Net:** combina L1 y L2; `λ` controla la fuerza total y `α` el balance entre ambas penalizaciones. [T03, p. 92]

`λ` es un hiperparámetro: valores mayores fuerzan coeficientes menores. Debe elegirse mediante validación, no por el resultado de test. [T03, p. 3] [T03, p. 90] [T02, p. 89]

## Lectura práctica

- L1 sirve cuando interesa un modelo disperso y selección automática.
- L2 conserva la participación de todas las variables y reduce coeficientes extremos.
- Elastic Net busca combinar sparsity y estabilidad. [T03, p. 90] [T03, p. 91] [T03, p. 92]

El preprocesamiento forma parte del pipeline que se valida junto con `λ` y el tipo de penalización. [T03, p. 3] [T03, p. 9]
