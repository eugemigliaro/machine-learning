# MLOps, despliegue y monitoreo

## Del proyecto al producto

El pipeline clásico de un proyecto, según la clase 12: [T12, p. 30]

1. Definición del problema.
2. Recolección de datos.
3. Data splitting: train, validación y test.
4. Limpieza: faltantes, outliers, inconsistencias.
5. EDA: distribuciones, correlaciones, primeros insights.
6. Feature engineering y selección.
7. Modelado.
8. Regularización: control del overfitting.
9. Evaluación en dev con métricas.
10. Iteración: si el resultado no es bueno, volver a mejorar.
11. Selección del modelo y evaluación final en test.

**MLOps** (*ML Operations*) es una disciplina que reúne herramientas y conceptos para todo el ciclo de vida de un proyecto de ML, sobre todo en datos, modelado y despliegue. Establece formas sistemáticas de encararlos. [T12, p. 32]

La motivación: no alcanza con entrenar el algoritmo; hay que ponerlo en producción, monitorearlo y mantenerlo funcionando. Haber hecho un deploy permite entender el ciclo de vida completo. [T12, p. 33]

El código de ML es una parte chica de la aplicación final. Alrededor hay configuración, recolección y verificación de datos, extracción de features, gestión de recursos, herramientas de análisis y de procesos, infraestructura de serving y monitoreo. La prueba de concepto del notebook todavía necesita mucho código para llegar a producción: es el **POC to Production Gap**. [T12, p. 34]

## Ciclo de vida

| Etapa | Qué incluye |
|---|---|
| **Scoping** | Definir el proyecto, objetivos, alcance y etapas; prioridades y errores que no se pueden cometer; cómo interactuará con otros sistemas y qué datos verá el sistema final. [T12, p. 37] |
| **Data** | Datos y etiquetas consistentes. En datasets online los datos suelen venir listos; en la realidad hay mucho trabajo para mejorar o al menos chequear su calidad (por ejemplo, normalizar el volumen de los audios o el brillo de las imágenes). [T12, p. 37] |
| **Modeling** | Modelo, hiperparámetros y datos forman el sistema. Análisis de errores: dónde falla el modelo, cómo mejorar los datos y qué datos recolectar si se graban más. [T12, p. 38] |
| **Deploy** | Implementar el modelo para que funcione en tiempo real: software y transformación de los datos. Comprobar que los datos sean comparables a los del diseño (data drift y concept drift). [T12, p. 39] |
| **Monitoreo y mantenimiento** | Evaluar periódicamente métricas para ver si el modelo funciona igual que en el diseño y detectar errores inesperados. [T12, p. 39] |

En el diseño centrado en datos, el ciclo vuelve de *Modeling* a *Data*. [T12, p. 36] Ver [Diseño centrado en datos](data-centric-y-analisis-de-errores.md).

## Data drift y concept drift

| | Qué cambia | Ejemplos |
|---|---|---|
| **Data drift** | La distribución de `x`: el sistema ve datos distintos de los esperados. | Cambios de iluminación en fotos de usuarios; en reconocimiento de voz, cambios lentos en el lenguaje o en la calidad de los micrófonos. [T12, p. 40] |
| **Concept drift** | La relación `x → y`: cambia el comportamiento que se modela. | Con el Covid-19, gente que nunca compraba online empezó a comprar mucho y los sistemas antifraude detectaron fraudes erróneamente; hubo que reentrenarlos. [T12, p. 41] |

Ambos se controlan durante y después del deploy. [T12, p. 41] La clase 11 los relaciona con los "buenos datos": la relación train–deployment debe mantenerse. [T11, p. 65]

## Despliegue

Desplegar son dos tareas: el software del deploy, y el mantenimiento y monitoreo para detectar drifts. [T12, p. 43]

Casos típicos: un producto o servicio nuevo (empezar con poco tráfico), automatizar o asistir una tarea manual (ideal para shadow mode) y reemplazar un sistema de ML anterior. Comparten dos ideas: **crecer el tráfico gradualmente con monitoreo** y poder hacer **rollback** al modelo anterior si algo falla. [T12, p. 44]

