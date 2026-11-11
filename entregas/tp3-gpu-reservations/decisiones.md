# Decisiones y supuestos

## Contexto

- Grupo 11. Defensa el 11/11/2026. No se envió ningún predictor el 04/11.
- La cátedra no aclaró la métrica del Model Score, las columnas del `X` de evaluación, el formato de salida ni el formato de envío. Esas cuestiones se resuelven con los supuestos de abajo. Si en la defensa resultan distintas, se ajusta el predictor para la entrega del 18/11. [P04]

## Confirmadas antes del EDA

### Reproducibilidad

`random_state = 42` en la partición, los folds y los modelos con aleatoriedad.

### Datos externos

No se usa el dataset público *Hotel Booking Demand*. **Inferencia:** columnas, valores y período coinciden con ese dataset con los nombres cambiados. Si es el origen, probablemente contiene las filas del test oculto con sus etiquetas, y usarlo invalidaría la competencia. Solo sirve como fuente de hipótesis, que se validan con nuestros datos. El punto 3.4 se responde proponiendo datos que la plataforma podría registrar.

### Librerías

Solo scikit-learn, para que el predictor corra en la máquina de la cátedra sin dependencias extra. Gradient boosting se cubre con `HistGradientBoostingClassifier`, que según la clase 12 está inspirado en LightGBM. [T12, p. 10] En el paso 4 se compara contra XGBoost (`apt install python3-xgboost`). Solo se adopta si la mejora supera claramente la variación entre folds.

### Leakage

| Columna | Decisión | Motivo |
|---|---|---|
| `execution_status` | Excluir | `canceled` y `no_show` coinciden siempre con `canceled_job = 1`, y `completed` con `0`. |
| `execution_status_date` | Excluir | En las canceladas cae en promedio 90 días antes de la ejecución programada; en las completadas, ese día o después. |
| `assigned_gpu_type` | Excluir y medir una vez cuánto infla | Es la GPU "finalmente asignada para la ejecución". [P03, p. 5] Cuando difiere de la pedida, solo se cancela el 6 % de las reservas, frente al 45 %. |
| `queue_wait_time` | Excluir y medir una vez cuánto infla | Mide la espera "antes de la asignación definitiva de recursos". [P03, p. 5] |

Es el mismo criterio que con `duration` en el TP2. [D03]

### Duplicados y validación

- Hay 15.936 filas que repiten exactamente otra fila, sin contar el objetivo ni las columnas de estado. El 41 % de las filas pertenece a uno de 3.499 grupos de reservas idénticas.
- La tasa de cancelación crece con el tamaño del grupo: 28 % en las filas únicas y 95 % en los grupos de más de 50 copias. Las filas con gemelas son, sobre todo, `locked_allocation` y `research_consortium`.
- **Inferencia:** son reservas en lote, no errores de carga. **Se conservan.**
- Hay 79 grupos (531 filas) con features idénticos y etiquetas distintas: son error irreducible.
- **Validación principal:** `StratifiedKFold(5)` sobre desarrollo. Imita una evaluación con filas del mismo conjunto de reservas, que es el supuesto para el Model Score.
- **Control:** `StratifiedGroupKFold(5)`, con un grupo por cada conjunto de filas idénticas, para estimar el rendimiento con reservas nunca vistas. [T11, p. 53] [T11, p. 79]
- En test se reporta por separado el rendimiento en las filas con gemela en desarrollo (38,6 % del test) y en las filas sin gemela.

### Partición de test

Split aleatorio estratificado por `canceled_job`, 20 %: 38.273 filas de desarrollo y 9.569 de test, ambos con 41,71 % de canceladas. Test no se usa para elegir preprocesamiento, variables, modelo, hiperparámetros ni umbral. [P03, p. 1] [T02, p. 89]

### Métricas

Se eligió AUC más accuracy (opción B) en lugar de AUC más F1.

