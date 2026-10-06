# Guion de defensa — TP2 Bank Marketing

La exposición principal usa las primeras once diapositivas (portada incluida), dura aproximadamente diez minutos y se reparte entre tres oradores: A, B y C. Las tres últimas quedan como respaldo para preguntas. La consigna pide enviar presentación y código 24 horas antes de la clase de defensa. [P02, p. 1]

| Diapositiva | Orador | Tiempo |
|---|:---:|---:|
| 1. Portada | A | 0:15 |
| 2. Problema y datos | A | 0:50 |
| 3. Los datos cambian con el tiempo | A | 0:55 |
| 4. Del EDA a las decisiones | A | 1:10 |
| 5. `duration`: leakage | B | 0:45 |
| 6. Pipeline, validación y métricas | B | 1:10 |
| 7. Comparación de modelos | B | 1:05 |
| 8. Sobreajuste y subajuste | C | 1:05 |
| 9. Modelo final en test | C | 1:00 |
| 10. Limitación: el modelo aprende el período | C | 0:55 |
| 11. Conclusiones | C | 0:45 |
| **Total** | | **9:55** |

## Reparto entre oradores

| Orador | Bloque | Diapositivas | Tiempo |
|:---:|---|---|---:|
| **A** | El problema y los datos | 1 a 4 | 3:10 |
| **B** | Leakage, evaluación y comparación | 5 a 7 | 3:00 |
| **C** | Ajuste, resultado y límites | 8 a 11 | 3:45 |

Cada bloque cuenta una parte completa del trabajo:

- **A** arma el contexto: el desbalance, la decisión del split por la deriva temporal y el paso del EDA a las decisiones.
- **B** queda unido por la idea de leakage: primero la variable que filtra la respuesta (`duration`), después el preprocesamiento ajustado dentro de cada fold. Con eso justifica las métricas y muestra la comparación.
- **C** cierra con el resultado y su límite. El experimento temporal retoma la deriva que mostró A.

**Equilibrar tiempos.** C tiene unos 45 segundos más que los demás. Hay dos opciones:

1. **Repartir las conclusiones:** A dice las mejoras (la validación temporal retoma la deriva), B dice los supuestos de los modelos, y C dice por qué ganó Random Forest, los errores y la frase final. Así quedan alrededor de 3:25, 3:15 y 3:15. Suma dos pases más, así que conviene ensayarlo.
2. **Que C recorte** unos 15 segundos en cada una de las diapositivas 8 y 10. Lo que no puede faltar es "sin límite: train 0,999, validación 0,766" y "en 2010 el AUC cae a 0,678".

**Preguntas.** Cada orador toma primero las preguntas de su bloque; están marcadas con (A), (B) o (C) en la sección final. Los tres tienen que poder responder cualquiera.

## 1. Portada — 15 segundos · Orador A

"El objetivo del trabajo es decidir a qué clientes conviene llamar en una campaña de plazo fijo. Comparamos Naive Bayes, SVM, KNN y Random Forest con validación cruzada, y estimamos cómo funcionaría el modelo elegido con clientes nuevos."

## 2. Problema y datos — 50 segundos · Orador A

"El dataset tiene 41.188 llamadas y 20 variables. Sólo el 11,3 % de los clientes contrató, así que las clases están desbalanceadas. Quitamos 12 filas exactamente duplicadas para que una copia no quedara en entrenamiento y otra en validación o test. Reservamos 20 % para test con un split estratificado por `y`. Elegimos 20 % porque deja unos 928 positivos para estimar el recall con estabilidad. Todo el EDA y todas las decisiones se tomaron sólo con desarrollo. Modelo, hiperparámetros y umbral se eligieron con validación cruzada de 5 folds, y test se usó una sola vez al final." [P02, p. 1] [T02, p. 89]

## 3. Los datos cambian con el tiempo — 55 segundos · Orador A

"La documentación dice que las filas están ordenadas por fecha, de mayo de 2008 a noviembre de 2010. El gráfico muestra que la tasa de éxito pasa de 4,8 % en 2008 a 52,1 % en 2010, acompañando la caída del euribor. Las cinco variables macro casi no varían entre clientes de una misma fecha: funcionan como un reloj. Teníamos que decidir el split. Un split temporal hubiera dejado test con 31 a 46 % de positivos contra 6 a 7 % en desarrollo, mezclando la calidad del modelo con el cambio de distribución. Elegimos el split aleatorio estratificado, que es lo que supone la consigna con k-fold, sabiendo que eso hace optimista la estimación para campañas futuras. Al final lo cuantificamos." [D03]

