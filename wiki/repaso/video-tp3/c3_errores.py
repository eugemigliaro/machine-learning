"""Capítulo 3: diseño centrado en datos y análisis de errores."""

import numpy as np
from manim import *

from base import *


def ciclo(pasos, color, radio=1.55, tam=22, resaltar=None):
    angulos = [PI / 2 - i * TAU / len(pasos) for i in range(len(pasos))]
    textos = VGroup()
    for i, (paso, ang) in enumerate(zip(pasos, angulos)):
        lineas = VGroup(*[T(l, tam, AMARILLO if i == resaltar else BLANCO) for l in paso.split("\n")]).arrange(DOWN, buff=0.05)
        lineas.move_to(radio * np.array([np.cos(ang), np.sin(ang), 0]))
        textos.add(lineas)
    flechas = VGroup()
    for i in range(len(pasos)):
        a0 = angulos[i] - 0.42
        a1 = angulos[(i + 1) % len(pasos)] + 0.42
        if a1 > a0:
            a1 -= TAU
        flechas.add(Arc(radius=radio, start_angle=a0, angle=a1 - a0, color=color, stroke_width=3).add_tip(tip_length=0.18))
    return VGroup(flechas, textos)


def waffle(n_resaltados, color, lado=0.32, buff=0.06):
    cuadros = VGroup(*[Square(lado, stroke_width=0, fill_opacity=1, fill_color=color if i < n_resaltados else GRIS_OSCURO)
                       for i in range(100)])
    return cuadros.arrange_in_grid(10, 10, buff=buff)


def barra_h(valor, maximo, ancho_max, color, alto=0.42):
    return Rectangle(width=max(0.02, ancho_max * valor / maximo), height=alto, stroke_width=0, fill_color=color, fill_opacity=0.9)


