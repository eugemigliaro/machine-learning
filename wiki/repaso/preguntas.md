# Preguntas de repaso

Preguntas recuperables por tema. Mantener las respuestas separadas o plegadas cuando eso ayude a practicar recuperación activa.

## Fundamentos

1. ¿Qué información recibe el aprendizaje supervisado que no recibe el no supervisado? [T01, p. 25] [T01, p. 28]
2. ¿Qué aprende un agente por refuerzo y qué papel cumplen las recompensas? [T01, p. 32]
3. ¿Cuándo preferirías aprendizaje online a batch y qué riesgo introduce? [T01, p. 38]
4. ¿En qué se diferencian instance-based y model-based learning al predecir datos nuevos? [T01, p. 43]

## Datos y EDA

5. ¿Por qué no conviene codificar una categoría nominal con números que sugieran orden? [T02, p. 13] [T02, p. 18]
6. Compará one-hot, frequency encoding y target encoding. ¿Qué problema aparece con categorías poco frecuentes y cómo lo atenúa la regularización? [T02, p. 18] [T02, p. 22] [T02, p. 23]
7. ¿Qué distingue un valor faltante de un outlier y qué alternativas hay para tratar cada uno? [T02, p. 34] [T02, p. 42]
8. ¿Cuándo elegirías min-max y cuándo z-score? [T03, p. 42] [T03, p. 43]
9. ¿Por qué más características pueden aumentar el riesgo de overfitting? [T03, p. 45] [T03, p. 59]
10. Compará filtros, wrappers y métodos embedded en costo, interacciones y dependencia del modelo. [T03, p. 62] [T03, p. 79]

## Modelado y evaluación

11. ¿Qué diferencia hay entre regresión lineal y polinómica si ambas se ajustan como modelos lineales en sus parámetros? [T02, p. 49] [T02, p. 52]
12. ¿Cómo reconocerías underfitting y overfitting comparando errores de train y dev? [T02, p. 53] [T02, p. 77]
13. ¿Qué decisión se toma con train, cuál con dev y cuál con test? [T03, p. 9]
14. ¿Por qué elegir un modelo mirando test sesga de manera optimista la estimación final? [T02, p. 70] [T02, p. 89]
15. Explicá k-fold cross-validation y por qué aprovecha mejor datasets pequeños. [T03, p. 12] [T03, p. 15]
16. ¿Qué mide RMSE y por qué los errores grandes pesan especialmente? [T03, p. 87]
17. Compará L1, L2 y Elastic Net respecto de los coeficientes que producen. [T03, p. 90] [T03, p. 91] [T03, p. 92]

## Aplicación al TP1

18. Diseñá el orden correcto de separación, preprocesamiento, validación cruzada, selección y test para evitar leakage. [P01, p. 1] [P01, p. 2] [P01, p. 3] [T02, p. 94] [T02, p. 96]
19. ¿Qué grado polinómico y valor de regularización elegirías si el menor error de train no coincide con el menor error de validación? [P01, p. 2]
20. ¿Qué RMSE comunicarías como rendimiento esperado en producción y de qué partición debe provenir? [P01, p. 3], [T02, p. 89]
