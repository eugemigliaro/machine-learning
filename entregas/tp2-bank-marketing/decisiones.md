# Decisiones y supuestos

## Confirmadas

### Dataset

Se usa Bank Marketing (`bank-additional-full.csv`), con `y` como variable objetivo y los otros 20 atributos como candidatos a predictores. [P02, p. 1] [D02] [D03]

### Reproducibilidad

Se fija `random_state = 42` para que la partición, los folds y los modelos con aleatoriedad puedan reproducirse.

### Duplicados exactos

Hay 12 filas idénticas a otra fila anterior en los 21 campos. Se conserva la primera aparición y se eliminan las copias de la copia de trabajo antes del split. Mantener ambas podría poner una en entrenamiento y otra en validación o test, y producir una estimación optimista. Es el mismo criterio que en el TP1. No hay filas con los mismos predictores y distinta `y`. El CSV `[D02]` no se modifica.

### Partición de test

Se reserva el 20 % como test con un split aleatorio estratificado por `y`: 32.940 filas de desarrollo (3.711 positivos) y 8.236 de test (928 positivos), ambos con 11,27 % de `yes`. Test no se usa para elegir preprocesamiento, variables, modelo ni hiperparámetros. [P02, p. 1] [T02, p. 89] [T02, p. 94]

Se descartó el split temporal: test tendría entre 31 % y 46 % de positivos frente a 6–7 % en desarrollo, y la métrica final mezclaría la calidad del modelo con el cambio de distribución. A cambio, se acepta que la estimación final supone datos parecidos a la mezcla de 2008 a 2010, y por eso es optimista para campañas futuras. Para cuantificarlo, al final se hará un experimento temporal: entrenar con 2008–2009 y evaluar en 2010.

Opciones evaluadas:

| Estrategia | Test | Tasa de `yes` en dev / test |
|---|---|---|
| **Aleatoria estratificada por `y`, 20 % (elegida)** | 8.236 filas, 928 positivos | 11,3 % / 11,3 % |
| Aleatoria estratificada por `y`, 10 % | 4.118 filas, ~464 positivos | 11,3 % / 11,3 % |
| Temporal, último 20 % | 8.235 filas | 6,4 % / 30,8 % |
| Temporal, último 10 % | 4.118 filas | 7,4 % / 45,9 % |

## Observaciones de integridad

Se calculan sobre las 41.176 filas de la copia de trabajo, antes del split. Sólo se usan para entender el esquema y diseñar la partición, no para decidir el preprocesamiento.

- No hay `NaN`. Los faltantes de las categóricas están codificados como `unknown`. [D03] Afectan a `default` (20,88 %), `education` (4,20 %), `housing` y `loan` (2,40 % cada una), `job` (0,80 %) y `marital` (0,19 %).
- `pdays = 999` significa "no contactado en una campaña previa". [D03] Aparece en el 96 % de las filas. Todos los `poutcome = nonexistent` (35.551) tienen `pdays = 999` y `previous = 0`. Además, 4.110 clientes con `poutcome = failure` tienen `pdays = 999`: fueron contactados antes, pero sin registro de días. Hay que tenerlo en cuenta al tratar `pdays` como numérica.
- La documentación indica que `duration` determina fuertemente `y`, que no se conoce antes de la llamada, y que debe descartarse en un modelo predictivo realista. [D03] Es el leakage que la consigna pide analizar. [P02, p. 1]

## Balance de clases y orden temporal

- `yes` representa el 11,27 % (4.639 de 41.176). Las clases están desbalanceadas.
- Las filas están ordenadas por fecha, de mayo de 2008 a noviembre de 2010. [D03] La secuencia de meses forma 26 bloques consecutivos, coherentes con ese período, así que el año se reconstruye sin ambigüedad. Esa columna auxiliar no es un predictor.
- La tasa de éxito cambia mucho con el tiempo: 4,8 % en 2008 (27.682 filas), 19,5 % en 2009 (11.436) y 52,1 % en 2010 (2.058).
- Las cinco variables macroeconómicas tienen sólo 375 combinaciones distintas y están muy correlacionadas: `euribor3m` con `emp.var.rate` 0,97 y con `nr.employed` 0,95. En la práctica identifican el período de la llamada.

