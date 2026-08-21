# Fundamentos del aprendizaje automático

## Idea central

El aprendizaje automático busca que un sistema mejore su comportamiento a partir de experiencia o información. A diferencia del flujo tradicional, donde datos y reglas programadas producen una salida, en ML los datos y las salidas conocidas pueden usarse para aprender el programa o modelo. [T01, p. 8] [T01, p. 10] [T01, p. 14]

## Paradigmas principales

- **Supervisado:** aprende una función entrada → salida a partir de ejemplos etiquetados. Una salida categórica define clasificación y una continua, regresión. [T01, p. 25], [T02, p. 46]
- **No supervisado:** busca patrones sin etiquetas, por ejemplo agrupamientos. [T01, p. 28]
- **Por refuerzo:** un agente descubre una política de decisiones al interactuar con un entorno y recibir recompensas o castigos, posiblemente diferidos. [T01, p. 32]

Hay otros ejes de clasificación. El aprendizaje **batch** entrena con el conjunto disponible y requiere reentrenamiento para incorporar datos nuevos; el aprendizaje **online** actualiza el modelo continuamente, pero puede ser vulnerable a secuencias ruidosas y depende de la velocidad de adaptación. [T01, p. 38] En **instance-based learning**, la predicción depende de la similitud con ejemplos almacenados; en **model-based learning**, se construye un modelo que luego generaliza. [T01, p. 43]

## Proyecto de ML

Una primera estructura conceptual es: obtener y preparar datos, elegir una estrategia de aprendizaje, definir la evaluación y estimar el comportamiento en datos nuevos. [T01, p. 59] La versión desarrollada agrega separación de datos, limpieza, EDA, ingeniería o selección de características, modelado, regularización, evaluación en dev, iteración y evaluación final en test. [T03, p. 16]

Desafíos recurrentes: datos insuficientes o no representativos, mala calidad, características irrelevantes y el equilibrio entre underfitting y overfitting. [T01, p. 65] [T01, p. 68] [T01, p. 70]

## Conexiones

- [Datos y preprocesamiento](datos-y-preprocesamiento.md)
- [Evaluación y validación](evaluacion-y-validacion.md)
- [EDA y selección](eda-y-seleccion.md)
