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

## Diagnóstico y diseño centrado en datos

76. Dos modelos tienen el mismo F1. Nombrá cuatro motivos distintos por los que cada uno podría estar limitado. ¿Por qué la métrica final no alcanza para elegir la intervención? [T11, p. 4]
77. ¿Cuáles son las tres fuentes de error y cuál de ellas no se puede reducir mejorando el modelo? [T11, p. 5]
78. ¿Para qué sirve el HLP? ¿Por qué es más útil en imágenes o audio que en datos tabulares? [T11, p. 14] [T11, p. 15]
79. Recorré el árbol de diagnóstico: con rendimiento bajo en validación, ¿qué preguntás primero? Para cada una de las cuatro causas, ¿con qué lo evaluás y qué hacés? [T11, p. 11]
80. Dibujá las curvas de aprendizaje de un modelo con underfitting y de uno con overfitting. ¿En cuál ayuda conseguir más datos? [T11, p. 21] [T11, p. 22] [T11, p. 23] [T11, p. 24]
81. ¿Qué acción elegirías para cada diagnóstico: más datos, menos features, más features, combinar features o hiperparámetros más restrictivos? [T11, p. 24]
82. ¿En qué se diferencian los bucles model-centric y data-centric? ¿Qué condición pone la cátedra para que el data-centric sea más efectivo? [T11, p. 31] [T11, p. 43]
83. En el análisis de errores, ¿qué te dice el porcentaje de errores con un tag y qué te dice la tasa de error dentro del tag? [T11, p. 34]
84. Con la tabla de tipos de imagen, ¿cómo se calcula la contribución al gap y por qué las imágenes recortadas, con el mayor gap, no son prioritarias? [T11, p. 35] [T11, p. 39]
85. ¿Qué tres condiciones deben cumplir los datos aumentados? Dá un ejemplo de augmentation que rompa la etiqueta. [T11, p. 52] [T11, p. 53]
86. ¿Por qué aumentar todo el dataset antes de la cross-validation produce leakage? ¿Cuál es el orden correcto? [T11, p. 59] [T11, p. 60] [T11, p. 61]
87. ¿Por qué la augmentation es menos útil en datos tabulares y qué riesgo tiene SMOTE? [T11, p. 56] [T11, p. 63]

## Validación avanzada

88. ¿Qué elige la cross-validation: una frontera de decisión o un modelo? ¿Qué se hace después de elegir? [T11, p. 68]
89. Enunciá la regla del split de la clase 11. ¿Por qué el uso del modelo define el split? [T11, p. 71] [T11, p. 72]
90. ¿Qué problema resuelve la k-fold estratificada y cuándo es más importante? [T11, p. 74]
91. Tenés datos de 5 escuelas y el sistema se usará en escuelas nuevas. ¿Qué validación usás y qué leakage evitás? ¿Qué diferencia hay entre Group K-Fold y LOGO? [T11, p. 76] [T11, p. 78] [T11, p. 79]
92. ¿Qué condición cumple siempre una validación temporal? ¿Por qué una k-fold aleatoria sobreestimaría el rendimiento si el modelo se usará en el futuro? [T11, p. 81]

## Boosting y combinación de modelos

93. ¿En qué se diferencia el entrenamiento de gradient boosting del de Random Forest? ¿Cuál reduce más el sesgo y cuál la varianza? [T12, p. 4] [T12, p. 6] [T12, p. 20] [T12, p. 21]
94. Compará XGBoost, LightGBM y CatBoost. ¿Por qué hay que tener cuidado con LightGBM en datasets chicos? [T12, p. 7] [T12, p. 8] [T12, p. 9]
95. ¿Qué ofrece scikit-learn para boosting y a qué biblioteca se parece `HistGradientBoosting`? [T12, p. 10]
96. ¿Por qué el meta-modelo del stacking no se entrena con predicciones sobre el training? ¿Qué son las predicciones out-of-fold? [T12, p. 24] [T12, p. 25]
97. ¿Cómo elegirías los modelos base de un stacking? ¿Qué indica una correlación alta entre sus salidas? [T12, p. 26]
98. ¿Qué diferencia hay entre stacking y blending según la clase 12? ¿Y según la clase 7? [T12, p. 27] [T07, p. 72]

## MLOps y despliegue

99. ¿Qué es el POC to Production Gap? [T12, p. 34]
100. Diferenciá data drift y concept drift con un ejemplo de cada uno. [T12, p. 40] [T12, p. 41]
101. ¿Cuándo usarías shadow mode, canary y blue-green? ¿Qué dos ideas comparten los patrones de despliegue? [T12, p. 44] [T12, p. 45] [T12, p. 46] [T12, p. 47]
102. Nombrá los cinco grados de automatización. ¿Hay que llegar siempre a la automatización total? [T12, p. 48]
103. ¿Qué requisitos tiene que cumplir la función `predictor(X)`? ¿Por qué no puede reentrenar ni usar variables del notebook? [T12, p. 49] [T12, p. 50]
104. Dá ejemplos de métricas de software, de entrada y de salida para monitorear un sistema. ¿Para qué sirven los umbrales con alarmas? [T12, p. 53] [T12, p. 54]