## 4. Del EDA a las decisiones — 1 minuto 10 segundos · Orador A

"El EDA lo usamos para decidir. A la izquierda está cuánto cambia la tasa de `yes` entre las categorías de cada variable. `housing`, `loan` y `day_of_week` la mueven menos de 2 puntos, así que las excluimos. En KNN, una variable sin información igual entra en la distancia y agrega ruido. También excluimos `pdays`: el 96 % vale 999 y el resto coincide con `poutcome`. Y excluimos `emp.var.rate`, que tiene correlación 0,97 con `euribor3m`. Dejamos `unknown` como categoría porque es informativo: los clientes con `default` desconocido aceptan 5,3 % contra 12,8 % de los que no están en mora. Aplicamos `log1p` a `campaign` y `previous`, que tienen colas largas. A la derecha, la edad tiene una relación en U: jóvenes y mayores de 60 aceptan mucho más. Es una no linealidad. Las exclusiones las verificamos después por validación cruzada, y eso nos hizo reincorporar `nr.employed`, que mejoraba a Naive Bayes." [P02, p. 1] [T09, p. 39]

**Pase a B:** "Con los datos preparados, [B] cuenta cómo evitamos que el modelo haga trampa y cómo lo evaluamos."

## 5. `duration`: leakage — 45 segundos · Orador B

"`duration` es la duración de la llamada. Es la variable más predictiva, pero se conoce recién al terminar la llamada, cuando ya sabemos la respuesta. La documentación del dataset recomienda descartarla en un modelo realista. Medimos cuánto inflaría el resultado: Random Forest pasa de 0,766 a 0,938 de AUC. Ese número no es alcanzable en el momento en que el modelo tiene que decidir a quién llamar, así que la excluimos de todos los modelos." [D03] [P02, p. 1]

## 6. Pipeline, validación y métricas — 1 minuto 10 segundos · Orador B

"El pipeline tiene dos partes. Las transformaciones fijas, como excluir columnas, construir `default_no` o aplicar `log1p`, no aprenden nada de los datos. El escalado y el one-hot sí aprenden, y se ajustan dentro de cada fold sólo con su parte de entrenamiento, para no filtrar información. Elegimos dos métricas. La principal es AUC: el negocio quiere priorizar, es decir, ordenar clientes, y el AUC mide ese orden para todos los umbrales; un modelo al azar da 0,5. La segunda es recall, porque perder a un cliente que habría contratado cuesta más que una llamada de más. Descartamos la accuracy: un modelo que siempre dice 'no' acierta 88,7 % sin encontrar a nadie. Como el recall depende del umbral, lo elegimos con el criterio de clase, el punto de la curva ROC más cercano a (0, 1), usando las predicciones out-of-fold de desarrollo." [T02, pp. 94, 96] [T04, pp. 26, 41, 51, 52]

## 7. Comparación de modelos — 1 minuto 5 segundos · Orador B

"En gris están los modelos con hiperparámetros por defecto y en azul, ajustados. Random Forest ajustado es el mejor en las dos métricas: AUC 0,798 y recall 0,690. El ajuste cambió el orden. SVM pasó de 0,700 a 0,777, y lo decisivo fue balancear las clases, no `C`. KNN pasó de 0,728 a 0,782 al llevar `k` de 5 a 321. Naive Bayes categórico, sin ajustar, llega a 0,780 y es el modelo más simple. Con el umbral elegido, todos encuentran entre 67 y 69 % de los interesados, pero RF lo hace con la mejor precisión." [P02, p. 2]

**Pase a C:** "Con Random Forest como mejor candidato, [C] muestra cómo elegimos sus hiperparámetros y qué esperamos en datos nuevos."

## 8. Sobreajuste y subajuste — 1 minuto 5 segundos · Orador C

"Las curvas muestran train y validación en función de un hiperparámetro de complejidad. En Random Forest sin límite de profundidad, train llega a 0,999 y validación cae a 0,766: los árboles memorizan, eso es sobreajuste. Con profundidad 2 las dos curvas están juntas pero bajas, un subajuste leve. El máximo de validación está en profundidad 10. En KNN con `k = 1`, train es 0,968 y validación 0,620. Al aumentar `k` la brecha se cierra y validación se estabiliza alrededor de `k = 321`. Hace falta un `k` tan grande porque las clases se superponen mucho: sin `duration`, el 20 % de los clientes comparte exactamente sus predictores con otro." [T07, p. 50] [T09, p. 29]

## 9. Modelo final en test — 1 minuto · Orador C

