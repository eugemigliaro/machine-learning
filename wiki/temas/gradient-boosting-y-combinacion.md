# Gradient boosting y combinación de modelos

## Gradient boosting

En gradient boosting los árboles no se entrenan de forma independiente, como en Random Forest, sino **en secuencia**: cada uno corrige los errores del anterior aprendiendo sobre los residuos. Por eso reduce el error progresivamente. [T12, p. 4]

1. Se entrena un primer árbol, que da una predicción inicial.
2. Se entrena un segundo árbol sobre los errores del primero.
3. Se entrena un tercero sobre los errores del ensamble 1–2.
4. Se repite: el ensamble se vuelve cada vez más preciso. [T12, p. 5]

### Qué mejora respecto de Random Forest

- Los árboles interactúan en lugar de ser independientes, y el modelo se enfoca explícitamente en los ejemplos difíciles.
- Logra mejor precisión con menos árboles, así que es más rápido y eficiente.
- Es especialmente potente en datasets tabulares, como RF, porque maneja bien variables heterogéneas: cada árbol mira cada variable por separado.
- **Reduce más el sesgo.** En RF, agregar árboles reduce la varianza pero no tanto el sesgo; gradient boosting, al enfocarse en los errores sucesivos, ataca el sesgo. [T12, p. 6]

**Conocimiento general:** como cada árbol nuevo corrige errores, agregar árboles sin límite puede sobreajustar, a diferencia de RF. Por eso se controlan juntos la tasa de aprendizaje (*learning rate*), la cantidad de árboles y su profundidad, a menudo con *early stopping* sobre validación.

### XGBoost, LightGBM y CatBoost

| Implementación | Qué aporta |
|---|---|
| **XGBoost** | Regularización explícita: penaliza árboles demasiado complejos (muchas hojas) y minimiza el error junto con la complejidad. Cada árbol nuevo minimiza una función de pérdida diferenciable. Optimiza el cómputo (paralelización, memoria) y trata automáticamente los valores faltantes. Es un estándar de la industria en datos tabulares: alta precisión con relativamente poco ajuste y datasets medianos. [T12, p. 7] |
| **LightGBM** | De Microsoft, pensado para datasets extremadamente grandes. Agrupa los valores en histogramas en lugar de evaluar todos los cortes posibles. Crece **leaf-wise**: expande primero las hojas que más reducen el error, en lugar de crecer por niveles. Suele mejorar precisión y velocidad, pero puede sobreajustar si no se regulariza: cuidado en datasets pequeños. [T12, p. 8] |
| **CatBoost** | De Yandex, pensado para variables categóricas. Usa *ordered boosting* y codificaciones estadísticas controladas para no usar información futura durante el entrenamiento. Permite trabajar directamente con muchas categóricas, con menos preprocesamiento manual. Suele funcionar muy bien en datos empresariales y tabulares reales. [T12, p. 9] |

La pérdida diferenciable conecta con la clase de árboles, que propone la log-loss para métodos avanzados porque es derivable y permite calcular gradientes. [T07, p. 73] [T12, p. 7]

### En scikit-learn

scikit-learn incluye boosting clásico: `GradientBoostingClassifier`, `GradientBoostingRegressor` y `HistGradientBoosting`. Este último se inspira en ideas tipo LightGBM: bins por histograma, entrenamiento más rápido y mejor escalabilidad. XGBoost, LightGBM y CatBoost no vienen incluidos: se instalan aparte. [T12, p. 10]

**Conocimiento general:** los nombres exactos son `HistGradientBoostingClassifier` y `HistGradientBoostingRegressor`; aceptan valores faltantes de forma nativa y, en versiones recientes, también variables categóricas.

## Combinar modelos

Distintos algoritmos capturan distintos patrones: un modelo puede acertar donde otro se equivoca. Combinarlos suele mejorar robustez y precisión; es la base de los ensambles modernos. [T12, p. 19]

| Técnica | Objetivo | Cómo |
|---|---|---|
| **Bagging** | Reducir **varianza**. | Entrenar el modelo varias veces sobre subconjuntos bootstrap y combinar las predicciones (voto, promedio). Es lo que lleva de un árbol a RF. [T12, p. 20] |
| **Boosting** | Reducir **sesgo**. | Entrenar en secuencia, por ejemplo sobre los mal clasificados de la iteración anterior, y combinar con un promedio ponderado. [T12, p. 21] |
| **Stacking** | Aprovechar las fortalezas de cada modelo. | Los modelos base predicen; un meta-modelo se entrena con esas predicciones como features. Conviene usar predicciones probabilísticas (`y = 0,31` en lugar de `y = 0`). [T12, p. 22] |

Bagging y Random Forest se desarrollan en [Ensambles y Random Forest](ensambles-random-forest.md).

### Arquitectura de stacking

- **Nivel 1:** modelos base variados, por ejemplo LDA, XGBoost, SVM o redes neuronales.
- **Nivel 2 (meta-modelo):** un modelo simple, como regresión logística, Ridge o un gradient boosting suave. Su entrada son las predicciones de los modelos base. [T12, p. 23]

### Stacking sin leakage

Si el meta-modelo se entrena con las predicciones de los modelos base **sobre su propio training**, aparece un overfitting severo: esas predicciones ya están sesgadas. El meta-modelo se entrena con predicciones sobre datos de validación: [T12, p. 24]

1. Entrenar los modelos base en train y predecir en validación.
2. Entrenar el meta-modelo con esas predicciones.

En la práctica se usan las predicciones **out-of-fold (OOF)** de la cross-validation: cada ejemplo de train recibe la predicción del modelo entrenado sin él. Esas predicciones insesgadas son el set con que se entrena el meta-modelo. Test sigue reservado para la evaluación final. Como no queda otra validación, el meta-modelo se ajusta poco o nada, o se usa nested CV. [T12, p. 25]

**Conocimiento general:** `StackingClassifier` de scikit-learn hace exactamente esto: entrena el meta-modelo con predicciones obtenidas por `cross_val_predict` y luego reentrena los modelos base con todo el train.

### Elegir los modelos base

Dentro de la cross-validation de train: [T12, p. 26]

1. Buscar los mejores hiperparámetros de cada modelo, como hasta ahora.
2. Medir qué tan parecidos son sus errores, por ejemplo con la correlación entre sus salidas. Dos modelos muy correlacionados aportan poco juntos; dos modelos con buen rendimiento y poco correlacionados son muy prometedores para stacking o blending.

### Blending

Una simplificación del stacking: lo mismo, pero **sin cross-validation**, con una sola partición de datos. Se usa para una implementación rápida; si no, conviene stacking. [T12, p. 27]

La clase 7 había usado "blending" para promediar las probabilidades de RF y KNN; ver [Dudas y conflictos](../dudas-y-conflictos.md). [T07, p. 72]

### Ejemplo: Netflix Prize

Una competencia de tres años con un premio de un millón de dólares. El ganador, BellKor's Pragmatic Chaos, superó en un 10 % al método anterior con un modelo de blending/stacking sobre varios modelos (kNN, factorización de matrices…). [T12, p. 28]

## Conexiones

- [Ensambles y Random Forest](ensambles-random-forest.md): bootstrap, bagging, RF y Extra Trees.
- [Árboles de decisión](arboles-de-decision.md): el modelo base del boosting.
- [Diagnóstico de modelos](diagnostico-de-ml.md): sesgo frente a varianza.
- [Evaluación y validación](evaluacion-y-validacion.md): predicciones fuera de fold y nested CV.
- [TP3: optimización de modelos](tp3-optimizacion.md): ensemble learning es una de las estrategias de mejora.
