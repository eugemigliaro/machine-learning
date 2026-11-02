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

Para leer el gap y decidir qué hacer, ver [Diagnóstico de modelos](diagnostico-de-ml.md), que agrega las curvas de aprendizaje. [T11, p. 11] [T11, p. 21]

## Validación cruzada avanzada

### Qué evalúa la validación

La validación mide la capacidad de generalización: cómo se va a comportar el modelo con datos nuevos. [T11, p. 67] Con cross-validation se evalúan y eligen **modelos** (features + algoritmo), no fronteras de decisión. La pregunta es, por ejemplo, si un RF con ciertas features generaliza lo suficiente. Una vez respondida, se entrena el algoritmo elegido con esas features sobre **todos** los datos salvo test, y ese es el modelo final para el deploy. [T11, p. 68]

### La regla del split

Train, validación y test deben "mostrar los mismos datos", para que lo aprendido en train se pueda aplicar en validación y test. [T11, p. 69] Dicho de otro modo:

> La relación train–validación debe ser la misma que habrá entre train y test. [T11, p. 71]

El uso que se le va a dar al modelo define el split que hay que usar. [T11, p. 72] Hasta ahora el enfoque fue el más simple: separar al azar y rotar los bloques para que todos los datos pasen una vez por validación. [T11, p. 69] [T11, p. 73]

### k-fold estratificada

Con un split aleatorio, la proporción de clases puede variar según la semilla, sobre todo en datasets chicos o desbalanceados: un fold con 5 % de positivos y otro con 20 %. La **stratified k-fold** mantiene la proporción de clases en train, validación y test. Se recomienda siempre, y especialmente en datasets pequeños, medianos o desbalanceados (medicina, fraude, diagnóstico). [T11, p. 70] [T11, p. 74]

### Grupos o cohortes

A veces las muestras no son independientes: hay grupos que comparten estructura, como hospitales, escuelas, países o dispositivos. [T11, p. 75] Comparten sesgos, correlaciones y cambios de distribución. Si no se tienen en cuenta, aparece un **leakage indirecto**: el modelo aprende el hospital, el escáner o el país en lugar del problema real. [T11, p. 76] Es un problema si la relación train–validación no se mantiene en test o deployment, porque el sistema usa información que no tendrá en su aplicación final. [T11, p. 77]

- **Group K-Fold:** los grupos se reparten entre folds, sin que un grupo quede partido entre train y validación.
- **Leave-One-Group-Out (LOGO):** en cada iteración, la validación son los datos de un grupo. [T11, p. 78]

Ejemplo: si hay datos de 5 escuelas y el sistema se va a usar en otras, hay que validar con Group K-Fold. Si no, el modelo puede funcionar en esas 5 y no en otras, y la validación no lo detecta. [T11, p. 79]

### Cohortes temporales

Si el tiempo importa, hay que comprobar que el sistema generaliza a datos "del futuro": la validación siempre contiene datos **posteriores** a los de train. Los esquemas son *time-series cross-validation* y *walk-forward validation*: el fold `k` entrena con los bloques anteriores y valida con el siguiente. [T11, p. 80] [T11, p. 81]

### Cómo elegir el split

Con varios niveles de cohortes, la pregunta guía es **a qué se quiere que generalice el sistema cuando se use**. A veces elegir el split correcto tiene más impacto que elegir un modelo u otro. No existe un split universalmente correcto: depende del uso del sistema en deployment. [T11, p. 82] [T11, p. 83]

**Conocimiento general:** en scikit-learn, `StratifiedKFold`, `GroupKFold`, `StratifiedGroupKFold`, `LeaveOneGroupOut` y `TimeSeriesSplit` implementan estos esquemas; los de grupo reciben el vector `groups` en `split` o en `cross_validate`.

## Métricas de clasificación

Accuracy, matriz de confusión, precisión, recall, especificidad, curva ROC y AUC se desarrollan en [Métricas de clasificación](metricas-de-clasificacion.md). [T04, p. 24] El umbral de decisión también es un hiperparámetro que se elige sin mirar test. [T04, p. 52] [T02, p. 89]
