# TP2 — Bank Marketing

Resolución del TP2 de clasificación supervisada con el dataset Bank Marketing. La consigna oficial está registrada como `[P02]`.

## Fuente

El dataset está registrado como `[D02]` y su descripción de atributos como `[D03]`. Se leen sin modificar desde:

```text
../../material/externo/datasets/bank-additional-full.csv
../../material/externo/datasets/bank-additional-names.txt
```

## Entorno

En Ubuntu 26.04 las dependencias se instalan con `apt`, porque el Python del sistema no admite `pip` global:

```bash
sudo apt install python3-sklearn python3-pandas python3-matplotlib python3-seaborn \
  jupyter-notebook python3-ipykernel python3-nbconvert
```

`requirements.txt` documenta los rangos de versión equivalentes para instalar con `pip` dentro de un entorno virtual.

Abrir `tp2_bank_marketing.ipynb` con `jupyter notebook` o desde el editor. Para ejecutarlo completo sin interfaz:

```bash
python3 -m nbconvert --to notebook --execute --inplace tp2_bank_marketing.ipynb
```

El notebook fue verificado con Python 3.14.4, scikit-learn 1.7.2, pandas 2.3.3, matplotlib 3.10.7 y seaborn 0.13.2.

## Estado

- Dataset obtenido y registrado como `[D02]`, con su descripción como `[D03]`.
- Esquema e integridad verificados: 41.188 filas, 21 columnas, sin `NaN`.
- 12 duplicados exactos eliminados de la copia de trabajo, por el mismo criterio que en el TP1.
- Faltantes codificados como `unknown` cuantificados; `pdays = 999` y `poutcome` revisados.
- Balance de clases y deriva temporal analizados para decidir la partición.
- Test reservado: split aleatorio estratificado por `y`, 20 %, con 32.940 filas de desarrollo y 8.236 de test.
- EDA de desarrollo ejecutado: faltantes, categorías raras, distribuciones, tasa de `yes` por categoría, edad, AUC univariado, correlaciones y `duration`.
- Decisiones de preprocesamiento confirmadas e implementadas en un pipeline. Las transformaciones fijas van antes; el escalado y el one-hot se ajustan dentro de cada fold.
- Métricas elegidas: AUC (principal) y recall con umbral elegido por la curva ROC out-of-fold. Validación cruzada estratificada de 5 folds.
- Exclusiones verificadas por validación cruzada; `nr.employed` se reincorporó.
- Benchmark con `duration`: el AUC de RF sube de 0,766 a 0,938 por leakage.
- Curvas de validación de KNN (`k`, ponderación), RF (`max_depth`, `n_estimators`) y SVM (`C`, balanceo, kernel).
- Mejor modelo en validación: Random Forest con `max_depth = 10` y 400 árboles, AUC 0,798 y recall 0,690.
- Pendiente: confirmar el modelo final y evaluarlo una única vez en test.

La primera ejecución completa tarda alrededor de una hora, sobre todo por SVM. Los resultados quedan en `cache/` y las ejecuciones siguientes tardan segundos.