- **AUC (principal):** compara modelos e hiperparámetros sin depender del umbral y no favorece a ninguna clase. Mide el orden por riesgo que usaría un operador. [T04, p. 51]
- **Accuracy:** mide la decisión 0/1 que devuelve el predictor. Cada acierto vale lo mismo, sea cancelación o no cancelación. Con 41,7 % de positivos no es engañosa, porque predecir siempre "no se cancela" da 58,3 %. Es la candidata más probable para el Model Score. Su límite es que no distingue el tipo de error [T04, p. 26], así que se complementa con la matriz de confusión, la especificidad y la precisión.
- **Por qué no F1:** `F1 = 2·TP / (2·TP + FP + FN)` no cuenta los aciertos en no cancelaciones, y su umbral óptimo es más bajo que el de accuracy, lo que inclina el modelo a predecir más cancelaciones. Con un modelo de prueba, los umbrales óptimos de F1 (0,40) y de accuracy (0,45 a 0,50) dieron casi la misma accuracy.
- **Asimetría de costos:** no se fija una proporción de costos para elegir modelos, porque no hay datos para justificarla. En el punto 3.3 se muestra cómo se movería el umbral si un falso positivo, que sobrecompromete una reserva que sí se ejecuta, costara 2 o 3 veces más que un falso negativo, que deja una GPU ociosa. **Conocimiento general:** con probabilidades calibradas, conviene predecir "se cancela" si `p > c_FP / (c_FP + c_FN)`.
- **Umbral:** 0,5 mientras se comparan modelos. El umbral final se elige al cerrar el modelo con las predicciones *out-of-fold* de desarrollo, nunca con test.

### Predictor

- Archivo `.py` con `predictor_v1_Grupo_11(X)`, que devuelve un `np.ndarray` de 0/1 con el largo y el orden de `X`.
- Una variante `predictor_v1_Grupo_11_proba(X)`, mencionada en el mail.
- El modelo se guarda en un `.joblib` que se carga con una ruta relativa al `.py`.
- Se envía un `.zip` con el `.py`, el modelo, un `requirements.txt` con las versiones exactas y un README con un ejemplo de uso.
- **Entrada:**
  - si llega un DataFrame, se seleccionan las columnas por nombre y se ignoran las sobrantes (`execution_status`, `canceled_job` u otras no documentadas);
  - si llega un array sin nombres con 33 columnas, se asume el orden del CSV sin el objetivo, y con 34 columnas, el del CSV completo, ignorando la primera (`canceled_job`). Una sola fila puede llegar como array o como `Series`. Ampliado el 09/11;
  - en cualquier otro caso, error claro.
- Tolera faltantes y categorías no vistas.
- Se prueba en un proceso nuevo con filas crudas del CSV antes de cada envío.

## Confirmadas tras el EDA (sección 4 del notebook)

Aceptadas sin objeciones el 07/11. Las transformaciones fijas están en `prepare_features` (`predictor_v1_Grupo_11.py`), que usan tanto el notebook como el predictor. Las que aprenden de los datos van dentro del pipeline.

| Variable o grupo | Decisión |
|---|---|
| `total_processes`, `total_gpu_hours`, `high_value_client` | No usar como entrada. Los totales son sumas exactas de variables documentadas y se pueden recalcular. `high_value_client` no tiene definición y no es un umbral simple del costo. |
| `organization_id` | Binaria `has_organization`: 95 % de faltantes. Con organización se cancela el 23 %, sin ella el 43 %. |
| `orchestration_agent_id`, `client_region` | Categóricas, con el faltante como categoría propia. |
| Categorías con menos de 50 filas | Agrupar como "infrecuente" dentro de cada fold (`min_frequency` del encoder). |
| `num_auxiliary_processes` | Imputar con la mediana de entrenamiento (un faltante). |
| `resource_modifications` | Conservar y medir su aporte. Su definición no la ubica después de la ejecución. |
| Fechas | Conservar `execution_year`, `month`, `week` y `day` como numéricas. No hay tendencia temporal sostenida. Revisar el aporte de `execution_year` en la selección de variables. |
| Valores extremos | Conservar el costo de 270 USD por hora. `log1p` a las numéricas de cola larga solo en modelos sensibles a la escala. |
| Reservas vacías | Conservar las de costo 0, sin procesos o sin horas GPU. Se siguen como cohortes en el análisis de errores. |

## Baseline (sección 6 del notebook)

### Preprocesamiento por modelo

- **Ambos modelos:**
  - Imputación con la mediana del fold.
  - One-hot con `min_frequency = 50` y `handle_unknown = 'infrequent_if_exist'`.
  - Quedan 139 columnas.
- **Regresión logística:** además, `log1p` a las numéricas de cola larga y `StandardScaler`.
- **Random Forest:** sin escalado.

### Resultados con validación cruzada de 5 folds sobre desarrollo

| Modelo | AUC aleatoria | AUC agrupada | Accuracy aleatoria | Accuracy agrupada |
|---|---:|---:|---:|---:|
| Referencia trivial ("nunca se cancela") | 0,500 | 0,500 | 0,583 | 0,583 |
| Regresión logística, `C = 1` | 0,913 | 0,908 | 0,829 | 0,825 |
| **Random Forest, sin límite de profundidad, hoja 1, 300 árboles** | **0,956** | **0,937** | **0,885** | **0,857** |

