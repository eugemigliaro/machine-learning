# Guion de defensa — TP1 Insurance Charges

La exposición principal usa las primeras nueve diapositivas y dura aproximadamente diez minutos. Las dos últimas quedan como respaldo para preguntas.

## 1. Portada — 20 segundos

“En este trabajo buscamos predecir los gastos médicos anuales del dataset Insurance Charges. El foco no fue solamente ajustar una regresión, sino construir una evaluación que nos permitiera elegir un modelo y estimar cómo funcionaría con personas nuevas.”

## 2. Problema y datos — 55 segundos

“El dataset original tenía 1.338 observaciones, seis predictores y `charges` como objetivo. Encontramos dos filas exactamente iguales y conservamos una sola para evitar que una copia pudiera quedar en entrenamiento y otra en validación. Después reservamos 10 % para test: 134 casos. Los otros 1.203 quedaron para desarrollo. Estratificamos por `smoker`, porque es la característica que más separa los costos, y fijamos semilla 42 para reproducibilidad.”

## 3. Train, validación y test — 1 minuto 10 segundos

“Train sirve para aprender coeficientes. Validación sirve para que nosotros elijamos grado y regularización. Test tiene un tercer rol: estimar una única vez el resultado del pipeline ya elegido. Como el dataset es pequeño, usamos diez folds sobre desarrollo. Cada observación se valida exactamente una vez y se usa para entrenar las otras nueve. Todo preprocesamiento que aprende parámetros se ajustó dentro del fold, para evitar leakage.” [T02, pp. 85, 89, 94–96] [T03, pp. 12, 15]

## 4. EDA — 1 minuto 10 segundos

“No había faltantes ni categorías inválidas. La observación más importante fue `smoker`: los no fumadores tenían un costo medio cercano a 8.536, mientras que los fumadores superaban 31.987. El IQR global marcaba muchos `charges` como atípicos, pero estaba mezclando dos poblaciones con escalas distintas. Al recalcularlo por fumadores y no fumadores, vimos que esos costos altos eran principalmente estructurales y plausibles. Por eso no los eliminamos. También conservamos las seis características.” [T02, pp. 39–42]

## 5. Pipeline y métrica — 1 minuto

“Las variables numéricas se estandarizaron y las categóricas se codificaron con one-hot, eliminando una referencia. Después generamos términos polinómicos. Para L1 estandarizamos nuevamente los términos generados, porque la penalización depende de su escala. Evaluamos con RMSE: raíz del promedio de errores cuadrados. Está en las unidades de `charges` y penaliza especialmente errores grandes.” [T03, p. 87]

## 6. Grados polinómicos — 1 minuto 15 segundos

“La regresión lineal obtuvo RMSE de validación 6.158. Grado 2 bajó a 4.909, una mejora aproximada del 20 %. Grado 3 siguió mejorando train, pero validación empeoró a 5.040 y la brecha creció de 114 a 430. Esa combinación —train baja, validación sube— es una señal de sobreajuste. Por eso elegimos grado 2 antes de probar regularización.” [T02, pp. 52–53, 76–77]

## 7. L1 — 1 minuto 15 segundos

“L1 agrega al error una penalización proporcional a la suma del valor absoluto de los coeficientes. Comparamos lambda 1, 10, 100 y 1000 en los mismos folds. Lambda 100 obtuvo el menor RMSE, 4.872, y redujo los coeficientes activos a 23,4 en promedio. La mejora frente a no regularizar fue sólo 0,74 %, por eso la describimos como modesta. Lambda 1000 dejó apenas cuatro coeficientes y empeoró el error: regularizó demasiado.” [T03, p. 90]

## 8. Modelo seleccionado — 1 minuto 10 segundos

“Congelamos grado 2, L1 y lambda 100. Lo reentrenamos con los 1.203 casos de desarrollo; quedaron 22 coeficientes activos. Recién entonces abrimos test. El RMSE final fue 3.957,83. Es menor que el promedio de validación, pero no usamos esa diferencia para cambiar nada. Test fue una muestra más favorable y sólo contiene 134 casos, así que el número tiene variabilidad.” [T02, pp. 88–89]

## 9. Conclusiones — 45 segundos

“El modelo con menor validación y el que elegiríamos para una aplicación es el polinómico de grado 2 con L1 y lambda 100. Si tuviéramos que comunicar un RMSE esperado, informaríamos 3.957,83, aclarando que es una estimación de un test independiente pequeño. La idea metodológica central es que elegimos con validación y usamos test sólo para estimar generalización.”

## Preguntas probables

### ¿Por qué reservar sólo 10 % para test?

Porque quedan más observaciones disponibles para los ajustes dentro de cross-validation. La contrapartida explícita es que el RMSE sobre 134 casos tiene mayor variabilidad que con un test más grande.

### ¿Por qué estratificar por `smoker` y no por otra variable?

Porque `smoker` define los grupos con mayor diferencia de escala en `charges`: medias aproximadas de 8.536 y 31.987. Mantener su proporción estabiliza los folds. No estratificamos directamente por `charges`, y `smoker` estaba disponible como predictor.

### ¿Por qué eliminar el duplicado antes del split?

Porque dos copias idénticas podrían quedar en particiones distintas. El modelo vería en train exactamente un caso evaluado después en validación o test, generando una estimación optimista.

### ¿Por qué no eliminar los outliers?

Porque IQR es una señal, no una prueba de error. Los BMI extremos eran posibles y los `charges` altos estaban asociados a fumadores. Eliminarlos habría cambiado la población que pretendemos modelar.

### ¿Qué minimizó cada modelo?

`LinearRegression` minimizó la suma de residuos cuadrados. `Lasso` minimizó $\frac{1}{2n}\lVert y-Xw\rVert_2^2 + \lambda\lVert w\rVert_1$. La implementación usa descenso por coordenadas.

### ¿Una regresión polinómica deja de ser lineal?

No en sus parámetros. Las entradas incluyen potencias e interacciones, pero la predicción sigue siendo una combinación lineal de coeficientes aprendidos.

### ¿Por qué estandarizar dentro de cada fold?

El escalador aprende medias y desvíos. Si se ajustara antes de separar los folds, incorporaría información de validación en el entrenamiento. Además, L1 necesita escalas comparables para que la penalización sea justa entre términos.

### ¿Por qué grado 2 y no grado 3 si grado 3 tiene menor error de train?

Porque el objetivo es generalizar. Grado 3 redujo train de 4.795 a 4.610, pero validación empeoró de 4.909 a 5.040 y la brecha aumentó. Eso indica que la flexibilidad adicional ajusta peculiaridades de train.

### ¿Por qué elegir L1 si la mejora fue tan pequeña?

Porque fue la regla de selección fijada: menor RMSE medio de validación. Además produjo un modelo más disperso. De todos modos, la mejora de 0,74 % no se presenta como concluyente; grado 2 sin L1 rindió de manera muy similar.

### ¿Por qué test dio mejor que validación?

Las métricas cambian según qué casos caen en cada muestra. Test tuvo sólo 134 observaciones y resultó más favorable. La diferencia no demuestra una mejora posterior ni autoriza a retocar el modelo; por eso también comunicamos el resultado de CV y su dispersión.

