# TP3: optimización de modelos y competencia

## Datos administrativos

- Materia 72.75, ciclo 2026 Q2.
- Defensas: 11/11/2026 y 18/11/2026.
- Presentación: 10 minutos y 10 minutos de preguntas.
- Enviar la presentación, el predictor y el código 24 horas antes de la clase de defensa. [P03, p. 1] El anuncio del Campus lo dice como "el día anterior a la defensa de cada grupo". [P04]

### Entregables

- **Función predictora**, que se usa para evaluar el modelo en la competencia. Debe correr de forma independiente, recibir un `X` con las dimensiones del dataset y devolver la predicción `y`. [P04] [T12, p. 2]
- **Notebook y presentación (PPT)**, con el formato habitual de los TPs. [P04] [T12, p. 2]
- La función se envía por mail con el nombre `predictor_v1_Grupo_X()`, donde `X` es el número de grupo. [P03, p. 3]

## Competencia

- Hay tres oportunidades para enviar el predictor: **04/11, 11/11 y 18/11, siempre antes de las 16:00**. El leaderboard se actualiza después de cada una. [P04] [T12, p. 2]
- Cada grupo puede enviar una sola vez (en la fecha de su defensa) o las tres veces. Para la competencia cuenta la **última** submission. [P04]
- `Competition Score = 90 % × Model Score (submission del 18/11) + 10 % × nota de presentación`. [P04] [T12, p. 2]
- Quedan **eximidos del examen final de diciembre** el TOP 1 por Model Score (mejor rendimiento predictivo) y el TOP 4 por Competition Score. Como condición, deben hacer una presentación breve el **25/11**, último día de clase, con una explicación técnica y otra no técnica. [P04] [T12, p. 2]

El material no dice con qué métrica se calcula el Model Score; ver [Dudas y conflictos](../dudas-y-conflictos.md).

## Dataset

Reservas de infraestructura GPU en un entorno de cómputo distribuido. El objetivo es predecir si una reserva **se cancelará antes de su ejecución** (`canceled_job`). Incluye características temporales de la reserva, recursos solicitados, historial del cliente, duración y complejidad del workload, y aspectos económicos y contractuales. [P03, p. 1] El archivo está en la carpeta Competición del Campus, registrado aquí como D04. [P03, p. 1] [P04]

### Diccionario de variables

| Grupo | Variables |
|---|---|
| Objetivo | `canceled_job`: si la reserva fue cancelada o no llegó a ejecutarse. |
| Tiempo | `hours_before_execution` (horas entre la creación de la reserva y el inicio programado); `execution_year`, `execution_month`, `execution_week`, `execution_day` (fecha programada de inicio). |
| Recursos y workload | `peak_gpu_hours`, `offpeak_gpu_hours` (horas GPU en alta y baja demanda); `num_primary_processes`, `num_auxiliary_processes`, `num_background_processes`; `reserved_gpu_type` (GPU pedida); `assigned_gpu_type` (GPU **finalmente** asignada); `workload_profile`; `reserved_storage_units`; `special_resource_requests`. |
| Cliente | `client_region`, `client_type`, `request_channel`, `returning_client`, `previous_job_cancellations`, `successful_previous_jobs`, `organization_id`. |
| Reserva y contrato | `service_tier`, `resource_modifications`, `reservation_commitment`, `orchestration_agent_id`, `queue_wait_time` (espera en cola antes de la asignación definitiva), `estimated_cost_per_hour` (USD por hora). |

Fuente de la tabla: [P03, p. 4] [P03, p. 5].

### Perfil del archivo

**Observaciones propias** sobre D04, calculadas con pandas el 2026-11-02; no son afirmaciones de la cátedra.

| Aspecto | Observación |
|---|---|
| Tamaño | 47.842 filas y 34 columnas. [D04] |
| Balance | 41,7 % de reservas canceladas (19.955) y 58,3 % no canceladas (27.887). [D04] |
| Período | Fechas de ejecución entre el 01/07/2015 y el 31/08/2017. [D04] |
| Faltantes | `organization_id` falta en 45.540 filas (95 %); `orchestration_agent_id` en 5.035 (10,5 %); `client_region` en 20; `num_auxiliary_processes` en 1. [D04] |
| Duplicados | 15.786 filas son copias exactas de otra fila (33 %). [D04] |
| Cardinalidad | `client_region` tiene 149 valores; `orchestration_agent_id`, 194; `organization_id`, 175. `client_type` y `request_channel` tienen una categoría `unknown` con una sola fila. [D04] |
| Señales fuertes | `reservation_commitment = locked_allocation` (7.876 filas) se cancela en el 99,8 % de los casos, frente al 30,3 % de `no_commitment`. Por tipo de cliente, la tasa va del 11 % (`sponsored_project`) al 68 % (`research_consortium`). [D04] |