## Aplicación al TP3

105. ¿Qué columnas del CSV del TP3 no deberían usarse para predecir una cancelación antes de la ejecución? ¿Cómo lo comprobás con los datos? [P03, p. 1] [D04]
106. ¿Qué cohortes pide analizar la consigna y cómo priorizarías una para la estrategia data-centered? [P03, p. 2] [P03, p. 3] [T11, p. 39]
107. ¿Qué split de validación imita mejor la evaluación de la competencia? ¿Qué información te falta para decidirlo? [T11, p. 72] [T11, p. 82] [P04]
108. ¿Cómo se calcula el Competition Score y qué condiciones dan la eximición del final? [P04] [T12, p. 2]
109. Si aplicás SMOTE o un stacking en el TP3, ¿en qué punto del pipeline van para no producir leakage? [T11, p. 60] [T12, p. 25]

## Clustering

110. ¿Qué diferencia al aprendizaje no supervisado del supervisado? Nombrá tres aplicaciones y tres usos del no supervisado. [T14, p. 3] [T14, p. 4] [T14, p. 5]
111. ¿Por qué no hay una única forma correcta de agrupar? Usá el ejemplo de la clase. [T14, p. 8] [T14, p. 9] [T14, p. 10]
112. Diferenciá clustering particional y jerárquico, y clusters basados en prototipos y en densidad. ¿Qué prototipo se usa con atributos categóricos? [T14, p. 11] [T14, p. 12]
113. Escribí la función objetivo de K-means. ¿Por qué la versión por pares de `W(C_k)` y la versión por distancia al centroide tienen el mismo minimizador? [T14, p. 15] [T14, p. 19] [T14, p. 21]
114. Describí los pasos de K-means. ¿Por qué siempre converge y por qué no garantiza el óptimo global? [T14, p. 22] [T14, p. 24]
115. En la figura de seis inicializaciones, ¿qué valores toma el objetivo y cuál elegirías? ¿Cómo se mitiga la dependencia de la inicialización? [T14, p. 26] [T14, p. 27]
116. ¿Por qué no se puede elegir `k` minimizando la WCSS? Explicá el método del codo y el coeficiente de silhouette. [T14, p. 28] [T14, p. 29] [T14, p. 30]
117. En el ejemplo de las medias lunas, K-means tiene mayor silhouette que DBSCAN. ¿Cuál agrupa mejor y qué dice eso del silhouette? [T14, p. 31]
118. Nombrá ventajas y desventajas de K-means. ¿Por qué es sensible a outliers y por qué conviene escalar las variables? [T14, p. 32] [T09, p. 32]
119. ¿Cómo se usa K-means para comprimir una imagen? [T14, p. 33]
120. Definí `ε`, `minPts` y los tres tipos de puntos de DBSCAN. [T14, p. 37] [T14, p. 38]
121. Recorré el algoritmo de DBSCAN. ¿Por qué un punto marcado como ruido lo es solo "por ahora"? [T14, p. 39]
122. Compará K-means y DBSCAN en hiperparámetros, forma de los clusters, outliers y densidades distintas. [T14, p. 31] [T14, p. 32] [T14, p. 41]

## Reducción de dimensionalidad

123. ¿Qué problemas trae la alta dimensionalidad? ¿Cuáles son los dos objetivos de reducirla? [T14, p. 44]
124. Enumerá las propiedades y los pasos de PCA. ¿Por qué hay que estandarizar primero? [T14, p. 45] [T14, p. 46] [T14, p. 48]
125. ¿Cómo elegís la cantidad de componentes? Con el scree plot de la clase, ¿cuántas hacen falta para explicar el 90 % de la varianza? [T14, p. 47]
126. PCA figura como interpretable y como difícil de interpretar. ¿Cómo se concilian las dos afirmaciones? [T14, p. 47] [T14, p. 48]
127. Si usás PCA antes de un clasificador, ¿dónde lo ajustás para evitar leakage? [T14, p. 48]
128. Compará PCA y LDA como proyecciones. [T14, p. 45] [T06, p. 27] [T06, p. 28]
129. Explicá los tres pasos de t-SNE. ¿Qué distribución usa en cada espacio y qué costo minimiza? [T14, p. 50] [T14, p. 51]
130. ¿Qué controla la perplejidad y qué pasa con valores bajos y altos? ¿Qué no se puede interpretar en un gráfico de t-SNE? [T14, p. 52]
131. ¿Por qué en MNIST t-SNE separa los dígitos y PCA a 2D no? ¿Usarías t-SNE como preprocesamiento de un modelo? [T14, p. 53] [T14, p. 54] [T14, p. 50]