"Congelamos Random Forest con profundidad 10, 400 árboles y umbral 0,084. Lo reentrenamos con todo desarrollo y recién entonces abrimos test, una sola vez. El AUC fue 0,809 y el recall 0,718. Con bootstrap sobre test, los intervalos de 95 % van de 0,791 a 0,826 y de 0,691 a 0,746. En términos del problema: llamando al 27 % de los clientes encontramos al 72 % de los interesados, y cada llamada tiene 30 % de éxito contra 11,3 % si llamáramos a todos." [T02, p. 88]

## 10. Limitación: el modelo aprende el período — 55 segundos · Orador C

"La principal limitación es temporal. Las cuatro variables macro y el mes suman el 59 % de la importancia del Random Forest: en parte, el modelo aprende cuándo se hizo la llamada y no sólo a quién. Para medirlo, entrenamos con 2008–2009 y evaluamos en 2010, usando sólo desarrollo. El AUC cae a 0,678. Además, el umbral deja de servir: todos los clientes de 2010 lo superan, así que llamaríamos al 100 %. `nr.employed` tomó en 2010 valores que nunca aparecieron antes, y un árbol no puede extrapolar." [T07, p. 71]

## 11. Conclusiones — 45 segundos · Orador C

"Random Forest funcionó mejor porque captura no linealidades como la edad e interacciones, no necesita escalar, y limitar la profundidad controló el sobreajuste. Los supuestos explican el resto: Naive Bayes sufre la correlación entre variables macro y las binarias no gaussianas; KNN, la superposición de clases y las 46 dimensiones; SVM, el desbalance. En test hubo 262 falsos negativos y 1.555 falsos positivos: unas 2,3 llamadas fallidas por cada éxito, contra 7,9 llamando a todos. Esperamos AUC cercano a 0,81 y recall cercano a 0,72 para clientes como los de 2008 a 2010, y menos en campañas futuras. Como mejoras: validación temporal y reentrenamiento, un umbral basado en el costo real, y más información previa a la llamada."

## Preguntas probables

### (A) ¿Por qué no hicieron un split temporal si los datos están ordenados por fecha?

Porque test hubiera tenido entre 31 y 46 % de positivos contra 6 a 7 % en desarrollo, y la métrica final habría mezclado la calidad del modelo con un cambio fuerte de distribución. Además, la consigna pide k-fold, que supone datos intercambiables. Elegimos el split aleatorio y cuantificamos la limitación con un experimento temporal aparte, que usó sólo desarrollo.

### (A) ¿Por qué 20 % de test y no 10 % como en el TP1?

Porque con 11 % de positivos, un test de 10 % tendría unos 464 positivos. Con 20 % hay 928, y el recall y la precisión se estiman con menos variabilidad. Desarrollo sigue teniendo 32.940 filas.

### (B) ¿Por qué 5 folds y no 10?

El material menciona 5 o 10 como valores usuales. [T02, p. 85] Con 33 mil filas, cada fold de validación tiene unos 742 positivos, suficiente para estimar AUC y recall. El límite práctico fue SVM: cada ajuste tarda hasta tres minutos.

### (B) ¿Por qué AUC y recall? ¿Por qué no F1?

AUC porque el objetivo es ordenar clientes para priorizar llamadas, y no depende del umbral. Recall porque el error más caro es no llamar a quien habría contratado. F1 aparece nombrado en la clase 4 pero no se desarrolla. [T04, p. 24] Además, F1 le da el mismo peso a precisión y recall, y nosotros priorizamos recall. La precisión la reportamos igual, como contexto.

### (B) ¿Cómo eligieron el umbral? ¿No es leakage elegirlo con los mismos datos?

Con las predicciones out-of-fold de desarrollo: cada cliente recibe el score de un modelo que no lo vio. Elegimos el punto de la curva ROC más cercano a (0, 1), el criterio de la clase. [T04, p. 52] Es un único parámetro elegido en desarrollo y fijado antes de mirar test, así que la estimación de test sigue siendo honesta.

### (B) ¿Por qué el umbral es tan bajo (0,084)?

Porque los positivos son 11 %, y los scores de RF reflejan esa tasa base. Con el umbral 0,5, el recall del RF ajustado es 0,23: se escaparía más de tres de cada cuatro interesados.

### (B) Si `duration` mejora tanto, ¿por qué no usarla?

Porque se conoce al terminar la llamada, cuando el resultado ya se sabe. El modelo tiene que decidir antes de llamar. Usarla sería leakage: el 0,938 de AUC no es alcanzable en la práctica. [D03]

### (B) ¿Cómo evitaron el leakage en el preprocesamiento?

