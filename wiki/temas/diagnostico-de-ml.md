# Diagnóstico de modelos de ML

## Para qué sirve

El punto de partida de la clase 11: ya se entrenó, se hizo cross-validation y se eligieron modelo e hiperparámetros, pero el rendimiento no alcanza. ¿Dónde conviene invertir el esfuerzo? [T11, p. 2]

Dos clasificadores con el mismo F1 pueden necesitar intervenciones completamente distintas. Uno puede no tener capacidad para representar la relación `X → Y`; otro, aprender train perfectamente y generalizar mal; otro, discriminar bien pero con un umbral inadecuado; y otro, rendir bien en global y fallar siempre en cierto tipo de observaciones. La métrica final detecta **que** hay un problema, no **cuál** es. [T11, p. 4]

El diagnóstico es una serie de tests para entender qué funciona y qué no en el modelo, y decidir cómo seguir. Es más "artesanal" y lleva tiempo, pero tiene un impacto importante en el resultado final. [T11, p. 17]

## Tres fuentes de error

El training set es una muestra finita de la distribución. Eso introduce tres fuentes de error conceptualmente distintas: [T11, p. 5]

| Fuente | Qué es |
|---|---|
| **Varianza** | Error por aprender de una muestra finita: cambia si se usa otra muestra. |
| **Sesgo** | Error asociado al modelo o hipótesis elegida. |
| **Error irreducible** | Error inherente al problema o a los datos, que no se puede explicar a partir de `X`. |

El primer diagnóstico busca cuál domina. [T11, p. 5] Alto sesgo significa predicciones con un error elevado y consistente (underfitting); alta varianza, un modelo demasiado sensible a los datos de entrenamiento, con predicciones ruidosas (overfitting). [T11, p. 18]

## Baseline y Human Level Performance

Al empezar un proyecto conviene conocer el **Human Level Performance (HLP)**. Ayuda a decidir dónde concentrar el esfuerzo y qué parte del rendimiento es más mejorable. [T11, p. 14]

- En datos **no estructurados** (imágenes, audio, texto) las personas son muy buenas, así que el HLP es un buen baseline.
- En datos **estructurados** (tablas de usuarios o productos) las personas no son tan buenas y el HLP sirve menos. [T11, p. 14]

Cómo obtener una referencia: buscar en la literatura o en proyectos open source (eso además puede dar rápido una primera versión del modelo), o usar el rendimiento de una versión previa. En algunos casos el HLP da una idea del error irreducible. [T11, p. 15]

No conviene plantear un problema y exigir de entrada un 90 %: primero hay que conocer un baseline y el estado del arte o el HLP, y a partir de ahí definir el objetivo. [T11, p. 15]

## Primer paso: ¿aprende al menos train?

Rendir bien en train no es el objetivo final, pero es un buen primer chequeo. Si el rendimiento en train es bajo, esa es la primera limitación: hay **alto sesgo** (underfitting). La combinación de features, clasificadores e hiperparámetros no logra extraer suficiente información de los datos. [T11, p. 7] [T11, p. 12]

Las causas se agrupan en dos: o falta información en `X`, o falta capacidad para extraerla. [T11, p. 8] [T11, p. 12]

| Capacidad insuficiente | Información insuficiente en `X` |
|---|---|
| Modelo demasiado simple o inadecuado. | Features poco informativas. |
| Regularización excesiva o hiperparámetros demasiado restrictivos. | Demasiado ruido respecto de la señal, en `X` **o en `Y`**. |
| Optimización insuficiente (redes neuronales). | Límite intrínseco del problema. |

Fuente de la tabla: [T11, p. 8].

## Segundo paso: ¿generaliza?

Si hay diferencia entre train y validación, hay un **generalization gap**. El modelo extrae información que explica train, pero parte de esa información no está en validación: aprendió algo de ruido. Es **alta varianza** (overfitting): si se repite con varios subconjuntos de datos, el error varía mucho. [T11, p. 10]

| Aprende ruido | Aprende información real que no generaliza |
|---|---|
| Modelo demasiado flexible o complejo. | Distribution shift (cambio de distribución). |
| Alta dimensionalidad: muchas features para pocos datos. | Leakage. |

Fuente de la tabla: [T11, p. 10]. El título de esas diapositivas dice "Overfitting - high bias", pero el texto describe alta varianza; ver [Dudas y conflictos](../dudas-y-conflictos.md). [T11, p. 9] [T11, p. 10]

## Resumen del diagnóstico

El diagrama de la clase parte de un rendimiento insuficiente en validación y pregunta cómo rinde el modelo en entrenamiento: [T11, p. 11]

