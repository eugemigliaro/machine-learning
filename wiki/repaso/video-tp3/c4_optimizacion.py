"""Capítulo 4: gradient boosting, combinación de modelos y nuestra optimización."""

import numpy as np
from manim import *

from base import *

# Datos de juguete para la animación de boosting (no son datos del TP).
RNG = np.random.default_rng(4)
X_DEMO = np.sort(RNG.uniform(0.2, 9.8, 46))
Y_DEMO = 2.2 + 1.3 * np.sin(0.85 * X_DEMO) + 0.22 * X_DEMO + RNG.normal(0, 0.28, X_DEMO.size)
GRILLA = np.linspace(0, 10, 500)
TASA = 0.4


def arbol_1d(x, r, profundidad=2, min_hoja=3):
    """Árbol de regresión en una dimensión. Devuelve una función que predice."""
    if profundidad == 0 or x.size < 2 * min_hoja:
        valor = r.mean()
        return lambda z: np.full_like(z, valor, dtype=float)
    mejor = None
    for i in range(min_hoja, x.size - min_hoja + 1):
        izq, der = r[:i], r[i:]
        sse = ((izq - izq.mean()) ** 2).sum() + ((der - der.mean()) ** 2).sum()
        if mejor is None or sse < mejor[0]:
            mejor = (sse, i)
    i = mejor[1]
    corte = (x[i - 1] + x[i]) / 2
    f_izq = arbol_1d(x[:i], r[:i], profundidad - 1, min_hoja)
    f_der = arbol_1d(x[i:], r[i:], profundidad - 1, min_hoja)
    return lambda z: np.where(z < corte, f_izq(z), f_der(z))


def boosting(n):
    """Predicciones en la grilla y en los puntos después de cada árbol."""
    pred_x = np.zeros_like(Y_DEMO)
    pred_g = np.zeros_like(GRILLA)
    historia = []
    arboles = []
    for k in range(n):
        r = Y_DEMO - pred_x
        f = arbol_1d(X_DEMO, r)
        eta = 1.0 if k == 0 else TASA
        arboles.append(f)
        pred_x = pred_x + eta * f(X_DEMO)
        pred_g = pred_g + eta * f(GRILLA)
        historia.append((pred_x.copy(), pred_g.copy()))
    return historia, arboles


HISTORIA, ARBOLES = boosting(80)


def arbolito(color, escala=1.0):
    tri = Triangle(color=color, fill_color=color, fill_opacity=0.35, stroke_width=2).scale(0.42 * escala)
    tronco = Line(tri.get_bottom(), tri.get_bottom() + DOWN * 0.18 * escala, color=color, stroke_width=3)
    return VGroup(tri, tronco)


