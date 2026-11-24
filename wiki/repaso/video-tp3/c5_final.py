"""Capítulo 5: modelo final, test, predictor y producción."""

import numpy as np
from manim import *

from base import *


def caja(texto, color, tam=24, ancho=None):
    etiqueta = VGroup(*[T(l, tam, BLANCO) for l in texto.split("\n")]).arrange(DOWN, buff=0.06)
    rect = RoundedRectangle(width=ancho or etiqueta.width + 0.5, height=etiqueta.height + 0.4, corner_radius=0.12,
                            stroke_color=color, stroke_width=2.5, fill_color=TARJETA, fill_opacity=1)
    return VGroup(rect, etiqueta.move_to(rect))


def intervalo(linea, a, b, color, y=0.0, alto=0.22):
    p0, p1 = linea.n2p(a) + UP * y, linea.n2p(b) + UP * y
    return VGroup(Line(p0, p1, color=color, stroke_width=6),
                  Line(p0 + UP * alto / 2, p0 + DOWN * alto / 2, color=color, stroke_width=4),
                  Line(p1 + UP * alto / 2, p1 + DOWN * alto / 2, color=color, stroke_width=4))


class Final(Escena):
    CAPITULO = "5 · Modelo final y producción"

    def construct(self):
        # f1: la validación elige una receta ------------------------------------------------
        self.seg("f1")
        self.hasta(1)
        frase = T("la validación cruzada elige…", 36).shift(UP * 2.0)
        frontera = T("una frontera de decisión", 36, GRIS).next_to(frase, DOWN, buff=0.35)
        self.play(FadeIn(frase), FadeIn(frontera), run_time=1.0)
        self.play(Create(tachar(frontera)), run_time=0.6)
        self.hasta(2)
        receta = tarjeta(T("una receta: variables + algoritmo + hiperparámetros", 32, AMARILLO), color=AMARILLO, buff=0.25)
        receta.next_to(frontera, DOWN, buff=0.45)
        self.play(FadeIn(receta, shift=UP * 0.2), run_time=1.0)
        self.hasta(3)
        dev = caja("desarrollo\n38.273 reservas", AZUL, 26)
        final = caja("modelo final", VERDE, 28)
        test = caja("test 9.569\nbajo llave", GRIS, 26)
        fila = VGroup(dev, final, test).arrange(RIGHT, buff=1.2).shift(DOWN * 1.9)
        flecha = Arrow(dev.get_right(), final.get_left(), buff=0.1, color=GRIS)
        self.play(FadeIn(dev), GrowArrow(flecha), FadeIn(final), FadeIn(test), run_time=1.4)

        # f2: umbral para balanced accuracy ----------------------------------------------
        self.seg("f2")
        self.limpiar()
        t2 = T("umbral elegido con predicciones out-of-fold", 34).to_edge(UP, buff=0.8)
        self.play(FadeIn(t2), run_time=0.8)
        self.hasta(1)
        aviso = tarjeta(T("leaderboard del 05/11: la competencia mide balanced accuracy", 28, AMARILLO), color=AMARILLO,
                        buff=0.2).next_to(t2, DOWN, buff=0.35)
        formula = M(f'balanced accuracy = ½ · (aciertos en <span foreground="{ROJO}">canceladas</span> + '
                    f'aciertos en <span foreground="{AZUL}">ejecutadas</span>)', 28).next_to(aviso, DOWN, buff=0.3)
        self.play(FadeIn(aviso, shift=DOWN * 0.2), run_time=0.8)
        self.play(Write(formula), run_time=1.6)
        self.hasta(2)
        linea = NumberLine(x_range=[0.25, 0.55, 0.05], length=10, color=GRIS_OSCURO, include_numbers=False).shift(DOWN * 1.6)
        marcas = VGroup(*[T(num(v, 2), 22, GRIS).next_to(linea.n2p(v), DOWN, buff=0.2) for v in [0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55]])
        tasas = VGroup()
        for valor, texto, color in [(0.417, "tasa de cancelación\nen desarrollo: 41,7 %", BLANCO), (0.287, "en reservas\núnicas: 29 %", NARANJA)]:
            tick = Line(linea.n2p(valor) + DOWN * 0.15, linea.n2p(valor) + UP * 0.15, color=color, stroke_width=4)
            etq = VGroup(*[T(l, 20, color) for l in texto.split("\n")]).arrange(DOWN, buff=0.04).next_to(tick, UP, buff=0.1)
            tasas.add(VGroup(tick, etq))
        nota_c = T("con probabilidades calibradas, el mejor umbral es la tasa de la clase", 22, GRIS).next_to(formula, DOWN, buff=0.3)
        self.play(Create(linea), FadeIn(marcas), FadeIn(nota_c), run_time=1.0)
        self.play(LaggedStart(*[FadeIn(t) for t in tasas], lag_ratio=0.4), run_time=1.2)
        self.hasta(3)
        zonas = VGroup()
        for (a, b), color, y, nombre in [((0.39, 0.45), AMARILLO, 1.15, "al azar"), ((0.40, 0.44), TURQUESA, 1.45, "agrupada")]:
            barra = Line(linea.n2p(a) + UP * y, linea.n2p(b) + UP * y, color=color, stroke_width=8)
            zonas.add(VGroup(barra, T(nombre, 18, color).next_to(barra, RIGHT, buff=0.12)))
        self.play(FadeIn(zonas), run_time=0.8)
        elegido = T("umbral = 0,40", 36, AMARILLO, weight=BOLD).next_to(marcas[3], DOWN, buff=0.3)
        self.play(marcas[3].animate.set_color(AMARILLO).scale(1.3), Write(elegido), run_time=1.0)

        # f3: test, una sola vez ---------------------------------------------------------------
        self.seg("f3")
        self.limpiar()
        candado = caja("test: 9.569 reservas", AMARILLO, 30).to_edge(UP, buff=0.8)
        self.play(FadeIn(candado, scale=1.1), run_time=0.8)
        self.hasta(1)
        auc = VGroup(T("AUC", 32, GRIS), T("0,960", 68, AMARILLO, weight=BOLD)).arrange(DOWN, buff=0.15).shift(LEFT * 3.2 + UP * 0.7)
        self.play(FadeIn(auc[0]), Write(auc[1]), run_time=1.0)
        self.hasta(2)
        ba = VGroup(T("balanced accuracy", 32, GRIS), T("0,888", 68, AMARILLO, weight=BOLD)).arrange(DOWN, buff=0.15).shift(RIGHT * 3.2 + UP * 0.7)
        self.play(FadeIn(ba[0]), Write(ba[1]), run_time=1.0)
        self.hasta(3)
        boot = T("bootstrap: 2.000 remuestreos de las filas de test", 26, GRIS).shift(DOWN * 2.0)
        ic_auc = T("IC 95 %: 0,957 a 0,963", 30, BLANCO).next_to(auc, DOWN, buff=0.5)
        ic_ba = T("IC 95 %: 0,881 a 0,894", 30, BLANCO).next_to(ba, DOWN, buff=0.5)
        self.play(FadeIn(boot), run_time=0.8)
        self.play(FadeIn(ic_auc, shift=UP * 0.2), FadeIn(ic_ba, shift=UP * 0.2), run_time=1.0)

        # f4: diferencia con el baseline ----------------------------------------------------------
        self.seg("f4")
        self.limpiar()
        t4 = T("modelo final menos baseline, en test (IC 95 %)", 32).to_edge(UP, buff=0.8)
        linea = NumberLine(x_range=[-0.004, 0.006, 0.001], length=10, color=GRIS_OSCURO, include_numbers=False).shift(DOWN * 1.6)
        marcas = VGroup(*[T(("+" if v > 0 else "") + num(v, 3), 22, GRIS).next_to(linea.n2p(v), DOWN, buff=0.2)
                          for v in [-0.004, -0.002, 0, 0.002, 0.004, 0.006]])
        cero = DashedLine(linea.n2p(0) + DOWN * 0.1, linea.n2p(0) + UP * 3.2, color=BLANCO, stroke_width=2)
        self.play(FadeIn(t4), Create(linea), FadeIn(marcas), Create(cero), run_time=1.0)
        i_auc = intervalo(linea, 0.0003, 0.0023, VERDE, y=2.6)
        p_auc = Dot(linea.n2p(0.0013) + UP * 2.6, radius=0.1, color=VERDE)
        e_auc = T("AUC: +0,0013  (0,0003 a 0,0023)", 26, VERDE).next_to(i_auc, UP, buff=0.2).align_to(i_auc, LEFT)
        self.play(Create(i_auc), FadeIn(p_auc), FadeIn(e_auc), run_time=1.2)
        si = T("no incluye el cero: la mejora se confirma", 24, VERDE).next_to(i_auc, DOWN, buff=0.15).align_to(i_auc, LEFT)
        self.play(FadeIn(si), run_time=0.6)
        self.hasta(1)
        i_ba = intervalo(linea, -0.0024, 0.0050, GRIS, y=1.0)
        p_ba = Dot(linea.n2p(0.0012) + UP * 1.0, radius=0.1, color=GRIS)
        e_ba = VGroup(T("balanced accuracy: +0,0012", 24, GRIS), T("(−0,0024 a +0,0050)", 24, GRIS))
        e_ba.arrange(DOWN, aligned_edge=RIGHT, buff=0.08).next_to(i_ba, UP, buff=0.2)
        e_ba.shift(RIGHT * (linea.n2p(-0.0002)[0] - e_ba.get_right()[0]))
        self.play(Create(i_ba), FadeIn(p_ba), FadeIn(e_ba), run_time=1.2)
        self.hasta(2)
        no = T("cruza el cero: no se distingue", 24, ROJO).next_to(i_ba, DOWN, buff=0.15)
        no.shift(RIGHT * (linea.n2p(-0.0002)[0] - no.get_right()[0]))
        self.play(FadeIn(no), run_time=0.6)

        # f5: gemelas y escenarios ---------------------------------------------------------------
        self.seg("f5")
        self.limpiar()
        self.hasta(1)
        escala = 5.0 / 0.5  # barras desde 0,5
        b_con = Rectangle(width=(0.988 - 0.5) * escala, height=0.5, stroke_width=0, fill_color=TURQUESA, fill_opacity=0.9)
        b_sin = Rectangle(width=(0.795 - 0.5) * escala, height=0.5, stroke_width=0, fill_color=NARANJA, fill_opacity=0.9)
        e_con = T("con gemela en desarrollo", 26, TURQUESA)
        e_sin = T("sin gemela", 26, NARANJA)
        VGroup(e_con, e_sin).arrange(DOWN, aligned_edge=RIGHT, buff=0.45).move_to([-2.3, 1.9, 0], aligned_edge=RIGHT)
        b_con.next_to(e_con, RIGHT, buff=0.3)
        b_sin.next_to(e_sin, RIGHT, buff=0.3).align_to(b_con, LEFT)
        v_con = T("0,988", 28).next_to(b_con, RIGHT, buff=0.2)
        v_sin = T("0,795", 28).next_to(b_sin, RIGHT, buff=0.2)
        t5 = T("balanced accuracy (BA) en test, barras desde 0,5", 26, GRIS).next_to(VGroup(e_con, b_con), UP, buff=0.3)
        self.play(FadeIn(t5), FadeIn(e_con), GrowFromEdge(b_con, LEFT), FadeIn(v_con), run_time=1.0)
        self.hasta(2)
        self.play(FadeIn(e_sin), GrowFromEdge(b_sin, LEFT), FadeIn(v_sin), run_time=1.0)
        self.hasta(3)
        escenarios = VGroup()
        for titulo_e, linea_e, color in [("mismo conjunto de reservas", "AUC 0,96 · BA 0,89", AMARILLO),
                                         ("reservas nuevas", "AUC 0,94 · BA 0,86", TURQUESA),
                                         ("solo reservas individuales", "AUC 0,89 · BA 0,79", NARANJA)]:
            escenarios.add(tarjeta(VGroup(T(titulo_e, 22, color), T(linea_e, 28)).arrange(DOWN, buff=0.12), color=color, ancho=4.3))
        escenarios.arrange(RIGHT, buff=0.2).shift(DOWN * 0.7)
        for i in range(3):
            self.hasta(4 + i)
            self.play(FadeIn(escenarios[i], shift=UP * 0.2), run_time=0.8)
        self.hasta(7)
        pista = VGroup(T("leaderboard 05/11: ningún grupo pasó de 0,91 de AUC", 26, BLANCO),
                       T("pista (interpretación): la evaluación se parece más a los dos últimos", 24, GRIS)).arrange(DOWN, buff=0.12)
        pista.next_to(escenarios, DOWN, buff=0.45)
        self.play(FadeIn(pista, shift=UP * 0.2), Indicate(escenarios[1]), Indicate(escenarios[2]), run_time=1.2)

        # f6: del POC a producción -------------------------------------------------------------
        self.seg("f6")
        self.limpiar()
        self.hasta(1)
        centro = caja("código\nde ML", VIOLETA, 24).scale(0.9)
        alrededor = ["configuración", "recolección\nde datos", "verificación\nde datos", "extracción\nde variables",
                     "gestión de\nrecursos", "infraestructura\nde serving", "monitoreo", "análisis"]
        cajas = VGroup()
        for i, texto in enumerate(alrededor):
            ang = PI / 2 - i * TAU / len(alrededor)
            c = caja(texto, GRIS, 22).move_to(np.array([4.2 * np.cos(ang), 2.4 * np.sin(ang) - 0.2, 0]))
            cajas.add(c)
        centro.move_to(DOWN * 0.2)
        self.play(FadeIn(centro, scale=0.8), run_time=0.8)
        self.hasta(2)
        self.play(Indicate(centro, color=VIOLETA), run_time=1.0)
        self.hasta(3)
        self.play(LaggedStart(*[FadeIn(c, scale=0.8) for c in cajas], lag_ratio=0.12), run_time=2.0)

        # f7: requisitos del predictor --------------------------------------------------------
        self.seg("f7")
        self.limpiar()
        t7 = C("predictor(X) → y", 40, AMARILLO).to_edge(UP, buff=0.8)
        self.play(FadeIn(t7), run_time=0.6)
        requisitos = VGroup(*[
            M(f'<span foreground="{VERDE}">✓</span>  {r}', 30) for r in [
                "recibe los datos crudos",
                "aplica el preprocesamiento aprendido en train",
                "contiene el modelo ya entrenado",
                "funciona solo, sin el notebook",
                "sin etiquetas, sin reentrenar, sin variables globales",
            ]
        ]).arrange(DOWN, aligned_edge=LEFT, buff=0.35).shift(DOWN * 0.3)
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in requisitos], lag_ratio=0.6), run_time=self.resto(0.85))

        # f8: nuestro predictor ---------------------------------------------------------------
        self.seg("f8")
        self.limpiar()
        pasos = VGroup(caja("X: DataFrame,\narray o CSV", GRIS, 22), caja("prepare_features\n(transformaciones fijas)", AZUL, 22),
                       caja("pipeline en .joblib\nRF + gradient boosting", VIOLETA, 22), caja("0 / 1\n(umbral 0,40)", AMARILLO, 22))
        pasos.arrange(RIGHT, buff=0.55).shift(UP * 1.4)
        flechas = VGroup(*[Arrow(pasos[i].get_right(), pasos[i + 1].get_left(), buff=0.08, color=GRIS) for i in range(3)])
        self.play(LaggedStart(*[FadeIn(p) for p in pasos], lag_ratio=0.3), Create(flechas), run_time=2.0)
        zipf = C("predictor_v1_Grupo_11.zip: .py + .joblib + requirements + README", 22, GRIS).next_to(pasos, DOWN, buff=0.4)
        prueba = T("probado en un proceso nuevo, con varios formatos de entrada", 24, GRIS).next_to(zipf, DOWN, buff=0.2)
        self.play(FadeIn(zipf), FadeIn(prueba), run_time=1.0)
        self.hasta(1)
        linea_t = VGroup(caja("entrenar con desarrollo\n38.273", AZUL, 22), caja("evaluar en test\nuna vez", AMARILLO, 22),
                         caja("reentrenar con todo\n47.842 → enviar", VERDE, 22)).arrange(RIGHT, buff=0.8).shift(DOWN * 2.2)
        fl_t = VGroup(*[Arrow(linea_t[i].get_right(), linea_t[i + 1].get_left(), buff=0.08, color=GRIS) for i in range(2)])
        self.play(FadeIn(linea_t[0]), run_time=0.8)
        self.hasta(2)
        self.play(GrowArrow(fl_t[0]), FadeIn(linea_t[1]), run_time=0.8)
        self.hasta(3)
        self.play(GrowArrow(fl_t[1]), FadeIn(linea_t[2]), run_time=0.8)

        # f9: drift ----------------------------------------------------------------------
        self.seg("f9")
        self.limpiar()
        self.hasta(1)
        ax1 = Axes(x_range=[0, 10, 1], y_range=[0, 1, 0.5], x_length=5.2, y_length=2.4, tips=False,
                   axis_config={"color": GRIS_OSCURO, "include_numbers": False}).shift(LEFT * 3.4 + DOWN * 0.3)
        xs = np.linspace(0, 10, 200)
        campana = lambda m: ax1.plot_line_graph(xs, np.exp(-0.5 * ((xs - m) / 1.2) ** 2), line_color=AZUL,  # noqa: E731
                                                add_vertex_dots=False, stroke_width=4)["line_graph"]
        c_ant = campana(3.5)
        c_nue = campana(6.0).set_color(NARANJA)
        t_dd = VGroup(T("data drift", 30, NARANJA, weight=BOLD), T("cambia la distribución de X", 22, GRIS)).arrange(DOWN, buff=0.1)
        t_dd.next_to(ax1, UP, buff=0.3)
        self.play(Create(ax1), Create(c_ant), FadeIn(t_dd), run_time=1.0)
        self.play(TransformFromCopy(c_ant, c_nue), run_time=1.2)
        self.hasta(2)
        plano = Square(3.0, color=GRIS_OSCURO).shift(RIGHT * 3.4 + DOWN * 0.3)
        rng = np.random.default_rng(8)
        pts = rng.uniform(-1.3, 1.3, (40, 2))
        dots = VGroup(*[Dot(plano.get_center() + np.array([x, y, 0]), radius=0.06, color=ROJO if x + y > 0 else AZUL)
                        for x, y in pts])
        frontera = Line(plano.get_center() + np.array([-1.4, 1.4, 0]), plano.get_center() + np.array([1.4, -1.4, 0]),
                        color=BLANCO, stroke_width=3)
        t_cd = VGroup(T("concept drift", 30, NARANJA, weight=BOLD), T("cambia la relación X → y", 22, GRIS)).arrange(DOWN, buff=0.1)
        t_cd.next_to(plano, UP, buff=0.3)
        self.play(Create(plano), FadeIn(dots), Create(frontera), FadeIn(t_cd), run_time=1.0)
        nuevos = VGroup(*[Dot(plano.get_center() + np.array([x, y, 0]), radius=0.06, color=ROJO if y > 0.3 else AZUL)
                          for x, y in pts])
        self.play(Transform(dots, nuevos), Rotate(frontera, angle=PI / 4, about_point=plano.get_center()),
                  run_time=1.4)
        self.play(frontera.animate.shift(UP * 0.3), run_time=0.4)
        self.hasta(3)
        monitoreo = T("por eso se monitorea: nuestro número agrupado es la referencia con clientes nuevos", 24, AMARILLO)
        monitoreo.to_edge(DOWN, buff=0.8)
        self.play(FadeIn(monitoreo), run_time=0.8)

        # f10: resumen -------------------------------------------------------------------------
        self.seg("f10")
        self.limpiar()
        titulo = T("En resumen", 44, BLANCO, weight=BOLD).to_edge(UP, buff=0.7)
        self.play(FadeIn(titulo), run_time=0.6)
        items = [
            ("Validar", "según el uso: al azar y agrupada por copias"),
            ("Diagnosticar", "curvas: el límite es la información, no el modelo"),
            ("Analizar errores", "las reservas únicas de cloud_marketplace"),
            ("Optimizar", "regla fija: max_features 0,2 + promedio con boosting"),
            ("Producción", "predictor independiente, probado fuera del notebook"),
        ]
        filas = VGroup()
        for i, (n, d) in enumerate(items):
            circ = Circle(0.3, color=AMARILLO, stroke_width=3).set_fill(TARJETA, 1)
            numero = T(str(i + 1), 26, AMARILLO, weight=BOLD).move_to(circ)
            nombre = T(n, 28, BLANCO, weight=BOLD)
            desc = T(d, 26, GRIS)
            fila = VGroup(VGroup(circ, numero), nombre, desc).arrange(RIGHT, buff=0.35)
            filas.add(fila)
        filas.arrange(DOWN, aligned_edge=LEFT, buff=0.38).shift(DOWN * 0.3)
        for i, f in enumerate(filas):
            self.hasta(i + 1)
            self.play(FadeIn(f, shift=RIGHT * 0.2), run_time=0.8)

        # f11: cierre -----------------------------------------------------------------------------
        self.seg("f11")
        self.limpiar()
        l1 = T("El siguiente punto de rendimiento casi nunca está", 36, BLANCO)
        l2 = T("en un algoritmo más sofisticado.", 36, BLANCO)
        l3 = M(f'Está en entender <span foreground="{AMARILLO}">qué información le falta</span> al modelo,', 36)
        l4 = M(f'y <span foreground="{AMARILLO}">dónde</span>.', 36)
        bloque1 = VGroup(l1, l2).arrange(DOWN, buff=0.2).shift(UP * 1.0)
        bloque2 = VGroup(l3, l4).arrange(DOWN, buff=0.2).next_to(bloque1, DOWN, buff=0.7)
        self.play(FadeIn(bloque1, shift=UP * 0.2), run_time=1.2)
        self.hasta(1)
        self.play(FadeIn(bloque2, shift=UP * 0.2), run_time=1.2)
        self.cerrar()
        self.wait(1.5)
        self.terminar()
