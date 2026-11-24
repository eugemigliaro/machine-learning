# Guion del pitch — TP3 (Grupo 11)

Presentación final de los primeros puestos: 5 minutos de pitch y 5 de preguntas, el 25/11/2026. El Grupo 11 quedó 4.º y presenta a las 16:10 (TOP 5 a las 16:00, un grupo cada 10 minutos). [P05] El anuncio dice "25/10/26"; se toma el 25/11 (ver `wiki/dudas-y-conflictos.md`).

La consigna pide presentar el modelo como un producto, para un público no técnico, y responder cinco preguntas: qué problema resuelve, cómo funciona, quién lo usaría, qué ventajas tiene frente a otras alternativas y cuáles son sus resultados y limitaciones. [P05]

- **Diapositivas:** [artifact de Slides](https://claude.ai/artifact/4UABdmLVR9HBmnkftMbjqC), 9 diapositivas. Fuente versionada en `project/`.
- **Nombre del producto:** "SafeGraphics", elegido por el grupo.
- **Oradores:** dos, A y B.

| Diapositiva | Pregunta de la consigna | Orador | Tiempo |
|---|---|:---:|---:|
| 1. SafeGraphics | — | A | 0:15 |
| 2. Muchas GPU reservadas nunca se usan | Problema | A | 0:40 |
| 3. Una revisión por semana | Cómo funciona | A | 0:35 |
| 4. Combina señales que un operador ya intuye | Cómo funciona | A | 0:40 |
| 5. El equipo que planifica la capacidad | Quién lo usa | B | 0:35 |
| 6. Frente a las alternativas | Ventajas | B | 0:45 |
| 7. Resultados | Resultados | B | 0:30 |
| 8. Lo que SafeGraphics no hace | Limitaciones | B | 0:40 |
| 9. Cierre | — | B | 0:15 |
| **Total** | | | **4:55** |

A cuenta el problema y el producto (2:10). B cuenta para quién es, por qué elegirlo y sus límites (2:45).

## Qué decir en cada diapositiva

### 1. SafeGraphics (A, 0:15)

> Somos el Grupo 11. Les presentamos SafeGraphics: una herramienta que avisa, cada semana, qué reservas de GPU se van a cancelar antes de que pase.

### 2. Muchas GPU reservadas nunca se usan (A, 0:40)

> En los datos que recibimos, 4 de cada 10 reservas de GPU se cancelaron antes de ejecutarse. Esas reservas sumaban el 43 % de las horas de GPU pedidas. El problema no es que la gente cancele: es enterarse tarde. Mientras la reserva existe, esa GPU no se le ofrece a nadie más.

### 3. Una revisión por semana (A, 0:35)

> Funciona como una revisión semanal. Toma todas las reservas activas, tal como ya están cargadas. Las compara con lo que pasó en casi 48 mil reservas anteriores. Y devuelve una lista: cuáles tienen riesgo de cancelarse. Tarda segundos y no hay que reentrenarlo cada semana.

### 4. Combina señales que un operador ya intuye (A, 0:40)

> No es magia. Quien reserva con más de medio año de anticipación cancela el 62 % de las veces; quien reserva para la semana que viene, el 13 %. Quien ya canceló antes vuelve a cancelar en el 93 % de los casos. Quien pidió recursos especiales cancela menos. Ninguna señal alcanza sola: el modelo pesa decenas a la vez, para miles de reservas. Le paso la palabra a B.

### 5. El equipo que planifica la capacidad (B, 0:35)

> Lo usa el equipo de operaciones que reparte las GPU. Con la lista puede sobreasignar con criterio, como una aerolínea que vende algún asiento de más pero sabiendo en qué vuelos; pedir confirmación sólo a quien tiene riesgo, y con tiempo; y planificar la lista de espera. La decisión sigue siendo de una persona: SafeGraphics le dice dónde mirar.

### 6. Frente a las alternativas (B, 0:45)

> ¿Por qué no alcanza una regla? Si no hacemos nada, no detectamos ninguna cancelación. Si marcamos a quien ya canceló antes, acertamos, pero encontramos menos de 1 de cada 20. Si marcamos todo lo reservado con más de tres semanas, encontramos 8 de cada 10, pero también marcamos a 6 de cada 10 clientes que sí iban a usar la GPU. SafeGraphics encuentra las mismas 8 de cada 10 y marca por error a 2 de cada 10.

### 7. Resultados (B, 0:30)

> Lo probamos dos veces. La cátedra lo evaluó con reservas que nunca vimos y quedamos cuartos entre 13 equipos. Y con reservas que el modelo no usó para aprender, detecta 8 de cada 10 cancelaciones, y 7 de cada 10 alertas son cancelaciones reales.

### 8. Lo que SafeGraphics no hace (B, 0:40)

> Tres límites. Uno: se equivoca; unas 3 de cada 10 alertas son reservas que sí se ejecutan, así que es un aviso para revisar, no una cancelación automática. Dos: aprendió de reservas de 2015 a 2017; si cambia el negocio, hay que reentrenarlo y controlar que siga acertando. Tres: donde más falla es con clientes nuevos que reservan solos, sin historial. La mejora más grande no es un modelo más complejo: es registrar más datos de esos clientes.

### 9. Cierre (B, 0:15)

> SafeGraphics: menos GPU bloqueadas por reservas que no van a ocurrir. Ya funciona, procesa la semana en segundos. ¿Preguntas?

## Preguntas probables

| Pregunta | Respuesta |
|---|---|
| ¿Qué es "detectar 8 de cada 10"? | De las reservas que terminan canceladas, el modelo marca 8 de cada 10 antes de que pase. Es el *recall* (sensibilidad). |
| ¿Por qué no marcar menos reservas, para equivocarse menos? | Se puede: es una perilla. Con el umbral de 0,5 detecta 7 de cada 10 y 3 de cada 4 alertas aciertan. Elegimos el punto que equilibra detectar y no molestar, que es lo que mide la competencia (balanced accuracy). |
| ¿Cómo mejoraron entre la primera entrega y la final? | El leaderboard del 11/11 nos mostró dos cosas: que la competencia mide balanced accuracy y que en la entrada vienen la GPU asignada y la espera en cola, que según la cátedra se conocen días antes de la ejecución. Con eso: (1) bajamos el umbral, porque la balanced accuracy se maximiza cerca de la tasa de cancelación, que sin copias repetidas ronda el 30 %; (2) sumamos esas dos columnas y variables de calendario y costo; (3) agregamos cuántas reservas similares hay en el mismo lote y cuántas se cancelaron; (4) hicimos que cada grupo de copias idénticas pese como una sola reserva. En nuestra validación agrupada la balanced accuracy pasó de 0,801 a 0,824. |
| ¿Qué modelo es? | Cinco modelos de *gradient boosting* (muchos árboles de decisión chicos, cada uno corrigiendo al anterior) promediados. |
| ¿Por qué 7 de cada 10 alertas aciertan y no más? | Depende de cuántas reservas se cancelan. Con menos cancelaciones, la misma herramienta tendría más falsas alarmas por cada acierto. |
| ¿Cómo se midieron los números? | Validación agrupada en 5 partes sobre el CSV de la cátedra: el modelo nunca ve en el entrenamiento una reserva idéntica a las que se evalúan. Balanced accuracy 0,824 y AUC 0,907. |
| ¿Qué pasa si el negocio cambia? | Hay que volver a entrenar con datos nuevos y medir el acierto semana a semana con las cancelaciones que efectivamente ocurren. |
| ¿Qué datos agregarían? | Historial del cliente en la plataforma, un identificador de lote para reservas hechas juntas y actividad del cliente antes de la ejecución (consigna 3.4 del TP). |

## De dónde salen los números

| Dato | Fuente |
|---|---|
| 47.842 reservas, 41,7 % canceladas, 43 % de las horas de GPU (`peak_gpu_hours` + `offpeak_gpu_hours`) en reservas canceladas, período 2015 a 2017 | CSV de la cátedra [D04] |
| Tasas por anticipación (`hours_before_execution`, que está en días), cancelaciones previas y pedidos especiales | CSV de la cátedra [D04], sin modelo |
| Detecta 0,831; especificidad 0,816; precisión 0,661; balanced accuracy 0,824; AUC 0,907 | `medir_pitch.py`: predictor del 18/11, `StratifiedGroupKFold(5)` del notebook sobre desarrollo, cada conjunto de filas idénticas pesa como una reserva |
| Reglas simples (regla de anticipación con corte elegido en el fold de entrenamiento: 20 a 22 días) | `medir_pitch.py`, misma validación |
| 4.º de 13 | Leaderboard final, informado por el estudiante; [P05] anuncia que el leaderboard está publicado |
| Evolución 0,801 → 0,824 entre la primera entrega y la final | `decisiones.md`, sección "Predictor del 18/11" |

Las tasas por señal (diapositiva 4) cuentan todas las filas del CSV. La tabla de alternativas y los resultados (diapositivas 6 a 8) pesan cada conjunto de copias como una reserva, para medir reservas nuevas; con ese peso se cancela el 30 %, no el 41,7 %.