class Optimizacion(Escena):
    CAPITULO = "4 · Optimizar"

    def construct(self):
        # o1 ---------------------------------------------------------------------
        self.seg("o1")
        titulo = T("Optimizar", 56, BLANCO, weight=BOLD)
        self.play(Write(titulo), run_time=1.2)
        self.hasta(1)
        gb = T("gradient boosting", 44, VIOLETA).next_to(titulo, DOWN, buff=0.6)
        self.play(FadeIn(gb, shift=UP * 0.2), run_time=0.8)
        self.hasta(2)
        rf = T("frente a  Random Forest", 36, VERDE).next_to(gb, DOWN, buff=0.3)
        self.play(FadeIn(rf), run_time=0.8)

        # o2: bagging --------------------------------------------------------------
        self.seg("o2")
        self.limpiar()
        t_bag = T("Random Forest = bagging", 38, VERDE).to_edge(UP, buff=0.8)
        datos = tarjeta(T("datos", 28), buff=0.25).shift(LEFT * 5.2)
        muestras = VGroup(*[tarjeta(T(f"bootstrap {i + 1}", 22), buff=0.15) for i in range(4)]).arrange(DOWN, buff=0.3).shift(LEFT * 2.2)
        arboles = VGroup(*[arbolito(VERDE) for _ in range(4)])
        for a, m in zip(arboles, muestras):
            a.next_to(m, RIGHT, buff=0.9)
        promedio = tarjeta(T("promedio", 28, VERDE), color=VERDE, buff=0.25).shift(RIGHT * 3.6)
        flechas1 = VGroup(*[Arrow(datos.get_right(), m.get_left(), buff=0.1, color=GRIS_OSCURO, stroke_width=2) for m in muestras])
        flechas2 = VGroup(*[Arrow(m.get_right(), a.get_left(), buff=0.1, color=GRIS_OSCURO, stroke_width=2) for m, a in zip(muestras, arboles)])
        flechas3 = VGroup(*[Arrow(a.get_right(), promedio.get_left(), buff=0.1, color=GRIS_OSCURO, stroke_width=2) for a in arboles])
        self.play(FadeIn(t_bag), FadeIn(datos), run_time=0.8)
        self.play(Create(flechas1), FadeIn(muestras), run_time=1.2)
        self.play(Create(flechas2), LaggedStart(*[GrowFromCenter(a) for a in arboles], lag_ratio=0.0), run_time=1.2)
        par = T("en paralelo, independientes", 24, GRIS).next_to(arboles, DOWN, buff=0.3)
        self.play(FadeIn(par), run_time=0.6)
        self.hasta(1)
        self.play(Create(flechas3), FadeIn(promedio), run_time=1.0)
        self.hasta(2)
        reduce = T("reduce la varianza", 34, VERDE).next_to(promedio, DOWN, buff=0.9).shift(RIGHT * 0.5)
        self.play(Write(reduce), run_time=1.0)

        # o3 a o6: boosting paso a paso ------------------------------------------------
        self.seg("o3")
        self.limpiar()
        t_boost = T("boosting: árboles en secuencia", 34, VIOLETA).to_edge(UP, buff=0.55)
        self.play(FadeIn(t_boost), run_time=0.6)
        self.hasta(1)
        ax = Axes(x_range=[0, 10, 1], y_range=[0, 6.5, 1], x_length=10, y_length=3.3, tips=False,
                  axis_config={"color": GRIS_OSCURO, "include_numbers": False}).shift(UP * 0.85)
        puntos = VGroup(*[Dot(ax.c2p(x, y), radius=0.06, color=BLANCO) for x, y in zip(X_DEMO, Y_DEMO)])
        etq_ax = T("datos de juguete", 20, GRIS_OSCURO).next_to(ax, DOWN, buff=0.12).align_to(ax, RIGHT)
        self.play(Create(ax), FadeIn(puntos, lag_ratio=0.03), FadeIn(etq_ax), run_time=1.2)
        self.hasta(2)

        def curva(pred_g, color=AMARILLO, ancho=4):
            return ax.plot_line_graph(GRILLA, np.clip(pred_g, 0, 6.5), line_color=color, add_vertex_dots=False,
                                      stroke_width=ancho)["line_graph"]

        pred = curva(HISTORIA[0][1])
        etq_pred = T("predicción con 1 árbol", 24, AMARILLO).next_to(ax, DOWN, buff=0.15).align_to(ax, LEFT)
        self.play(Create(pred), FadeIn(etq_pred), run_time=1.4)

        # o4: residuos y segundo árbol
        self.seg("o4")
        pred_x = HISTORIA[0][0]
        residuos = VGroup(*[Line(ax.c2p(x, p), ax.c2p(x, y), color=ROJO, stroke_width=3)
                            for x, y, p in zip(X_DEMO, Y_DEMO, pred_x)])
        self.play(LaggedStart(*[Create(r) for r in residuos], lag_ratio=0.03), run_time=1.6)
        ax_r = Axes(x_range=[0, 10, 1], y_range=[-1.6, 1.6, 0.5], x_length=10, y_length=1.9, tips=False,
                    axis_config={"color": GRIS_OSCURO, "include_numbers": False}).shift(DOWN * 2.45)
        etq_r = T("residuos", 22, ROJO).next_to(ax_r, LEFT, buff=0.15)
        self.hasta(1)
        r1 = Y_DEMO - pred_x
        puntos_r = VGroup(*[Dot(ax_r.c2p(x, r), radius=0.05, color=ROJO) for x, r in zip(X_DEMO, r1)])
        self.play(FadeOut(etq_pred), Create(ax_r), FadeIn(etq_r), TransformFromCopy(residuos, puntos_r), run_time=1.4)
        self.hasta(2)
        arbol2 = ax_r.plot_line_graph(GRILLA, ARBOLES[1](GRILLA), line_color=VIOLETA, add_vertex_dots=False,
                                      stroke_width=4)["line_graph"]
        etq_a2 = T("árbol nuevo: aprende los residuos", 22, VIOLETA).next_to(ax_r, UP, buff=0.05)
        self.play(Create(arbol2), FadeIn(etq_a2), run_time=1.2)

        # o5: sumar con tasa de aprendizaje
        self.seg("o5")
        formula = M(f'nueva predicción = anterior + <span foreground="{AMARILLO}">η</span> × árbol 2'
                    f'    (η = {num(TASA, 1)})', 26).next_to(t_boost, DOWN, buff=0.15)
        self.play(FadeIn(formula), run_time=0.8)
        pred2 = curva(HISTORIA[1][1])
        residuos2 = VGroup(*[Line(ax.c2p(x, p), ax.c2p(x, y), color=ROJO, stroke_width=3)
                             for x, y, p in zip(X_DEMO, Y_DEMO, HISTORIA[1][0])])
        self.play(Transform(pred, pred2), Transform(residuos, residuos2), run_time=1.5)
        self.hasta(1)
        contador = T("árboles: 2", 26, VIOLETA).next_to(ax, DOWN, buff=0.15).align_to(ax, LEFT)
        self.play(FadeIn(contador), run_time=0.4)
        for k in [2, 3]:
            rk = Y_DEMO - HISTORIA[k - 1][0]
            nuevos_r = VGroup(*[Dot(ax_r.c2p(x, r), radius=0.05, color=ROJO) for x, r in zip(X_DEMO, rk)])
            arbol_k = ax_r.plot_line_graph(GRILLA, ARBOLES[k](GRILLA), line_color=VIOLETA, add_vertex_dots=False,
                                           stroke_width=4)["line_graph"]
            self.play(Transform(puntos_r, nuevos_r), Transform(arbol2, arbol_k), run_time=0.8)
            residuos_k = VGroup(*[Line(ax.c2p(x, p), ax.c2p(x, y), color=ROJO, stroke_width=3)
                                  for x, y, p in zip(X_DEMO, Y_DEMO, HISTORIA[k][0])])
            self.play(Transform(pred, curva(HISTORIA[k][1])), Transform(residuos, residuos_k),
                      Transform(contador, T(f"árboles: {k + 1}", 26, VIOLETA).move_to(contador, aligned_edge=LEFT)),
                      run_time=0.9)

        # o6: muchos árboles
        self.seg("o6")
        for k in [7, 15, 30, 50, 79]:
            rk = Y_DEMO - HISTORIA[k][0]
            residuos_k = VGroup(*[Line(ax.c2p(x, p), ax.c2p(x, y), color=ROJO, stroke_width=3)
                                  for x, y, p in zip(X_DEMO, Y_DEMO, HISTORIA[k][0])])
            nuevos_r = VGroup(*[Dot(ax_r.c2p(x, r), radius=0.05, color=ROJO) for x, r in zip(X_DEMO, rk)])
            arbol_k = ax_r.plot_line_graph(GRILLA, ARBOLES[min(k + 1, 79)](GRILLA), line_color=VIOLETA,
                                           add_vertex_dots=False, stroke_width=4)["line_graph"]
            self.play(Transform(pred, curva(HISTORIA[k][1])), Transform(residuos, residuos_k), Transform(puntos_r, nuevos_r),
                      Transform(arbol2, arbol_k),
                      Transform(contador, T(f"árboles: {k + 1}", 26, VIOLETA).move_to(contador, aligned_edge=LEFT)),
                      run_time=0.7)
        self.hasta(1)
        sesgo = tarjeta(T("boosting reduce el sesgo", 30, VIOLETA), color=VIOLETA, buff=0.2)
        sesgo.move_to(ax.c2p(2.6, 5.7))
        self.play(FadeIn(sesgo, scale=0.9), run_time=0.8)
        self.hasta(2)
        self.play(FadeOut(VGroup(ax_r, puntos_r, arbol2, etq_r, etq_a2, formula)), run_time=0.6)
        perillas = VGroup(
            T("tasa de aprendizaje η", 26, AMARILLO), T("cantidad de árboles", 26, AMARILLO), T("tamaño de cada árbol", 26, AMARILLO),
            T("early stopping: parar cuando la validación interna deja de mejorar", 24, GRIS),
        )
        VGroup(VGroup(*perillas[:3]).arrange(RIGHT, buff=0.7), perillas[3]).arrange(DOWN, buff=0.3).shift(DOWN * 2.4)
        self.play(LaggedStart(*[FadeIn(p, shift=UP * 0.2) for p in perillas], lag_ratio=0.3), run_time=2.0)

        # o7: implementaciones -----------------------------------------------------------
        self.seg("o7")
        self.limpiar()
        impl = VGroup(
            tarjeta(VGroup(T("XGBoost", 30, BLANCO, weight=BOLD), T("regularización explícita", 22, GRIS)).arrange(DOWN, buff=0.1), ancho=3.8),
            tarjeta(VGroup(T("LightGBM", 30, BLANCO, weight=BOLD), T("histogramas, crece por hojas", 22, GRIS)).arrange(DOWN, buff=0.1), ancho=3.8),
            tarjeta(VGroup(T("CatBoost", 30, BLANCO, weight=BOLD), T("muchas categóricas", 22, GRIS)).arrange(DOWN, buff=0.1), ancho=3.8),
        ).arrange(RIGHT, buff=0.4).shift(UP * 1.8)
        self.play(LaggedStart(*[FadeIn(i, shift=UP * 0.2) for i in impl], lag_ratio=0.3), run_time=1.5)
        self.hasta(1)
        nuestro = tarjeta(VGroup(T("scikit-learn: HistGradientBoosting", 30, VIOLETA, weight=BOLD),
                                 T("inspirado en LightGBM · faltantes y categóricas nativas", 22, GRIS)).arrange(DOWN, buff=0.1),
                          color=VIOLETA, buff=0.25).shift(DOWN * 0.2)
        flecha = Arrow(impl[1].get_bottom(), nuestro.get_top(), buff=0.1, color=VIOLETA)
        self.play(GrowArrow(flecha), FadeIn(nuestro), run_time=1.0)
        # histogramas
        linea = NumberLine(x_range=[0, 8, 1], length=8, color=GRIS_OSCURO, include_numbers=False).shift(DOWN * 2.3)
        valores = np.sort(RNG.uniform(0.05, 7.95, 40))
        dots = VGroup(*[Dot(linea.n2p(v) + UP * 0.25, radius=0.05, color=BLANCO) for v in valores])
        self.play(Create(linea), FadeIn(dots, lag_ratio=0.02), run_time=1.2)
        conteos = np.bincount(valores.astype(int), minlength=8)
        barras = VGroup(*[Rectangle(width=0.9, height=0.18 * c, stroke_width=0, fill_color=VIOLETA, fill_opacity=0.7)
                          .move_to(linea.n2p(i + 0.5), aligned_edge=DOWN).shift(UP * 0.02) for i, c in enumerate(conteos)])
        destinos = []
        apilados = np.zeros(8)
        for d, v in zip(dots, valores):
            b = int(v)
            destinos.append(d.animate.move_to(linea.n2p(b + 0.5) + UP * (0.09 + 0.18 * apilados[b])).set_color(VIOLETA))
            apilados[b] += 1
        etq_h = T("los cortes se buscan entre 8 bins, no entre 40 valores", 22, GRIS).next_to(linea, DOWN, buff=0.25)
        self.play(*destinos, run_time=1.4)
        self.play(FadeIn(barras), FadeOut(dots), FadeIn(etq_h), run_time=0.8)

        # o8: combinar ---------------------------------------------------------------------
        self.seg("o8")
        self.limpiar()
        t8 = T("combinar modelos", 40).to_edge(UP, buff=0.8)
        self.play(FadeIn(t8), run_time=0.6)
        self.hasta(1)
        m_rf = tarjeta(VGroup(T("Random Forest", 26, VERDE), T("p = 0,71", 26)).arrange(DOWN, buff=0.1), color=VERDE, ancho=3.2)
        m_gb = tarjeta(VGroup(T("gradient boosting", 26, VIOLETA), T("p = 0,63", 26)).arrange(DOWN, buff=0.1), color=VIOLETA, ancho=3.2)
        VGroup(m_rf, m_gb).arrange(DOWN, buff=0.4).shift(LEFT * 4.0 + DOWN * 0.3)
        prom = tarjeta(VGroup(T("promedio", 26, AMARILLO), T("p = 0,67", 26)).arrange(DOWN, buff=0.1), color=AMARILLO, ancho=2.6)
        prom.shift(LEFT * 0.4 + DOWN * 0.3)
        fl = VGroup(Arrow(m_rf.get_right(), prom.get_left(), buff=0.1, color=GRIS), Arrow(m_gb.get_right(), prom.get_left(), buff=0.1, color=GRIS))
        ejemplo = T("valores de ejemplo", 18, GRIS_OSCURO).next_to(VGroup(m_rf, m_gb), DOWN, buff=0.2)
        self.play(FadeIn(m_rf), FadeIn(m_gb), FadeIn(ejemplo), run_time=0.8)
        self.play(Create(fl), FadeIn(prom), run_time=1.0)
        self.hasta(2)
        meta = tarjeta(VGroup(T("stacking", 28, NARANJA, weight=BOLD), T("meta-modelo entrenado con", 22, GRIS),
                              T("predicciones out-of-fold", 22, GRIS)).arrange(DOWN, buff=0.1), color=NARANJA, ancho=4.0)
        meta.shift(RIGHT * 4.2 + DOWN * 0.3)
        fl2 = Arrow(prom.get_right(), meta.get_left(), buff=0.1, color=GRIS)
        self.play(GrowArrow(fl2), FadeIn(meta), run_time=1.2)
        nota_m = T("si el meta-modelo ve predicciones sobre su propio train: leakage", 22, ROJO).next_to(meta, DOWN, buff=0.3)
        nota_m.shift(LEFT * max(0, nota_m.get_right()[0] - 6.9))
        self.play(FadeIn(nota_m), run_time=0.8)

        # o9: correlación de errores ----------------------------------------------------------
        self.seg("o9")
        self.limpiar()
        self.hasta(1)
        c1 = Circle(1.5, color=VERDE, fill_color=VERDE, fill_opacity=0.25).shift(LEFT * 1.0)
        c2 = Circle(1.5, color=VIOLETA, fill_color=VIOLETA, fill_opacity=0.25).shift(RIGHT * 1.0)
        e1 = T("errores de RF", 24, VERDE).next_to(c1, LEFT, buff=0.2)
        e2 = T("errores de GB", 24, VIOLETA).next_to(c2, RIGHT, buff=0.2)
        ok = T("se equivocan en lugares distintos: el promedio corrige", 26, VERDE).to_edge(DOWN, buff=1.0)
        self.play(FadeIn(c1), FadeIn(c2), FadeIn(e1), FadeIn(e2), FadeIn(ok), run_time=1.2)
        self.hasta(2)
        self.play(c1.animate.shift(RIGHT * 0.85), c2.animate.shift(LEFT * 0.85), e1.animate.shift(RIGHT * 0.85),
                  e2.animate.shift(LEFT * 0.85),
                  Transform(ok, T("errores superpuestos: promediar casi no corrige", 26, ROJO).move_to(ok)), run_time=1.6)
        self.hasta(3)
        corr = T("se mide con la correlación entre sus predicciones", 28, AMARILLO).next_to(ok, UP, buff=0.3)
        self.play(FadeIn(corr), run_time=0.8)

        # o10: regla de adopción ----------------------------------------------------------
        self.seg("o10")
        self.limpiar()
        t10 = T("regla de adopción, fijada antes de mirar", 36).to_edge(UP, buff=0.8)
        self.play(FadeIn(t10), run_time=0.8)
        self.hasta(1)
        base_v = [0.9551, 0.9560, 0.9548, 0.9566, 0.9560]
        mejoras = [0.0011, 0.0014, 0.0009, 0.0013, 0.0012]
        filas = VGroup()
        for k, (b, d) in enumerate(zip(base_v, mejoras)):
            y = 1.2 - k * 0.6
            p_base = Dot([-3.0 + (b - 0.954) * 600, y, 0], radius=0.09, color=GRIS)
            p_var = Dot([-3.0 + (b + d - 0.954) * 600, y, 0], radius=0.09, color=AMARILLO)
            enlace = Line(p_base.get_center(), p_var.get_center(), color=AMARILLO, stroke_width=3)
            etq = T(f"fold {k + 1}", 22, GRIS).move_to([-4.6, y, 0])
            filas.add(VGroup(etq, p_base, enlace, p_var))
        leyenda = VGroup(VGroup(Dot(color=GRIS), T("antes", 22, GRIS)).arrange(RIGHT, buff=0.15),
                         VGroup(Dot(color=AMARILLO), T("con el cambio", 22, AMARILLO)).arrange(RIGHT, buff=0.15)).arrange(RIGHT, buff=0.5)
        leyenda.next_to(filas, UP, buff=0.3)
        ilustr = T("(ilustración)", 18, GRIS_OSCURO).next_to(leyenda, RIGHT, buff=0.4)
        self.play(FadeIn(leyenda), FadeIn(ilustr), LaggedStart(*[FadeIn(f[:2]) for f in filas], lag_ratio=0.15), run_time=1.2)
        self.play(LaggedStart(*[AnimationGroup(Create(f[2]), FadeIn(f[3])) for f in filas], lag_ratio=0.2), run_time=1.6)
        reglas = VGroup(
            M(f'<span foreground="{AMARILLO}">1.</span> la AUC media mejora (al azar)', 26),
            M(f'<span foreground="{AMARILLO}">2.</span> mejora en al menos 4 de 5 folds', 26),
            M(f'<span foreground="{TURQUESA}">3.</span> la AUC agrupada no empeora', 26),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        reglas.move_to([0.4, 0.2, 0], aligned_edge=LEFT)
        self.play(FadeIn(reglas[:2], shift=LEFT * 0.2), run_time=1.0)
        self.hasta(2)
        self.play(FadeIn(reglas[2], shift=LEFT * 0.2), run_time=0.8)

        # o11 a o13: la tabla de estrategias --------------------------------------------------
        self.seg("o11")
        self.limpiar()
        filas_t = [
            ("variables derivadas", "−0,0014 de AUC", "no", ROJO),
            ("gradient boosting por defecto", "−0,009 al azar; empata agrupada", "no", ROJO),
            ("gradient boosting ajustado", "−0,0011 al azar; +0,0026 agrupada", "para combinar", AMARILLO),
            ("max_features = 0,2 en RF", "+0,0007 (5 de 5); +0,0017 agrupada", "sí", VERDE),
            ("promedio RF + GB", "+0,0012 (5 de 5); +0,0026 agrupada", "sí", VERDE),
            ("100 árboles en lugar de 300", "misma AUC; 37 MB → 12 MB", "sí", VERDE),
            ("stacking", "correlación entre modelos 0,976", "no se probó", GRIS),
        ]
        tabla = VGroup()
        for nombre, res, dec, color in filas_t:
            fila = VGroup(T(nombre, 24, BLANCO), T(res, 22, GRIS), T(dec, 24, color))
            fila[0].move_to([-5.9, 0, 0], aligned_edge=LEFT)
            fila[1].move_to([-1.3, 0, 0], aligned_edge=LEFT)
            fila[2].move_to([4.6, 0, 0], aligned_edge=LEFT)
            tabla.add(fila)
        for i, fila in enumerate(tabla):
            fila.shift(UP * (2.4 - i * 0.68))
        encabezado = VGroup(T("estrategia", 22, GRIS_OSCURO).move_to([-5.9, 3.0, 0], aligned_edge=LEFT),
                            T("frente al paso anterior", 22, GRIS_OSCURO).move_to([-1.3, 3.0, 0], aligned_edge=LEFT),
                            T("decisión", 22, GRIS_OSCURO).move_to([4.6, 3.0, 0], aligned_edge=LEFT))
        self.play(FadeIn(encabezado), run_time=0.6)
        self.hasta(1)
        self.play(FadeIn(tabla[0], shift=RIGHT * 0.2), run_time=0.8)
        nota_d = T("son funciones de columnas que el modelo ya tiene", 22, GRIS).next_to(tabla[0][0], DOWN, buff=0.08, aligned_edge=LEFT)
        self.play(FadeIn(nota_d), run_time=0.6)
        self.hasta(2)
        self.play(FadeOut(nota_d), FadeIn(tabla[1], shift=RIGHT * 0.2), run_time=0.8)
        self.play(FadeIn(tabla[2], shift=RIGHT * 0.2), run_time=0.8)
        self.hasta(3)
        self.play(Indicate(tabla[2][2], color=AMARILLO), run_time=1.0)

        self.seg("o12")
        self.hasta(1)
        self.play(FadeIn(tabla[3], shift=RIGHT * 0.2), run_time=0.8)
        self.hasta(2)
        self.play(FadeIn(tabla[4], shift=RIGHT * 0.2), run_time=0.8)
        self.hasta(3)
        self.play(FadeIn(tabla[5], shift=RIGHT * 0.2), run_time=0.8)

        self.seg("o13")
        self.play(FadeIn(tabla[6], shift=RIGHT * 0.2), run_time=0.8)
        resaltes = VGroup(*[SurroundingRectangle(tabla[i], color=VERDE, buff=0.08, stroke_width=2) for i in (3, 4, 5)])
        self.play(Create(resaltes), run_time=1.0)

        # o14: dónde mejoró --------------------------------------------------------------------
        self.seg("o14")
        self.limpiar()
        total = M(f'mejora total frente al baseline: <span foreground="{AMARILLO}">+0,0018</span> de AUC', 34).to_edge(UP, buff=0.75)
        self.play(Write(total), run_time=1.4)
        self.hasta(2)
        lema = T("si el límite es la información, ningún modelo la inventa", 26, GRIS).next_to(total, DOWN, buff=0.2)
        self.play(FadeIn(lema), run_time=0.8)
        self.hasta(3)
        cohortes = [
            ("independent_client", 0.0140, 0.833), ("región elegida", 0.0075, 0.860), ("reservas únicas", 0.0075, 0.881),
            ("enterprise_client", 0.0049, 0.942), ("basic", 0.0043, 0.887), ("GPU_T4", 0.0036, 0.892),
            ("todas las filas", 0.0018, 0.956), ("research_consortium", 0.0013, 0.997), ("reservas en lote", 0.0003, 0.997),
        ]
        barras = VGroup()
        for i, (nombre, delta, auc) in enumerate(cohortes):
            color = GRIS if auc > 0.95 else AMARILLO
            if nombre == "todas las filas":
                color = BLANCO
            y = 1.35 - i * 0.48
            etq = T(f"{nombre} ({num(auc)})", 22, color).move_to([-1.2, y, 0], aligned_edge=RIGHT)
            b = Rectangle(width=max(0.03, delta * 420), height=0.3, stroke_width=0, fill_color=color, fill_opacity=0.85)
            b.move_to([-0.95, y, 0], aligned_edge=LEFT)
            v = T(f"+{num(delta, 4)}", 22, BLANCO).next_to(b, RIGHT, buff=0.15)
            barras.add(VGroup(etq, b, v))
        nota_b = T("cambio de AUC por cohorte (entre paréntesis, la AUC del baseline)", 20, GRIS).next_to(lema, DOWN, buff=0.2)
        self.play(LaggedStart(*[AnimationGroup(FadeIn(b[0]), GrowFromEdge(b[1], LEFT), FadeIn(b[2])) for b in barras],
                              lag_ratio=0.12), FadeIn(nota_b), run_time=3.0)
        self.hasta(4)
        lotes = T("en los lotes, el error subió de 1,9 % a 2,1 %: memoriza menos", 24, ROJO).to_edge(DOWN, buff=0.6)
        self.play(FadeIn(lotes), Indicate(barras[-1], color=ROJO), run_time=1.2)
        self.terminar()
