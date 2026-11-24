"""Capítulo 1: validar según el uso (k-fold estratificada y por grupos)."""

import numpy as np
from manim import *

from base import *

HOSPITALES = ["#58C4DD", "#83C167", "#B189D8", "#F0AC5F", "#E07A9B"]


def bloque(texto, color, ancho=2.6, alto=0.8, tam=28):
    etiqueta = T(texto, tam, BLANCO)
    caja = RoundedRectangle(width=max(ancho, etiqueta.width + 0.6), height=alto, corner_radius=0.12,
                            stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.15)
    return VGroup(caja, etiqueta.move_to(caja))


def barra_clases(ancho, alto, frac_roja=0.417):
    roja = Rectangle(width=ancho * frac_roja, height=alto, stroke_width=0, fill_color=ROJO, fill_opacity=1)
    azul = Rectangle(width=ancho * (1 - frac_roja), height=alto, stroke_width=0, fill_color=AZUL, fill_opacity=1)
    azul.next_to(roja, RIGHT, buff=0)
    return VGroup(roja, azul)


def fila_reserva(colores, ancho_celda=0.42, alto=0.3):
    return VGroup(*[
        Rectangle(width=ancho_celda, height=alto, stroke_color=FONDO, stroke_width=2, fill_color=c, fill_opacity=1)
        for c in colores
    ]).arrange(RIGHT, buff=0)