- **Regresión logística:** la AUC deja de mejorar desde `C = 1`. Entrenamiento y validación difieren en menos de 0,002, un síntoma de sesgo por la forma lineal.
- **Random Forest:** se probaron `max_depth` en {8, 12, 16, 20, sin límite} y `min_samples_leaf` en {1, 5}. Más profundidad y hojas de una fila son mejores en los dos esquemas de validación.
- **Brecha entre validación aleatoria y agrupada:** crece con la profundidad, de 0,006 a 0,018 de AUC. Los árboles profundos memorizan las reservas en lote. Aun así, la configuración elegida también es la mejor con reservas nunca vistas.
- **Baseline elegido:** Random Forest sin límite de profundidad, hojas de una fila y 300 árboles.

### Mediciones únicas

Diferencias fold a fold con validación aleatoria, frente al baseline:

| Variante | Δ AUC | Δ accuracy | Conclusión |
|---|---:|---:|---|
| Agregar `assigned_gpu_type` y `queue_wait_time` | +0,0014 | +0,0013 | Excluirlas casi no cuesta rendimiento. Se confirma la exclusión. |
| Quitar `resource_modifications` | −0,0010 | −0,0012 | Aporte chico y consistente, nada desproporcionado. Se conserva. |

## Diagnóstico del baseline (secciones 7 y 8 del notebook)

### Análisis de errores

Se usan las predicciones *out-of-fold* del baseline con validación aleatoria y umbral 0,5.

- **Errores:** 4.423 sobre 38.273 filas. Son 2.827 falsos negativos (17,7 % de las canceladas) y 1.596 falsos positivos (7,2 % de las ejecutadas). Sólo 113 (0,3 %) son inevitables por filas idénticas con etiquetas distintas.
- **Región problemática:** las reservas individuales (sin gemelas) de `cloud_marketplace`.
  - Son el 41 % de las filas y tienen el 77 % de los errores, con 21,4 % de error contra 4,6 % en el resto, y una AUC interna de 0,86.
  - Dentro de la región el error es parejo: ningún subgrupo por tier, GPU, región o anticipación se separa.
  - Casi no hay historial del cliente: 0,9 % con cancelaciones previas, contra 10,9 % en el resto.
- **Cohortes de la consigna:**
  - `client_type`: `cloud_marketplace` tiene el 80 % de los errores.
  - `basic` y `GPU_T4` tienen casi el doble de error que `standard` y `GPU_T1`. La diferencia se explica sobre todo por composición: el 93 % y el 79 % de sus filas son `cloud_marketplace`.
- **Cohortes que casi no se cancelan:** en `independent_client`, `sponsored_project` y `high_priority_partner`, entre el 67 % y el 92 % de las cancelaciones pasa sin aviso.
- **Lotes:** con validación agrupada, el error de los lotes sube de 0,5 %–5 % a 4 %–17 %. Los aciertos dependen de haber visto una gemela.
- **Falsos positivos y falsos negativos:**
  - El 61 % de los errores tiene probabilidad entre 0,3 y 0,7.
  - Los falsos negativos se parecen a las reservas ejecutadas, y los falsos positivos a las canceladas de `cloud_marketplace`.
  - Las probabilidades *out-of-fold* están calibradas.

### Costo de los errores y umbral

Es un análisis del baseline. El umbral final se elige en el paso 5.

| Costo FP : FN | Umbral teórico | Umbral óptimo en desarrollo | Falsos positivos | Falsos negativos | Accuracy |
|---|---:|---:|---:|---:|---:|
| 1 : 1 | 0,50 | 0,48 | 1.757 | 2.650 | 0,885 |
| 2 : 1 | 0,67 | 0,62 | 842 | 3.955 | 0,875 |
| 3 : 1 | 0,75 | 0,68 | 568 | 4.620 | 0,864 |

Los modelos se eligen por AUC y accuracy, sin fijar costos. El umbral es una decisión operativa que se puede cambiar sin reentrenar.

### Curvas de aprendizaje

- **Validación agrupada:** la AUC pasa de 0,919 (3.000 filas) a 0,933 (15.300) y a 0,937 (30.600). El último 25 % sumó 0,0014, menos que el desvío entre folds.
- **Validación aleatoria:** sube más, en parte porque con más entrenamiento hay más gemelas.
- **Diagnóstico (inferencia):** el sistema está limitado por la información de las variables, no por la cantidad de filas ni por la capacidad del modelo. Lo prioritario es agregar información: variables derivadas o datos nuevos.
- **Reentrenamiento del predictor:** decidido el 09/11 reentrenarlo con desarrollo y test juntos, después de la evaluación única en test (sección 12.6).

