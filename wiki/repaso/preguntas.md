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

## Clasificación y regresión logística

21. ¿Por qué la regresión lineal no sirve para estimar la probabilidad de una clase, y qué problema aparece cuando se agrega un ejemplo extremo bien etiquetado? [T04, p. 15] [T04, p. 16] [T04, p. 17]
22. Partiendo de `logit(p) = β0 + β1·x`, despejá `p` y explicá en qué sentido el modelo es lineal. [T04, p. 55] [T04, p. 56]
23. Si `p = 0,8`, ¿cuánto valen las odds y cómo se interpretan? [T04, p. 55]

## Métricas de clasificación

24. Dos modelos tienen 80 % de accuracy sobre los mismos pacientes. ¿Qué información falta para elegir entre ellos? [T04, p. 27]
25. Escribí precisión, recall, especificidad, valor predictivo negativo y FPR a partir de la matriz de confusión, e indicá cuáles se leen por fila y cuáles por columna. [T04, p. 31] [T04, p. 34] [T04, p. 36] [T04, p. 45]
26. ¿Qué pasa con precisión y recall al bajar el umbral? ¿Qué umbral preferirías para detectar cáncer y cuál para un filtro de spam? [T04, p. 39] [T04, p. 42] [T04, p. 43]
27. ¿Qué puntos de la curva ROC corresponden a un umbral mayor que todos los scores y a uno menor que todos? ¿Dónde está el clasificador ideal? [T04, p. 46] [T04, p. 48] [T04, p. 51]
28. ¿Qué significan `AUC = 1` y `AUC = 0,5`? ¿Con qué partición elegirías el umbral que minimiza la distancia a (0, 1)? [T04, p. 51] [T04, p. 52] [T02, p. 89]

## Modelos generativos

29. ¿Qué modela un clasificador discriminativo y qué modela uno generativo? Da un ejemplo de cada uno. [T06, p. 3]
30. ¿Cuándo coinciden MAP y máxima verosimilitud? Usá el ejemplo del detector de metales para explicar el papel del prior. [T06, p. 18] [T06, p. 19] [T06, p. 20]
31. ¿Qué supuesto hace que la frontera de LDA sea lineal, y qué cambia en QDA? [T06, p. 26] [T06, p. 30]
32. Compará LDA y PCA como proyecciones. [T06, p. 27] [T06, p. 28]
33. Con 200 pacientes y 500 características, ¿elegirías LDA o QDA? Justificalo contando parámetros. [T06, p. 31]
34. ¿Qué supuesto hace Naive Bayes y qué forma toma su matriz de covarianza en la versión gaussiana? [T06, p. 32] [T06, p. 38]
35. ¿Qué problema resuelve la corrección de Laplace? Recalculá el score de spam de «oferta urgente». [T06, p. 42] [T06, p. 44] [T06, p. 46]
36. Resolvé el ejemplo del tenis para `<soleado, frío, alta, fuerte>`. [T06, p. 40] [T06, p. 41]

## Árboles y ensambles

37. ¿Por qué el error de clasificación es un mal criterio de corte comparado con Gini o entropía? [T07, p. 11] [T07, p. 15]
38. Calculá la impureza de Gini de un nodo 50/50 y de un nodo puro. ¿Qué fórmula usaste y por qué? [T07, p. 12] [T07, p. 15]
39. Describí el algoritmo CART y cuántos umbrales evalúa por nodo con `n` muestras y `d` características. [T07, p. 35] [T07, p. 47] [T07, p. 48]
40. Nombrá tres desventajas de los árboles y dos maneras de controlar el sobreajuste. [T07, p. 27] [T07, p. 28]
41. Un árbol obtiene 1,00 en train y 0,86 en validación. ¿Qué diagnóstico hacés y qué hiperparámetros ajustarías? [T07, p. 49] [T07, p. 50] [T07, p. 54]
42. ¿Qué es bootstrap, por qué cada muestra contiene alrededor del 63 % de los datos únicos y para qué sirve el out-of-bag? [T07, p. 56] [T07, p. 57]
43. ¿Qué dos fuentes de aleatoriedad usa Random Forest y qué agrega Extra Trees? [T07, p. 59] [T07, p. 63] [T07, p. 64]
44. ¿Por qué el bagging ayuda más con árboles que con regresión logística? [T07, p. 69]
45. ¿Qué ventajas tiene el log-loss frente a Gini y entropía? [T07, p. 73]

## Máquinas de vectores de soporte

