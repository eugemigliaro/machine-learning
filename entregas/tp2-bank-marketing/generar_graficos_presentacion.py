"""Genera los gráficos resumidos usados en la presentación del TP2.

Los números provienen de `resultados_presentacion.json`, que exporta el notebook.
El gráfico de deriva temporal se recalcula desde el CSV original `[D02]`.
"""

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import PercentFormatter


BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "presentacion-assets"
RESULTS = json.loads((BASE_DIR / "resultados_presentacion.json").read_text())
DATA_PATH = BASE_DIR / "../../material/externo/datasets/bank-additional-full.csv"

NAVY = "#102A43"
BLUE = "#2F80ED"
TEAL = "#2CA58D"
ORANGE = "#F2994A"
RED = "#EB5757"
GRAY = "#9AA5B1"
GRID = "#D9E2EC"


def spanish_number(value, decimals=0):
    formatted = f"{value:,.{decimals}f}"
    return formatted.replace(",", "X").replace(".", ",").replace("X", ".")


def style_axis(ax, grid_axis="y"):
    ax.grid(axis=grid_axis, color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.spines[["top", "right"]].set_visible(False)


def finish_figure(path):
    plt.tight_layout()
    plt.savefig(path, dpi=180, bbox_inches="tight", facecolor="white")
    plt.close()


def short_name(model):
    return (
        model.split(" (")[0]
        .replace("Naive Bayes", "NB")
        .replace("Random Forest", "RF")
    )


plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 13,
    "axes.titleweight": "bold",
    "axes.titlesize": 17,
    "axes.labelsize": 14,
    "xtick.labelsize": 13,
    "ytick.labelsize": 13,
    "legend.fontsize": 12,
})
OUTPUT_DIR.mkdir(exist_ok=True)


# Deriva temporal: tasa de éxito y euribor a lo largo del orden cronológico.
df = pd.read_csv(DATA_PATH, sep=";")
df = df.loc[~df.duplicated()].reset_index(drop=True)
month_order = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
year = 2008 + df["month"].map({m: i for i, m in enumerate(month_order)}).diff().lt(0).cumsum()
rolling = df["y"].eq("yes").astype(float).rolling(1000, center=True).mean()

fig, ax = plt.subplots(figsize=(10, 6.3))
ax.plot(rolling.index, rolling, color=BLUE, linewidth=2.2, label="tasa de yes (ventana de 1.000 llamadas)")
ax.set_ylabel("tasa de yes", color=BLUE)
ax.yaxis.set_major_formatter(PercentFormatter(1.0))
ax.set_xlabel("llamadas en orden cronológico")
style_axis(ax)
ax_macro = ax.twinx()
ax_macro.plot(df.index, df["euribor3m"], color=ORANGE, linewidth=2, alpha=0.9)
ax_macro.set_ylabel("euribor 3 meses (%)", color=ORANGE)
ax_macro.spines[["top"]].set_visible(False)
for boundary in np.flatnonzero(year.diff().ne(0).to_numpy()):
    if boundary > 0:
        ax.axvline(boundary, color=GRAY, linestyle="--", linewidth=1)
for entry in RESULTS["tasa_por_anio"]:
    start = int(np.flatnonzero(year.eq(entry["anio"]).to_numpy())[0])
    last = entry["anio"] == RESULTS["tasa_por_anio"][-1]["anio"]
    separator = "\n" if last else " "
    ax.text(start + 300, 0.32 if last else 0.62,
            f"{entry['anio']}\n{spanish_number(100 * entry['tasa_yes'], 1)} %{separator}yes",
            color=NAVY, fontsize=13, fontweight="bold", va="top", transform=ax.get_xaxis_transform())
ax.set_title("La tasa de éxito sube 10 veces entre 2008 y 2010")
finish_figure(OUTPUT_DIR / "deriva_temporal.png")


# EDA: qué variables categóricas separan y relación en U de la edad.
spread = pd.DataFrame(RESULTS["rango_tasa_por_variable"]).set_index("variable")["rango"].sort_values()
age = pd.DataFrame(RESULTS["tasa_por_edad"])
fig, axes = plt.subplots(1, 2, figsize=(11, 6.6), gridspec_kw={"width_ratios": [1.1, 1]})
excluded = {"loan", "housing", "day_of_week"}
colors = [GRAY if variable in excluded else BLUE for variable in spread.index]
axes[0].barh(spread.index, spread.values, color=colors)
for position, value in enumerate(spread.values):
    axes[0].text(value + 0.8, position, spanish_number(value, 1), va="center", fontsize=12, color=NAVY)
