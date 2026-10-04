---
title: "TP2 · Bank Marketing"
subtitle: "Clasificación supervisada: ¿a qué clientes llamar?"
date: "Machine Learning · 2026"
lang: es-AR
---

## Problema y datos

**Objetivo:** predecir si el cliente contrata un plazo fijo (`y`) para priorizar a quién llamar.

- **41.188** llamadas · 20 variables · **11,3 %** respondió que sí · quitamos 12 duplicados exactos.
- Split estratificado por `y`, semilla 42: **32.940** desarrollo (80 %) · **8.236** test (20 %).

**Qué datos usamos en cada etapa**

- **EDA y decisiones** → sólo desarrollo.
- **Modelo, hiperparámetros y umbral** → 5-fold CV en desarrollo.
- **Desempeño esperado** → test, una sola vez.

*[P02, p. 1] [D02] [T02, p. 89]*

## Los datos cambian con el tiempo

:::: {.columns}
::: {.column width="65%"}
![](presentacion-assets/deriva_temporal.png)
:::
::: {.column width="35%"}
- De **4,8 %** (2008) a **52,1 %** (2010) de "yes".
- Los índices macro funcionan como un reloj: r de 0,91 a 0,97.
- **Split aleatorio estratificado**, como pide la consigna.
- Test será optimista para campañas futuras: lo medimos al final.

*[D03] [P02, p. 2]*
:::
::::

## Del EDA a las decisiones

:::: {.columns}
::: {.column width="65%"}
![](presentacion-assets/eda_decisiones.png)
:::
::: {.column width="35%"}
- Excluimos `housing`, `loan`, `day_of_week`, `pdays` y `emp.var.rate`.
- `unknown` como categoría: `default` desconocido acepta 5,3 % vs. 12,8 %.
- `log1p` en `campaign` y `previous`.
- Edad en U: relación no lineal.
- Verificado por CV: `nr.employed` volvió (+0,007 en NB).

*[P02, p. 1] [T09, p. 39]*
:::
::::

## `duration`: leakage

:::: {.columns}
::: {.column width="65%"}
![](presentacion-assets/benchmark_duration.png)
:::
::: {.column width="35%"}
- Se conoce **al terminar** la llamada.
- Con ella, RF pasa de 0,766 a **0,938** de AUC.
- Ese número no es alcanzable antes de llamar.
- **La excluimos de todos los modelos.**

*[D03] [P02, p. 1]*
:::
::::

## Pipeline, validación y métricas

- **Pipeline por fold:** transformaciones fijas (exclusiones, `default_no`, `log1p`) → escalado → one-hot, o discretización en NB categórico → modelo.
- **5 folds estratificados:** ~742 positivos por fold.
- **AUC:** priorizar es ordenar clientes; al azar vale 0,5.
- **Recall:** perder un interesado (FN) cuesta más que una llamada de más (FP).
- **Accuracy no:** "siempre no" acierta el 88,7 % sin encontrar a nadie.
- **Umbral:** punto de la curva ROC más cercano a (0, 1), con predicciones out-of-fold de desarrollo.

*[T02, pp. 94, 96] [T04, pp. 26, 41, 51, 52]*

## Comparación de modelos

:::: {.columns}
::: {.column width="65%"}
![](presentacion-assets/comparacion_modelos.png)
:::
::: {.column width="35%"}
- **RF** gana en AUC y en recall.
- **SVM:** balancear clases lo lleva de 0,700 a 0,777.
- **KNN:** `k` pasa de 5 a 321.
- **NB categórico:** 0,780 sin ajustar.

*[P02, p. 2]*
:::
::::

## Sobreajuste y subajuste

:::: {.columns}
::: {.column width="65%"}
![](presentacion-assets/curvas_validacion.png)
:::
::: {.column width="35%"}
- **RF sin límite:** train 0,999 · validación 0,766 → sobreajuste.
- `max_depth = 2`: subajuste leve.
- Elegimos `max_depth = 10`.
- **KNN con `k = 1`** memoriza; con `k` grande la brecha se cierra.