46. ¿Qué condición única cumple un hiperplano que separa correctamente ejemplos con `yᵢ ∈ {1, −1}`? Verificala con la recta `−2 − 4x₁ + 3x₂ = 0` y los puntos `(2, 10)` y `(6, 4)`. [T08, p. 14] [T08, p. 15]
47. Definí margen, hiperplano de margen maximal y vectores de soporte. ¿Qué papel cumple la restricción `Σ bⱼ² = 1`? [T08, p. 19] [T08, p. 21] [T08, p. 23] [T08, p. 24]
48. Con margen duro, se eliminan el 80 % de los datos alejados de la frontera y se reentrena. ¿Qué le pasa al hiperplano y por qué? [T08, p. 23] [T08, p. 25]
49. ¿Por qué un único ejemplo cercano a la otra clase puede justificar pasar a un margen tolerante? [T08, p. 26] [T08, p. 27]
50. Interpretá `εᵢ = 0`, `0 < εᵢ ≤ 1` y `εᵢ > 1`. ¿Qué pasa si `C = 0` en la formulación con `Σ εᵢ ≤ C`? [T08, p. 31] [T08, p. 32]
51. En la diapositiva del kernel RBF, ¿qué efecto tiene aumentar `C`? ¿Por qué parece contradecir la formulación con `Σ εᵢ ≤ C`? [T08, p. 30] [T08, p. 49]
52. Mostrá que los puntos `(±2, ±2)` (clase −1) y `(±1, ±1)` (clase 1) se vuelven linealmente separables con `(x₁, x₂, x₁²)`. ¿Qué plano los separa? [T08, p. 34] [T08, p. 35]
53. Escribí los núcleos lineal, polinómico y radial. ¿Qué pasa con la frontera al aumentar `d` o `γ`? [T08, p. 43] [T08, p. 44] [T08, p. 46] [T08, p. 49]
54. Compará uno contra uno y uno contra todos: cuántos modelos entrenás con 4 clases y cómo decidís la clase final. [T08, p. 52] [T08, p. 53]
55. ¿Por qué SVM necesita atributos escalados y un árbol de decisión no? [T08, p. 54] [T07, p. 26]

## Aprendizaje basado en instancias

56. ¿Qué significa que kNN sea un método "perezoso"? ¿En qué etapa queda el costo computacional y qué supuesto sobre los datos lo justifica? [T09, p. 9] [T09, p. 11] [T09, p. 14]
57. Escribí las distancias euclídea y de Manhattan y la similitud coseno. ¿Para qué tipo de datos conviene cada una? [T09, p. 21] [T09, p. 23] [T09, p. 24] [T09, p. 25]
58. ¿Cómo codificarías "día del año" para que el 31 de diciembre y el 1 de enero queden cerca con distancia euclídea? [T09, p. 26]
59. ¿Qué pasa con el sesgo y la varianza al aumentar `k`? ¿Por qué no se puede elegir `k` mirando el error de train? [T09, p. 29] [T09, p. 31]
60. Nombrá tres consideraciones para elegir `k`: clases desbalanceadas, alta dimensionalidad y empates. [T09, p. 31]
61. Una feature está en metros y otra en milímetros. ¿Qué le pasa a kNN si no escalás, y qué dos opciones de escalado da la clase? [T09, p. 32]
62. Con `k = 3`, un vecino de clase A está a distancia 1 y dos de clase B están a distancia 3. ¿Qué predice kNN uniforme y qué predice el ponderado? ¿Por qué "achicar `k`" y "ponderar" no son equivalentes? [T09, p. 34] [T09, p. 36]
63. ¿Cuáles son las dos limitaciones principales de kNN y por qué la segunda afecta menos a los árboles? [T09, p. 38] [T09, p. 39]
64. ¿Cómo divide el espacio un KD-Tree? ¿Cuándo falla la búsqueda en la hoja y cómo lo corrige el backtracking? [T09, p. 45] [T09, p. 50] [T09, p. 51]
65. Describí LSH con hiperplanos aleatorios y sus tres hiperparámetros. ¿Qué pasa al aumentar el número de hiperplanos por hash? ¿Y la cantidad de proyecciones? [T09, p. 58] [T09, p. 60]
66. ¿Cómo predice kNN como regresor? ¿Qué efecto tiene un `k` grande sobre los máximos de la función? [T09, p. 63] [T09, p. 65]
67. ¿Por qué un ANN afecta más a la regresión que a la clasificación? [T09, p. 67]
68. ¿Cómo predice un árbol de regresión y qué efecto tiene aumentar `max_depth`? Compará árbol y Random Forest como regresores. [T09, p. 69] [T09, p. 70] [T09, p. 71] [T09, p. 72]

## Aplicación al TP2

69. En Bank Marketing, ¿qué criterio usarías para decidir si una variable introduce leakage? Pensá en qué información está disponible antes de la llamada. [P02, p. 1]
70. ¿Por qué el escalado y el encoding deben vivir dentro del pipeline que se valida con k-fold, y no aplicarse antes a todo train? [P02, p. 1] [P02, p. 2] [T02, p. 94] [T02, p. 96]
71. Si el EDA muestra pocas respuestas `yes`, ¿qué problema tiene usar solo accuracy? ¿Qué dos métricas elegirías y cómo las justificarías por el costo de cada error? [P02, p. 2] [T04, p. 26] [T04, p. 41]
72. ¿Qué modelos del TP2 necesitan escalado y cuál no? ¿Por qué? [T07, p. 26] [T08, p. 54] [T09, p. 32]
73. ¿Qué supuesto de Naive Bayes se rompe si hay variables muy correlacionadas, y qué efecto puede tener en sus probabilidades? [P02, p. 2] [T06, p. 38]
74. En una curva de validación de `k` para KNN, ¿dónde esperás sobreajuste y dónde subajuste? [P02, p. 2] [T09, p. 29] [T07, p. 50]
75. ¿Con qué datos estimás el rendimiento del modelo final en datos nuevos, y por qué no podés usar ese resultado para cambiar de modelo? [P02, p. 2] [T02, p. 88] [T02, p. 89]
