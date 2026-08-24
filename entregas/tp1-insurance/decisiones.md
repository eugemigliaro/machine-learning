# Decisiones y supuestos

## Confirmadas

### Dataset

Se usa Insurance Charges, con `charges` como variable objetivo y las otras seis columnas como variables predictoras. [P01, p. 1] [D01]

### Reserva de test

Se reserva el 10 % como test y se utiliza el 90 % restante para desarrollo. Después de eliminar una copia de la fila duplicada quedan 1.337 observaciones: 134 casos de test y 1.203 casos para validación cruzada.

Se prioriza aumentar los datos disponibles en cada ajuste del modelo. Como contrapartida, se acepta que el RMSE final calculado sobre 134 casos tendrá más variabilidad que con una reserva mayor. Test no se usará para elegir preprocesamiento, características, grado polinómico ni regularización. [P01, pp. 2–3] [T02, pp. 89, 94–96]

### Reproducibilidad

Se fija `random_state = 42` para que la partición y los folds puedan reproducirse.

### Partición y validación cruzada

El split 90/10 y los 10 folds se estratifican por `smoker`. En cross-validation cada ajuste usa 1.082 o 1.083 casos y cada validación 120 o 121. Cada observación de desarrollo aparece exactamente una vez en validación. [T03, pp. 12, 15]

### Duplicado exacto

Las filas originales 195 y 581 contienen los mismos seis predictores y el mismo valor de `charges`. Se conserva la primera y se elimina la segunda de la copia de trabajo antes del split. Mantener ambas podría ubicar una en entrenamiento y otra en validación, produciendo una estimación optimista. El CSV `[D01]` no se modifica.

## Observaciones de integridad

- El CSV tiene 1.338 observaciones, 7 columnas y no contiene valores faltantes. [D01]
- Existe un duplicado exacto: las filas originales 195 y 581 contienen los mismos seis predictores y el mismo valor de `charges`.

## Resultados del EDA de desarrollo

- No hay faltantes, duplicados remanentes ni categorías inesperadas.
- `charges` tiene media 13.350,56, mediana 9.447,25 y máximo 63.770,43; su distribución presenta asimetría positiva.
- La media de `charges` es 31.986,79 para fumadores y 8.535,55 para no fumadores.
- Las correlaciones de Pearson de `charges` con `age`, `bmi` y `children` son 0,289, 0,196 y 0,072 respectivamente. Esto describe asociación lineal y no descarta relaciones no lineales. [T03, pp. 48–51]
- El criterio IQR marca 7 valores de `bmi` (0,58 %) y 118 de `charges` (9,81 %); no marca valores de `age` ni `children`. Entre los 118 costos atípicos, 116 corresponden a fumadores.
- Al recalcular IQR dentro de cada grupo de `smoker`, aparecen 6 BMI altos en no fumadores y 1 en fumadores. Para `charges` aparecen 43 costos altos en no fumadores y ninguno en fumadores; el límite superior de estos últimos es 72.265,44, por encima del máximo observado de 63.770,43.
- La diferencia entre el IQR global y el condicionado muestra que gran parte de los supuestos outliers globales de `charges` son una consecuencia de mezclar dos distribuciones con escalas diferentes.

## Decisiones confirmadas tras el EDA

- Conservar los BMI extremos porque son posibles y no muestran evidencia de error de carga.
- Conservar los valores altos de `charges` porque están estructuralmente asociados a `smoker`; eliminarlos cambiaría el problema que se quiere modelar.
- Conservar inicialmente las seis características y comparar modelos mediante validación cruzada.
- Aplicar one-hot con una categoría de referencia a las categóricas nominales y estandarización a las numéricas dentro de cada fold.

## Resultado de regresión lineal

- Referencia que predice la media: RMSE de validación 12.096,21 ± 881,00.
- Regresión lineal: RMSE de train 6.135,04 ± 64,44 y de validación 6.157,57 ± 593,14.
- La brecha media train-validación es pequeña. El siguiente experimento evaluará si términos polinómicos reducen el error sin abrir una brecha excesiva.

## Comparación de grados polinómicos

| Grado | Términos generados | RMSE train | RMSE validación | Brecha |
|---:|---:|---:|---:|---:|
| 1 | 8 | 6.135,04 | 6.157,57 | 22,53 |
| 2 | 44 | 4.795,02 | **4.908,79** | 113,77 |
| 3 | 164 | 4.609,56 | 5.040,02 | 430,46 |

El grado 2 queda como candidato actual: mejora aproximadamente 20 % el RMSE de validación respecto del lineal. El grado 3 reduce train pero empeora validación y aumenta la brecha, señal de complejidad excesiva frente a grado 2. [T02, pp. 52–53] [T02, pp. 76–77]

## Comparación de regularización L1

Sobre el polinomio de grado 2 se comparan `lambda` 1, 10, 100 y 1000 en los mismos diez folds. Las 44 columnas polinómicas se estandarizan dentro de cada fold antes de aplicar L1, porque la penalización depende de la escala de los predictores. [T03, p. 90]

| Lambda | RMSE train | RMSE validación | Brecha | Coeficientes activos medios |
|---:|---:|---:|---:|---:|
| 0 (sin L1) | 4.795,02 | 4.908,79 | 113,77 | — |
| 1 | 4.795,04 | 4.907,90 | 112,86 | 40,1 |
| 10 | 4.796,78 | 4.899,64 | 102,86 | 39,0 |
| 100 | 4.839,40 | **4.872,42** | 33,02 | 23,4 |
| 1000 | 5.285,18 | 5.250,36 | -34,82 | 4,0 |

`lambda=100` queda seleccionado porque alcanza el menor RMSE medio de validación. Mejora 36,37 (0,74 %) respecto del grado 2 sin L1 y obtiene menor RMSE en 7 de 10 folds. La magnitud es pequeña frente a la dispersión entre folds, por lo que se considera una mejora modesta. `lambda=1000` muestra penalización excesiva y subajuste. El candidato final pasa a ser grado 2 con L1 y `lambda=100`; test no se consultó para tomar esta decisión. [P01, pp. 2–3] [T02, p. 89]

## Evaluación final

Una vez congelada la configuración, se reentrena el pipeline de grado 2 con L1 y `lambda=100` sobre los 1.203 casos de desarrollo completos. El modelo final conserva 22 de los 44 coeficientes distintos de cero.

La única evaluación sobre los 134 casos de test obtiene **RMSE 3.957,83**. Este valor es menor que el RMSE medio de validación de 4.872,42, pero no se usa para cambiar el modelo. Se reporta como estimación final para datos nuevos con la cautela de que test es pequeño y la validación mostró un desvío de 776,46 entre folds. [P01, p. 3] [T02, pp. 89, 94–96]