| Train | Diagnóstico | Causa | Evaluar con | Entonces |
|---|---|---|---|---|
| Bajo | Subajuste | **Información insuficiente**: variables, relación señal-ruido, datos. | Curva de aprendizaje y análisis de la información. | Mejorar variables o recolectar mejores datos. |
| Bajo | Subajuste | **Capacidad insuficiente**: modelo simple o exceso de regularización. | Curva de validación. | Aumentar capacidad o reducir regularización. |
| Alto | Sobreajuste | **Aprende ruido**: modelo demasiado complejo, `N` bajo respecto de `X`. | Curvas de aprendizaje y de validación. | Simplificar, regularizar o reducir dimensionalidad. |
| Alto | Sobreajuste | **Aprende señal que no generaliza**: cambio de dominio, grupos, tiempo, sitio, cámara. | CV por grupos, temporal o por dominio. | Usar una CV acorde al objetivo o recolectar datos del dominio objetivo. |

La última fila conecta con la [validación cruzada avanzada](evaluacion-y-validacion.md#validación-cruzada-avanzada).

## Curvas de validación: sesgo frente a varianza

El ejemplo grafica la precisión (accuracy) de un árbol en función de su profundidad. [T11, p. 19]

- La precisión en **entrenamiento** siempre sube al aumentar la capacidad del algoritmo para aprender fronteras complejas; en el gráfico llega a 1,0.
- La de **validación** es distinta: empieza a bajar cuando el modelo sobreajusta. En el gráfico alcanza su máximo (cerca de 0,90) a profundidad 2–3 y luego cae a alrededor de 0,86. [T11, p. 19]

La zona de poca profundidad es **underfitting**: errores parecidos y altos en train y validación. La de mucha profundidad es **overfitting**: errores distintos, con un gap entre train y validación. [T11, p. 20]

Es la misma lectura de las curvas de validación de la clase de árboles. [T07, p. 50] Ver [Árboles de decisión](arboles-de-decision.md).

## Curvas de aprendizaje

Una curva de aprendizaje muestra cómo cambia el rendimiento en función del **tamaño del set de entrenamiento**. [T11, p. 21]

| Patrón | Forma de las curvas | Diagnóstico |
|---|---|---|
| Precisión baja | La de entrenamiento baja y la de validación sube hasta que **convergen en un valor bajo**. | Underfitting. |
| Gap entre ambas | Entrenamiento alta y validación más baja; la de validación **sigue subiendo** al agregar datos. | Overfitting. |

Fuentes de la tabla: [T11, p. 21] [T11, p. 22]. En la versión con overfitting, la diapositiva prolonga ambas curvas con líneas punteadas que tienden a acercarse: con más datos, el gap se seguiría cerrando. [T11, p. 23]

**Inferencia:** si las curvas ya convergieron, más datos del mismo tipo no van a ayudar; hay que mejorar las features o la capacidad del modelo. Es la pregunta 3.2 del [TP3: optimización](tp3-optimizacion.md): ¿el sistema está limitado por el modelo o por los datos? [P03, p. 2]

## Qué hacer según el diagnóstico

Ante un rendimiento insatisfactorio, las estrategias habituales son conseguir más datos, usar menos características, agregar características (o variaciones de ellas) y cambiar los hiperparámetros para que sean más o menos restrictivos. La pregunta es cuál conviene en cada caso. [T11, p. 16]

| Acción | Cuándo sirve |
|---|---|
| Conseguir más datos de entrenamiento | La curva de aprendizaje muestra train y validación todavía lejos (overfitting), pero siguen cambiando al agregar datos. |
| Usar menos features | Hay signos de overfitting: quitar features reduce los patrones que el modelo puede sobreajustar. |
| Agregar features | Hay underfitting: el modelo tiene más con qué aprender. |
| Combinar features | Hay underfitting, por la misma razón. |
| Hiperparámetros más restrictivos | Hay overfitting. |

Fuente de la tabla: [T11, p. 24].

## Conexiones

- [Regresión, complejidad y generalización](regresion-y-generalizacion.md): underfitting y overfitting.
- [Evaluación y validación](evaluacion-y-validacion.md): curvas de validación y validación cruzada avanzada.
- [Diseño centrado en datos y análisis de errores](data-centric-y-analisis-de-errores.md): qué hacer después del diagnóstico.
- [Gradient boosting y combinación de modelos](gradient-boosting-y-combinacion.md): boosting ataca el sesgo; bagging, la varianza. [T12, p. 6] [T12, p. 20] [T12, p. 21]
- [TP3: optimización de modelos](tp3-optimizacion.md)