### Estrategia data-centered (sección 9, consigna 3.3)

Elegida el 08/11: **las reservas individuales de `cloud_marketplace`.**

- **Frecuencia e impacto:**
  - 41 % de las filas y 77 % de los errores.
  - 2.002 falsos negativos (71 % del total) y 1.391 falsos positivos (87 %).
  - Cada punto de error que baje en la región suma 0,41 puntos de accuracy global.
- **Lo que no explica el error:**
  - La falta de filas: la accuracy de la región pasa de 0,784 a 0,786 entre la mitad de los datos y el total.
  - El umbral: el óptimo en la región es 0,48 y gana 0,2 puntos.
- **Causas probables (inferencia):**
  - No hay historial del cliente.
  - No tienen `locked_allocation` ni lote.
  - El modelo se apoya en `special_resource_requests` como señal sustituta.
- **Próximos pasos:**
  - variables derivadas (día de la semana, totales, proporciones y costo total);
  - datos nuevos;
  - métrica de la región en la selección de modelos;
  - gradient boosting.
- **Descartadas:** más filas, un umbral por cohorte, data augmentation o SMOTE, y un modelo separado.

### Adquisición de datos (sección 10, consigna 3.4)

Por prioridad, todos como inferencia:

1. Historial del cliente final, con un identificador estable aunque reserve por un broker. En las reservas únicas con algún historial, la AUC es 0,916, contra 0,876 sin historial.
2. Identificador de lote.
3. Actividad entre la reserva y la ejecución, con fecha, usando sólo la anterior al momento de predecir.
4. Condiciones comerciales.

No se propone conseguir más reservas del mismo tipo.

## Optimización (sección 11 del notebook, consigna 4)

**Regla de adopción**, acordada el 08/11 antes de ver los resultados:
- con diferencias pareadas, la AUC media de la validación aleatoria tiene que mejorar, y en al menos 4 de los 5 folds;
- la AUC media de la validación agrupada no tiene que empeorar.

Cada variante se reporta también con la AUC y el error de la región elegida.

| Estrategia | Resultado | Decisión |
|---|---|---|
| Variables derivadas (calendario, totales, costo, día de la reserva) con Random Forest | Ninguna cumple la regla; todas juntas, −0,0014 de AUC. El día de la reserva sube la accuracy 0,0017, pero la AUC sólo mejora en 3 de 5 folds. | No se adoptan. Son funciones de columnas existentes. |
| Quitar `execution_year` | −0,0014 de AUC en los 5 folds | Se conserva. |
| Gradient boosting por defecto (`HistGradientBoostingClassifier`, categóricas nativas) | −0,0094 de AUC con validación aleatoria; empata con la agrupada | No se adopta solo. |
| Búsqueda aleatoria de 30 combinaciones para gradient boosting | Mejor: 0,9546 de AUC (−0,0011), pero 0,9401 con la agrupada (+0,0026) | Candidato para combinar. |
| Grilla de `max_features` para Random Forest | 0,2: +0,0007 de AUC (5/5), +0,0017 con la agrupada | Se adopta. |
| Promedio 50/50 de Random Forest ajustado y gradient boosting ajustado | Frente a Random Forest ajustado: +0,0012 de AUC (5/5), +0,0026 con la agrupada | Se adopta. Es el promedio simple, sin pesos elegidos con los datos. |
| Random Forest de 100 árboles en lugar de 300 dentro del promedio | AUC 0,9575 contra 0,9576; el archivo pasa de 37 MB a 12 MB | Se adopta, para que el predictor se pueda enviar por mail. |

- **Modelo final:** promedio de Random Forest (100 árboles, sin límite de profundidad, hoja 1, `max_features = 0,2`) y gradient boosting ajustado:
  - `learning_rate` 0,048, `max_leaf_nodes` 127, `min_samples_leaf` 5, `l2_regularization` 0,1, `max_features` 0,5;
  - *early stopping* con un 10 % interno y paciencia de 30 iteraciones.
- **Resultados en desarrollo:** AUC 0,9575, accuracy 0,8862, AUC agrupada 0,9416 y error de la región 21,0 %.
- **XGBoost:** no se prueba. Gradient boosting no superó a Random Forest en la validación principal, el límite es la información y agregaría una dependencia.
- **Stacking:** no se prueba. Las predicciones de los dos modelos tienen una correlación de 0,976.

## Modelo final (sección 12 del notebook, consigna 5)

Decidido el 09/11: se confirma el modelo de la sección 11, se deja fuera XGBoost y se reentrena el predictor con desarrollo y test juntos.