axes[0].set_xlabel("rango de la tasa de yes entre categorías (puntos)")
axes[0].set_title("Excluimos las que casi no separan")
style_axis(axes[0], "x")
axes[1].bar(age["tramo"], 100 * age["tasa_yes"], color=TEAL)
global_rate = 100 * RESULTS["positivos_desarrollo"] / RESULTS["filas_desarrollo"]
axes[1].axhline(global_rate, color=NAVY, linestyle="--", linewidth=1.2,
                label=f"tasa global: {spanish_number(global_rate, 1)} %")
axes[1].legend(frameon=False, loc="upper left")
for position, value in enumerate(100 * age["tasa_yes"]):
    axes[1].text(position, value - 1, spanish_number(value, 0), ha="center", va="top", fontsize=12,
                 color="white", fontweight="bold")
axes[1].set_ylabel("% de yes")
axes[1].set_xlabel("edad")
axes[1].tick_params(axis="x", rotation=35)
axes[1].set_title("La edad se relaciona en U")
style_axis(axes[1])
finish_figure(OUTPUT_DIR / "eda_decisiones.png")


# Benchmark con duration: cuánto infla el AUC el leakage.
benchmark = pd.DataFrame(RESULTS["benchmark_duration"]).set_index("modelo")
fig, ax = plt.subplots(figsize=(9.5, 6.1))
positions = np.arange(len(benchmark))
ax.barh(positions + 0.2, benchmark["sin duration"], height=0.4, color=BLUE, label="sin duration (realista)")
ax.barh(positions - 0.2, benchmark["con duration"], height=0.4, color=RED, label="con duration (leakage)")
for position, (without, with_) in enumerate(benchmark[["sin duration", "con duration"]].to_numpy()):
    ax.text(without + 0.005, position + 0.2, spanish_number(without, 3), va="center", color=NAVY)
    ax.text(with_ + 0.005, position - 0.2, spanish_number(with_, 3), va="center", color=RED, fontweight="bold")
ax.set_yticks(positions, benchmark.index)
ax.set_xlim(0.5, 1.0)
ax.set_xlabel("AUC de validación (5 folds)")
ax.set_title("duration infla el AUC: se conoce al terminar la llamada")
ax.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.17), ncols=2)
style_axis(ax, "x")
finish_figure(OUTPUT_DIR / "benchmark_duration.png")


# Comparación de modelos: por defecto frente a ajustados.
default = pd.DataFrame(RESULTS["resultados_defecto"]).set_index("modelo")
default.index = default.index.map(short_name)
tuned = pd.DataFrame(RESULTS["resultados_ajustados"]).set_index("modelo")
tuned.index = tuned.index.map(short_name)
tuned = tuned.sort_values("auc_val")
fig, axes = plt.subplots(1, 2, figsize=(11, 6.6), gridspec_kw={"width_ratios": [1.25, 1]})
positions = np.arange(len(tuned))
axes[0].barh(positions - 0.2, default.loc[tuned.index, "auc_val"], height=0.4, color=GRAY, label="por defecto")
axes[0].barh(positions + 0.2, tuned["auc_val"], height=0.4, xerr=tuned["auc_val_std"], color=BLUE,
             capsize=3, label="ajustado")
for position, (before, after) in enumerate(zip(default.loc[tuned.index, "auc_val"], tuned["auc_val"])):
    axes[0].text(before + 0.004, position - 0.2, spanish_number(before, 3), va="center", fontsize=12, color=NAVY)
    axes[0].text(after + 0.016, position + 0.2, spanish_number(after, 3), va="center", fontsize=12,
                 color=NAVY, fontweight="bold")
axes[0].set_yticks(positions, tuned.index)
axes[0].set_xlim(0.65, 0.84)
axes[0].set_xlabel("AUC de validación")
axes[0].set_title("AUC: el ajuste cambia el orden")
axes[0].legend(frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.15), ncols=2)
style_axis(axes[0], "x")
axes[1].barh(positions + 0.2, tuned["recall_val"], height=0.4, color=TEAL, label="recall")
axes[1].barh(positions - 0.2, tuned["precision_val"], height=0.4, color=ORANGE, label="precisión")
for position, (recall, precision) in enumerate(tuned[["recall_val", "precision_val"]].to_numpy()):
    axes[1].text(recall + 0.01, position + 0.2, spanish_number(recall, 3), va="center", fontsize=12, color=NAVY)
    axes[1].text(precision + 0.01, position - 0.2, spanish_number(precision, 3), va="center", fontsize=12, color=NAVY)
