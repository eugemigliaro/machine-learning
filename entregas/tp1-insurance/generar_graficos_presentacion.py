"""Genera los gráficos resumidos usados en la presentación del TP1."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


OUTPUT_DIR = Path(__file__).parent / "presentacion-assets"

NAVY = "#102A43"
BLUE = "#2F80ED"
TEAL = "#2CA58D"
ORANGE = "#F2994A"
RED = "#EB5757"
GRID = "#D9E2EC"


def spanish_number(value, decimals=0):
    formatted = f"{value:,.{decimals}f}"
    return formatted.replace(",", "X").replace(".", ",").replace("X", ".")


def finish_figure(path):
    plt.tight_layout()
    plt.savefig(path, dpi=180, bbox_inches="tight", facecolor="white")
    plt.close()


plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.titleweight": "bold",
    "axes.titlesize": 17,
    "axes.labelsize": 12,
    "xtick.labelsize": 11,
    "ytick.labelsize": 11,
})


# EDA: diferencia estructural de charges según smoker.
groups = ["No fumador", "Fumador"]
means = [8535.55, 31986.79]
fig, ax = plt.subplots(figsize=(8.2, 4.8))
bars = ax.bar(groups, means, color=[BLUE, ORANGE], width=0.58)
ax.set_title("El hábito de fumar separa dos escalas de costos")
ax.set_ylabel("Media de charges")
ax.grid(axis="y", color=GRID, linewidth=0.8)
ax.set_axisbelow(True)
ax.spines[["top", "right"]].set_visible(False)
for bar, value in zip(bars, means):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        value + 900,
        f"$ {spanish_number(value, 0)}",
        ha="center",
        va="bottom",
        color=NAVY,
        fontsize=13,
        fontweight="bold",
    )
ax.set_ylim(0, 37000)
finish_figure(OUTPUT_DIR / "eda_smoker.png")


# Comparación de complejidad polinómica.
degrees = np.array([1, 2, 3])
train_rmse = np.array([6135.04, 4795.02, 4609.56])
validation_rmse = np.array([6157.57, 4908.79, 5040.02])
width = 0.32
fig, ax = plt.subplots(figsize=(8.2, 4.8))
train_bars = ax.bar(
    degrees - width / 2,
    train_rmse,
    width,
    label="Train",
    color=TEAL,
)
validation_bars = ax.bar(
    degrees + width / 2,
    validation_rmse,
    width,
    label="Validación",
    color=BLUE,
)
ax.set_title("Grado 2 logra el menor RMSE de validación")
ax.set_xlabel("Grado polinómico")
ax.set_ylabel("RMSE")
ax.set_xticks(degrees)
ax.set_ylim(4000, 6500)
ax.grid(axis="y", color=GRID, linewidth=0.8)
ax.set_axisbelow(True)
ax.spines[["top", "right"]].set_visible(False)
ax.legend(frameon=False, ncols=2, loc="upper right")
for bars in [train_bars, validation_bars]:
    for bar in bars:
        value = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 45,
            spanish_number(value, 0),
            ha="center",
            va="bottom",
            fontsize=9.5,
            color=NAVY,
        )
ax.annotate(
    "mejor validación",
    xy=(2 + width / 2, validation_rmse[1]),
    xytext=(2.45, 4400),
    arrowprops={"arrowstyle": "->", "color": ORANGE, "lw": 2},
    color=ORANGE,
    fontweight="bold",
)
finish_figure(OUTPUT_DIR / "comparacion_grados.png")


# Efecto conjunto de lambda en RMSE y sparsity.
lambdas = np.array([0, 1, 10, 100, 1000])
validation = np.array([4908.79, 4907.90, 4899.64, 4872.42, 5250.36])
active = np.array([44, 40.1, 39.0, 23.4, 4.0])
fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.6))

axes[0].plot(lambdas, validation, marker="o", color=BLUE, linewidth=2.5)
axes[0].scatter([100], [4872.42], s=110, color=ORANGE, zorder=3)
axes[0].set_xscale("symlog", linthresh=1)
axes[0].set_xticks(lambdas)
axes[0].set_xticklabels(["0", "1", "10", "100", "1000"])
axes[0].set_title("Error de validación")
axes[0].set_xlabel("λ de L1")
axes[0].set_ylabel("RMSE")
axes[0].grid(color=GRID, linewidth=0.8)
axes[0].spines[["top", "right"]].set_visible(False)
axes[0].annotate(
    "mínimo: 4.872",
    xy=(100, 4872.42),
    xytext=(9, 5120),
    arrowprops={"arrowstyle": "->", "color": ORANGE, "lw": 1.8},
    color=ORANGE,
    fontweight="bold",
)

axes[1].plot(lambdas, active, marker="o", color=TEAL, linewidth=2.5)
axes[1].scatter([100], [23.4], s=110, color=ORANGE, zorder=3)
axes[1].set_xscale("symlog", linthresh=1)
axes[1].set_xticks(lambdas)
axes[1].set_xticklabels(["0", "1", "10", "100", "1000"])
axes[1].set_title("Complejidad efectiva")
axes[1].set_xlabel("λ de L1")
axes[1].set_ylabel("Coeficientes activos medios")
axes[1].set_ylim(0, 48)
axes[1].grid(color=GRID, linewidth=0.8)
axes[1].spines[["top", "right"]].set_visible(False)
axes[1].annotate(
    "23,4 activos",
    xy=(100, 23.4),
    xytext=(4, 10),
    arrowprops={"arrowstyle": "->", "color": ORANGE, "lw": 1.8},
    color=ORANGE,
    fontweight="bold",
)

fig.suptitle("L1: mejora modesta y modelo más disperso", fontsize=17, fontweight="bold")
finish_figure(OUTPUT_DIR / "regularizacion_l1.png")

