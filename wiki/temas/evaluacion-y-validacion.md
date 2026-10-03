# Evaluación y validación

## Roles de las particiones

| Partición | Uso correcto |
|---|---|
| Train | Aprender los parámetros del modelo. |
| Dev / validación | Elegir modelos, hiperparámetros, características y demás decisiones del pipeline. |
| Test | Estimar una vez el rendimiento del pipeline final en datos no vistos. |

Estos roles son distintos porque elegir el mejor modelo sobre una partición adapta las decisiones también a su ruido: por eso el resultado del ganador en esa misma partición queda optimistamente sesgado. [T02, p. 70] [T02, p. 81] [T02, p. 82] [T03, p. 4] [T03, p. 8] [T03, p. 9]

El test debe ser independiente y representar la población donde se usará el modelo. No se utiliza para tomar decisiones; se reserva para reportar la estimación final. [T02, p. 69] [T02, p. 89]

## Validación cruzada

En k-fold cross-validation se divide el conjunto de desarrollo en `k` bloques: cada bloque actúa una vez como validación y los restantes como entrenamiento. Así cada observación participa en validación una vez y se aprovechan mejor datasets pequeños, a cambio de mayor costo computacional. [T03, p. 12] [T03, p. 15] El material menciona `k = 5` o `10` como elecciones usuales y leave-one-out para conjuntos extremadamente pequeños. [T02, p. 85] [T02, p. 87]

Tras elegir el pipeline, la presentación propone reentrenarlo con train+dev y evaluarlo en test. [T02, p. 88]

## Leakage y orden del flujo

La separación debe ocurrir antes de aprender transformaciones desde los datos. Si outliers, imputación, encoding, escalado o selección se deciden usando todo el dataset, test deja de ser independiente. [T02, p. 94] [T02, p. 96]

Flujo recomendado por el material:

1. Reservar test y separar dev o definir los folds.
2. Ajustar preprocesamiento y modelo solamente con el train de cada partición.
3. Elegir el pipeline por su rendimiento agregado en dev.
4. Reentrenar la configuración elegida sin consultar test.
5. Evaluar una vez en test. [T02, p. 85] [T02, p. 89] [T02, p. 94] [T02, p. 96]

## Métricas de regresión

Para residuos `eᵢ = yᵢ - ŷᵢ`, el material define:

- `RMSE = sqrt((1/n) · Σ(yᵢ - ŷᵢ)²)`. **Inferencia a partir de la fórmula:** conserva las unidades del objetivo y da mayor peso relativo a errores grandes por elevarlos al cuadrado. [T03, p. 87]
- `R²`: proporción de variabilidad del objetivo explicada por el modelo; valores cercanos a 1 indican mejor ajuste y cercanos a 0, poca información explicada, en la interpretación introductoria de la cátedra. [T03, p. 88]

Si se prueban muchas configuraciones, también puede haber overfitting a dev. El material recomienda cross-validation, limitar búsquedas ad hoc, mantener test intacto y, para selección intensiva o pocos datos, nested cross-validation. [T03, p. 100]

## Diagnóstico y búsqueda de hiperparámetros

La clase de árboles repasa el mismo esquema con clasificación: calcular la métrica en train y validación, usar k-fold para una estimación más estable, leer el gap de generalización (gap grande: sobreajuste; gap chico con desempeño bajo: subajuste) y trazar curvas de validación en función de un hiperparámetro de complejidad. [T07, p. 50] [T07, p. 51] Para varios hiperparámetros propone grid search: primero rangos amplios por separado y después un rango acotado con margen, porque los hiperparámetros interactúan. [T07, p. 52] [T07, p. 53]

## Métricas de clasificación

Accuracy, matriz de confusión, precisión, recall, especificidad, curva ROC y AUC se desarrollan en [Métricas de clasificación](metricas-de-clasificacion.md). [T04, p. 24] El umbral de decisión también es un hiperparámetro que se elige sin mirar test. [T04, p. 52] [T02, p. 89]
