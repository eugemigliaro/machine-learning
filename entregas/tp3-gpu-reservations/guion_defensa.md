# Guion de defensa — TP3 Reservas de GPU

La presentación tiene 13 diapositivas y dura unos 9:45. La consigna da 10 minutos de exposición y 10 de preguntas, y pide enviar la presentación, el predictor y el código 24 horas antes de la clase. [P03, p. 1]

- **Diapositivas:** [artifact de Slides](https://claude.ai/artifact/RTKkJodPsGvyJakUPFCy26). Su fuente está versionada en `presentacion/project/`.
- **Números:** salen del notebook `tp3_gpu_reservations.ipynb` y de `decisiones.md`.
- **Reparto:** propuesto para tres oradores (A, B y C), como en el TP2.

| Diapositiva | Orador | Tiempo |
|---|:---:|---:|
| 1. ¿Se va a cancelar esta reserva de GPU? | A | 0:20 |
| 2. Dos hallazgos de los datos definieron el diseño | A | 0:50 |
| 3. Dos validaciones | A | 0:50 |
| 4. Baseline | A | 0:45 |
| 5. Dónde se equivoca el modelo | B | 0:50 |
| 6. Por qué se equivoca | B | 0:50 |
| 7. Curvas de aprendizaje | B | 0:45 |
| 8. Enfoque data-centered | B | 0:55 |
| 9. Optimización | C | 0:55 |
| 10. Dónde mejoró | C | 0:45 |
| 11. Evaluación en test | C | 0:45 |
| 12. Rendimiento esperado y predictor | C | 0:45 |
| 13. Conclusiones | A | 0:30 |
| **Total** | | **9:45** |

## Reparto entre oradores

| Orador | Bloque | Diapositivas | Tiempo |
|:---:|---|---|---:|
| **A** | El problema, los datos y cómo evaluamos; cierre | 1 a 4 y 13 | 3:15 |
| **B** | Diagnóstico: errores, curvas y datos que faltan | 5 a 8 | 3:20 |
| **C** | Optimización, modelo final y predictor | 9 a 12 | 3:10 |

- **A** arma el contexto: el leakage, los lotes y por qué hay dos validaciones. Vuelve al final para cerrar con las conclusiones, que retoman el mensaje de la portada.
- **B** cuenta el diagnóstico de punta a punta: dónde se equivoca el modelo, por qué, que no faltan filas sino información, y qué datos habría que registrar.
- **C** muestra que la optimización confirma el diagnóstico: mejoras chicas, concentradas en las cohortes difíciles, confirmadas en test.

## Qué decir en cada diapositiva

### 1. ¿Se va a cancelar esta reserva de GPU? (A, 0:20)

> Tenemos 47.842 reservas de GPU y queremos saber cuáles se van a cancelar: se cancela el 41,7 %. El modelo final acierta el 88,9 % en test y ordena muy bien por riesgo, con AUC 0,96. Pero la conclusión principal es otra: lo que limita al sistema es la información de las variables, y vamos a mostrar cómo llegamos a eso.

### 2. Dos hallazgos de los datos definieron el diseño (A, 0:50)

> Antes de modelar encontramos dos cosas. Primero, columnas con leakage: `execution_status` es el objetivo con otro nombre, y la GPU asignada y la espera en cola se conocen recién al asignar los recursos. Las sacamos; medimos una sola vez que dejarlas inflaba la AUC en 0,0014.
>
> Segundo, el 41 % de las filas son copias exactas de otras: reservas en lote, y los grupos de más de 50 copias se cancelan en un 95 %. No son errores de carga, así que las dejamos, pero cambian cómo hay que validar.

### 3. Dos validaciones (A, 0:50)

> Con tantas copias, una validación aleatoria premia memorizar: si una copia está en entrenamiento, la otra se acierta gratis. Por eso usamos dos validaciones con los mismos folds. La aleatoria imita lo que suponemos de la competencia, que son filas del mismo conjunto de reservas. La agrupada mantiene cada lote junto y estima cómo le va al modelo con reservas nuevas.
>
> AUC es la métrica principal porque mide el orden por riesgo sin depender del umbral; accuracy, para comparar decisiones 0/1 durante el desarrollo. La competencia mide balanced accuracy, y con ella elegimos el umbral final. Antes de optimizar fijamos una regla: un cambio se adopta solo si mejora en al menos 4 de los 5 folds y no empeora con reservas nuevas.

### 4. Baseline (A, 0:45)

> Probamos dos clasificadores vistos en clase. La regresión logística se queda en 0,913 y casi no se separa de entrenamiento: es sesgo por la forma lineal. Random Forest capta interacciones, como la del tipo de cliente con el compromiso, y llega a 0,956.
>
> Con más profundidad crece la brecha entre las dos validaciones, de 0,006 a 0,018, porque los árboles profundos memorizan los lotes. Aun así, el bosque sin límite también es el mejor con reservas nuevas, y por eso es el baseline.

### 5. Dónde se equivoca el modelo (B, 0:50)

> Cruzamos el tipo de cliente con si la reserva es parte de un lote. Las reservas individuales de `cloud_marketplace` son el 41 % de las filas y tienen el 77 % de los errores: 21,4 % de error contra 4,6 % en el resto.
>
> Las cohortes que pide la consigna, `basic` y `GPU_T4`, tienen casi el doble de error. Pero casi toda esa diferencia viene de que son mayormente `cloud_marketplace`: heredan su error.

### 6. Por qué se equivoca (B, 0:50)

> En esa región el modelo no tiene con qué decidir. Solo el 0,9 % tiene cancelaciones previas, contra 10,9 % en el resto, y casi ninguna es de un cliente que vuelve o tiene organización. Tampoco tienen las dos señales fuertes, el compromiso `locked_allocation` y el lote. El resultado son casos dudosos: el 38 % tiene probabilidad entre 0,3 y 0,7.
>
> En la operación, ahí están el 71 % de los falsos negativos, GPUs que quedan ociosas, y el 87 % de los falsos positivos, clientes que se quedarían sin recursos si se reasigna la GPU. Descartamos el umbral: ajustarlo en la región gana 0,2 puntos.

### 7. Curvas de aprendizaje (B, 0:45)

> Entrenamos el baseline con fracciones de cada fold. En entrenamiento la AUC es casi 1 siempre, así que no le falta capacidad. Con reservas nuevas, la curva agrupada sube rápido y después se aplana: duplicar de 15.300 a 30.600 filas sumó 0,004. En la región elegida, la accuracy casi no se mueve.
>
> Conclusión: más filas del mismo tipo ayudan poco. Lo que falta es otra información.

### 8. Enfoque data-centered (B, 0:55)

> Elegimos esta región con los criterios de la clase 11: es frecuente, tiene el mayor margen, cada punto de error que baje suma 0,41 puntos de accuracy global, y su error no depende de memorizar lotes. [T11, p. 39]
>
> Como el problema es falta de información, proponemos registrar datos nuevos, no conseguir más filas. Primero, el historial del cliente: cuando una reserva única lo trae, la AUC sube de 0,876 a 0,916. Después, un identificador de lote, la actividad entre la reserva y la ejecución, registrada con fecha para no meter leakage, y las condiciones comerciales.

### 9. Optimización (C, 0:55)

> Probamos las cuatro estrategias con la misma regla. Las variables derivadas no ayudaron: son funciones de columnas que el modelo ya tiene. Gradient boosting pierde con validación aleatoria, pero es el mejor con reservas nuevas, porque memoriza menos: por eso lo combinamos.
>
> Se adoptaron tres cambios: `max_features` 0,2 en el bosque, el promedio 50/50 con gradient boosting, y 100 árboles en lugar de 300, para que el archivo se pueda mandar por mail. En total, +0,0018 de AUC: una mejora chica, como anticipaba el diagnóstico.

### 10. Dónde mejoró (C, 0:45)

> La consigna pide discutir si la mejora fue global o de subgrupos. Fue específica: se concentra en las cohortes que el baseline ordenaba peor, `independent_client`, la región elegida, las reservas únicas, `basic` y `GPU_T4`. En las fáciles casi no cambia, y en los lotes el error sube 0,2 puntos porque el modelo memoriza menos.
>
> El cambio que más aportó fue la combinación con gradient boosting.

### 11. Evaluación en test (C, 0:45)

> Entrenamos con todo desarrollo y evaluamos una sola vez en test, con el umbral 0,40: AUC 0,960 y balanced accuracy 0,888. Queda algo por encima de la validación cruzada, porque el modelo vio más filas, y dentro del intervalo.
>
> Frente al baseline, la mejora de AUC se confirma; la de balanced accuracy no se distingue de cero, igual que en desarrollo. Y el diagnóstico se sostiene: sin una fila idéntica en desarrollo, la balanced accuracy es 0,795, igual que en las reservas únicas de desarrollo.

### 12. Rendimiento esperado y predictor (C, 0:45)

> Lo esperado depende de cuántas reservas de la evaluación tengan una copia en el CSV. Con el mismo conjunto de reservas: AUC cerca de 0,96 y balanced accuracy cerca de 0,89. Con reservas nuevas: 0,94 y 0,86. Con sólo reservas individuales: 0,89 y 0,79.
>
> Como la competencia mide balanced accuracy, el umbral del predictor es 0,40 y no 0,5: la mejora en los tres escenarios. El predictor se reentrenó con todas las filas, con la misma receta. La receta vive en el `.py`, verificamos que reproduce el modelo evaluado, y lo probamos fuera del notebook con filas crudas del CSV.

### 13. Conclusiones (A, 0:30)

> Tres ideas. Uno: optimizar el modelo dio milésimas, porque el límite es la información. Dos: los errores están en las reservas individuales de `cloud_marketplace`, que no traen historial. Tres: lo que más puede mejorar el sistema es registrar el historial del cliente, un identificador de lote y la actividad previa a la ejecución. Gracias; pasamos a preguntas.

## Preguntas probables

Cada orador toma primero las preguntas de su bloque, marcadas con (A), (B) o (C). Los tres tienen que poder responder cualquiera.

### Datos y evaluación (A)

**¿Por qué no usaron el dataset público del que parece venir este?**
Columnas, valores y período coinciden con el dataset público *Hotel Booking Demand*, con los nombres cambiados (**inferencia**). Si es el origen, probablemente contiene las filas del test oculto con sus etiquetas, y usarlo invalidaría la competencia. Solo lo tomamos como fuente de hipótesis.

**¿Por qué no eliminaron los duplicados?**
Son reservas en lote reales: casi todas son `locked_allocation` o `research_consortium`, y la tasa de cancelación crece con el tamaño del grupo. Eliminarlas cambiaría la distribución que va a ver el predictor. La memorización se controla con la validación agrupada. Hay 79 grupos con etiquetas distintas (531 filas): son error irreducible.

**¿Por qué un split aleatorio y no temporal?**
No sabemos cómo arma la cátedra el conjunto del Model Score. Suponemos que son otras reservas del mismo período y del mismo origen que el CSV, así que no hay motivo para un split temporal; además, la tasa de cancelación no tiene tendencia en el tiempo. Lo que el leaderboard del 05/11 sugiere es que la evaluación tiene menos copias del CSV que un split aleatorio, así que la estimación más realista es la de la validación agrupada. Para reservas nuevas usamos la validación agrupada y las filas de test sin gemela en desarrollo. Las fechas posteriores a 2017 quedan como riesgo no medido.

**¿Por qué AUC y accuracy y no F1? ¿Y la balanced accuracy?**
AUC mide el orden por riesgo sin depender del umbral. [T04, p. 51] Accuracy mide la decisión 0/1; con 41,7 % de canceladas no engaña, porque la referencia trivial da 0,583. F1 no cuenta los aciertos en no cancelaciones, y su umbral óptimo es más bajo, lo que empuja a predecir más cancelaciones. El límite de accuracy, que no distingue el tipo de error [T04, p. 26], se cubre analizando falsos positivos y falsos negativos por separado. Cuando el leaderboard mostró que la competencia mide balanced accuracy, no hizo falta volver a elegir el modelo, porque se eligió por AUC: solo cambió el umbral.

**¿Cómo saben que `assigned_gpu_type` y `queue_wait_time` son leakage si casi no cambian el resultado?**
Se excluyen por definición: describen la asignación definitiva de recursos, que ocurre después del momento de predecir. [P03, p. 5] Medimos una sola vez cuánto inflaban: +0,0014 de AUC. Excluirlas casi no cuesta rendimiento.

**¿El Random Forest sin límite de profundidad no sobreajusta? Tiene AUC 0,9997 en entrenamiento.**
La brecha con entrenamiento es estructural: un bosque de árboles completos siempre ajusta lo que ve. Lo que decide es la validación, y la configuración sin límite es la mejor en los dos esquemas, también con reservas nuevas. La varianza la controla el bosque: `max_features` hace que los árboles sean distintos [T07, p. 61], y el promedio atenúa sus errores. [T07, p. 62]

### Diagnóstico y datos (B)

**¿Cómo definieron la región elegida?**
Reservas de `client_type = cloud_marketplace` que no tienen ninguna fila idéntica en desarrollo. Son 15.855 reservas, el 41 % de desarrollo, con el 77 % de los errores. En test se usa la misma definición, contando las filas idénticas en todo el archivo.

**¿Por qué no entrenaron un modelo separado para la región, o usaron SMOTE?**
Un modelo separado no agrega información, y un Random Forest ya puede separar por `client_type` en sus primeros cortes (**inferencia**). SMOTE no ataca el problema: la región no está desbalanceada (36 % de cancelaciones), y en datos tabulares puede generar combinaciones imposibles de variables. [T11, p. 56]

**¿Cómo saben que falta información y no filas?**
Por tres evidencias:
- con reservas nuevas, duplicar las filas sumó 0,004 de AUC;
- en la región, la accuracy pasó de 0,784 a 0,786 entre la mitad y el total de las filas;
- en entrenamiento la AUC es casi 1, así que no falta capacidad.

Además, ni el feature engineering ni otro modelo mejoraron más que milésimas.

**¿El historial del cliente realmente mejoraría el modelo?**
Hay evidencia, no prueba. En las reservas únicas, cuando hay algún dato del cliente la AUC es 0,916, y sin él 0,876. Es una asociación: los clientes con historial pueden ser distintos por otros motivos. Para confirmarlo se mediría con la misma validación cruzada y diferencias pareadas, globalmente y en la región.

**¿Por qué no bajar el umbral para detectar más cancelaciones?**
Lo bajamos a 0,40, pero por la métrica de la competencia: la balanced accuracy pesa más los falsos negativos que la accuracy. En la operación, con costos iguales para cada error, 0,5 es el óptimo. Si un falso positivo costara el doble que un falso negativo, el umbral subiría a alrededor de 0,62, no bajaría (sección 7.4). Es una decisión operativa que se puede cambiar sin reentrenar. En la región, el mejor umbral (0,48) gana solo 0,2 puntos.

**¿Por qué `basic` y `GPU_T4` no son la región problemática, si la consigna las pide?**
Se analizaron y tienen casi el doble de error que `standard` y `GPU_T1`. Pero el 93 % y el 79 % de sus filas son `cloud_marketplace`, y dentro de esa cohorte la diferencia casi desaparece: `basic` tiene 19,5 % de error y `standard` 18,6 %. Heredan el error por composición: mejorar `cloud_marketplace` las mejora también. [T11, p. 42]

### Optimización y resultado (C)

**¿Por qué no probaron XGBoost o LightGBM?**
`HistGradientBoostingClassifier` está inspirado en LightGBM. [T12, p. 10] Gradient boosting no superó a Random Forest en la validación principal, y el diagnóstico dice que el límite es la información, no la implementación. Además, agregaría una dependencia al predictor que la cátedra tiene que instalar.

**¿Por qué promedio 50/50 y no pesos optimizados o stacking?**
El 75/25 da casi lo mismo, dentro del ruido entre folds. Elegir pesos con los mismos datos que se usan para evaluar es sobreajustar la combinación. Stacking necesita otra capa de validación, y con predicciones tan correlacionadas (0,976) un meta-modelo tiene poco que aprender. [T12, p. 26]

**¿Por qué 100 árboles y no 300?**
Por el tamaño del archivo que se envía por mail. Con 300 árboles el bosque pesa 37 MB comprimido, y con 100, 12 MB. Dentro del promedio, la AUC pasa de 0,9576 a 0,9575.

**¿Por qué test da mejor que la validación cruzada?**
El modelo de test se entrenó con todo desarrollo (38.273 filas), contra unas 30.600 en cada fold, y la curva aleatoria todavía sube con más filas. La diferencia está dentro del intervalo bootstrap.

**¿La mejora frente al baseline es significativa?**
- En AUC sí: +0,0013 en test, con un intervalo de 0,0003 a 0,0023, positiva en el 99 % de los remuestreos.
- En balanced accuracy no se distingue de cero: +0,0012, con un intervalo de −0,002 a +0,005.

El bootstrap remuestrea filas y no tiene en cuenta que las filas de un lote están correlacionadas, así que probablemente subestima algo la incertidumbre.

**¿No es trampa reentrenar el predictor con test?**
No: test se usó una sola vez para evaluar, y nada se eligió con él. Después se reentrena la misma receta con más filas. El rendimiento informado es el del modelo entrenado solo con desarrollo, así que, si cambia algo, es conservador.

**¿Por qué el umbral es 0,40?**
La competencia mide balanced accuracy. Con probabilidades calibradas, el umbral que la maximiza es la tasa de cancelación del conjunto evaluado: 41,7 % en el CSV, 29 % en las reservas únicas. Elegimos el menor umbral que queda a menos de 0,001 del máximo en las dos validaciones: 0,40. Frente a 0,5 mejora en los tres escenarios (aleatoria, agrupada y reservas únicas), y test lo confirma.

**¿Qué pasa si el predictor no carga en la máquina de la cátedra?**
El paquete trae las versiones exactas en `requirements.txt`. Si igual falla, `python predictor_v1_Grupo_11.py entrenar gpu_resource_reservations.csv` regenera el modelo con la misma receta; lo probamos y da las mismas predicciones.

**¿Qué pasa con reservas de 2018 en adelante?**
`execution_year` tomaría valores que el modelo no vio. **Inferencia:** los árboles las tratarían como el último año conocido, y puede haber deriva. No lo medimos: es un riesgo documentado.

## Antes de la defensa

- [ ] Enviar 24 horas antes `predictor_v1_Grupo_11.zip`, el notebook y la presentación. [P03, p. 1]
- [ ] Exportar las diapositivas a PowerPoint (y, si se quiere, a PDF) desde el artifact y guardar el archivo en esta carpeta.
- [ ] Ensayar con cronómetro: el total tiene que quedar debajo de 10 minutos.