## Resultados del EDA de desarrollo

Calculados sólo sobre las 32.940 filas de desarrollo.

### Categóricas

- **Variables casi sin información:** la tasa de `yes` apenas cambia entre categorías de `loan` (rango 0,5 puntos), `housing` (0,7) y `day_of_week` (1,6), frente a una tasa global de 11,3 %.
- **Variables informativas:** `poutcome` (`success` 66,0 % frente a `nonexistent` 8,8 %), `month` (6,4 % a 50,3 %), `job` (`student` 32,3 % y `retired` 25,8 % frente a `blue-collar` 6,9 %), `contact` (`cellular` 14,7 % frente a `telephone` 5,2 %) y `default`.
- **`unknown` informativo:** `default = unknown` (20,8 % de las filas) tiene 5,3 % de `yes` frente a 12,8 % de `default = no`. El faltante es en sí una señal, no ruido.
- **Categorías casi vacías:** `default = yes` (2 filas) y `education = illiterate` (18 filas).
- **`housing` y `loan`:** sus `unknown` son exactamente las mismas 779 filas.
- **`month` y el período:** los meses con tasa alta (`mar`, `sep`, `oct`, `dec`) son casi exclusivamente de 2009–2010. `month` es, en parte, otro indicador del período.

### Numéricas

- **Asimetría:** `campaign` (asimetría 4,9, máximo 56), `previous` (3,9; 86 % de ceros) y `duration` (3,2) tienen colas largas a la derecha.
- **`pdays`:** vale 999 en el 96 % de las filas. Sus valores menores que 999 coinciden con los 1.094 `poutcome = success` más 113 `failure`, así que la información ya está en `poutcome`.
- **`age`:** relación no monótona con `y`. La tasa es de 24 % hasta 24 años, baja a 8 % entre 40 y 49, y sube a 35 % y 47 % después de los 60. Su AUC univariado (0,51) no la detecta, aunque es informativa. [T03, p. 51]
- **AUC univariado:** `duration` 0,82; `nr.employed` 0,75; `euribor3m` 0,74; `emp.var.rate` 0,71. El resto queda por debajo de 0,61.
- **Correlaciones:** `emp.var.rate`–`euribor3m` 0,97, `euribor3m`–`nr.employed` 0,94, `emp.var.rate`–`nr.employed` 0,91 y `emp.var.rate`–`cons.price.idx` 0,77. Las tres primeras miden prácticamente lo mismo.

### `duration`

La tasa de `yes` crece monótonamente con la duración: casi 0 % en el primer decil y 46 % en el último. Las 4 llamadas con `duration = 0` tienen `y = no`. Esto coincide con la advertencia de la documentación: es la mejor variable individual precisamente porque se conoce recién al terminar la llamada. [D03] [P02, p. 1]

## Decisiones confirmadas tras el EDA

- **`duration`:** se excluye de todos los modelos, porque no se conoce antes de la llamada. [D03] [P02, p. 1] Se medirá una vez cuánto inflaría las métricas si se incluyera (benchmark).
- **`default`:** pasa a la binaria `default_no` (1 si `default = no`, 0 si es `unknown` o `yes`). Las 2 filas con `yes` no alcanzan para que un modelo aprenda esa categoría. Se agrupan con `unknown` y no con `no`, porque un cliente en mora no puede quedar dentro de "consta que no está en mora". Que el dato falte por algún motivo vinculado al crédito es sólo una hipótesis. Lo observado es que ese grupo acepta menos.
- **`education = illiterate`:** se agrupa con `basic.4y`. En el resto de las categóricas, `unknown` queda como categoría propia. [D03]
- **Exclusiones:** `pdays`, que es redundante con `poutcome`; `housing`, `loan` y `day_of_week`, que casi no tienen información; y `emp.var.rate`, que es redundante con `euribor3m`. [T07, p. 72] [T09, p. 39] Al principio también se excluía `nr.employed`, pero la verificación por validación cruzada mostró que aporta (ver abajo) y se reincorporó.
- **`log1p`:** se aplica a `campaign` y `previous` antes de escalar. Baja el z máximo de `campaign` de 19,3 a 6,0. No aprende parámetros, así que no produce leakage, y no cambia el orden de los valores, así que no afecta a Random Forest.
- **Escalado y codificación:** `StandardScaler` en las 7 numéricas y one-hot en las 6 categóricas, ajustados dentro de cada fold. El pipeline pasa de 20 columnas originales a 46.

