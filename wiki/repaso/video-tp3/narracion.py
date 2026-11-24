"""Guion narrado del video del TP3.

Cada escena es una lista de segmentos (clave, texto, fuente). El texto es el
que se lee en voz alta; `fuente` aparece en la esquina inferior derecha
mientras suena el segmento. Los números salen del notebook
`entregas/tp3-gpu-reservations/tp3_gpu_reservations.ipynb` y de
`entregas/tp3-gpu-reservations/decisiones.md`.

`PRONUNCIACION` reescribe los términos en inglés para que la voz de Piper
(es_AR) los lea como se dicen en clase. Solo afecta al audio.
"""

ESCENAS = {
    "Intro": [
        ("i1", "Una plataforma alquila GPUs por reserva. Alguien reserva hoy una máquina para dentro de tres semanas. "
               "La pregunta del TP3 es simple: ¿esa reserva se va a cancelar antes de ejecutarse?",
         "Consigna [P03, p. 1]"),
        ("i2", "Tenemos 47.842 reservas pasadas. Cada una es una fila con unas treinta columnas: cuándo se pidió, "
               "qué GPU, qué tipo de cliente, su historial. Y una etiqueta: el 41,7 % se canceló.",
         "Dataset D04"),
        ("i3", "En el TP2, la pregunta era qué modelo elegir. El TP3 empieza donde termina el TP2: ya tenés un modelo "
               "que funciona bastante bien. Ahora la pregunta es otra. ¿Por qué se equivoca? ¿Y qué conviene hacer "
               "para que se equivoque menos?",
         "Consigna [P03, p. 2-3]"),
        ("i4", "Para responderla hace falta teoría nueva, de las clases 11 y 12. La vamos a ver en cinco pasos, y en "
               "cada uno la aplicamos a nuestra resolución: cómo validar, cómo diagnosticar, cómo analizar los errores, "
               "cómo optimizar, y cómo llevar el modelo a producción.",
         "Clases T11 y T12"),
    ],
    "Validacion": [
        ("v1", "Empecemos por una idea que parece obvia, pero que tiene consecuencias enormes. La validación cruzada "
               "intenta responder una pregunta: ¿cómo le va a ir al modelo con datos nuevos? Pero datos nuevos puede "
               "significar cosas muy distintas.",
         "[T11, p. 67]"),
        ("v2", "La clase 11 lo resume en una regla. La relación entre train y validación tiene que ser la misma que "
               "habrá entre train y los datos en los que se va a usar el modelo. El split lo define el uso.",
         "[T11, p. 71-72]"),
        ("v3", "El caso más simple ya lo conocés: k-fold. La versión estratificada agrega un detalle: cada fold "
               "mantiene la proporción de clases. Con un 41,7 % de cancelaciones, todos los folds tienen más o menos "
               "ese mismo porcentaje.",
         "[T11, p. 70, 74]"),
        ("v4", "Pero a veces las filas no son independientes. Imaginá datos de pacientes de cinco hospitales. Si "
               "mezclás al azar, el mismo hospital queda de los dos lados, y el modelo puede aprender a reconocer el "
               "hospital en lugar del problema. La clase lo llama leakage indirecto.",
         "[T11, p. 75-77]"),
        ("v5", "La solución es validar por grupos. Cada grupo entero va a train o a validación, nunca partido. Así, "
               "la validación mide lo que importa si el sistema se va a usar en hospitales que nunca vio.",
         "[T11, p. 78-79]"),
        ("v6", "¿Y esto qué tiene que ver con las GPUs? Mirando los datos encontramos algo raro. El 33 % de las filas "
               "es una copia exacta de otra. Hay 3.499 grupos de reservas idénticas, que cubren el 41 % de las filas.",
         "Notebook, sección 1.2"),
        ("v7", "Y no parecen errores de carga. Cuanto más grande el grupo, más se cancela: 28 % en las reservas "
               "únicas, 95 % en los grupos de más de 50 copias. Nuestra interpretación es que son reservas en lote, "
               "que se cancelan juntas.",
         "Notebook, sección 1.2 · inferencia nuestra"),
        ("v8", "Con k-fold al azar, una reserva de validación muchas veces tiene una gemela en train, con la misma "
               "etiqueta. El modelo no necesita entender nada: le alcanza con recordar.",
         "Inferencia nuestra"),
        ("v9", "Entonces usamos dos validaciones. La principal es estratificada al azar, porque suponemos que la "
               "competencia evalúa con reservas del mismo conjunto. Y como control, una agrupada, que nunca separa "
               "a las gemelas: estima el rendimiento con reservas nunca vistas.",
         "decisiones.md · notebook, sección 5"),
        ("v10", "La diferencia entre las dos mide cuánto ayuda memorizar. Para el Random Forest del baseline, la AUC "
                "es 0,956 al azar, y 0,937 agrupada. Esa brecha va a reaparecer en todo el video.",
         "Notebook, sección 6.3"),
        ("v11", "Y un recordatorio del TP2. El dataset trae columnas que se conocen recién después de ejecutar, como "
                "el estado final de la reserva. Las sacamos por leakage, igual que la duración de la llamada en Bank "
                "Marketing. También sacamos la GPU finalmente asignada y la espera en cola: agregarlas subía la AUC "
                "apenas 0,0014.",
         "[P03, p. 1, 5] · notebook, secciones 1.1 y 6.4"),
    ],
    "Diagnostico": [
        ("d1", "Supongamos que el modelo ya está entrenado y validado, pero no alcanza. ¿Dónde conviene invertir el "
               "esfuerzo? Una métrica sola te dice que hay un problema, pero no cuál es.",
         "[T11, p. 2, 4]"),
        ("d2", "La clase 11 separa tres fuentes de error. El sesgo: el modelo elegido no puede representar la "
               "relación, y se equivoca de forma consistente. La varianza: aprendió detalles de esta muestra "
               "particular, y con otra muestra cambiaría. Y el error irreducible: lo que las variables no pueden "
               "explicar.",
         "[T11, p. 5, 18]"),
        ("d3", "En nuestros datos, el error irreducible se ve a simple vista. Hay 79 grupos de reservas idénticas con "
               "etiquetas distintas. Mismas variables, distinto resultado. Ningún modelo puede acertarlas a todas.",
         "Notebook, sección 1.2"),
        ("d4", "El diagnóstico arranca con una pregunta: ¿al menos aprende train? Si el rendimiento en train es bajo, "
               "hay subajuste. O le falta capacidad al modelo, o les falta información a las variables.",
         "[T11, p. 7-8, 11]"),
        ("d5", "Si train está bien pero validación no, hay sobreajuste. Puede estar aprendiendo ruido, o algo real "
               "que no se va a repetir en el uso, como un hospital, o un lote. Para eso último, la herramienta es la "
               "validación por grupos.",
         "[T11, p. 10-11]"),
        ("d6", "Para distinguir estos casos hay dos gráficos. El primero es la curva de validación: el rendimiento en "
               "función de la complejidad. Acá, la profundidad máxima de los árboles del Random Forest.",
         "[T11, p. 19-20] · notebook, sección 6.2"),
        ("d7", "Train sube siempre. Con árboles sin límite, la AUC de train llega a 0,9997: casi perfecta. La "
               "validación al azar también sube, hasta 0,956. Pero la agrupada sube mucho menos.",
         "Notebook, sección 6.2"),
        ("d8", "Mirá la brecha entre las dos validaciones. Pasa de 0,006 con profundidad 8, a 0,018 sin límite. Los "
               "árboles profundos memorizan los lotes. Igual, la mejor profundidad es la misma en los dos esquemas, "
               "así que nos quedamos con árboles sin límite.",
         "Notebook, sección 6.2"),
        ("d9", "La regresión logística, en cambio, mostraba lo opuesto: train y validación casi iguales, pero los "
               "dos más bajos, con AUC 0,913. Eso es sesgo. Una frontera lineal no alcanza.",
         "Notebook, sección 6.1"),
        ("d10", "El segundo gráfico es la curva de aprendizaje: el rendimiento en función de la cantidad de filas de "
                "entrenamiento. Tiene dos firmas típicas.",
         "[T11, p. 21]"),
        ("d11", "Si train y validación convergen en un valor bajo, es subajuste: más datos no van a ayudar. Si quedan "
                "separadas, y la validación todavía sube, es sobreajuste: más datos sí podrían cerrar la brecha.",
         "[T11, p. 21-24]"),
        ("d12", "Esta es la nuestra. Train queda pegada arriba, cerca de uno. La validación al azar sube de 0,93 a "
                "0,96. Pero la agrupada, la que mide reservas nuevas, se aplana. El último 25 % de los datos le sumó "
                "apenas 0,0014: menos que la variación entre folds.",
         "Notebook, sección 8"),
        ("d13", "Nuestro diagnóstico es este. El modelo tiene capacidad de sobra, y más reservas del mismo tipo casi "
                "no ayudan. El límite es la información que traen las variables. Entonces, la pregunta pasa a ser: "
                "¿dónde falta información?",
         "Inferencia nuestra · notebook, sección 8"),
    ],
    "Errores": [
        ("e1", "Acá entra el diseño centrado en datos. En el enfoque centrado en el modelo, los datos quedan fijos y "
               "se itera sobre el algoritmo. En el centrado en datos, se fija un modelo razonable y se itera sobre los "
               "datos, lo que incluye agregar variables.",
         "[T11, p. 31, 43]"),
        ("e2", "La diferencia está en el segundo paso del ciclo: evaluar con análisis de errores. Es ir más allá de "
               "la matriz de confusión, y preguntarse qué tienen en común los errores.",
         "[T11, p. 32, 43]"),
        ("e3", "Se eligen tags, características que pueden tener los ejemplos, y para cada uno se calculan dos "
               "números. Primero: qué porcentaje de los errores tiene ese tag. Eso dice cuánto ganarías si lo "
               "resolvieras. Segundo: de los ejemplos con ese tag, qué porcentaje está mal. Eso dice si el modelo "
               "funciona peor ahí.",
         "[T11, p. 32-34]"),
        ("e4", "Para priorizar, la clase multiplica la brecha de cada grupo por su frecuencia. Un grupo con mucho "
               "error, pero muy raro, aporta poco. Uno con error moderado y muy frecuente puede aportar mucho más.",
         "[T11, p. 35, 39]"),
        ("e5", "Lo aplicamos a las predicciones out-of-fold del baseline. Son 4.423 errores sobre 38.273 reservas. "
               "Cruzamos dos tags: el tipo de cliente, y si la reserva es única o parte de un lote.",
         "Notebook, secciones 7.1 y 7.2"),
        ("e6", "Este cuadrado representa todas las reservas. Las reservas únicas de cloud_marketplace son el 41 %. "
               "Ahora mirá los errores: esas mismas reservas concentran el 77 %.",
         "Notebook, sección 7.2"),
        ("e7", "Dentro de esa región, el error es 21,4 %. En todo el resto, 4,6 %. Y es parejo adentro: ningún tier, "
               "GPU o región geográfica lo explica por separado. Esa es nuestra región problemática.",
         "Notebook, sección 7.2"),
        ("e8", "La consigna pedía mirar cohortes como el tier basic o la GPU T4. Las dos tienen casi el doble de error "
               "que el resto. Pero es un efecto de composición: el 93 % de basic y el 79 % de T4 son reservas de "
               "cloud_marketplace. No son difíciles por sí mismas: están llenas de la región difícil.",
         "[P03, p. 2] · notebook, sección 7.1"),
        ("e9", "¿Por qué falla ahí? Casi no hay historial: solo el 0,9 % tiene cancelaciones previas, contra el "
               "10,9 % del resto. Y no tienen las señales fuertes del dataset: ni el compromiso locked_allocation, "
               "que se cancela el 99,8 % de las veces, ni el lote.",
         "Notebook, secciones 7.3 y 9.2"),
        ("e10", "Sin señales, el modelo duda. El 38 % de esas reservas recibe una probabilidad entre 0,3 y 0,7. No es "
                "un problema de umbral: optimizarlo en la región gana 0,2 puntos. Y no es falta de filas: con la mitad "
                "de los datos, la accuracy de la región era casi la misma.",
         "Notebook, secciones 9.1 y 9.2"),
        ("e11", "Los dos tipos de error cuestan distinto. Un falso negativo es una cancelación sin aviso: una GPU que "
                "queda ociosa. Un falso positivo, si se reasigna la GPU, es un cliente que llega y no tiene recursos. "
                "Si un falso positivo costara el doble, con probabilidades calibradas convendría subir el umbral a "
                "dos tercios.",
         "Notebook, sección 7.4 · umbral: conocimiento general"),
        ("e12", "¿Y data augmentation? La clase la muestra para imágenes, audio o texto, y advierte dos cosas: se "
                "aplica solo al train de cada fold, y en datos tabulares puede generar filas imposibles. En nuestro "
                "caso el problema no es la cantidad sino la información, así que la descartamos.",
         "[T11, p. 48, 56, 59-61]"),
        ("e13", "Lo que sí proponemos es adquirir datos nuevos. Primero, el historial del cliente final: entre las "
                "reservas únicas, las que tienen algo de historial llegan a AUC 0,916, contra 0,876 sin historial. "
                "Después, un identificador de lote, la actividad entre la reserva y la ejecución, y las condiciones "
                "comerciales.",
         "Notebook, sección 10 · inferencia nuestra"),
    ],
    "Optimizacion": [
        ("o1", "Con el diagnóstico hecho, toca optimizar. La herramienta nueva más importante de la clase 12 es "
               "gradient boosting. Para entenderlo, conviene compararlo con algo que ya conocés: Random Forest.",
         "[T12, p. 4-6]"),
        ("o2", "Random Forest es bagging: muchos árboles profundos, cada uno entrenado con una muestra bootstrap "
               "distinta, en paralelo e independientes. Al promediarlos, sus errores se compensan. Bagging reduce la "
               "varianza.",
         "[T12, p. 20] · [T07]"),
        ("o3", "Boosting hace otra cosa: entrena árboles en secuencia. Mirá este ejemplo de regresión. El primer "
               "árbol, muy chiquito, apenas captura la tendencia.",
         "[T12, p. 4-5, 21]"),
        ("o4", "Ahora calculamos los residuos: lo que le falta a la predicción para llegar a cada punto. El segundo "
               "árbol no aprende los datos. Aprende esos residuos.",
         "[T12, p. 4-5]"),
        ("o5", "Sumamos su predicción, pero achicada por la tasa de aprendizaje, para no corregir de más. Y repetimos: "
               "cada árbol nuevo corrige lo que el conjunto todavía hace mal.",
         "[T12, p. 5] · tasa de aprendizaje: conocimiento general"),
        ("o6", "Después de muchos árboles, una suma de árboles simples dibuja una curva compleja. Boosting reduce el "
               "sesgo. Por eso se controlan juntos la tasa de aprendizaje, la cantidad de árboles y su tamaño, y se "
               "usa early stopping: dejar de agregar árboles cuando una validación interna deja de mejorar.",
         "[T12, p. 6] · early stopping: conocimiento general"),
        ("o7", "Hay varias implementaciones: XGBoost, LightGBM, CatBoost. Nosotros usamos la de scikit-learn, "
               "HistGradientBoosting, inspirada en LightGBM: agrupa los valores en histogramas para entrenar rápido, "
               "y maneja faltantes y categóricas.",
         "[T12, p. 7-10]"),
        ("o8", "La otra idea de la clase 12 es combinar modelos. Lo más simple es promediar sus probabilidades. El "
               "stacking va más lejos: un meta-modelo aprende a combinarlos, entrenado con predicciones out-of-fold "
               "para no tener leakage.",
         "[T12, p. 19, 22-25]"),
        ("o9", "¿Cuándo sirve combinar? Cuando los modelos se equivocan en lugares distintos. Si sus errores se "
               "superponen casi por completo, promediarlos no corrige nada. Por eso la clase sugiere medir la "
               "correlación entre sus predicciones.",
         "[T12, p. 19, 26]"),
        ("o10", "Antes de probar nada, fijamos una regla de adopción. Un cambio se adopta si la AUC media mejora con "
                "la validación al azar, y en al menos cuatro de los cinco folds, comparando fold contra fold. Y si, "
                "con la validación agrupada, no empeora.",
         "decisiones.md · notebook, sección 11"),
        ("o11", "Así quedaron las estrategias. Las variables derivadas no pasaron: son funciones de columnas que el "
                "modelo ya tiene, coherente con el diagnóstico. Gradient boosting, aun ajustado, perdió un poco con "
                "la validación al azar, pero ganó con la agrupada: memoriza menos. Quedó como candidato para combinar.",
         "Notebook, secciones 11.1 a 11.3"),
        ("o12", "Se adoptaron tres cambios. Usar el 20 % de las variables en cada corte del Random Forest, que "
                "decorrelaciona los árboles: más 0,0007, en los cinco folds. Promediar Random Forest y gradient "
                "boosting: más 0,0012 al azar, y más 0,0026 agrupada. Y bajar a 100 árboles: la misma AUC, con un "
                "archivo de 12 megas en lugar de 37.",
         "Notebook, secciones 11.3 a 11.5"),
        ("o13", "No probamos stacking. Las predicciones de los dos modelos tienen correlación 0,976: un meta-modelo "
                "no tiene mucho que combinar.",
         "Notebook, sección 11.4"),
        ("o14", "La mejora total es chica: más 0,0018 de AUC. Era esperable. Si el límite es la información, ningún "
                "modelo la inventa. Pero no fue pareja: se concentró donde el baseline ordenaba peor. "
                "independent_client, la región elegida, las reservas únicas. En los lotes, el error subió un poco, "
                "porque el modelo memoriza menos.",
         "Notebook, sección 12.3"),
    ],
    "Final": [
        ("f1", "Último paso. Una idea importante de la clase 11: la validación cruzada no elige una frontera de "
               "decisión. Elige una receta: variables, algoritmo e hiperparámetros. Con la receta elegida, se entrena "
               "el modelo final con todos los datos de desarrollo.",
         "[T11, p. 68]"),
        ("f2", "El umbral también se elige sin tocar test, con las predicciones out-of-fold. Y acá hubo una novedad: "
               "el leaderboard de la primera entrega mostró que la competencia mide balanced accuracy, el promedio de la "
               "tasa de aciertos en las canceladas y en las que se ejecutan. Con probabilidades calibradas, el umbral que "
               "la maximiza es la tasa de cancelación: 41,7 % en desarrollo, y 29 % en las reservas únicas. Elegimos el "
               "menor umbral a menos de 0,001 de la mejor balanced accuracy en las dos validaciones: 0,40.",
         "Notebook, sección 12.2 · decisiones.md, actualización del 11/11"),
        ("f3", "Recién ahí se abre test, una sola vez. La AUC da 0,960. La balanced accuracy, 0,888. Con bootstrap, remuestreando "
               "las filas de test dos mil veces, los intervalos del 95 % van de 0,957 a 0,963, y de 0,881 a 0,894.",
         "Notebook, sección 12.4"),
        ("f4", "Contra el baseline, la mejora de AUC se confirma en test: más 0,0013, con un intervalo que no incluye "
               "el cero. La de balanced accuracy, en cambio, no se distingue de cero. Así hay que decirlo en la defensa.",
         "Notebook, sección 12.4"),
        ("f5", "Y otra vez aparece la brecha de las gemelas. En test, las reservas con una gemela en desarrollo tienen "
               "balanced accuracy 0,988. Las que no, 0,795. Por eso damos tres escenarios. Con reservas del mismo "
               "conjunto, AUC 0,96 y balanced accuracy 0,89. Con reservas nuevas, 0,94 y 0,86. Y solo con reservas "
               "individuales, 0,89 y 0,79. En el leaderboard, ningún grupo pasó de 0,91 de AUC: es una pista de que la "
               "evaluación se parece más a los dos últimos escenarios.",
         "Notebook, secciones 12.4 y 12.5 · leaderboard: interpretación nuestra"),
        ("f6", "Falta lo último: sacar el modelo del notebook. La clase 12 habla del salto de la prueba de concepto a "
               "producción. El código del modelo es una parte chica. Alrededor hay datos, transformaciones, "
               "empaquetado y monitoreo.",
         "[T12, p. 33-34]"),
        ("f7", "La función predictora tiene que recibir datos crudos, aplicar el preprocesamiento aprendido en train, "
               "contener el modelo ya entrenado, y funcionar sola: sin el notebook, sin etiquetas, sin reentrenar, y "
               "sin variables globales.",
         "[T12, p. 49-50]"),
        ("f8", "La nuestra guarda todo el pipeline en un archivo joblib, aplica las mismas transformaciones fijas que "
               "el notebook, y la probamos en un proceso nuevo con distintos formatos de entrada. La clase dice "
               "entrenar el modelo final sin test. Así lo evaluamos. Recién después de usar test, sumamos sus filas "
               "para el predictor que enviamos: 47.842 reservas.",
         "[T11, p. 68] · notebook, sección 12.6"),
        ("f9", "Y en producción, el mundo cambia. Si cambian las reservas que llegan, es data drift. Si cambia la "
               "relación entre las variables y la cancelación, es concept drift. Por eso un modelo desplegado se "
               "monitorea.",
         "[T12, p. 39-41]"),
        ("f10", "En resumen. Elegimos la validación según el uso. Diagnosticamos con curvas que el límite era la "
                "información, no el modelo. El análisis de errores nos llevó a una región concreta. Optimizamos con "
                "una regla fija, y medimos dónde mejoró. Y empaquetamos el modelo para usarlo fuera del notebook.",
         "Resumen"),
        ("f11", "La lección del TP3: el siguiente punto de rendimiento casi nunca está en un algoritmo más "
                "sofisticado. Está en entender qué información le falta al modelo, y dónde.",
         "Inferencia nuestra"),
    ],
}

