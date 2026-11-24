"""Capítulo 2: diagnóstico (sesgo, varianza, error irreducible, curvas)."""

import numpy as np
from manim import *

from base import *

PROFUNDIDADES = ["8", "12", "16", "20", "sin límite"]
AUC_TRAIN = [0.9281, 0.9529, 0.9733, 0.9870, 0.9997]
AUC_AZAR = [0.9217, 0.9367, 0.9457, 0.9512, 0.9557]
AUC_GRUPOS = [0.9161, 0.9273, 0.9342, 0.9371, 0.9374]

FILAS = [3062, 7655, 15309, 22964, 30618]
LC_AZAR = [0.9275, 0.9396, 0.9484, 0.9530, 0.9555]
LC_GRUPOS = [0.9186, 0.9285, 0.9334, 0.9359, 0.9373]


def diana(puntos, color):
    anillos = VGroup(*[Circle(r, color=GRIS_OSCURO, stroke_width=2) for r in (1.2, 0.8, 0.4)])
    centro = Dot(radius=0.06, color=BLANCO)
    tiros = VGroup(*[Dot(np.array([x, y, 0]), radius=0.07, color=color) for x, y in puntos])
    return VGroup(anillos, centro, tiros)


def nodo(lineas, color, ancho=3.3, tam=22):
    texto = VGroup(*[T(l, tam, BLANCO) for l in lineas]).arrange(DOWN, buff=0.08)
    caja = RoundedRectangle(width=max(ancho, texto.width + 0.3), height=texto.height + 0.4, corner_radius=0.12, stroke_color=color,
                            stroke_width=2.5, fill_color=TARJETA, fill_opacity=1)
    return VGroup(caja, texto.move_to(caja))


def ejes(x_rango, y_rango, largo_x, largo_y):
    return Axes(x_range=x_rango, y_range=y_rango, x_length=largo_x, y_length=largo_y, tips=False,
                axis_config={"color": GRIS_OSCURO, "include_numbers": False, "stroke_width": 2})


def serie(ax, xs, ys, color, ancho=4):
    puntos = [ax.c2p(x, y) for x, y in zip(xs, ys)]
    linea = VMobject(color=color, stroke_width=ancho).set_points_as_corners(puntos)
    dots = VGroup(*[Dot(p, radius=0.07, color=color) for p in puntos])
    return VGroup(linea, dots)