Variables finales:

| Tipo | Variables |
|---|---|
| Numéricas | `age`, `campaign` (log), `previous` (log), `cons.price.idx`, `cons.conf.idx`, `euribor3m`, `nr.employed` |
| Categóricas | `job`, `marital`, `education`, `contact`, `month`, `poutcome` |
| Binaria | `default_no` |

## Verificación de las exclusiones

Partiendo del conjunto que proponía el EDA, se agregó cada grupo excluido por separado y se midió el cambio de AUC de validación (5 folds, hiperparámetros por defecto). [P02, p. 1]

| Grupo agregado | NB gaussiano | NB categórico | RF | KNN |
|---|---:|---:|---:|---:|
| `pdays` | +0,000 | 0,000 | −0,001 | 0,000 |
| `housing`, `loan`, `day_of_week` | −0,001 | 0,000 | +0,007 | −0,008 |
| `nr.employed` | +0,007 | +0,004 | 0,000 | 0,000 |
| `emp.var.rate`, `nr.employed` | +0,009 | +0,003 | −0,002 | −0,001 |

- **`pdays`:** se confirma la exclusión, porque no aporta nada.
- **`housing`, `loan` y `day_of_week`:** empeoran KNN y mejoran RF con hiperparámetros por defecto. Para conservar un único conjunto de variables se mantienen excluidas, y se vuelven a probar con el RF ajustado.
- **`nr.employed`:** mejora las dos variantes de Naive Bayes sin afectar a los demás modelos. Se **reincorpora**, aunque esté correlacionada con `euribor3m`.
- **`emp.var.rate`:** no agrega nada sobre `nr.employed`, así que se mantiene excluida.

## Validación y métricas

- **Validación cruzada:** k-fold estratificado con `k = 5`, `shuffle=True` y `random_state = 42`, sólo sobre desarrollo. Cada fold de validación tiene unos 742 positivos. [P02, p. 2] [T02, p. 85] [T03, p. 12] Se eligió 5 en lugar de 10 por el costo de SVM: con todo desarrollo, cada ajuste tarda alrededor de dos minutos.
- **AUC (métrica principal):** el objetivo es priorizar a qué clientes llamar, es decir, ordenarlos por probabilidad de aceptar. El AUC mide ese orden sin depender del umbral, y vale 0,5 tanto al azar como para "siempre no". [P02, p. 1] [T04, p. 51]
- **Recall:** perder a un cliente que habría contratado (FN) cuesta más que una llamada de más (FP). [T04, p. 31] [T04, p. 41]
- **Accuracy descartada:** "siempre no" obtiene 88,7 % sin encontrar positivos. [T04, p. 26]
- **Umbral:** para cada modelo, el punto de la curva ROC *out-of-fold* de desarrollo más cercano a `(0, 1)`. [T04, p. 52] Se fija antes de mirar test. Como contexto se reportan precisión, especificidad, matriz de confusión y el recall con el umbral por defecto.
- **Naive Bayes:** se comparan dos variantes. La gaussiana usa las mismas columnas escaladas y one-hot, y viola a propósito el supuesto de normalidad en las binarias. La categórica discretiza las numéricas en 5 cuantiles por fold y usa Laplace con `alpha = 1`. [T06, p. 32] [T06, p. 43]
- **Hiperparámetros iniciales:** los valores por defecto de scikit-learn. El ajuste se hace con curvas de validación en la etapa siguiente.
- **AUC de entrenamiento:** para leer el gap, se calcula sobre una muestra de 5.000 filas de cada fold de entrenamiento. Sobre las 26 mil filas multiplicaría el costo de KNN y SVM.
- **SVM con todo desarrollo:** se evaluó submuestrear, pero un ajuste tarda entre 40 y 180 s según `C`. Con 8 núcleos y los folds en paralelo, una curva completa se calcula en minutos, así que se usa todo desarrollo.
- **Caché:** los resultados de cada validación se guardan en `cache/` (no versionado) con `joblib.Memory`. Si se modifica el código de `prepare_features` o de la evaluación, hay que borrar `cache/`.