# Orden de los términos: primero los más largos, para que no los pise uno corto.
PRONUNCIACION = [
    ("independent_client", "independent cláient"),
    ("cloud_marketplace", "cláud márketpleis"),
    ("locked_allocation", "lókt alokéishon"),
    ("HistGradientBoosting", "hist gradient bústing"),
    ("gradient boosting", "gradient bústing"),
    ("Bank Marketing", "bank márketing"),
    ("early stopping", "érli stóping"),
    ("scikit-learn", "sáikit lern"),
    ("out-of-fold", "áut of fóuld"),
    ("meta-modelo", "meta modelo"),
    ("Random Forest", "rándom fórest"),
    ("LightGBM", "láit yi bi em"),
    ("CatBoost", "kát bust"),
    ("XGBoost", "éks yi bust"),
    ("Boosting", "Bústing"),
    ("boosting", "bústing"),
    ("bootstrap", "bútstrap"),
    ("stacking", "stáking"),
    ("bagging", "bágin"),
    ("Bagging", "Bágin"),
    ("leakage", "líkech"),
    ("Balanced accuracy", "Bálanst acúrasi"),
    ("balanced accuracy", "bálanst acúrasi"),
    ("leaderboard", "líderbord"),
    ("accuracy", "acúrasi"),
    ("pipeline", "páiplain"),
    ("notebook", "nóutbuk"),
    ("baseline", "béislain"),
    ("joblib", "yóblib"),
    ("k-fold", "kei fóuld"),
    ("folds", "fóulds"),
    ("fold", "fóuld"),
    ("split", "split"),
    ("train", "tréin"),
    ("tier", "tíer"),
    ("basic", "béisic"),
    ("data augmentation", "déita ógmentéishon"),
    ("data drift", "déita drift"),
    ("concept drift", "cónsept drift"),
    ("tags", "tags"),
    ("GPUs", "gepeús"),
    ("AUC", "a u ce"),
    ("GPU T4", "ge pe u te cuatro"),
    ("Random", "rándom"),
]


def texto_hablado(texto: str) -> str:
    """Devuelve el texto con los términos en inglés escritos como se pronuncian."""
    import re

    for original, hablado in PRONUNCIACION:
        texto = re.sub(rf"(?<![\w-]){re.escape(original)}(?![\w-])", hablado, texto)
    return texto


def segmentos():
    """Itera (escena, clave, texto, fuente) en el orden del video."""
    for escena, lista in ESCENAS.items():
        for clave, texto, fuente in lista:
            yield escena, clave, texto, fuente
