# Diseño centrado en datos y análisis de errores

## Model-centric frente a data-centric

| Diseño centrado en el modelo | Diseño centrado en los datos |
|---|---|
| Dados unos datos, buscar el modelo y los hiperparámetros que mejor funcionan. | Fijar un modelo que se sabe que funciona razonablemente bien. |
| Mantener los datos fijos y mejorar el modelo iterativamente. | Aumentar la calidad o la cantidad de los datos, lo que incluye **agregar features**. |

Fuente de la tabla: [T11, p. 31].

El bucle de iteración cambia en el tercer paso: [T11, p. 43]

| Model-centric | Data-centric |
|---|---|
| 1. Entrenar. | 1. Entrenar. |
| 2. Evaluar. | 2. Evaluar con **análisis de errores**. |
| 3. Aplicar cambios al modelo. | 3. Agregar, mejorar o modificar los datos. |
| 4. Volver a 1. | 4. Volver a 1. |

Para muchas aplicaciones, el bucle de datos es más efectivo y mejora más rápido que el de modelo, **siempre que se use una búsqueda de hiperparámetros y un clasificador robusto**. [T11, p. 43] En investigación suele trabajarse en modo model-centric, con datasets predefinidos y estandarizados; en producción suele ser más efectivo dejar el modelo fijo y optimizar datos e hiperparámetros. [T12, p. 38] En el ciclo de vida del proyecto, el enfoque data-centric agrega una flecha que vuelve de *Modeling* a *Data*. [T12, p. 35] [T12, p. 36]

Si no hay HLP disponible, el análisis de errores es más difícil. Se puede buscar en papers o problemas similares features útiles: **agregar features también es agregar datos**. [T11, p. 43]

## Análisis de errores

El objetivo es entender qué tipo de errores comete el modelo y qué tienen en común: ir uno o varios pasos más allá de la matriz de confusión. Si aparece un patrón, se puede mejorar el modelo en ese aspecto concreto. [T11, p. 32]

Se puede hacer a mano: mirar las predicciones incorrectas y anotar **tags**, es decir, factores que pueden estar presentes. El primer paso es elegir qué tags analizar. [T11, p. 32] Ejemplos: [T11, p. 33]

- una clase específica con más errores (se ve en la matriz de confusión);
- propiedades del dato (en imágenes: borrosa, oscura, con reflejos);
- metadatos (modelo de cámara, empresa, tipo de usuario);
- un tipo concreto de dato (por ejemplo, recomendaciones a jóvenes).

Con los tags elegidos se calculan dos proporciones distintas: [T11, p. 34]

1. **Qué porcentaje de los errores tiene ese tag.** Dice cuánto mejoraría el rendimiento global si se resolviera ese error.
2. **De todos los datos con ese tag, cuántos están mal clasificados.** Si es alto, el modelo funciona mal en ese grupo; se compara con los datos sin el tag.

Con ese análisis se decide qué datos priorizar al mejorar el modelo o los datos. [T11, p. 34]

### Priorizar un tag

La tabla de ejemplo compara cada tipo de imagen con su HLP: [T11, p. 35]

| Tipo de imagen | Accuracy | HLP | Gap al HLP | % de datos | Contribución al gap |
|---|---|---|---|---|---|
| Imagen limpia | 96 % | 97 % | 1 % | 50 % | 0,5 % |
| Bajo contraste | 88 % | 94 % | 6 % | 20 % | 1,2 % |
| Artefacto de movimiento | 82 % | 90 % | 8 % | 15 % | 1,2 % |
| Dispositivo distinto | 85 % | 92 % | 7 % | 10 % | 0,7 % |
| Imagen recortada o parcial | 70 % | 80 % | 10 % | 5 % | 0,5 % |

**Inferencia a partir de los números:** la contribución es el gap multiplicado por la fracción de datos (`6 % × 20 % = 1,2 %`). El grupo con el mayor gap (recortadas, 10 %) aporta poco porque es raro; bajo contraste y artefacto de movimiento son los que más rendimiento global pueden devolver.

Criterios para elegir en qué trabajar: [T11, p. 39]

- cuánto margen de mejora hay;
- con qué frecuencia aparece esa categoría;
- qué tan fácil es mejorarla (quizás alcance con una feature específica);
- qué tan importante es mejorarla. Si es muy importante, se puede agregar una métrica específica para ella en la selección de modelo.

Una vez elegida la categoría, las opciones son mejorar la calidad de sus etiquetas o datos, recolectar más datos de ese tipo o usar data augmentation. La segunda versión de la diapositiva pone primero la mejora de las etiquetas. [T11, p. 39] [T11, p. 40]

En el ejemplo gráfico, conseguir datos de más dispositivos reduciría el error. A veces hay relaciones entre "tags vecinos": mejorar uno mejora otro (artefacto de movimiento e imagen desenfocada, o imagen recortada). [T11, p. 41] [T11, p. 42]

## Data augmentation

No siempre se pueden conseguir datos nuevos; ahí entra la data augmentation. [T11, p. 46] Es muy efectiva para conseguir más datos, sobre todo en datos no estructurados (no tabulares): crea datos sintéticos combinando señal y ruido obtenidos por separado. [T11, p. 48]