class Validacion(Escena):
    CAPITULO = "1 · Validar"

    def construct(self):
        # v1 -------------------------------------------------------------
        self.seg("v1")
        titulo = T("Validar según el uso", 56, BLANCO, weight=BOLD)
        self.play(Write(titulo), run_time=1.5)
        self.hasta(1)
        self.play(titulo.animate.scale(0.7).to_edge(UP, buff=0.6), run_time=0.8)
        pregunta = T("¿Cómo le va a ir al modelo con datos nuevos?", 38, AMARILLO).shift(UP * 0.8)
        self.play(Write(pregunta), run_time=1.5)
        self.hasta(2)
        opciones = VGroup(
            bloque("más reservas del mismo conjunto", GRIS, 5.4),
            bloque("reservas de clientes nuevos", GRIS, 5.4),
            bloque("las reservas del mes que viene", GRIS, 5.4),
        ).arrange(DOWN, buff=0.25).next_to(pregunta, DOWN, buff=0.6)
        self.play(LaggedStart(*[FadeIn(o, shift=UP * 0.2) for o in opciones], lag_ratio=0.3), run_time=1.6)

        # v2: la regla del split ---------------------------------------------
        self.seg("v2")
        self.play(FadeOut(pregunta), FadeOut(opciones), run_time=0.6)
        izq = VGroup(bloque("train", AZUL, 2.0), bloque("validación", AMARILLO, 2.4)).arrange(RIGHT, buff=0.9)
        izq_flecha = Arrow(izq[0].get_right(), izq[1].get_left(), buff=0.1, color=GRIS)
        der = VGroup(bloque("train", AZUL, 2.0), bloque("uso real", VERDE, 2.4)).arrange(RIGHT, buff=0.9)
        der_flecha = Arrow(der[0].get_right(), der[1].get_left(), buff=0.1, color=GRIS)
        par_izq = VGroup(izq, izq_flecha)
        par_der = VGroup(der, der_flecha)
        igual = T("=", 64, BLANCO)
        regla = VGroup(par_izq, igual, par_der).arrange(RIGHT, buff=0.5).shift(UP * 0.4)
        self.hasta(1)
        self.play(FadeIn(par_izq, shift=RIGHT * 0.2), run_time=1.0)
        self.play(Write(igual), FadeIn(par_der, shift=LEFT * 0.2), run_time=1.2)
        etiqueta = T("misma relación", 30, GRIS).next_to(igual, DOWN, buff=0.9)
        self.play(FadeIn(etiqueta), run_time=0.6)
        self.hasta(2)
        lema = T("El uso define el split.", 40, AMARILLO).next_to(regla, DOWN, buff=1.6)
        self.play(Write(lema), run_time=1.2)

        # v3: k-fold estratificada -------------------------------------------
        self.seg("v3")
        self.play(FadeOut(VGroup(regla, etiqueta, lema)), run_time=0.6)
        filas = VGroup()
        for k in range(5):
            bloques = VGroup(*[
                Rectangle(width=1.5, height=0.5, stroke_color=FONDO, stroke_width=3,
                          fill_color=AMARILLO if j == k else AZUL, fill_opacity=0.85 if j == k else 0.35)
                for j in range(5)
            ]).arrange(RIGHT, buff=0)
            nombre = T(f"fold {k + 1}", 24, GRIS).next_to(bloques, LEFT, buff=0.3)
            filas.add(VGroup(nombre, bloques))
        filas.arrange(DOWN, buff=0.18).shift(DOWN * 0.3)
        leyenda = VGroup(
            VGroup(Square(0.25, fill_color=AZUL, fill_opacity=0.35, stroke_width=0), T("train", 24)).arrange(RIGHT),
            VGroup(Square(0.25, fill_color=AMARILLO, fill_opacity=0.85, stroke_width=0), T("validación", 24)).arrange(RIGHT),
        ).arrange(RIGHT, buff=0.6).next_to(filas, UP, buff=0.4)
        self.play(LaggedStart(*[FadeIn(f) for f in filas], lag_ratio=0.2), FadeIn(leyenda), run_time=2.0)
        self.hasta(1)
        # proporción de clases dentro de cada bloque
        barras = VGroup()
        for fila in filas:
            for bloque_ in fila[1]:
                b = barra_clases(bloque_.width - 0.12, 0.12).move_to(bloque_).align_to(bloque_, DOWN).shift(UP * 0.06)
                barras.add(b)
        self.play(LaggedStart(*[GrowFromEdge(b, LEFT) for b in barras], lag_ratio=0.02), run_time=2.0)
        self.hasta(2)
        nota = M(f'en cada fold: <span foreground="{ROJO}">41,7 % se cancela</span>', 30).next_to(filas, DOWN, buff=0.45)
        self.play(FadeIn(nota, shift=UP * 0.2), run_time=0.8)

        # v4: hospitales y leakage indirecto ----------------------------------------
        self.seg("v4")
        self.play(FadeOut(VGroup(filas, barras, leyenda, nota)), run_time=0.6)
        self.hasta(1)
        rng = np.random.default_rng(7)
        centros = [LEFT * 4.6 + UP * 0.6, LEFT * 2.3 + DOWN * 0.9, ORIGIN + UP * 0.7, RIGHT * 2.3 + DOWN * 0.9,
                   RIGHT * 4.6 + UP * 0.6]
        puntos = VGroup()
        grupos = []
        for h, (c, color) in enumerate(zip(centros, HOSPITALES)):
            g = VGroup(*[Dot(c + np.array([*rng.normal(0, 0.38, 2), 0]), radius=0.08, color=color) for _ in range(12)])
            puntos.add(*g)
            grupos.append(g)
        etiquetas = VGroup(*[T(f"hospital {h + 1}", 22, HOSPITALES[h]).next_to(grupos[h], UP if h % 2 == 0 else DOWN, buff=0.15)
                             for h in range(5)])
        self.play(LaggedStart(*[FadeIn(g, scale=0.6) for g in grupos], lag_ratio=0.2), FadeIn(etiquetas), run_time=2.0)
        self.hasta(2)
        caja_tr = RoundedRectangle(width=6.0, height=3.6, corner_radius=0.2, stroke_color=AZUL).shift(LEFT * 3.3 + DOWN * 0.4)
        caja_va = RoundedRectangle(width=4.2, height=3.6, corner_radius=0.2, stroke_color=AMARILLO).shift(RIGHT * 3.9 + DOWN * 0.4)
        t_tr = T("train", 28, AZUL).next_to(caja_tr, UP, buff=0.15)
        t_va = T("validación", 28, AMARILLO).next_to(caja_va, UP, buff=0.15)
        destino = []
        orden = rng.permutation(len(puntos))
        for i, idx in enumerate(orden):
            if i < 42:
                fila, col = divmod(i, 7)
                destino.append((idx, caja_tr.get_center() + np.array([-2.4 + col * 0.8, 1.2 - fila * 0.48, 0])))
            else:
                fila, col = divmod(i - 42, 5)
                destino.append((idx, caja_va.get_center() + np.array([-1.6 + col * 0.8, 1.0 - fila * 0.6, 0])))
        self.play(FadeOut(etiquetas), Create(caja_tr), Create(caja_va), FadeIn(t_tr), FadeIn(t_va),
                  *[puntos[idx].animate.move_to(pos) for idx, pos in destino], run_time=2.2)
        # unir puntos del mismo hospital a ambos lados
        en_va = {idx for i, (idx, _) in enumerate(destino) if i >= 42}
        enlaces = VGroup()
        color_idx = lambda idx: idx // 12  # noqa: E731
        for v in list(en_va)[:6]:
            pares = [idx for idx, _ in destino[:42] if color_idx(idx) == color_idx(v)]
            if pares:
                enlaces.add(DashedLine(puntos[pares[0]].get_center(), puntos[v].get_center(), color=HOSPITALES[color_idx(v)],
                                       stroke_width=2, dash_length=0.1).set_opacity(0.8))
        self.play(LaggedStart(*[Create(e) for e in enlaces], lag_ratio=0.2), run_time=1.6)
        aviso = T("el modelo puede aprender el hospital, no el problema", 28, BLANCO).to_edge(DOWN, buff=0.9)
        self.play(FadeIn(aviso), run_time=0.8)
        self.hasta(3)
        nombre = T("leakage indirecto", 34, ROJO).next_to(aviso, DOWN, buff=0.2)
        self.play(Write(nombre), run_time=1.0)

        # v5: validación por grupos --------------------------------------------
        self.seg("v5")
        self.play(FadeOut(enlaces), FadeOut(aviso), FadeOut(nombre), run_time=0.5)
        nuevos = []
        for h in range(5):
            for j in range(12):
                idx = h * 12 + j
                if h < 4:
                    base = caja_tr.get_center() + np.array([-2.25 + (h % 2) * 2.6, 0.95 - (h // 2) * 1.6, 0])
                    pos = base + np.array([(j % 4) * 0.42, -(j // 4) * 0.4, 0])
                else:
                    base = caja_va.get_center() + np.array([-0.65, 0.6, 0])
                    pos = base + np.array([(j % 4) * 0.42, -(j // 4) * 0.45, 0])
                nuevos.append(puntos[idx].animate.move_to(pos))
        self.play(*nuevos, run_time=2.0)
        lema = T("cada grupo entero de un solo lado", 30, TURQUESA).to_edge(DOWN, buff=0.9)
        self.play(FadeIn(lema), run_time=0.8)
        self.hasta(2)
        lema2 = T("mide el rendimiento en hospitales nunca vistos", 28, BLANCO).next_to(lema, DOWN, buff=0.2)
        self.play(FadeIn(lema2), run_time=0.8)

        # v6: duplicados en el dataset -----------------------------------------
        self.seg("v6")
        self.play(FadeOut(VGroup(puntos, caja_tr, caja_va, t_tr, t_va, lema, lema2, titulo)), run_time=0.7)
        paleta = ["#3A4A5C", "#4B5D73", "#2E3B4A", "#556B82", "#36475A", "#43566B"]
        rng = np.random.default_rng(11)
        base_filas = [list(rng.choice(paleta, 10)) for _ in range(8)]
        gemelas = {1: 0, 4: 0, 6: 3, 7: 3}  # fila -> copia de
        for f, original in gemelas.items():
            base_filas[f] = list(base_filas[original])
        tabla = VGroup(*[fila_reserva(c) for c in base_filas]).arrange(DOWN, buff=0.12).shift(LEFT * 4.1)
        self.hasta(1)
        self.play(LaggedStart(*[FadeIn(f, shift=RIGHT * 0.2) for f in tabla], lag_ratio=0.1), run_time=1.5)
        self.hasta(2)
        resaltes = VGroup()
        for indices, color in [([0, 1, 4], NARANJA), ([3, 6, 7], VIOLETA)]:
            for i in indices:
                resaltes.add(SurroundingRectangle(tabla[i], color=color, buff=0.04, stroke_width=3))
        self.play(LaggedStart(*[Create(r) for r in resaltes], lag_ratio=0.15), run_time=1.6)
        dato1 = M(f'<span foreground="{NARANJA}">33 %</span> de las filas es copia exacta de otra', 30)
        dato1.next_to(tabla, RIGHT, buff=0.7).shift(UP * 0.6)
        self.play(FadeIn(dato1), run_time=0.8)
        self.hasta(3)
        dato2 = M(f'<span foreground="{NARANJA}">3.499</span> grupos de reservas idénticas', 30)
        dato3 = M(f'con el <span foreground="{NARANJA}">41 %</span> de las filas', 30)
        VGroup(dato2, dato3).arrange(DOWN, aligned_edge=LEFT).next_to(dato1, DOWN, buff=0.4, aligned_edge=LEFT)
        self.play(FadeIn(dato2), FadeIn(dato3), run_time=1.0)

        # v7: la tasa de cancelación crece con el tamaño del grupo ---------------------
        self.seg("v7")
        self.play(FadeOut(VGroup(tabla, resaltes, dato1, dato2, dato3)), run_time=0.6)
        categorias = ["única", "2", "3–5", "6–10", "11–50", "más de 50"]
        tasas = [28.4, 35.7, 37.8, 50.6, 73.9, 94.5]
        base_y = -2.6
        alto_max = 3.9
        barras = VGroup()
        textos = VGroup()
        for i, (cat, tasa) in enumerate(zip(categorias, tasas)):
            x = -4.5 + i * 1.8
            b = Rectangle(width=1.1, height=alto_max * tasa / 100, stroke_width=0, fill_color=ROJO, fill_opacity=0.85)
            b.move_to([x, base_y, 0], aligned_edge=DOWN)
            barras.add(b)
            textos.add(VGroup(T(cat, 24, GRIS).next_to(b, DOWN, buff=0.15),
                              T(f"{num(tasa, 1)} %", 24, BLANCO).next_to(b, UP, buff=0.1)))
        eje = Line([-5.4, base_y, 0], [5.4, base_y, 0], color=GRIS_OSCURO)
        titulo_g = T("tasa de cancelación según el tamaño del grupo de copias", 30, BLANCO).to_edge(UP, buff=0.9)
        self.play(FadeIn(titulo_g), Create(eje), run_time=0.8)
        self.hasta(1)
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in barras], lag_ratio=0.15),
                  LaggedStart(*[FadeIn(t) for t in textos], lag_ratio=0.15), run_time=2.5)
        self.hasta(2)
        interp = tarjeta(T("inferencia: son reservas en lote, que se cancelan juntas", 28, AMARILLO), buff=0.25)
        interp.next_to(titulo_g, DOWN, buff=0.3)
        self.play(FadeIn(interp, shift=DOWN * 0.2), run_time=1.0)

        # v8: la gemela en train ------------------------------------------------
        self.seg("v8")
        self.play(FadeOut(VGroup(barras, textos, eje, titulo_g, interp)), run_time=0.6)
        caja_tr = RoundedRectangle(width=5.6, height=3.4, corner_radius=0.2, stroke_color=AZUL).shift(LEFT * 3.2)
        caja_va = RoundedRectangle(width=5.6, height=3.4, corner_radius=0.2, stroke_color=AMARILLO).shift(RIGHT * 3.2)
        t_tr = T("train", 28, AZUL).next_to(caja_tr, UP, buff=0.15)
        t_va = T("validación", 28, AMARILLO).next_to(caja_va, UP, buff=0.15)
        colores = list(rng.choice(paleta, 7))
        gem_tr = fila_reserva(colores).move_to(caja_tr).shift(UP * 0.4)
        gem_va = fila_reserva(colores).move_to(caja_va).shift(UP * 0.4)
        lab_tr = T("se canceló", 26, ROJO).next_to(gem_tr, DOWN, buff=0.3)
        lab_va = T("?", 40, AMARILLO).next_to(gem_va, DOWN, buff=0.25)
        self.play(Create(caja_tr), Create(caja_va), FadeIn(t_tr), FadeIn(t_va), FadeIn(gem_va), run_time=1.0)
        self.play(FadeIn(gem_tr), FadeIn(lab_tr), FadeIn(lab_va), run_time=0.8)
        arco = CurvedArrow(gem_tr.get_top() + UP * 0.1, gem_va.get_top() + UP * 0.1, angle=-PI / 3, color=NARANJA)
        self.play(Create(arco), run_time=1.0)
        self.play(Transform(lab_va, T("se canceló", 26, ROJO).move_to(lab_va)), run_time=0.8)
        self.hasta(1)
        frase = T("recordar no es entender", 36, NARANJA).to_edge(DOWN, buff=1.0)
        self.play(Write(frase), run_time=1.0)

        # v9: dos validaciones ---------------------------------------------------
        self.seg("v9")
        self.play(FadeOut(VGroup(caja_tr, caja_va, t_tr, t_va, gem_tr, gem_va, lab_tr, lab_va, arco, frase)), run_time=0.6)
        self.hasta(1)

        def esquema(color, nombre, juntas):
            caja = RoundedRectangle(width=5.6, height=4.2, corner_radius=0.2, stroke_color=color)
            titulo_e = T(nombre, 28, color).next_to(caja, UP, buff=0.15)
            tr = Rectangle(width=2.3, height=2.6, stroke_color=AZUL).move_to(caja).shift(LEFT * 1.3 + DOWN * 0.2)
            va = Rectangle(width=2.3, height=2.6, stroke_color=AMARILLO if color == AMARILLO else TURQUESA)
            va.move_to(caja).shift(RIGHT * 1.3 + DOWN * 0.2)
            etq = VGroup(T("train", 22, AZUL).next_to(tr, UP, buff=0.08), T("validación", 22, GRIS).next_to(va, UP, buff=0.08))
            filas_e = VGroup()
            colores_grupo = [NARANJA, VIOLETA, VERDE]
            for g, cg in enumerate(colores_grupo):
                for j in range(2):
                    r = Rectangle(width=1.7, height=0.24, stroke_width=0, fill_color=cg, fill_opacity=0.9)
                    if juntas:
                        destino_ = tr if g < 2 else va
                        r.move_to(destino_).shift(UP * (0.9 - (g % 2) * 0.8 - j * 0.32) if g < 2 else UP * (0.5 - j * 0.32))
                    else:
                        destino_ = tr if j == 0 else va
                        r.move_to(destino_).shift(UP * (0.8 - g * 0.6))
                    filas_e.add(r)
            return VGroup(caja, titulo_e, tr, va, etq, filas_e)

        izq = esquema(AMARILLO, "principal: estratificada al azar", juntas=False).scale(0.95).shift(LEFT * 3.3 + DOWN * 0.3)
        der = esquema(TURQUESA, "control: agrupada por copias", juntas=True).scale(0.95).shift(RIGHT * 3.3 + DOWN * 0.3)
        sub_i = VGroup(T("supuesto: la competencia evalúa", 24, GRIS), T("con reservas del mismo conjunto", 24, GRIS))
        sub_i.arrange(DOWN, buff=0.1).next_to(izq, DOWN, buff=0.2)
        sub_d = VGroup(T("estima el rendimiento con", 24, GRIS), T("reservas nunca vistas", 24, GRIS))
        sub_d.arrange(DOWN, buff=0.1).next_to(der, DOWN, buff=0.2)
        self.play(FadeIn(izq), run_time=1.2)
        self.play(FadeIn(sub_i), run_time=0.6)
        self.hasta(2)
        self.play(FadeIn(der), run_time=1.2)
        self.play(FadeIn(sub_d), run_time=0.6)

        # v10: la brecha ---------------------------------------------------------
        self.seg("v10")
        self.play(FadeOut(VGroup(izq, der, sub_i, sub_d)), run_time=0.6)
        escala = NumberLine(x_range=[0.92, 0.96, 0.01], length=5, rotation=PI / 2, color=GRIS_OSCURO,
                            include_numbers=False).shift(RIGHT * 1.2 + DOWN * 0.5)
        marcas = VGroup(*[T(num(v, 2), 22, GRIS).next_to(escala.n2p(v), LEFT, buff=0.2) for v in [0.92, 0.93, 0.94, 0.95, 0.96]])
        titulo_b = T("AUC del Random Forest baseline", 30).to_edge(UP, buff=0.9)
        self.play(FadeIn(titulo_b), Create(escala), FadeIn(marcas), run_time=1.0)
        self.hasta(1)
        p_azar = Dot(escala.n2p(0.9557), radius=0.12, color=AMARILLO)
        p_grup = Dot(escala.n2p(0.9374), radius=0.12, color=TURQUESA)
        l_azar = T("al azar: 0,956", 30, AMARILLO).next_to(p_azar, RIGHT, buff=0.3)
        l_grup = T("agrupada: 0,937", 30, TURQUESA).next_to(p_grup, RIGHT, buff=0.3)
        self.play(FadeIn(p_azar, scale=2), Write(l_azar), run_time=1.0)
        self.play(FadeIn(p_grup, scale=2), Write(l_grup), run_time=1.0)
        llave = BraceBetweenPoints(p_azar.get_center() + LEFT * 0.4, p_grup.get_center() + LEFT * 0.4, direction=LEFT)
        llave.next_to(VGroup(p_azar, p_grup), LEFT, buff=1.1)
        texto_llave = VGroup(T("brecha 0,018:", 26, NARANJA), T("lo que aporta memorizar", 26, NARANJA)).arrange(DOWN, aligned_edge=RIGHT)
        texto_llave.next_to(llave, LEFT, buff=0.2)
        self.play(FadeOut(marcas), GrowFromCenter(llave), FadeIn(texto_llave), run_time=1.2)

        # v11: leakage ---------------------------------------------------------------
        self.seg("v11")
        self.play(FadeOut(VGroup(escala, titulo_b, p_azar, p_grup, l_azar, l_grup, llave, texto_llave)), run_time=0.6)
        self.hasta(1)
        cols = VGroup(*[C(c, 30, BLANCO) for c in ["execution_status", "execution_status_date"]]).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        cols.shift(LEFT * 2.5 + UP * 1.3)
        self.play(FadeIn(cols), run_time=0.8)
        tachas = VGroup(*[tachar(c) for c in cols])
        motivo = T("se conocen después de ejecutar", 26, ROJO).next_to(cols, RIGHT, buff=0.6)
        self.play(Create(tachas), FadeIn(motivo), run_time=1.0)
        self.hasta(2)
        tp2 = T("como duration en Bank Marketing (TP2)", 26, GRIS).next_to(motivo, DOWN, buff=0.25, aligned_edge=LEFT)
        self.play(FadeIn(tp2), run_time=0.8)
        self.hasta(3)
        cols2 = VGroup(*[C(c, 30, BLANCO) for c in ["assigned_gpu_type", "queue_wait_time"]]).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        cols2.next_to(cols, DOWN, buff=1.0, aligned_edge=LEFT)
        self.play(FadeIn(cols2), run_time=0.8)
        tachas2 = VGroup(*[tachar(c, NARANJA) for c in cols2])
        motivo2 = VGroup(T("GPU finalmente asignada y espera en cola", 26, NARANJA),
                         T("agregarlas: +0,0014 de AUC", 26, GRIS)).arrange(DOWN, aligned_edge=LEFT)
        motivo2.next_to(cols2, RIGHT, buff=0.6)
        self.play(Create(tachas2), FadeIn(motivo2), run_time=1.2)
        self.terminar()