### Columnas fuera del diccionario y leakage

El CSV trae cinco columnas que la consigna no documenta: `execution_status`, `execution_status_date`, `total_processes`, `total_gpu_hours` y `high_value_client`. [D04] [P03, p. 4] [P03, p. 5]

- **`execution_status` determina el objetivo:** `canceled` y `no_show` coinciden siempre con `canceled_job = 1`, y `completed` con `0`. [D04]
- **`execution_status_date` también:** en las canceladas cae antes de la fecha de ejecución o ese mismo día (en promedio, 90 días antes); en las completadas, en esa fecha o después; en los `no_show`, siempre el mismo día. [D04]
- `total_processes` es la suma de los tres conteos de procesos, y `total_gpu_hours` la suma de horas peak y off-peak. `high_value_client` no tiene definición; se asocia con un costo por hora más alto. [D04]

**Inferencia:** como el objetivo es predecir la cancelación **antes** de la ejecución [P03, p. 1], `execution_status` y su fecha son información del futuro y deben excluirse. Es el mismo criterio que `duration` en el TP2. [D03] Otras variables merecen discusión por su definición: `assigned_gpu_type` es la GPU "finalmente" asignada, y `queue_wait_time` mide la espera "antes de la asignación definitiva". [P03, p. 5] En D04, las reservas con GPU asignada distinta de la pedida (9,1 %) se cancelan solo en un 6,1 %, frente al 45,3 % del resto: es una señal fuerte que podría reflejar algo que se conoce recién al ejecutar. [D04] Justificar la decisión, como pide la consigna. [P03, p. 1]

No está claro qué columnas recibirá el predictor en la evaluación; ver [Dudas y conflictos](../dudas-y-conflictos.md).

## Entregables por sección

1. **Preprocesamiento y EDA.** No es el foco, pero suma aplicar y mencionar limpieza, tratamiento de faltantes, encoding de categóricas, escalado, análisis exploratorio y análisis de cohortes o subgrupos. Se puede eliminar, seleccionar, combinar o transformar features o datos, siempre justificando. Separar train y test **antes** de cualquier técnica que pueda producir leakage. [P03, p. 1]
2. **Model-centered ML.** [P03, p. 2]
   - 2.1 *Baseline:* implementar con scikit-learn al menos un clasificador visto en clase, con una calibración breve de hiperparámetros.
   - 2.2 *Validación cruzada:* k-fold usando solo el conjunto de entrenamiento.
   - 2.3 *Métricas:* elegir y justificar dos métricas vistas en clase, y usarlas para comparar modelos, elegir hiperparámetros y decidir el baseline final.
3. **Error analysis y enfoque data-centered.** [P03, p. 2] [P03, p. 3]
   - 3.1 *Análisis de errores* sobre el mejor baseline: definir cohortes relevantes (en particular `client_type`, `service_tier` y `reserved_gpu_type`), analizar por cohorte, estudiar falsos positivos y falsos negativos, e identificar regiones problemáticas.
   - 3.2 *Curvas de aprendizaje:* ¿el sistema está limitado por el modelo o por los datos? ¿Más datos mejorarían mucho el rendimiento?
   - 3.3 *Estrategia data-centered:* elegir una cohorte problemática o prometedora y justificar por qué intervenir ahí: frecuencia del problema, impacto operativo, posibles causas y próximos pasos.
   - 3.4 *Adquisición de datos:* qué datos adicionales se incorporarían y por qué mejorarían el sistema.
4. **Optimización.** Explorar al menos **dos** estrategias de mejora entre feature engineering y selección, model selection (RF, SVM, gradient boosting…), optimización de hiperparámetros, ensembles (bagging, boosting, voting, stacking) y mejoras data-centered (desbalance, selección de ejemplos, datos adicionales). Para cada una: justificarla, preferentemente con los análisis anteriores; evaluarla con una validación consistente; y compararla con el baseline. [P03, p. 3]
5. **Modelo final.** Documentar la estrategia elegida, estimar el rendimiento esperado en datos nuevos y discutir qué cambios mejoraron más y si esas mejoras fueron globales o propias de ciertos subgrupos. Enviar la función predictora. [P03, p. 3]