*[T07, p. 50] [T09, p. 29]*
:::
::::

## Modelo final en test

:::: {.columns}
::: {.column width="65%"}
![](presentacion-assets/modelo_final.png)
:::
::: {.column width="35%"}
**RF** · profundidad 10 · 400 árboles · umbral 0,084

- Reentrenado con desarrollo; test consultado **una vez**.
- **AUC 0,809** (0,791–0,826)
- **Recall 0,718** (0,691–0,746)
- Precisión 0,300 vs. 0,113 llamando a todos.

*IC 95 % bootstrap · [T02, p. 88]*
:::
::::

## Limitación: el modelo aprende el período

:::: {.columns}
::: {.column width="65%"}
![](presentacion-assets/limitacion_temporal.png)
:::
::: {.column width="35%"}
- Índices macro y `month`: **59 %** de la importancia.
- Entrenado con 2008–2009, el AUC en 2010 cae a **0,678**.
- Con el umbral fijo llamaría al **100 %** de 2010.

*[T07, p. 71]*
:::
::::

## Conclusiones

1. **RF** captura no linealidades (edad) e interacciones, no necesita escalar, y limitar la profundidad controló el sobreajuste.
2. **Supuestos:** NB sufre la correlación (`euribor3m`–`nr.employed`: 0,94) y las binarias no gaussianas; KNN, la superposición de clases y las 46 dimensiones; SVM, el desbalance.
3. **Errores:** FN = depósito perdido; FP = llamada fallida. En test: 262 FN y 1.555 FP, es decir 2,3 llamadas fallidas por éxito vs. 7,9 llamando a todos.
4. **Mejoras:** validación temporal y reentrenamiento, umbral por costo o capacidad, más información previa a la llamada.

**Esperamos AUC ≈ 0,81 y recall ≈ 0,72 para clientes como los de 2008–2010; menos para campañas futuras.**

## Apéndice · SVM y desbalance

:::: {.columns}
::: {.column width="65%"}
![](presentacion-assets/svm_balanceo.png)
:::
::: {.column width="35%"}
- Sin balanceo: validación de 0,70 a 0,71 con cualquier `C`.
- Con `balanced`, un error en un positivo pesa ~4,4 y en un negativo ~0,56.
- `C` grande sube train y abre la brecha.
- Kernels con `C = 0,1`: lineal 0,769 · polinómico 0,777 · RBF 0,777.

*[T08, p. 49]*
:::
::::

## Apéndice · Exclusiones verificadas por CV

Cambio de AUC de validación al agregar cada grupo al conjunto del EDA. Con el RF ajustado, housing, loan y day_of_week tampoco mejoran (0,7979 vs. 0,7984). *[P02, p. 1]*

| Grupo agregado | NB gauss. | NB categ. | RF | KNN |
|---|---:|---:|---:|---:|
| pdays | +0,000 | 0,000 | −0,001 | 0,000 |
| housing, loan, day_of_week | −0,001 | 0,000 | +0,007 | −0,008 |
| nr.employed | **+0,007** | **+0,004** | 0,000 | 0,000 |
| emp.var.rate + nr.employed | +0,009 | +0,003 | −0,002 | −0,001 |

## Apéndice · Decisiones defendibles

- **¿Por qué no un split temporal?** Test tendría 31–46 % de positivos frente a 6–7 % en desarrollo: mezclaría la calidad del modelo con el cambio de distribución. Lo medimos aparte.
- **¿Por qué un umbral tan bajo (0,084)?** Con 11 % de positivos, el umbral 0,5 deja al RF con recall 0,23.
- **¿Por qué AUC y no accuracy?** "Siempre no" acierta 88,7 % sin encontrar ningún interesado.
- **¿Por qué test dio mejor que CV?** 0,809 vs. 0,798 está dentro de la variabilidad (IC 95 %: 0,791–0,826). No cambiamos nada después de mirarlo.