| Patrón | Cómo funciona | Cuándo |
|---|---|---|
| **Shadow mode** | El sistema corre en paralelo con el trabajo humano y su salida no se usa para decidir. Permite verificar si funcionaría bien. | Asistir o automatizar una tarea humana, como detectar piezas defectuosas. [T12, p. 45] |
| **Canary** | Usar una fracción chica del tráfico (por ejemplo 5 %), monitorear e ir aumentando. Si hay un error, el impacto es mínimo. El nombre viene del canario que llevaban los mineros para detectar gas. | Cuando el algoritmo ya puede decidir solo. [T12, p. 46] |
| **Blue-green** | Las entradas van al azar a la versión vieja (*blue*) o a la nueva (*green*). Permite medir la mejora, hacer rollback fácil y aumentar gradualmente lo que va a *green*. | Reemplazar una versión. [T12, p. 47] |

### Grados de automatización

El deployment no es un salto de 0 a 1 sino gradual: (1) humano solo, (2) shadow mode, (3) asistencia de IA, (4) automatización parcial y (5) automatización total. No siempre hay que llegar a la automatización total: el sistema puede quedarse en un punto *human in the loop*, como la asistencia o la automatización parcial. [T12, p. 48]

### Del notebook al predictor

Para simular un escenario cercano a producción se escribe código que se ejecuta externamente, una función `predictor(X)` que devuelve `y_pred`. Debe: [T12, p. 49]

- recibir los datos;
- aplicar el preprocesamiento (por ejemplo, escalar con la media y el desvío **de train**);
- contener el modelo entrenado;
- producir predicciones;
- funcionar de forma independiente, sin acceso al notebook;
- no usar labels, no reentrenar el modelo adentro y no usar variables globales del notebook.

En ML real, entrenamiento e inferencia son etapas muy diferenciadas: el entrenamiento ocurre una vez y la inferencia ocurre de forma continua, sobre datos nuevos y en un entorno externo. El modelo solo es útil si generaliza y puede ejecutarse fuera e integrarse en un pipeline real: "lo importante ocurre fuera del notebook". [T12, p. 50] Es el entregable de la competencia del [TP3: optimización](tp3-optimizacion.md#el-predictor).

## Monitoreo

El primer paso es una lluvia de ideas de métricas: qué puede salir mal y qué estadísticas ayudarían a detectarlo. Las métricas dependen del problema, así que hay que dedicarle tiempo. Se puede empezar con muchas e ir quitando las que no sirvan. [T12, p. 52]

| Tipo | Ejemplos |
|---|---|
| **Software** | Memoria, latencia, carga del servidor. |
| **Entrada (`x`)** | Longitud o volumen promedio del audio, brillo promedio de las imágenes, cantidad de valores faltantes. |
| **Salida (`y`)** | Veces que el modelo devuelve null; veces que el usuario repite la búsqueda o abandona la voz para escribir la misma consulta. |

Fuente de la tabla: [T12, p. 53].

Algunas métricas se reducen a **umbrales con alarmas**: no se miran todo el tiempo, solo avisan si se cruzan. Pueden ser superiores, inferiores o ambos, y quizás haya que adaptarlos con el tiempo (por ejemplo, carga de software demasiado alta o accuracy demasiado baja). [T12, p. 54]

Con dos sistemas de ML en serie (detector de voz y luego reconocimiento del habla; o clickstream → perfil de usuario → recomendador), un cambio en el primero se propaga al segundo. Ahí importan aún más las métricas bien elegidas, incluidas las intermedias entre sistemas. [T12, p. 56]

La velocidad de cambio varía: los datos de usuarios suelen cambiar lento, porque la suma de decisiones individuales no cambia de golpe (con excepciones como el Covid). En algunos negocios los datos pueden cambiar bruscamente, porque dependen de decisiones de empresas. [T12, p. 57]

## Mantenimiento

- **Manual:** un equipo de ML engineers reentrena el modelo para resolver el problema. Es el método más usado.
- **Automático:** a partir del análisis de errores, reentrenar automáticamente para atacar debilidades y drifts, con alarmas para los casos más importantes. [T12, p. 55]

## Mensaje final

Construir un modelo no es lo mismo que crear un producto. Los sistemas de IA reales funcionan cuando modelos, datos, infraestructura, despliegue, monitoreo y trabajo humano se diseñan en conjunto. [T12, p. 58]

## Conexiones

- [Fundamentos](fundamentos.md): estructura general de un proyecto.
- [Diseño centrado en datos y análisis de errores](data-centric-y-analisis-de-errores.md)
- [Evaluación y validación](evaluacion-y-validacion.md): elegir el split según el uso en deployment.
- [TP3: optimización de modelos](tp3-optimizacion.md): la función predictora.