- **Receta única:** la receta del modelo final está en `predictor_v1_Grupo_11.py` (`build_model`, `train`). El notebook comprueba que sus hiperparámetros son los elegidos y que, reentrenada en un fold, reproduce las predicciones evaluadas.
- **Umbral 0,40** (reemplaza al 0,5 del 09/11; ver la actualización del 11/11 al final).
- **Dónde mejoró:**
  - la combinación con gradient boosting aportó más que el ajuste de `max_features` (+0,0011 contra +0,0007 de AUC);
  - la mejora se concentra en las reservas únicas, la región elegida, `independent_client`, `basic` y `GPU_T4`;
  - en las cohortes fáciles casi no cambia, y las reservas en lote empeoran 0,2 puntos de error con validación aleatoria, porque el modelo memoriza menos.
- **Test, evaluado una sola vez:**
  - con umbral 0,40: AUC 0,960 (intervalo *bootstrap* del 95 %: 0,957 a 0,963), balanced accuracy 0,888 (0,881 a 0,894) y accuracy 0,889;
  - frente al baseline, con el mismo umbral, la mejora de AUC se confirma (+0,0013, intervalo de 0,0003 a 0,0023), y la de balanced accuracy no se distingue de cero (+0,0012, de −0,002 a +0,005);
  - sin gemela en desarrollo: AUC 0,889 y balanced accuracy 0,795; con gemela: 1,1 % de error y balanced accuracy 0,988. La región elegida tiene 20,5 % de error.
- **Rendimiento esperado (balanced accuracy):** 0,89 con datos del mismo conjunto de reservas (AUC 0,96), 0,86 con reservas nuevas (validación agrupada, AUC 0,94) y 0,79 con sólo reservas individuales (AUC 0,89).
- **Predictor entregado:**
  - el modelo se entrena con las 47.842 filas y se guarda en `predictor_v1_Grupo_11.joblib` (18,1 MB, compresión zlib nivel 3);
  - no se usa xz, que lo bajaría a 9,5 MB, porque algunas instalaciones de Python no traen `lzma` y el archivo no cargaría;
  - `predictor_v1_Grupo_11.zip` (17,8 MB) se genera desde el notebook y lleva el `.py`, el `.joblib`, `requirements_predictor.txt` (como `requirements.txt`) y `README_predictor.md` (como `README.md`);
  - se probó desde la carpeta descomprimida en un proceso nuevo: da las mismas probabilidades con todos los formatos de entrada y por línea de comandos;
  - si el `.joblib` no carga en otra versión de scikit-learn, se regenera con `python predictor_v1_Grupo_11.py entrenar gpu_resource_reservations.csv`.

## Actualización después del leaderboard de la primera ventana (11/11)

La cátedra publicó el leaderboard de la entrega del 04/11 (reporte del 05/11): 4 de 13 grupos evaluados sobre 10.686 reservas, ordenados por **balanced accuracy**. El mejor grupo tiene balanced accuracy 0,815 y AUC 0,907; el resto, de 0,746 a 0,798 y de 0,836 a 0,898. El grupo 12 tuvo un error de ejecución.

- **Métrica del Model Score:** balanced accuracy, no accuracy. La selección de modelos no cambia, porque se hizo por AUC, que no depende del umbral.
- **Umbral 0,40:** con probabilidades calibradas, el umbral que maximiza la balanced accuracy es la tasa de cancelación del conjunto evaluado (41,7 % en desarrollo, 28,7 % en las reservas únicas). Regla: el menor umbral a menos de 0,001 de la mejor balanced accuracy *out-of-fold* en las dos validaciones (zonas 0,39–0,45 y 0,40–0,44). Frente a 0,5 mejora en los tres escenarios: +0,003 con validación aleatoria, +0,004 con la agrupada y +0,023 en las reservas únicas. En test (sólo para reportar) pasa de 0,882 a 0,888.
- **Supuesto sobre el conjunto de evaluación:** se mantiene que son reservas del mismo período y origen, así que no hace falta un split temporal. **Inferencia:** las AUC del leaderboard (0,84 a 0,91), muy por debajo de la validación aleatoria (0,96) y de nuestra regresión logística (0,913), sugieren que el conjunto de evaluación tiene menos copias del CSV que un split aleatorio. La estimación más realista pasa a ser la de la validación agrupada o la de las reservas únicas. No se puede descartar que los otros modelos sean más débiles.
- **Predictor:** sólo cambia `THRESHOLD` en el `.py`; el `.joblib` es idéntico byte a byte al del 09/11. Se regeneró el `.zip` con el `.py` y el README nuevos.