## Comparación con hiperparámetros por defecto

Validación cruzada de 5 folds sobre desarrollo, con el conjunto final de variables:

| Modelo | AUC train | AUC val | Recall val (umbral CV) |
|---|---:|---:|---:|
| Referencia (siempre no) | 0,500 | 0,500 | 0,000 |
| Naive Bayes gaussiano | 0,773 | 0,763 | 0,683 |
| Naive Bayes categórico | 0,793 | 0,780 | 0,682 |
| KNN (`k = 5`) | 0,928 | 0,728 | 0,668 |
| Random Forest (sin límite de profundidad) | 0,999 | 0,766 | 0,662 |
| SVM (RBF, `C = 1`) | 0,849 | 0,700 | 0,576 |

## Benchmark con `duration`

Agregar `duration` sube el AUC de validación de Random Forest de 0,766 a 0,938, el de KNN de 0,728 a 0,861 y el de Naive Bayes categórico de 0,780 a 0,867. Es la magnitud del leakage: el modelo "aprende" algo que sólo se sabe al terminar la llamada. [D03]

## Ajuste de hiperparámetros

Curvas de validación con AUC de train y de validación. [P02, p. 2] [T07, p. 50]

- **KNN:** con pesos uniformes, el AUC de validación sube de 0,620 (`k = 1`) a 0,782 (`k = 321`) y se estabiliza hasta `k = 1281`. Train baja de 0,968 a 0,804: `k` chico sobreajusta y la brecha se cierra al aumentar `k`. [T09, p. 29] Con ponderación por distancia, train queda en 0,999 (cada punto es su propio vecino) y validación no pasa de 0,748. **Elegido: `k = 321`, uniforme.**
- **Random Forest:** con 100 árboles, validación sube de 0,778 (`max_depth = 2`, leve subajuste) a 0,798 (`max_depth` 10–12). Con 20 baja a 0,786, y sin límite a 0,766, con train en 0,999: sobreajuste. Los árboles mejoran validación de 0,792 (10) a 0,798 (100 a 400). **Elegido: `max_depth = 10`, 400 árboles.** Con este RF, reincorporar `housing`, `loan` y `day_of_week` no mejora (0,7979 frente a 0,7984): se confirma la exclusión.
- **SVM:** sin balanceo, validación queda entre 0,695 y 0,710 para cualquier `C`, mientras train sube de 0,737 a 0,881 al aumentar `C`. Con `class_weight='balanced'` llega a 0,777 con `C = 0,1` y cae a 0,750 con `C = 10`, por sobreajuste. **Conocimiento general:** el balanceo multiplica el costo de los errores en positivos (alrededor de 4,4 frente a 0,56). Sin él, la solución de margen favorece a la clase mayoritaria. Kernels con `C = 0,1` balanceado: lineal 0,769, polinómico 0,777 y RBF 0,777. **Elegido: polinómico, `C = 0,1`, balanceado** (empatado con RBF). `γ` se dejó en `'scale'`: valores entre 0,001 y 0,078 cambiaron el AUC menos de 0,02 en una prueba sobre un fold.
- **Naive Bayes:** la consigna no pide ajustarlo. [P02, p. 2]

## Modelos ajustados