Antes de usarla conviene comprobar que el dato sintético sea realista, que una persona pueda hacer la tarea (es decir, que exista el mapeo `x → y`) y que el análisis de errores muestre que el algoritmo hoy falla en ese tipo de dato. Si no falla, no hace falta. En medicina, problemas industriales y datasets pequeños o medianos suele ser extremadamente útil. [T11, p. 48]

| Datos | Ejemplos de augmentation |
|---|---|
| Audio | Agregar distintos niveles o tipos de ruido, recortar un segmento (*windowing*). |
| Imagen | Rotar, cambiar el brillo, desenfocar (*blur*), recortar (*crop*), agregar ruido. |
| Texto (NLP) | Reemplazar palabras por sinónimos, borrar palabras al azar, parafrasear con un LLM. |

Fuente de la tabla: [T11, p. 49].

### Restricciones y riesgos

Los datos nuevos deben preservar la etiqueta, respetar la fisiología o la física del problema y no cambiar la distribución esperada. Por eso se aplica sobre todo al dato crudo: sobre una "tabla de números" se pueden generar relaciones extrañas entre variables. [T11, p. 52]

| Riesgo | Qué pasa |
|---|---|
| *Garbage in, garbage out* | La aumentación no simula datos reales y confunde al algoritmo: rotar 180° un dígito puede confundir un 6 con un 9. |
| Leakage | Se generan datos a partir de un paciente y quedan datos del mismo paciente en train y en validación: el algoritmo "aprende al paciente", como en el caso que resuelve la CV por grupos. |
| Cambio de distribución | Si se aplica en exceso (en cantidad o en tamaño de las perturbaciones), los datos se alejan del escenario real. |

Fuente de la tabla: [T11, p. 53].

### Datos tabulares

En datos tabulares suele ser más interesante el **feature engineering**. Existen métodos como **SMOTE** o GANs que generan datos interpolando vecinos; funcionan, pero pueden producir datos imposibles y empeorar la generalización. En EEG, por ejemplo, aumentar después de calcular la potencia por banda de frecuencia pierde la coherencia fisiológica: es mejor aumentar la señal cruda. [T11, p. 56] Es menos útil cuando el dataset es grande o los datos son tabulares o con features abstractas, y más útil con pocos datos, riesgo de overfitting o datos caros de recolectar. [T11, p. 63]

### Dónde va en el pipeline

**Incorrecto:** aumentar todo el dataset y después hacer cross-validation. Habría leakage entre train y validación, porque en validación quedarían datos sintéticos generados a partir de un dato real que está en train (o "hijos" del mismo dato en ambos lados). [T11, p. 59]

**Correcto:** hacer primero la partición o la cross-validation y aumentar **solo el train de cada fold**. Validación y test se quedan con datos reales; si no, la estimación de la generalización queda sesgada, algo que pasa con frecuencia en algunos papers. [T11, p. 60] [T11, p. 61]

**Inferencia operativa:** con scikit-learn eso exige que la aumentación (por ejemplo SMOTE) sea un paso del pipeline que se reajusta dentro de cada fold, igual que el escalado. **Conocimiento general:** el `Pipeline` de scikit-learn no admite pasos que cambian la cantidad de filas; la biblioteca `imbalanced-learn` ofrece un `Pipeline` que aplica el remuestreo solo al ajustar.

### Test-time augmentation (TTA)

Un caso especial: predecir sobre el dato original y sobre sus variaciones, y combinar o promediar esas predicciones. [T11, p. 62]

### Conclusiones de la cátedra

La data augmentation puede mejorar la generalización y reducir el overfitting. Se aplica solo al entrenamiento; validación y test usan datos reales. Las transformaciones respetan la semántica y la fisiología del problema, y una aumentación incorrecta puede introducir leakage e inflar las métricas. [T11, p. 64]

## Muchos datos frente a buenos datos

Big data siempre ayuda si hay recursos y un algoritmo para procesarlo, pero no siempre es posible. Tener buenos datos ayuda siempre y es más fácil. Un algoritmo correcto con buenos datos funciona mucho mejor que un muy buen algoritmo con datos no tan buenos. Por eso no conviene obsesionarse con el modelo al principio: empezar a iterar permite mejorar más rápido y entender mejor los datos. [T11, p. 65]

"Buenos datos" significa: [T11, p. 65]

- relación `x → y` consistente (HLP mejor que el azar);
- cobertura de los casos de uso importantes (tipos de clientes, etc.);
- tamaño razonable;
- que se mantenga la relación train–validación, train–test y train–deployment. Ver [data drift y concept drift](mlops-y-despliegue.md#data-drift-y-concept-drift).

## Conexiones

- [Diagnóstico de modelos](diagnostico-de-ml.md): el paso previo.
- [Evaluación y validación](evaluacion-y-validacion.md): leakage y CV por grupos.
- [Métricas de clasificación](metricas-de-clasificacion.md): matriz de confusión, falsos positivos y falsos negativos.
- [MLOps y despliegue](mlops-y-despliegue.md): el ciclo de vida data-centric.
- [TP3: optimización de modelos](tp3-optimizacion.md): análisis de errores por cohortes y estrategia data-centered.
