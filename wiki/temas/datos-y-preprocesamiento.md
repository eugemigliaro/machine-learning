# Datos y preprocesamiento

## Tipos de variables

Las variables numéricas representan cantidades. Las categóricas representan etiquetas y, como muchos algoritmos requieren entradas numéricas, suelen transformarse. Si existe un orden real entre categorías puede utilizarse encoding ordinal. **Inferencia didáctica:** para categorías nominales no corresponde inventar un orden que los datos no tienen. [T02, p. 10] [T02, p. 13] [T02, p. 15]

Codificaciones presentadas:

- **One-hot:** crea una columna indicadora por categoría; es simple, pero puede aumentar mucho la dimensionalidad. [T02, p. 18]
- **Frequency encoding:** reemplaza cada categoría por su frecuencia de aparición. [T02, p. 19]
- **Target encoding:** reemplaza la categoría por un promedio del objetivo y puede ser inestable para categorías poco frecuentes; la versión regularizada pondera hacia la media global. [T02, p. 21] [T02, p. 22] [T02, p. 23] **Inferencia operativa:** como usa `y`, debe calcularse sin permitir que dev o test informen al entrenamiento, por la regla general contra leakage. [T02, p. 94]

## Limpieza

Antes de entrenar se revisan valores faltantes o erróneos, outliers y duplicados. [T02, p. 26]

Los faltantes pueden tratarse eliminando observaciones o variables, o imputando mediante estadísticos globales, estadísticos por grupo, una constante o un modelo. La estrategia depende de la cantidad, del significado de la ausencia y del costo de perder datos; una imputación basada en todo el dataset puede introducir leakage. [T02, p. 34] [T02, p. 37] [T02, p. 38]

Los outliers pueden distorsionar estadísticos y sesgar modelos sensibles, pero no son necesariamente errores. [T02, p. 39] Se detectan visualmente o mediante criterios como:

- IQR: fuera de `Q1 - 1.5·IQR` o `Q3 + 1.5·IQR`.
- Z-score: `|z| > 3`, con `z = (x - μ) / σ`.

Ambas reglas aparecen en el material como criterios operativos, no como permiso automático para borrar observaciones. [T02, p. 40] [T02, p. 41] [T02, p. 42]

## Escalado

Las diferencias grandes de escala pueden afectar a algunos modelos. Min-max lleva los valores a un rango fijo y es sensible a outliers; z-score centra y escala con media y desvío, y el material lo presenta como opción predeterminada para muchos modelos. [T03, p. 40] [T03, p. 42] [T03, p. 43]

## Regla contra leakage

Separar test antes de aprender decisiones de limpieza, imputación, codificación, escalado o selección. **Inferencia operativa:** esas transformaciones deben ajustarse con train y aplicarse, sin volver a ajustarlas, a dev y test. [T02, p. 94] [T02, p. 95] [T02, p. 96]