class Errores(Escena):
    CAPITULO = "3 · Analizar errores"

    def construct(self):
        # e1: model-centric frente a data-centric -----------------------------
        self.seg("e1")
        izq = ciclo(["entrenar", "evaluar", "cambiar\nel modelo"], GRIS)
        der = ciclo(["entrenar", "evaluar con\nanálisis de errores", "mejorar\nlos datos"], AMARILLO)
        izq.shift(LEFT * 3.4 + DOWN * 0.4)
        der.shift(RIGHT * 3.4 + DOWN * 0.4)
        t_izq = VGroup(T("centrado en el modelo", 30, GRIS, weight=BOLD), T("datos fijos", 24, GRIS)).arrange(DOWN, buff=0.1)
        t_der = VGroup(T("centrado en datos", 30, AMARILLO, weight=BOLD), T("modelo fijo y razonable", 24, GRIS)).arrange(DOWN, buff=0.1)
        t_izq.next_to(izq, UP, buff=0.4)
        t_der.next_to(der, UP, buff=0.4)
        self.hasta(1)
        self.play(FadeIn(t_izq), Create(izq[0]), FadeIn(izq[1]), run_time=1.5)
        self.hasta(2)
        self.play(FadeIn(t_der), Create(der[0]), FadeIn(der[1]), run_time=1.5)
        nota = T("agregar variables también es agregar datos", 26, GRIS).to_edge(DOWN, buff=0.8)
        self.play(FadeIn(nota), run_time=0.8)

        # e2 -------------------------------------------------------------------
        self.seg("e2")
        self.play(FadeOut(VGroup(izq, t_izq, nota)), VGroup(der, t_der).animate.move_to(LEFT * 3.2 + DOWN * 0.2), run_time=1.0)
        self.play(der[1][1].animate.set_color(AMARILLO).scale(1.15), run_time=0.6)
        self.hasta(1)
        matriz = VGroup(*[Square(0.9, stroke_color=GRIS, stroke_width=2) for _ in range(4)]).arrange_in_grid(2, 2, buff=0)
        matriz.shift(RIGHT * 2.2 + UP * 0.4)
        lupa = VGroup(Circle(0.55, color=AMARILLO, stroke_width=5), Line(ORIGIN, DR * 0.6, color=AMARILLO, stroke_width=6))
        lupa[1].next_to(lupa[0], DR, buff=-0.12)
        lupa.next_to(matriz, RIGHT, buff=0.5)
        texto_m = T("¿qué tienen en común los errores?", 28, BLANCO).next_to(VGroup(matriz, lupa), DOWN, buff=0.5)
        self.play(FadeIn(matriz), run_time=0.6)
        self.play(FadeIn(lupa, shift=LEFT * 0.3), Write(texto_m), run_time=1.2)

        # e3: tags y dos proporciones --------------------------------------------
        self.seg("e3")
        self.limpiar()
        rng = np.random.default_rng(2)
        grilla = VGroup(*[Square(0.36, stroke_width=0, fill_color=GRIS_OSCURO, fill_opacity=1) for _ in range(100)])
        grilla.arrange_in_grid(10, 10, buff=0.07).shift(LEFT * 3.6 + DOWN * 0.2)
        con_tag = set(range(0, 100, 10)) | set(range(1, 100, 10)) | set(range(2, 100, 10))  # tres columnas
        errores = {i for i in con_tag if rng.random() < 0.4} | {i for i in range(100) if i not in con_tag and rng.random() < 0.06}
        cruces = VGroup(*[Cross(grilla[i], stroke_color=ROJO, stroke_width=4, scale_factor=0.7) for i in sorted(errores)])
        self.play(FadeIn(grilla), run_time=0.8)
        self.play(LaggedStart(*[Create(c) for c in cruces], lag_ratio=0.05), run_time=1.4)
        marco = SurroundingRectangle(VGroup(*[grilla[i] for i in con_tag]), color=NARANJA, buff=0.06)
        etq_tag = T("tag", 26, NARANJA).next_to(marco, UP, buff=0.1)
        self.play(Create(marco), FadeIn(etq_tag), run_time=0.8)
        n_err = len(errores)
        n_err_tag = len(errores & con_tag)
        self.hasta(1)
        f1 = VGroup(T("1. de los errores, ¿cuántos tienen el tag?", 28, BLANCO),
                    M(f'<span foreground="{NARANJA}">{n_err_tag} de {n_err}</span>  → cuánto ganarías si lo resolvés', 26, GRIS))
        f1.arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to(RIGHT * 2.6 + UP * 1.3)
        self.play(FadeIn(f1[0]), run_time=0.8)
        self.hasta(2)
        self.play(FadeIn(f1[1]), *[Indicate(cruces[j], color=NARANJA) for j, i in enumerate(sorted(errores)) if i in con_tag],
                  run_time=1.2)
        self.hasta(3)
        f2 = VGroup(T("2. con el tag, ¿cuántos están mal?", 28, BLANCO),
                    M(f'<span foreground="{NARANJA}">{n_err_tag} de {len(con_tag)}</span>  frente a '
                      f'{n_err - n_err_tag} de {100 - len(con_tag)} sin el tag', 26, GRIS))
        f2.arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(f1, DOWN, buff=0.7, aligned_edge=LEFT)
        self.play(FadeIn(f2[0]), run_time=0.8)
        self.hasta(4)
        self.play(FadeIn(f2[1]), run_time=0.8)

        # e4: priorizar: brecha × frecuencia ------------------------------------------
        self.seg("e4")
        self.limpiar()
        titulo = T("prioridad = brecha × frecuencia", 40, BLANCO).to_edge(UP, buff=0.8)
        self.play(Write(titulo), run_time=1.0)
        escala = 0.3  # unidades por punto porcentual
        ejemplos = [("imagen recortada", 5, 10, ROJO), ("bajo contraste", 20, 6, AMARILLO)]
        rects = VGroup()
        for nombre, frec, brecha, color in ejemplos:
            r = Rectangle(width=frec * 0.3, height=brecha * escala, stroke_color=color, fill_color=color, fill_opacity=0.35)
            etq = VGroup(T(nombre, 26, color), T(f"{frec} % de los datos × {brecha} % de brecha", 22, GRIS),
                         T(f"= {num(frec * brecha / 100, 1)} % del error global", 22, GRIS))
            etq.arrange(DOWN, buff=0.08)
            rects.add(VGroup(r, etq))
        rects[0][0].move_to(LEFT * 3.9 + DOWN * 0.2)
        rects[1][0].move_to(RIGHT * 1.8 + DOWN * 0.2).align_to(rects[0][0], DOWN)
        for g in rects:
            g[1].next_to(g[0], DOWN, buff=0.25)
        self.hasta(1)
        self.play(GrowFromEdge(rects[0][0], DOWN), FadeIn(rects[0][1]), run_time=1.2)
        self.hasta(2)
        self.play(GrowFromEdge(rects[1][0], DOWN), FadeIn(rects[1][1]), run_time=1.2)
        area = T("el área es lo que el grupo aporta al error global", 26, GRIS).next_to(titulo, DOWN, buff=0.3)
        self.play(FadeIn(area), run_time=0.8)

        # e5: nuestros errores -----------------------------------------------------
        self.seg("e5")
        self.limpiar()
        total = M(f'<span foreground="{ROJO}">4.423</span> errores en 38.273 reservas', 40).shift(UP * 1.6)
        self.play(Write(total), run_time=1.4)
        tipos = VGroup(
            M(f'<span foreground="{ROJO}">2.827</span> falsos negativos: se canceló y dijimos que no', 28),
            M(f'<span foreground="{ROJO}">1.596</span> falsos positivos: se ejecutó y dijimos que se cancelaba', 28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(total, DOWN, buff=0.5)
        self.play(FadeIn(tipos), run_time=1.0)
        self.hasta(2)
        tags = VGroup(tarjeta(T("tipo de cliente", 28, NARANJA), buff=0.2), T("×", 36), tarjeta(T("única o en lote", 28, NARANJA), buff=0.2))
        tags.arrange(RIGHT, buff=0.4).next_to(tipos, DOWN, buff=0.7)
        self.play(FadeIn(tags, shift=UP * 0.2), run_time=1.0)

        # e6: 41 % de las filas, 77 % de los errores ---------------------------------------
        self.seg("e6")
        self.limpiar()
        filas = waffle(41, NARANJA).shift(LEFT * 4.2 + DOWN * 0.3)
        t_filas = T("todas las reservas", 28, BLANCO).next_to(filas, UP, buff=0.3)
        self.play(FadeIn(filas, lag_ratio=0.01), FadeIn(t_filas), run_time=1.5)
        self.hasta(1)
        region = T("únicas de cloud_marketplace", 26, NARANJA).next_to(filas, DOWN, buff=0.3)
        p_filas = T("41 %", 56, NARANJA, weight=BOLD).next_to(filas, RIGHT, buff=0.3)
        self.play(FadeIn(region), Write(p_filas), run_time=1.0)
        self.hasta(2)
        errs = waffle(77, NARANJA).shift(RIGHT * 4.2 + DOWN * 0.3)
        t_errs = T("los errores del baseline", 28, ROJO).next_to(errs, UP, buff=0.3)
        p_errs = T("77 %", 56, NARANJA, weight=BOLD).next_to(errs, LEFT, buff=0.3)
        self.play(FadeIn(t_errs), TransformFromCopy(filas, errs), run_time=1.6)
        self.play(Write(p_errs), run_time=0.8)

        # e7: tasa de error en la región ------------------------------------------------
        self.seg("e7")
        self.limpiar()
        titulo7 = T("tasa de error del baseline", 34, BLANCO).to_edge(UP, buff=0.9)
        b_reg = barra_h(21.4, 21.4, 7.0, NARANJA)
        b_res = barra_h(4.6, 21.4, 7.0, GRIS)
        etiquetas = VGroup(T("región elegida", 28, NARANJA), T("resto", 28, GRIS))
        grupo = VGroup(VGroup(etiquetas[0], b_reg), VGroup(etiquetas[1], b_res))
        for g in grupo:
            g.arrange(RIGHT, buff=0.4)
        grupo.arrange(DOWN, aligned_edge=LEFT, buff=0.6).shift(LEFT * 0.8)
        etiquetas[1].align_to(etiquetas[0], RIGHT)
        b_res.next_to(etiquetas[1], RIGHT, buff=0.4).align_to(b_reg, LEFT)
        v_reg = T("21,4 %", 30, BLANCO).next_to(b_reg, RIGHT, buff=0.2)
        v_res = T("4,6 %", 30, BLANCO).next_to(b_res, RIGHT, buff=0.2)
        self.play(FadeIn(titulo7), FadeIn(etiquetas), run_time=0.8)
        self.play(GrowFromEdge(b_reg, LEFT), GrowFromEdge(b_res, LEFT), run_time=1.4)
        self.play(FadeIn(v_reg), FadeIn(v_res), run_time=0.6)
        self.hasta(2)
        parejo = T("adentro es parejo: ningún tier, GPU o región lo explica solo", 26, GRIS).next_to(grupo, DOWN, buff=0.9)
        self.play(FadeIn(parejo), run_time=0.8)
        self.hasta(3)
        sello = tarjeta(T("región problemática elegida", 30, NARANJA), color=NARANJA, buff=0.22).next_to(parejo, DOWN, buff=0.4)
        self.play(FadeIn(sello, scale=0.9), run_time=0.8)

        # e8: composición de basic y GPU_T4 ---------------------------------------------
        self.seg("e8")
        self.limpiar()
        titulo8 = T("las cohortes de la consigna", 34).to_edge(UP, buff=0.9)
        self.play(FadeIn(titulo8), run_time=0.6)
        cohortes = VGroup()
        for nombre, frac in [("basic", 0.93), ("GPU_T4", 0.79)]:
            ancho = 7.0
            parte = Rectangle(width=ancho * frac, height=0.6, stroke_width=0, fill_color=NARANJA, fill_opacity=0.85)
            resto = Rectangle(width=ancho * (1 - frac), height=0.6, stroke_width=0, fill_color=GRIS_OSCURO, fill_opacity=1)
            resto.next_to(parte, RIGHT, buff=0)
            barra = VGroup(parte, resto)
            etq = T(nombre, 30, BLANCO)
            pct = T(f"{int(frac * 100)} % cloud_marketplace", 24, FONDO, weight=BOLD).move_to(parte)
            cohortes.add(VGroup(etq, barra, pct))
        for c in cohortes:
            c[0].next_to(c[1], LEFT, buff=0.4)
        cohortes.arrange(DOWN, buff=0.8).shift(RIGHT * 0.6 + DOWN * 0.2)
        for c in cohortes:
            c[2].move_to(c[1][0])
        self.hasta(1)
        doble = T("casi el doble de error que el resto", 28, ROJO).next_to(titulo8, DOWN, buff=0.4)
        self.play(FadeIn(VGroup(*[c[0] for c in cohortes])), FadeIn(doble), run_time=1.0)
        self.hasta(2)
        self.play(*[GrowFromEdge(c[1], LEFT) for c in cohortes], run_time=1.4)
        self.play(*[FadeIn(c[2]) for c in cohortes], run_time=0.6)
        self.hasta(3)
        conclusion = T("no son difíciles por sí mismas: están llenas de la región difícil", 28, AMARILLO)
        conclusion.to_edge(DOWN, buff=1.0)
        self.play(FadeIn(conclusion, shift=UP * 0.2), run_time=1.0)

        # e9: por qué falla: sin historial ni señales --------------------------------------
        self.seg("e9")
        self.limpiar()
        self.hasta(1)
        titulo9 = T("cancelaciones previas", 32).to_edge(UP, buff=0.9)
        b1 = barra_h(0.9, 10.9, 6.0, NARANJA)
        b2 = barra_h(10.9, 10.9, 6.0, GRIS)
        filas9 = VGroup(
            VGroup(T("región", 28, NARANJA), b1, T("0,9 %", 28)),
            VGroup(T("resto", 28, GRIS), b2, T("10,9 %", 28)),
        )
        for f in filas9:
            f.arrange(RIGHT, buff=0.35)
        filas9.arrange(DOWN, aligned_edge=LEFT, buff=0.4).shift(UP * 1.0 + LEFT * 0.5)
        filas9[1][1].align_to(filas9[0][1], LEFT)
        filas9[1][2].next_to(filas9[1][1], RIGHT, buff=0.35)
        filas9[0][0].align_to(filas9[1][0], RIGHT)
        self.play(FadeIn(titulo9), FadeIn(VGroup(filas9[0][0], filas9[1][0])), run_time=0.6)
        self.play(GrowFromEdge(b1, LEFT), GrowFromEdge(b2, LEFT), FadeIn(filas9[0][2]), FadeIn(filas9[1][2]), run_time=1.2)
        self.hasta(2)
        senales = VGroup(
            M(f'<span foreground="{ROJO}">✗</span>  compromiso locked_allocation (se cancela el 99,8 %)', 28),
            M(f'<span foreground="{ROJO}">✗</span>  ser parte de un lote', 28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).shift(DOWN * 1.5)
        t_sen = T("señales fuertes que la región no tiene:", 28, GRIS).next_to(senales, UP, buff=0.35, aligned_edge=LEFT)
        self.play(FadeIn(t_sen), LaggedStart(*[FadeIn(s, shift=RIGHT * 0.2) for s in senales], lag_ratio=0.4), run_time=1.6)

        # e10: el modelo duda ------------------------------------------------------------
        self.seg("e10")
        self.limpiar()
        ax = Axes(x_range=[0, 1, 0.1], y_range=[0, 3.2, 1], x_length=7.5, y_length=3.0, tips=False,
                  axis_config={"color": GRIS_OSCURO, "include_numbers": False}).shift(UP * 0.7 + LEFT * 0.4)
        xs = np.linspace(0.01, 0.99, 120)
        dens = lambda m, s: np.exp(-0.5 * ((xs - m) / s) ** 2) / (s * np.sqrt(2 * np.pi)) * 0.55  # noqa: E731
        c_ej = ax.plot_line_graph(xs, dens(0.38, 0.14), line_color=AZUL, add_vertex_dots=False, stroke_width=4)
        c_ca = ax.plot_line_graph(xs, dens(0.58, 0.15), line_color=ROJO, add_vertex_dots=False, stroke_width=4)
        marcas = VGroup(*[T(num(v, 1), 20, GRIS).next_to(ax.c2p(v, 0), DOWN, buff=0.12) for v in [0, 0.3, 0.5, 0.7, 1.0]])
        t_x = T("probabilidad de cancelación que da el modelo (esquema)", 22, GRIS).next_to(marcas, DOWN, buff=0.15)
        leyenda = VGroup(T("se ejecutó", 24, AZUL), T("se canceló", 24, ROJO)).arrange(DOWN, aligned_edge=LEFT).next_to(ax, RIGHT, buff=0.3)
        self.play(Create(ax), FadeIn(marcas), FadeIn(t_x), run_time=0.8)
        self.play(Create(c_ej), Create(c_ca), FadeIn(leyenda), run_time=1.4)
        self.hasta(1)
        banda = Rectangle(width=ax.c2p(0.7, 0)[0] - ax.c2p(0.3, 0)[0], height=3.0, stroke_width=0, fill_color=AMARILLO,
                          fill_opacity=0.15).move_to(ax.c2p(0.5, 1.6))
        dudosas = M(f'<span foreground="{AMARILLO}">38 %</span> de la región entre 0,3 y 0,7 (5,8 % en el resto)', 28)
        dudosas.next_to(ax, UP, buff=0.25)
        self.play(FadeIn(banda), FadeIn(dudosas), run_time=1.0)
        self.hasta(2)
        descartes = VGroup(
            M(f'<span foreground="{ROJO}">✗</span> umbral propio de la región: +0,2 puntos de accuracy', 26),
            M(f'<span foreground="{ROJO}">✗</span> más filas: accuracy de la región 0,784 con la mitad, 0,786 con todo', 26),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(DOWN, buff=0.7)
        self.play(FadeIn(descartes[0], shift=RIGHT * 0.2), run_time=0.8)
        self.hasta(3)
        self.play(FadeIn(descartes[1], shift=RIGHT * 0.2), run_time=0.8)

        # e11: costos de FP y FN --------------------------------------------------------
        self.seg("e11")
        self.limpiar()
        self.hasta(1)
        fn = tarjeta(VGroup(T("falso negativo", 30, ROJO, weight=BOLD), T("cancelación sin aviso:", 24, GRIS),
                            T("la GPU queda ociosa", 24, GRIS)).arrange(DOWN, buff=0.12), color=ROJO, ancho=5.2)
        fp = tarjeta(VGroup(T("falso positivo", 30, AZUL, weight=BOLD), T("si se reasigna la GPU:", 24, GRIS),
                            T("el cliente llega y no hay recursos", 24, GRIS)).arrange(DOWN, buff=0.12), color=AZUL, ancho=5.2)
        VGroup(fn, fp).arrange(RIGHT, buff=0.8).shift(UP * 1.2)
        self.play(FadeIn(fn, shift=UP * 0.2), run_time=0.8)
        self.hasta(2)
        self.play(FadeIn(fp, shift=UP * 0.2), run_time=0.8)
        self.hasta(3)
        formula = M(f'predecir "se cancela" si  p &gt; c<sub>FP</sub> / (c<sub>FP</sub> + c<sub>FN</sub>)', 34)
        formula.shift(DOWN * 0.8)
        ejemplo = M(f'si c<sub>FP</sub> = 2 · c<sub>FN</sub>:  umbral = 2/3 ≈ <span foreground="{AMARILLO}">0,67</span>', 30)
        ejemplo.next_to(formula, DOWN, buff=0.4)
        self.play(Write(formula), run_time=1.4)
        self.play(FadeIn(ejemplo), run_time=0.8)

        # e12: data augmentation -------------------------------------------------------
        self.seg("e12")
        self.limpiar()
        titulo12 = T("data augmentation", 40, BLANCO).to_edge(UP, buff=0.8)
        tipos12 = VGroup(*[tarjeta(T(t, 26), buff=0.2) for t in ["imágenes", "audio", "texto"]]).arrange(RIGHT, buff=0.4)
        tipos12.next_to(titulo12, DOWN, buff=0.5)
        self.play(FadeIn(titulo12), LaggedStart(*[FadeIn(t) for t in tipos12], lag_ratio=0.2), run_time=1.2)
        self.hasta(1)
        pasos = VGroup(bloque_paso("split / folds", GRIS), bloque_paso("aumentar solo train", VERDE),
                       bloque_paso("validar con datos reales", AMARILLO)).arrange(RIGHT, buff=0.7).shift(DOWN * 0.3)
        flechas = VGroup(*[Arrow(pasos[i].get_right(), pasos[i + 1].get_left(), buff=0.1, color=GRIS) for i in range(2)])
        self.play(LaggedStart(*[FadeIn(p) for p in pasos], lag_ratio=0.3), Create(flechas), run_time=1.6)
        tabular = T("en tablas: puede crear filas imposibles (SMOTE)", 26, ROJO).next_to(pasos, DOWN, buff=0.6)
        self.play(FadeIn(tabular), run_time=0.8)
        self.hasta(2)
        nuestro = tarjeta(T("nosotros: el problema es información, no cantidad → descartada", 28, AMARILLO), color=AMARILLO, buff=0.2)
        nuestro.to_edge(DOWN, buff=0.7)
        self.play(FadeIn(nuestro, shift=UP * 0.2), run_time=1.0)

        # e13: adquisición de datos ------------------------------------------------------
        self.seg("e13")
        self.limpiar()
        titulo13 = T("datos que pediríamos (consigna 3.4)", 36).to_edge(UP, buff=0.8)
        self.play(FadeIn(titulo13), run_time=0.6)
        self.hasta(1)
        lista = VGroup(
            M(f'<span foreground="{AMARILLO}">1.</span> historial del cliente final', 30),
            M(f'<span foreground="{AMARILLO}">2.</span> identificador de lote', 30),
            M(f'<span foreground="{AMARILLO}">3.</span> actividad entre la reserva y la ejecución', 30),
            M(f'<span foreground="{AMARILLO}">4.</span> condiciones comerciales', 30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).shift(LEFT * 2.6 + DOWN * 0.3)
        self.play(FadeIn(lista[0], shift=RIGHT * 0.2), run_time=0.8)
        b_con = barra_h(0.916 - 0.85, 0.07, 3.0, VERDE, 0.4)
        b_sin = barra_h(0.876 - 0.85, 0.07, 3.0, GRIS, 0.4)
        evid = VGroup(
            T("AUC en reservas únicas", 24, GRIS),
            VGroup(T("con historial", 22, VERDE), b_con, T("0,916", 24)).arrange(RIGHT, buff=0.2),
            VGroup(T("sin historial", 22, GRIS), b_sin, T("0,876", 24)).arrange(RIGHT, buff=0.2),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.6).shift(UP * 0.6)
        evid[2][1].align_to(evid[1][1], LEFT)
        evid[2][2].next_to(evid[2][1], RIGHT, buff=0.2)
        nota_ev = T("(barras desde 0,85)", 18, GRIS_OSCURO).next_to(evid, DOWN, buff=0.1, aligned_edge=LEFT)
        self.play(FadeIn(evid), FadeIn(nota_ev), run_time=1.0)
        self.hasta(2)
        self.play(LaggedStart(*[FadeIn(l, shift=RIGHT * 0.2) for l in lista[1:]], lag_ratio=0.4), run_time=2.0)
        self.terminar()


def bloque_paso(texto, color):
    etiqueta = T(texto, 26, BLANCO)
    caja = RoundedRectangle(width=etiqueta.width + 0.5, height=0.8, corner_radius=0.12, stroke_color=color,
                            fill_color=color, fill_opacity=0.15)
    return VGroup(caja, etiqueta.move_to(caja))