| Modelo | AUC train | AUC val | Recall val | Precisión val | Especificidad val | Umbral |
|---|---:|---:|---:|---:|---:|---:|
| Random Forest (`max_depth = 10`, 400 árboles) | 0,853 | **0,798 ± 0,009** | **0,690** | 0,290 | 0,786 | 0,084 |
| KNN (`k = 321`) | 0,804 | 0,782 ± 0,010 | 0,671 | 0,276 | 0,776 | 0,087 |
| Naive Bayes categórico | 0,793 | 0,780 ± 0,009 | 0,682 | 0,279 | 0,776 | 0,081 |
| SVM (polinómico, `C = 0,1`, balanceado) | 0,827 | 0,777 ± 0,009 | 0,685 | 0,280 | 0,777 | −0,855 (decision function) |
| Naive Bayes gaussiano | 0,773 | 0,763 ± 0,010 | 0,683 | 0,252 | 0,743 | 0,0002 |

Con el umbral elegido por CV, Random Forest llama al 26,8 % de los clientes de desarrollo y encuentra al 69 % de quienes contratarían. Para llegar a 80 % de recall habría que llamar al 45,4 % (precisión 19,8 %), y para 90 %, al 67,4 % (precisión 15 %).

## Observación: predictores idénticos sin `duration`

Sin `duration`, el 20,5 % de las filas de desarrollo comparte exactamente sus predictores con otra fila. Hay 1.067 filas en 414 grupos con predictores idénticos y distinta `y`. Es un error irreducible con la información disponible antes de la llamada. Por eso KNN con `k = 1` no llega a AUC 1 en train (0,968).

## Modelo final

- **Elegido:** Random Forest con `max_depth = 10` y 400 árboles, por tener el mayor AUC y el mayor recall de validación. [P02, p. 2]
- **Umbral:** 0,084, el punto de la curva ROC *out-of-fold* de desarrollo más cercano a `(0, 1)`. [T04, p. 52] Se fijó antes de mirar test.
- **Entrenamiento:** se reentrenó con las 32.940 filas de desarrollo [T02, p. 88] y se evaluó **una sola vez** en test.

| Métrica | Desarrollo (CV out-of-fold) | Test | IC 95 % bootstrap en test |
|---|---:|---:|---:|
| AUC | 0,798 | **0,809** | 0,791 – 0,826 |
| Recall | 0,690 | **0,718** | 0,691 – 0,746 |
| Precisión | 0,290 | 0,300 | 0,281 – 0,317 |
| Especificidad | 0,786 | 0,787 | — |
| Clientes llamados | 26,8 % | 27,0 % | — |

En test, el modelo llamaría a 2.221 de 8.236 clientes y encontraría a 666 de los 928 interesados. La tasa de éxito de las llamadas sería de 30,0 %, frente a 11,3 % llamando a todos. La matriz de confusión tiene 666 TP, 1.555 FP, 262 FN y 5.753 TN.

**Importancias:** `euribor3m` (0,193), `nr.employed` (0,183) y `poutcome` (0,157) son las principales. Los índices macro y `month` suman el 59,1 % de la importancia. [T07, p. 71]

## Experimento temporal

Se entrenó el pipeline final con las filas de desarrollo de 2008–2009 (31.275 filas, 9,1 % de `yes`) y se evaluó con las de 2010 (1.665 filas, 51,9 % de `yes`). Test no intervino.

| Escenario sobre las filas de 2010 | AUC | Clientes llamados con umbral 0,084 |
|---|---:|---:|
| CV aleatoria (el modelo vio otras filas de 2010) | 0,748 | 100 % |
| Entrenado sólo con 2008–2009 | 0,678 | 100 % |

El 100 % de las filas de 2010 tiene `nr.employed` por debajo del mínimo de 2008–2009, y el 30,9 % tiene `euribor3m` por debajo del mínimo. La estimación de test es válida para clientes parecidos a la mezcla de 2008 a 2010, pero es optimista para campañas futuras. Es la principal limitación del sistema.