axes[1].set_yticks(positions, [""] * len(positions))
axes[1].set_xlim(0, 0.85)
axes[1].set_title("Con el umbral elegido por CV")
axes[1].legend(frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.15), ncols=2)
style_axis(axes[1], "x")
finish_figure(OUTPUT_DIR / "comparacion_modelos.png")


# Curvas de validación: Random Forest (profundidad) y KNN (k).
depth = pd.DataFrame(RESULTS["curva_rf_profundidad"])
knn = pd.DataFrame(RESULTS["curva_knn"])
knn = knn.loc[knn["weights"] == "uniform"]
fig, axes = plt.subplots(1, 2, figsize=(11.5, 6.8))
x = np.arange(len(depth))
for column, color, style, label in [("auc_train", TEAL, "--", "train"), ("auc_val", BLUE, "-", "validación")]:
    axes[0].plot(x, depth[column], style, marker="o", color=color, linewidth=2.2, label=label)
axes[0].set_xticks(x, [label.replace("sin límite", "sin\nlímite") for label in depth["valor"]])
axes[0].set_xlabel("max_depth")
axes[0].set_ylabel("AUC")
axes[0].set_title("Random Forest: profundidad")
best_depth = int(np.flatnonzero(depth["valor"].astype(str).eq(str(RESULTS["mejores"]["max_depth"])))[0])
axes[0].scatter([best_depth], [depth["auc_val"].iloc[best_depth]], s=130, color=ORANGE, zorder=3)
axes[0].annotate(f"elegido: {spanish_number(depth['auc_val'].iloc[best_depth], 3)}",
                 xy=(best_depth, depth["auc_val"].iloc[best_depth]), xytext=(best_depth - 2.6, 0.9),
                 arrowprops={"arrowstyle": "->", "color": ORANGE, "lw": 1.8}, color=ORANGE, fontweight="bold")
axes[0].text(len(depth) - 1, 0.875, "sobreajuste:\ntrain 0,999\nval 0,766", ha="right", va="top", color=RED,
             fontsize=12, fontweight="bold")
axes[0].text(0, 0.81, "subajuste\nleve", ha="left", va="bottom", color=NAVY, fontsize=12)
axes[0].legend(frameon=False, loc="upper left")
style_axis(axes[0])
for column, color, style, label in [("auc_train", TEAL, "--", "train"), ("auc_val", BLUE, "-", "validación")]:
    axes[1].plot(knn["valor"], knn[column], style, marker="o", color=color, linewidth=2.2, label=label)
axes[1].set_xscale("log")
axes[1].set_xticks(knn["valor"], [str(int(k)) for k in knn["valor"]])
axes[1].tick_params(axis="x", rotation=45)
axes[1].set_xlabel("k vecinos (escala logarítmica)")
axes[1].set_title("KNN: número de vecinos")
best_k = RESULTS["mejores"]["k"]
best_k_val = float(knn.loc[knn["valor"] == best_k, "auc_val"].iloc[0])
axes[1].scatter([best_k], [best_k_val], s=130, color=ORANGE, zorder=3)
axes[1].annotate(f"elegido k = {best_k}: {spanish_number(best_k_val, 3)}", xy=(best_k, best_k_val),
                 xytext=(12, 0.70), arrowprops={"arrowstyle": "->", "color": ORANGE, "lw": 1.8},
                 color=ORANGE, fontweight="bold")
axes[1].text(1.25, 0.615, "k = 1: train 0,968 · val 0,620", color=RED, fontsize=12, fontweight="bold", va="center")
axes[1].legend(frameon=False, loc="upper right")
style_axis(axes[1])
finish_figure(OUTPUT_DIR / "curvas_validacion.png")


# Modelo final en test.
cm = RESULTS["matriz_confusion_test"]
report = RESULTS["reporte_final"]["test"]
fig, axes = plt.subplots(1, 2, figsize=(11.5, 6.4), gridspec_kw={"width_ratios": [1, 1.15]})
cells = np.array([[cm["TP"], cm["FP"]], [cm["FN"], cm["TN"]]])
axes[0].imshow(np.log(cells), cmap="Blues")
for (row, col), value in np.ndenumerate(cells):
    label = [["TP", "FP"], ["FN", "TN"]][row][col]
    axes[0].text(col, row, f"{label}\n{spanish_number(value)}", ha="center", va="center", fontsize=17,
                 fontweight="bold", color="white" if value > 2000 else NAVY)