Las transformaciones que aprenden de los datos (escalado, one-hot, discretización) están dentro del pipeline y se ajustan en cada fold sólo con su entrenamiento. Las transformaciones fijas no aprenden parámetros. Test se separó antes del EDA. [T02, pp. 94, 96]

### (A) ¿Por qué dejar `unknown` como categoría en vez de imputar o eliminar?

Porque es informativo: `default = unknown` acepta 5,3 % frente a 12,8 % de `default = no`. Eliminar esas filas habría tirado el 21 % de los datos, e imputar con la moda habría borrado la señal. La documentación admite tratarlo como categoría. [D03]

### (A) ¿Por qué `default = yes` se agrupó con `unknown`?

Porque había 2 filas en desarrollo: ningún modelo puede aprender una categoría así. La variable quedó como "consta que no está en mora". Un cliente en mora no puede quedar del lado de `no`, así que se agrupa con `unknown`.

### (A) Si `nr.employed` y `euribor3m` tienen correlación 0,94, ¿por qué dejaron las dos?

El EDA proponía excluir `nr.employed`, pero la verificación por CV mostró que agregarla mejora Naive Bayes (+0,007 el gaussiano, +0,004 el categórico) sin afectar a RF ni a KNN. Aporta información propia, así que la reincorporamos. `emp.var.rate` no sumaba nada encima y quedó afuera.

### (C) ¿No es exagerado `k = 321` en KNN?

Con 26 mil clientes de entrenamiento por fold, 321 vecinos son el 1,2 %. Hace falta un vecindario grande porque las clases se superponen mucho: sin `duration`, el 20,5 % de los clientes comparte exactamente sus predictores con otro, y 1.067 tienen un "gemelo" con la respuesta opuesta. Validación queda prácticamente igual entre `k = 161` y `k = 1281`.

### (C) ¿Por qué KNN con ponderación por distancia tiene AUC de train 0,999?

Porque cada punto de entrenamiento es su propio vecino a distancia 0, con peso máximo, así que el modelo memoriza train. En validación rinde peor (0,748) que con pesos uniformes (0,782).

### (C) ¿Por qué SVM rindió tan mal sin balancear clases?

SVM no estima probabilidades: busca un margen. Con 11 % de positivos y clases muy superpuestas, la solución favorece a la clase mayoritaria y el score ordena mal. Con `class_weight = balanced`, un error en un positivo pesa unas 8 veces más que en un negativo, y el AUC sube de 0,71 a 0,777. Esta explicación es conocimiento general: no está en las diapositivas.

### (C) ¿Qué significa `C`?

En scikit-learn es el costo de violar el margen: un `C` chico regulariza más. Coincide con la diapositiva del kernel RBF. [T08, p. 49] La formulación del margen tolerante usa `C` como presupuesto de holguras, con el sentido opuesto. [T08, p. 30] En la curva, `C` grande sube train y baja validación: sobreajuste.

### (B) ¿Por qué Naive Bayes categórico le gana al gaussiano?

Porque 39 de las 46 columnas son binarias y las numéricas son asimétricas: el supuesto de normalidad no se cumple. El categórico discretiza y estima frecuencias con Laplace, que se ajusta mejor a datos discretos. [T06, p. 43] Los dos comparten el supuesto de independencia, que la correlación entre variables macro viola.

### (C) ¿Por qué test dio mejor que la validación cruzada?

0,809 contra 0,798 está dentro de la variabilidad. El desvío entre folds es 0,009 y el intervalo bootstrap de test va de 0,791 a 0,826. No cambiamos nada después de mirar test.

### (C) ¿Qué es el intervalo bootstrap?

Remuestreamos con reposición las 8.236 filas de test 1.000 veces y recalculamos las métricas sin reentrenar. Los percentiles 2,5 y 97,5 dan el rango esperable de la estimación. Es conocimiento general: no está en el material de la cátedra.

### (C) ¿Cómo se lee la importancia de variables?

Es la reducción de impureza acumulada en los cortes donde se usa cada variable. [T07, p. 71] Tiende a favorecer a las numéricas con muchos valores, así que el orden es orientativo. Lo robusto es la conclusión de que el contexto macro y el mes pesan mucho.

### (C) Entonces, ¿el modelo sirve para una campaña nueva?

Sirve para clientes parecidos a los de 2008–2010. Para una campaña futura habría que validar temporalmente, reentrenar con datos recientes y recalibrar el umbral. Sin eso, como muestra el experimento, el umbral puede quedar inútil.

### (B) ¿Por qué no usaron oversampling o SMOTE?

No está en el material de la materia. Trabajamos el desbalance con métricas que no se engañan (AUC y recall), con el umbral elegido por validación y, en SVM, con `class_weight`.