class Diagnostico(Escena):
    CAPITULO = "2 · Diagnosticar"

    def construct(self):
        # d1 -------------------------------------------------------------------
        self.seg("d1")
        metrica = T("AUC 0,956", 72, AMARILLO)
        self.play(Write(metrica), run_time=1.5)
        self.hasta(1)
        self.play(metrica.animate.scale(0.6).to_edge(UP, buff=0.8), run_time=0.8)
        opciones = VGroup(*[tarjeta(T(o, 28), buff=0.22) for o in
                            ["más datos", "otro modelo", "más variables", "otros hiperparámetros"]])
        opciones.arrange_in_grid(2, 2, buff=(0.8, 0.5)).shift(DOWN * 0.1)
        self.play(LaggedStart(*[FadeIn(o, scale=0.8) for o in opciones], lag_ratio=0.2), run_time=1.2)
        self.hasta(2)
        frase = M(f'la métrica dice <span foreground="{AMARILLO}">que</span> hay un problema, '
                  f'no <span foreground="{AMARILLO}">cuál</span>', 32).to_edge(DOWN, buff=1.0)
        self.play(FadeIn(frase, shift=UP * 0.2), run_time=1.0)

        # d2: tres fuentes de error ----------------------------------------------------
        self.seg("d2")
        self.limpiar()
        titulo = self.titulo("Tres fuentes de error")
        self.play(Write(titulo), run_time=1.0)
        rng = np.random.default_rng(5)
        sesgo = diana([(0.55 + rng.normal(0, 0.1), 0.45 + rng.normal(0, 0.1)) for _ in range(9)], ROJO)
        varianza = diana([tuple(rng.normal(0, 0.55, 2)) for _ in range(9)], AMARILLO)
        irreducible = VGroup(
            Circle(1.2, color=GRIS_OSCURO, stroke_width=2),
            T("misma X", 26, BLANCO).shift(UP * 0.35),
            M(f'<span foreground="{ROJO}">se cancela</span> / <span foreground="{AZUL}">se ejecuta</span>', 22).shift(DOWN * 0.2),
        )
        columnas = VGroup(sesgo, varianza, irreducible).arrange(RIGHT, buff=1.6).shift(DOWN * 0.1)
        nombres = [("Sesgo", ROJO, ["el modelo no puede", "representar la relación"]),
                   ("Varianza", AMARILLO, ["aprendió detalles", "de esta muestra"]),
                   ("Irreducible", TURQUESA, ["lo que X", "no explica"])]
        textos = VGroup()
        for col, (n, c, desc) in zip(columnas, nombres):
            g = VGroup(T(n, 32, c, weight=BOLD), *[T(d, 22, GRIS) for d in desc]).arrange(DOWN, buff=0.1)
            g.next_to(col, DOWN, buff=0.3)
            textos.add(g)
        for i in range(3):
            self.hasta(i + 1)
            self.play(FadeIn(columnas[i], scale=0.8), FadeIn(textos[i], shift=UP * 0.2), run_time=1.0)

        # d3: error irreducible en nuestros datos --------------------------------------
        self.seg("d3")
        self.play(FadeOut(VGroup(columnas[:2], textos[:2])), FadeOut(titulo), run_time=0.6)
        self.play(VGroup(columnas[2], textos[2]).animate.scale(0.8).to_edge(LEFT, buff=1.0), run_time=0.8)
        self.hasta(1)
        colores = ["#3A4A5C", "#556B82", "#2E3B4A", "#4B5D73", "#43566B", "#36475A", "#556B82", "#3A4A5C"]
        filas = VGroup()
        for _ in range(2):
            filas.add(VGroup(*[Rectangle(width=0.45, height=0.32, stroke_color=FONDO, stroke_width=2, fill_color=c,
                                         fill_opacity=1) for c in colores]).arrange(RIGHT, buff=0))
        filas.arrange(DOWN, buff=0.35).shift(RIGHT * 1.6 + UP * 0.6)
        etq = VGroup(T("se canceló", 26, ROJO).next_to(filas[0], RIGHT, buff=0.4),
                     T("se ejecutó", 26, AZUL).next_to(filas[1], RIGHT, buff=0.4))
        self.play(FadeIn(filas), run_time=0.8)
        dato = M(f'<span foreground="{TURQUESA}">79 grupos</span> idénticos con etiquetas distintas (531 filas)', 28)
        dato.next_to(filas, DOWN, buff=0.7).shift(RIGHT * 0.6)
        self.play(FadeIn(dato), run_time=0.8)
        self.hasta(2)
        self.play(FadeIn(etq, shift=LEFT * 0.2), run_time=0.8)
        self.hasta(3)
        cota = T("ningún modelo puede acertarlas a todas", 28, GRIS).next_to(dato, DOWN, buff=0.3)
        self.play(FadeIn(cota), run_time=0.8)

        # d4 y d5: árbol de diagnóstico ----------------------------------------------
        self.seg("d4")
        self.limpiar()
        raiz = nodo(["¿rinde bien en train?"], BLANCO, 4.2, 28).move_to(UP * 2.4)
        izq = nodo(["no: subajuste", "(sesgo)"], ROJO, 3.4, 26).move_to(LEFT * 3.6 + UP * 0.7)
        der = nodo(["sí, pero validación no:", "sobreajuste (varianza)"], AMARILLO, 4.2, 26).move_to(RIGHT * 3.6 + UP * 0.7)
        hojas_i = VGroup(nodo(["falta capacidad", "→ modelo", "más flexible"], ROJO, 3.0, 21),
                         nodo(["falta información", "→ mejores variables", "o más datos"], ROJO, 3.0, 21))
        hojas_d = VGroup(nodo(["aprende ruido", "→ simplificar", "o regularizar"], AMARILLO, 3.0, 21),
                         nodo(["señal que no", "generaliza", "→ validar por grupos"], AMARILLO, 3.0, 21))
        for h, x in zip([*hojas_i, *hojas_d], [-5.25, -1.85, 1.85, 5.25]):
            h.move_to([x, -1.5, 0])

        def flecha(a, b, texto=None):
            f = Arrow(a.get_bottom(), b.get_top(), buff=0.08, color=GRIS, stroke_width=3, max_tip_length_to_length_ratio=0.12)
            if texto:
                return VGroup(f, T(texto, 22, GRIS).next_to(f.get_center(), UP if False else LEFT, buff=0.1))
            return VGroup(f)

        self.play(FadeIn(raiz, shift=DOWN * 0.2), run_time=0.8)
        self.hasta(1)
        f_izq = flecha(raiz, izq)
        self.play(Create(f_izq), FadeIn(izq), run_time=0.9)
        self.hasta(2)
        f_hi = VGroup(*[flecha(izq, h) for h in hojas_i])
        self.play(Create(f_hi), LaggedStart(*[FadeIn(h) for h in hojas_i], lag_ratio=0.3), run_time=1.2)

        self.seg("d5")
        f_der = flecha(raiz, der)
        self.play(Create(f_der), FadeIn(der), run_time=0.9)
        self.hasta(1)
        f_hd = VGroup(*[flecha(der, h) for h in hojas_d])
        self.play(Create(f_hd), LaggedStart(*[FadeIn(h) for h in hojas_d], lag_ratio=0.3), run_time=1.2)
        self.hasta(2)
        self.play(hojas_d[1][0].animate.set_stroke(TURQUESA, 4), Indicate(hojas_d[1][1], color=TURQUESA), run_time=1.2)
        ref = T("¡las reservas en lote!", 26, TURQUESA).next_to(hojas_d[1], DOWN, buff=0.3)
        self.play(FadeIn(ref), run_time=0.6)

        # d6 a d9: curva de validación ----------------------------------------------
        self.seg("d6")
        self.limpiar()
        self.hasta(1)
        ax = ejes([-0.4, 4.4, 1], [0.90, 1.005, 0.02], 8.4, 4.5).shift(DOWN * 0.05 + LEFT * 0.6)
        y_marcas = VGroup(*[T(num(v, 2), 20, GRIS).next_to(ax.c2p(-0.4, v), LEFT, buff=0.15) for v in [0.90, 0.92, 0.94, 0.96, 0.98, 1.0]])
        x_marcas = VGroup(*[T(p, 22, GRIS).next_to(ax.c2p(i, 0.90), DOWN, buff=0.2) for i, p in enumerate(PROFUNDIDADES)])
        x_titulo = T("profundidad máxima (complejidad →)", 24, GRIS).next_to(x_marcas, DOWN, buff=0.2)
        y_titulo = T("AUC", 24, GRIS).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        titulo_g = T("Curva de validación del Random Forest", 32, BLANCO).to_edge(UP, buff=0.75)
        self.play(FadeIn(titulo_g), Create(ax), FadeIn(y_marcas), FadeIn(x_marcas), FadeIn(x_titulo), FadeIn(y_titulo),
                  run_time=1.5)
        xs = list(range(5))
        tr = serie(ax, xs, AUC_TRAIN, AZUL)
        az = serie(ax, xs, AUC_AZAR, AMARILLO)
        gr = serie(ax, xs, AUC_GRUPOS, TURQUESA)
        leyenda = VGroup(
            VGroup(Line(ORIGIN, RIGHT * 0.5, color=AZUL, stroke_width=5), T("train", 24, AZUL)).arrange(RIGHT),
            VGroup(Line(ORIGIN, RIGHT * 0.5, color=AMARILLO, stroke_width=5), T("validación al azar", 24, AMARILLO)).arrange(RIGHT),
            VGroup(Line(ORIGIN, RIGHT * 0.5, color=TURQUESA, stroke_width=5), T("validación agrupada", 24, TURQUESA)).arrange(RIGHT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        leyenda.move_to(ax.c2p(-0.2, 1.0), aligned_edge=UL)

        self.seg("d7")
        self.play(Create(tr[0]), FadeIn(tr[1]), FadeIn(leyenda[0]), run_time=1.3)
        self.hasta(1)
        etq_tr = T("0,9997", 24, AZUL).next_to(tr[1][-1], UP, buff=0.12)
        self.play(FadeIn(etq_tr), Indicate(tr[1][-1], color=AZUL), run_time=1.0)
        self.hasta(2)
        self.play(Create(az[0]), FadeIn(az[1]), FadeIn(leyenda[1]), run_time=1.3)
        etq_az = T("0,956", 24, AMARILLO).next_to(az[1][-1], RIGHT, buff=0.12)
        self.play(FadeIn(etq_az), run_time=0.5)
        self.hasta(3)
        self.play(Create(gr[0]), FadeIn(gr[1]), FadeIn(leyenda[2]), run_time=1.3)
        etq_gr = T("0,937", 24, TURQUESA).next_to(gr[1][-1], RIGHT, buff=0.12)
        self.play(FadeIn(etq_gr), run_time=0.5)

        self.seg("d8")
        self.hasta(1)
        brechas = VGroup()
        for i, texto in [(0, "0,006"), (4, "0,018")]:
            arriba, abajo = ax.c2p(i, AUC_AZAR[i]), ax.c2p(i, AUC_GRUPOS[i])
            seg_ = Line(arriba, abajo, color=NARANJA, stroke_width=6)
            etq_b = T(texto, 24, NARANJA).next_to(seg_, LEFT if i == 4 else RIGHT, buff=0.12)
            if i == 0:
                etq_b.shift(DOWN * 0.35)
            brechas.add(VGroup(seg_, etq_b))
        self.play(LaggedStart(*[Create(b) for b in brechas], lag_ratio=0.5), run_time=1.6)
        self.hasta(2)
        lote = T("los árboles profundos memorizan los lotes", 26, NARANJA).next_to(titulo_g, DOWN, buff=0.2)
        self.play(FadeIn(lote), run_time=0.8)
        self.hasta(3)
        elegida = SurroundingRectangle(VGroup(x_marcas[4], gr[1][-1], tr[1][-1]), color=VERDE, buff=0.15)
        self.play(Create(elegida), run_time=1.0)

        self.seg("d9")
        logistica = DashedLine(ax.c2p(-0.4, 0.913), ax.c2p(4.4, 0.913), color=GRIS, dash_length=0.12)
        etq_lr = T("regresión logística: train ≈ validación ≈ 0,913", 22, GRIS)
        etq_lr.move_to(ax.c2p(1.3, 0.9145), aligned_edge=DL)
        self.play(FadeOut(elegida), FadeOut(lote), FadeOut(brechas[0][1]), Create(logistica), FadeIn(etq_lr), run_time=1.2)
        self.hasta(1)
        sesgo_t = T("→ sesgo: una frontera lineal no alcanza", 24, ROJO)
        sesgo_t.move_to(ax.c2p(1.3, 0.9115), aligned_edge=UL)
        self.play(FadeIn(sesgo_t), run_time=0.8)

        # d10 y d11: curvas de aprendizaje teóricas ------------------------------------
        self.seg("d10")
        self.limpiar()
        titulo_lc = T("Curva de aprendizaje: rendimiento según la cantidad de filas", 32).to_edge(UP, buff=0.75)
        self.play(FadeIn(titulo_lc), run_time=0.8)
        self.hasta(1)
        paneles = VGroup()
        for _ in range(2):
            a = ejes([0, 10, 1], [0.5, 1.0, 0.1], 5.0, 3.4)
            paneles.add(a)
        paneles.arrange(RIGHT, buff=1.4).shift(DOWN * 0.4)
        xs_t = np.linspace(0.6, 10, 40)
        sub_tr = paneles[0].plot_line_graph(xs_t, 0.78 + 0.18 * np.exp(-xs_t / 2.2), line_color=AZUL, add_vertex_dots=False, stroke_width=4)
        sub_va = paneles[0].plot_line_graph(xs_t, 0.76 - 0.2 * np.exp(-xs_t / 2.0), line_color=AMARILLO, add_vertex_dots=False, stroke_width=4)
        sob_tr = paneles[1].plot_line_graph(xs_t, 0.99 - 0.0035 * xs_t, line_color=AZUL, add_vertex_dots=False, stroke_width=4)
        xs_v = np.linspace(0.6, 6.5, 30)
        curva_v = lambda x: 0.985 - 0.36 * np.exp(-x / 4.2)  # noqa: E731
        sob_va = paneles[1].plot_line_graph(xs_v, curva_v(xs_v), line_color=AMARILLO, add_vertex_dots=False, stroke_width=4)
        xs_e = np.linspace(6.5, 10, 12)
        sob_ext = DashedVMobject(paneles[1].plot_line_graph(xs_e, curva_v(xs_e), line_color=AMARILLO,
                                                            add_vertex_dots=False, stroke_width=4)["line_graph"], num_dashes=8)
        nombres_p = VGroup(T("subajuste", 30, ROJO).next_to(paneles[0], UP, buff=0.2),
                           T("sobreajuste", 30, AMARILLO).next_to(paneles[1], UP, buff=0.2))
        ejes_x = VGroup(*[T("filas de entrenamiento →", 20, GRIS).next_to(p, DOWN, buff=0.15) for p in paneles])
        leyenda_lc = VGroup(
            VGroup(Line(ORIGIN, RIGHT * 0.4, color=AZUL, stroke_width=5), T("train", 22, AZUL)).arrange(RIGHT),
            VGroup(Line(ORIGIN, RIGHT * 0.4, color=AMARILLO, stroke_width=5), T("validación", 22, AMARILLO)).arrange(RIGHT),
        ).arrange(RIGHT, buff=0.6).to_edge(DOWN, buff=0.6)
        self.play(Create(paneles), FadeIn(ejes_x), FadeIn(leyenda_lc), FadeIn(nombres_p), run_time=1.2)

        self.seg("d11")
        self.play(Create(sub_tr), Create(sub_va), run_time=2.0)
        nota_sub = T("convergen abajo: más datos no ayudan", 22, GRIS).next_to(paneles[0], DOWN, buff=0.6)
        self.play(FadeIn(nota_sub), run_time=0.6)
        self.hasta(1)
        self.play(Create(sob_tr), Create(sob_va), run_time=2.0)
        self.play(Create(sob_ext), run_time=0.8)
        nota_sob = T("brecha y validación subiendo: más datos sí", 22, GRIS).next_to(paneles[1], DOWN, buff=0.6)
        self.play(FadeIn(nota_sob), run_time=0.6)

        # d12: nuestra curva -------------------------------------------------------------
        self.seg("d12")
        self.limpiar()
        ax2 = ejes([0, 32000, 5000], [0.91, 1.005, 0.01], 8.4, 4.8).shift(DOWN * 0.3 + LEFT * 0.9)
        y_m = VGroup(*[T(num(v, 2), 20, GRIS).next_to(ax2.c2p(0, v), LEFT, buff=0.15) for v in [0.92, 0.94, 0.96, 0.98, 1.0]])
        x_m = VGroup(*[T(f"{v:,}".replace(",", "."), 20, GRIS).next_to(ax2.c2p(v, 0.91), DOWN, buff=0.15) for v in [5000, 15000, 25000]])
        x_t = T("filas de entrenamiento", 22, GRIS).next_to(x_m, DOWN, buff=0.2)
        titulo_n = T("Nuestra curva de aprendizaje (baseline)", 32).to_edge(UP, buff=0.75)
        self.play(FadeIn(titulo_n), Create(ax2), FadeIn(y_m), FadeIn(x_m), FadeIn(x_t), run_time=1.2)
        self.hasta(1)
        tr2 = DashedLine(ax2.c2p(FILAS[0], 0.9995), ax2.c2p(FILAS[-1], 0.9995), color=AZUL, stroke_width=4)
        etq_tr2 = T("train ≈ 1", 24, AZUL).next_to(tr2, RIGHT, buff=0.15)
        self.play(Create(tr2), FadeIn(etq_tr2), run_time=1.0)
        self.hasta(2)
        az2 = serie(ax2, FILAS, LC_AZAR, AMARILLO)
        self.play(Create(az2[0]), FadeIn(az2[1]), run_time=1.6)
        etq_az2 = T("al azar: 0,93 → 0,96", 24, AMARILLO).next_to(az2[1][-1], RIGHT, buff=0.15)
        self.play(FadeIn(etq_az2), run_time=0.6)
        self.hasta(3)
        gr2 = serie(ax2, FILAS, LC_GRUPOS, TURQUESA)
        self.play(Create(gr2[0]), FadeIn(gr2[1]), run_time=1.6)
        etq_gr2 = T("agrupada: 0,919 → 0,937", 24, TURQUESA).next_to(gr2[1][-1], RIGHT, buff=0.15).shift(DOWN * 0.15)
        self.play(FadeIn(etq_gr2), run_time=0.6)
        self.hasta(4)
        tramo = Line(gr2[1][-2].get_center(), gr2[1][-1].get_center(), color=NARANJA, stroke_width=9)
        etq_tramo = T("último 25 %: +0,0014", 24, NARANJA).next_to(tramo, DOWN, buff=0.35)
        self.play(Create(tramo), FadeIn(etq_tramo), run_time=1.2)

        # d13: conclusión ------------------------------------------------------------
        self.seg("d13")
        self.limpiar()
        self.hasta(1)
        renglones = VGroup(
            M(f'<span foreground="{VERDE}">✓</span>  capacidad del modelo: de sobra (train ≈ 1)', 32),
            M(f'<span foreground="{ROJO}">✗</span>  más reservas del mismo tipo: casi nada', 32),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).shift(UP * 1.0)
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in renglones], lag_ratio=0.5), run_time=2.0)
        self.hasta(2)
        limite = tarjeta(T("el límite es la información de las variables", 36, AMARILLO), color=AMARILLO, buff=0.3)
        limite.next_to(renglones, DOWN, buff=0.7)
        self.play(FadeIn(limite, scale=0.9), run_time=1.0)
        self.hasta(3)
        pregunta = T("¿dónde falta información?", 44, BLANCO, weight=BOLD).next_to(limite, DOWN, buff=0.7)
        self.play(Write(pregunta), run_time=1.4)
        self.terminar()