axes[0].set_xticks([0, 1], ["real: yes", "real: no"])
axes[0].set_yticks([0, 1], ["llamar", "no llamar"])
axes[0].set_title(f"Test: {spanish_number(RESULTS['filas_test'])} clientes")
axes[0].grid(False)
bars = {
    "clientes llamados": report["llamados"],
    "interesados encontrados (recall)": report["recall"],
    "éxito por llamada (precisión)": report["precision"],
    "éxito llamando a todos": RESULTS["positivos_test"] / RESULTS["filas_test"],
}
colors = [GRAY, TEAL, BLUE, GRAY]
axes[1].barh(list(bars)[::-1], list(bars.values())[::-1], color=colors[::-1])
for position, value in enumerate(list(bars.values())[::-1]):
    axes[1].text(value + 0.01, position, f"{spanish_number(100 * value, 1)} %", va="center", fontsize=14,
                 color=NAVY, fontweight="bold")
axes[1].set_xlim(0, 1)
axes[1].xaxis.set_major_formatter(PercentFormatter(1.0))
axes[1].set_title("Llamar al 27 % → 72 % de los interesados")
style_axis(axes[1], "x")
finish_figure(OUTPUT_DIR / "modelo_final.png")


# Limitación: importancia del contexto y evaluación temporal.
importances = pd.Series(RESULTS["importancias"]).sort_values()
context = {"euribor3m", "nr.employed", "cons.conf.idx", "cons.price.idx", "month"}
temporal = pd.DataFrame(RESULTS["temporal"]).set_index("escenario")
fig, axes = plt.subplots(1, 2, figsize=(11.5, 6.8), gridspec_kw={"width_ratios": [1, 1.05]})
axes[0].barh(importances.index, importances.values,
             color=[ORANGE if name in context else BLUE for name in importances.index])
axes[0].set_xlabel("importancia en el Random Forest final")
axes[0].set_title(f"Contexto (naranja): {spanish_number(100 * RESULTS['importancia_contexto'], 0)} %",
                  fontsize=16)
style_axis(axes[0], "x")
scenarios = {
    "test\n(aleatorio)": RESULTS["reporte_final"]["test"]["auc"],
    "2010\nCV aleatoria": temporal.loc["CV aleatoria, filas de 2010", "auc"],
    "2010\nentrenado con\n2008–2009": temporal.loc["entrenado en 2008-2009, filas de 2010", "auc"],
}
axes[1].bar(list(scenarios), list(scenarios.values()), color=[BLUE, GRAY, RED], width=0.6)
for position, value in enumerate(scenarios.values()):
    axes[1].text(position, value + 0.008, spanish_number(value, 3), ha="center", fontsize=15,
                 fontweight="bold", color=NAVY)
axes[1].set_ylim(0.5, 0.86)
axes[1].set_ylabel("AUC")
axes[1].set_title("AUC con datos del futuro", fontsize=16)
style_axis(axes[1])
finish_figure(OUTPUT_DIR / "limitacion_temporal.png")


# Apéndice: SVM con y sin balanceo de clases.
svm = pd.DataFrame(RESULTS["curva_svm_c"])
fig, ax = plt.subplots(figsize=(9.5, 6.1))
for weight, color, label in [("None", GRAY, "sin balanceo"), ("balanced", BLUE, "class_weight = balanced")]:
    curve = svm.loc[svm["class_weight"] == weight]
    ax.plot(curve["valor"], curve["auc_train"], "--", marker="o", color=color, alpha=0.7, label=f"train, {label}")
    ax.plot(curve["valor"], curve["auc_val"], "-", marker="o", color=color, linewidth=2.4,
            label=f"validación, {label}")
ax.set_xscale("log")
ax.set_xlabel("C (escala logarítmica)")
ax.set_ylabel("AUC")
ax.set_title("SVM (RBF): balancear clases importa más que C")
ax.legend(frameon=False, fontsize=11, loc="upper left")
style_axis(ax)
finish_figure(OUTPUT_DIR / "svm_balanceo.png")

print(f"Gráficos generados en {OUTPUT_DIR}")
