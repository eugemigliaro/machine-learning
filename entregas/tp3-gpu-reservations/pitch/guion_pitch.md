# Guion del pitch — TP3 (Grupo 11)

Presentación final de los primeros puestos: 5 minutos de pitch y 5 de preguntas, el 25/11/2026. El Grupo 11 quedó 4.º y presenta a las 16:10 (TOP 5 a las 16:00, un grupo cada 10 minutos). [P05] El anuncio dice "25/10/26"; se toma el 25/11 (ver `wiki/dudas-y-conflictos.md`).

La consigna pide presentar el modelo como un producto, para un público no técnico, y responder cinco preguntas: qué problema resuelve, cómo funciona, quién lo usaría, qué ventajas tiene frente a otras alternativas y cuáles son sus resultados y limitaciones. [P05]

- **Diapositivas:** [artifact de Slides](https://claude.ai/artifact/4UABdmLVR9HBmnkftMbjqC), 8 diapositivas. Fuente versionada en `project/`.
- **Nombre del producto:** "SafeGraphics", elegido por el grupo.
- **Oradores:** dos, A y B.
- **Hilo:** el problema no es cuántas reservas se cancelan sino cuáles; SafeGraphics responde eso cada lunes, mejor que una regla simple, y se propone probarlo con un piloto.

| Diapositiva | Pregunta de la consigna | Orador | Tiempo |
|---|---|:---:|---:|
| 1. SafeGraphics | — | A | 0:15 |
| 2. 423 reservas, 176 se cancelan. ¿Cuáles? | Problema | A | 0:40 |
| 3. Cada lunes, las reservas en riesgo | Cómo funciona | A | 0:40 |
| 4. Aprende señales que un operador ya intuye | Cómo funciona | A | 0:35 |
| 5. Para el equipo que reparte las GPU | Quién lo usa | B | 0:30 |
| 6. Las mismas cancelaciones, un tercio de las falsas alarmas | Ventajas | B | 0:45 |
| 7. Una semana típica con SafeGraphics | Resultados | B | 0:30 |
| 8. Proponemos un piloto | — | B | 0:20 |
| **Total** | | | **4:15** |

A cuenta el problema y qué hace el producto (2:10). B cuenta para quién es, por qué elegirlo, qué logra y el pedido final (2:05).

Las limitaciones no tienen diapositiva propia. En el pitch aparecen las falsas alarmas (diapositivas 3 y 7) y la acción "pedir confirmación, nunca cancelar" (diapositiva 3). Las cuatro limitaciones están preparadas para las preguntas.

## Qué decir en cada diapositiva

### 1. SafeGraphics (A, 0:15)

> Somos el Grupo 11 y les presentamos SafeGraphics: una herramienta que, cada semana, le dice al equipo que reparte las GPU qué reservas probablemente se cancelen.

### 2. 423 reservas, 176 se cancelan. ¿Cuáles? (A, 0:40)

> En una semana típica se programan unas 423 reservas de GPU, y 176 se van a cancelar. El problema no es cuántas: es cuáles. Mientras tanto, cada una tiene una GPU apartada: en la mitad de los casos pasan casi cuatro semanas hasta que el cliente cancela. Y no es poco: son 1,2 millones de dólares por año en reservas que terminan canceladas.

### 3. Cada lunes, las reservas en riesgo (A, 0:40)

> Así se ve. Cada lunes, SafeGraphics toma todas las reservas activas, sin que nadie cargue nada nuevo, y le pone un riesgo a cada una. Estas son seis reservas reales que el modelo no había visto. Las de riesgo alto y medio son alertas, con una acción sugerida. La última columna muestra qué pasó después. La tercera fue una falsa alarma: se marcó y el cliente la usó. Por eso la acción es pedir confirmación, nunca cancelar.

### 4. Aprende señales que un operador ya intuye (A, 0:35)

> ¿Cómo decide? Con señales que cualquiera que opere el sistema reconoce. Quien reserva con medio año de anticipación cancela mucho más que quien reserva para la semana que viene. Quien ya canceló antes vuelve a cancelar casi siempre. Quien pidió recursos especiales está más comprometido. Lo que una persona no puede hacer es combinar decenas de señales para cientos de reservas cada semana. Eso hace SafeGraphics. Le paso la palabra a B.

### 5. Para el equipo que reparte las GPU (B, 0:30)

> ¿Quién lo usa? El equipo de operaciones que reparte las GPU. Ofrece a la lista de espera las GPU de las reservas de riesgo alto, como una aerolínea que vende un asiento de más, pero sabiendo en qué vuelo. Pide confirmación a las de riesgo medio, con tiempo. Y planifica sabiendo cuánta capacidad se va a liberar. La decisión sigue siendo de una persona.

### 6. Las mismas cancelaciones, un tercio de las falsas alarmas (B, 0:45)

> ¿Por qué no alcanza con una regla? Probamos una regla simple, con el corte de anticipación que mejor funciona: marcar toda reserva hecha con más de tres semanas. Detecta 8 de cada 10 cancelaciones, pero molesta a 6 de cada 10 clientes que sí iban a usar su GPU. SafeGraphics detecta las mismas 8 y molesta a 2. Las otras opciones son peores: no hacer nada no detecta ninguna, y marcar sólo a quien ya canceló antes encuentra menos de 2 de cada 10.

### 7. Una semana típica con SafeGraphics (B, 0:30)

> ¿Qué significa en una semana típica? De las 176 cancelaciones, unas 115 todavía tienen la GPU apartada después de la primera semana, y SafeGraphics marca unas 97 de ellas. A cambio, genera unas 45 falsas alarmas entre las casi 250 reservas que sí se usan. Y es rápido: revisa más de 10.000 reservas en 3 segundos.

### 8. Proponemos un piloto (B, 0:20)

> Cerramos con una propuesta concreta: un piloto de cuatro semanas. SafeGraphics corre cada lunes en paralelo, sin tocar ninguna reserva, y al final comparamos sus alertas con lo que realmente se canceló. Si cumple, se usa; si no, no se perdió nada. ¿Preguntas?

## Preguntas probables

| Pregunta | Respuesta |
|---|---|
| ¿Qué limitaciones tiene? | Cuatro. Uno: 1 de cada 3 alertas es una falsa alarma, así que es un aviso para revisar, nunca una cancelación automática. Dos: como revisa una vez por semana, no llega a ver lo que se cancela en los primeros días; esas reservas apartan la GPU poco tiempo. Tres: aprendió de reservas de 2015 a 2017; si el negocio cambia, hay que reentrenarlo. Cuatro: donde más falla es con clientes nuevos sin historial; la mejora más grande es registrar más datos de esos clientes. |
| ¿Qué es "detecta 8 de cada 10"? | De las reservas que terminan canceladas, SafeGraphics marca 8 de cada 10. Es el *recall* (sensibilidad). "Molesta a 2 de cada 10" es la tasa de falsos positivos entre las reservas que se usan. |
| ¿Qué significan Alto, Medio y Bajo? | Son cortes sobre la probabilidad que da el modelo: Alto desde 70 %, Medio entre 29 % y 70 %, Bajo debajo de 29 %. Alto y Medio son alertas: el predictor entregado devuelve 1 desde 29 %. |
| ¿Por qué no marcar menos reservas, para equivocarse menos? | Se puede: es una perilla. Con el corte en 50 % detecta 7 de cada 10 y molesta a 1 de cada 10. Elegimos el punto que equilibra detectar y no molestar, que es lo que mide la competencia (balanced accuracy). |
| ¿Cómo mejoraron entre la primera entrega y la final? | El leaderboard del 11/11 nos mostró dos cosas: que la competencia mide balanced accuracy y que en la entrada vienen la GPU asignada y la espera en cola, que según la cátedra se conocen días antes de la ejecución. Con eso: (1) bajamos el umbral, porque la balanced accuracy se maximiza cerca de la tasa de cancelación, que sin copias repetidas ronda el 30 %; (2) sumamos esas dos columnas y variables de calendario y costo; (3) agregamos cuántas reservas similares hay en el mismo lote y cuántas se cancelaron; (4) hicimos que cada grupo de copias idénticas pese como una sola reserva. En nuestra validación agrupada la balanced accuracy pasó de 0,801 a 0,824. |
| ¿Cómo les fue en la competencia? | Quedamos 4.º entre 13 equipos, evaluados por la cátedra con reservas que no estaban en nuestros datos. No está en las diapositivas: el pitch habla del producto. |
| ¿Qué modelo es? | Cinco modelos de *gradient boosting* (muchos árboles de decisión chicos, cada uno corrigiendo al anterior) promediados. |
| ¿Cómo se midieron los números? | Validación agrupada en 5 partes sobre el CSV de la cátedra: el modelo nunca ve en el entrenamiento una reserva idéntica a las que se evalúan, y cada grupo de copias idénticas cuenta como una reserva. Balanced accuracy 0,824 y AUC 0,907. Si cada copia cuenta por separado, los números mejoran (detecta 9 de cada 10); en el pitch usamos los más conservadores. |
| ¿Por qué "1 de cada 3 alertas falla" si en el ejemplo falló una de seis? | Las seis reservas del ejemplo las elegimos para mostrar cada nivel de riesgo y una falsa alarma; no son una muestra al azar. El número real es el de la validación. |
| ¿De dónde sale USD 1,2 M? | Costo estimado por hora por horas de GPU de cada reserva cancelada, sumado y dividido por los 26 meses del CSV. Es el valor de lo que se canceló, no plata perdida: parte de esas GPU se reasignan igual. |
| ¿Por qué 97 y no 176? | Un tercio de las cancelaciones ocurre en la primera semana después de reservar, muchas antes de la revisión semanal. Las 97 salen de las unas 115 que siguen activas más de una semana. |
| ¿Qué pasa si el negocio cambia? | Hay que volver a entrenar con datos nuevos y medir el acierto semana a semana con las cancelaciones que efectivamente ocurren. El piloto sirve justamente para eso. |
| ¿Qué datos agregarían? | Historial del cliente en la plataforma, un identificador de lote para reservas hechas juntas y actividad del cliente antes de la ejecución (consigna 3.4 del TP). |

## De dónde salen los números

Todos se reproducen con `medir_pitch.py`.

| Dato | Cómo se calcula |
|---|---|
| 423 reservas y 176 cancelaciones por semana | Filas y canceladas del CSV [D04] divididas por las semanas entre la primera y la última fecha de ejecución (julio de 2015 a agosto de 2017). |
| USD 1,2 M por año (43 % del valor reservado) | `estimated_cost_per_hour × total_gpu_hours` de las canceladas, por año. |
| 26 días | Mediana, entre las canceladas, de los días entre la fecha de reserva (ejecución menos `hours_before_execution`, que está en días) y `execution_status_date`. |
| 1 de cada 3 cancelaciones en la primera semana | Canceladas con 7 días o menos entre reserva y cancelación: 34,8 %. |
| Tasas por señal (diapositiva 4) | Tasa de cancelación del CSV por grupo, sin modelo. |
| Reporte de ejemplo (diapositiva 3) | Seis reservas únicas de desarrollo, elegidas a mano para mostrar cada nivel, con su predicción de la validación agrupada. Los cortes Alto/Medio/Bajo (70 % y 29 %) son una decisión de presentación. |
| 8 y 2 de cada 10; regla simple 8 y 6 | Validación agrupada del predictor del 18/11 (`StratifiedGroupKFold(5)` del notebook sobre desarrollo), cada conjunto de copias idénticas pesa como una reserva. Regla: más de 21 días de anticipación, el corte que maximiza la balanced accuracy en cada fold de entrenamiento (20 a 22 días). |
| 1 de cada 3 alertas es falsa | Precisión de 0,66 en la misma validación. |
| ≈97 y ≈45 por semana | Estimación: detección entre las canceladas que siguen activas más de una semana (0,84) por las unas 115 semanales; tasa de falsas alarmas (0,18) por las unas 246 que se ejecutan. |
| 3 s para más de 10.000 reservas | Prueba del paquete del 18/11: 10.686 filas en 2,9 s (`decisiones.md`). |
| Evolución 0,801 → 0,824 entre la primera entrega y la final | `decisiones.md`, sección "Predictor del 18/11". |