## Mapa consigna → teoría

| Punto | Material de referencia |
|---|---|
| 1 y 2.2 | [Evaluación y validación](evaluacion-y-validacion.md): leakage, k-fold y validación avanzada. |
| 2.1 | [Árboles](arboles-de-decision.md), [Random Forest](ensambles-random-forest.md), [máquinas de vectores de soporte](svm.md), [kNN](aprendizaje-basado-en-instancias.md), [Naive Bayes](gda-y-naive-bayes.md), [regresión logística](regresion-logistica.md). |
| 2.3 | [Métricas de clasificación](metricas-de-clasificacion.md). |
| 3.1, 3.3, 3.4 | [Diseño centrado en datos y análisis de errores](data-centric-y-analisis-de-errores.md). |
| 3.2 | [Diagnóstico de modelos](diagnostico-de-ml.md#curvas-de-aprendizaje). |
| 4 | [Gradient boosting y combinación de modelos](gradient-boosting-y-combinacion.md), [EDA y selección](eda-y-seleccion.md). |
| 5 y predictor | [MLOps y despliegue](mlops-y-despliegue.md#del-notebook-al-predictor). |

## Controles conceptuales

### El predictor

La función debe recibir los datos, aplicar el preprocesamiento con los parámetros aprendidos en train, contener el modelo ya entrenado y producir predicciones. Debe funcionar sin el notebook, sin usar labels, sin reentrenar y sin variables globales. [T12, p. 49] **Inferencia operativa:** conviene guardar un único pipeline (preprocesamiento y modelo) ya ajustado y probar la función en un proceso nuevo con filas crudas del CSV, incluidas categorías no vistas y faltantes, antes de cada envío.

### Validación

- Usar k-fold solo con train y reservar test para la estimación final. [P03, p. 2] [T02, p. 89]
- Con clases desbalanceadas conviene la k-fold **estratificada**. [T11, p. 74] Con 41,7 % de positivos el desbalance es moderado. [D04]
- La relación train–validación debe ser la misma que habrá entre train y test o deployment. [T11, p. 71] [T11, p. 72] **Inferencia:** el dataset abarca dos años y tiene identificadores de organización y de agente. [D04] Si la competencia evalúa sobre reservas de otro período u otros clientes, una validación temporal o por grupos estimaría mejor el Model Score que una aleatoria. [T11, p. 79] [T11, p. 81] El material no dice cómo se armó el conjunto de evaluación.
- **Inferencia:** con un tercio de filas duplicadas, una k-fold aleatoria pone copias idénticas en train y en validación, y eso puede inflar la estimación. [D04] [T11, p. 53] Vale la pena medirlo y discutirlo.

### Métricas

Se eligen dos métricas vistas en clase y se justifican. [P03, p. 2] **Inferencia:** el costo de un falso positivo (prever una cancelación que no ocurre) y de un falso negativo (no prever una que ocurre) depende del uso operativo de la predicción. Como 3.3 pide discutir el impacto operativo, conviene que las métricas salgan de ese análisis. [P03, p. 3] Ver [Métricas de clasificación](metricas-de-clasificacion.md).

### Mejoras sin leakage

- La aumentación de datos y el remuestreo tipo SMOTE se aplican solo al train de cada fold; validación y test quedan con datos reales. [T11, p. 56] [T11, p. 60] [T11, p. 61]
- En stacking, el meta-modelo se entrena con predicciones out-of-fold, nunca con predicciones sobre el propio training. [T12, p. 24] [T12, p. 25]
- Las curvas de aprendizaje y de validación se leen con la guía de la clase 11: si train ya es bajo, faltan información o capacidad; si hay gap, sobra varianza. [T11, p. 11] [T11, p. 24]

## Relación con el TP2

El flujo se mantiene: EDA con decisiones, separación temprana de test, k-fold solo con train, dos métricas justificadas y una estimación final. [P02, p. 1] [P02, p. 2] [P03, p. 1] [P03, p. 2] El TP3 agrega el análisis de errores por cohortes, las curvas de aprendizaje, un ciclo data-centered, al menos dos estrategias de mejora y un predictor que se ejecuta fuera del notebook. [P03, p. 2] [P03, p. 3] Ver [TP2: clasificación supervisada](tp2-clasificacion.md).
