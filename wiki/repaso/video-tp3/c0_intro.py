"""Capítulo 0: el problema y el mapa del video."""

import numpy as np
from manim import *

from base import *


class Intro(Escena):
    def construct(self):
        # i1: una reserva y la pregunta
        self.seg("i1")
        filas = VGroup(
            T("Reserva #18.204", 30, BLANCO, weight=BOLD),
            T("GPU pedida: GPU_T4", 26, GRIS),
            T("cliente: cloud_marketplace", 26, GRIS),
            T("se ejecuta dentro de 21 días", 26, GRIS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        reserva = tarjeta(filas, color=AZUL).shift(LEFT * 2.8)
        self.play(FadeIn(reserva, shift=UP * 0.3), run_time=1.2)
        self.hasta(2)
        flecha = Arrow(reserva.get_right(), reserva.get_right() + RIGHT * 1.8, buff=0.25, color=GRIS)
        pregunta = T("¿se cancela?", 48, AMARILLO).next_to(flecha, RIGHT, buff=0.3)
        self.play(GrowArrow(flecha), Write(pregunta), run_time=1.5)

        # i2: 47.842 reservas, 41,7 % canceladas
        self.seg("i2")
        self.play(FadeOut(flecha), FadeOut(pregunta), reserva.animate.scale(0.5).to_edge(LEFT, buff=0.6).shift(UP * 1.6),
                  run_time=1.0)
        n_col, n_fil = 50, 20
        rng = np.random.default_rng(3)
        canceladas = set(rng.choice(n_col * n_fil, size=int(round(0.417 * n_col * n_fil)), replace=False))
        puntos = VGroup(*[
            Square(0.13, stroke_width=0, fill_opacity=1, fill_color=GRIS_OSCURO)
            for _ in range(n_col * n_fil)
        ]).arrange_in_grid(n_fil, n_col, buff=0.05).shift(DOWN * 0.6 + RIGHT * 0.6)
        etiqueta = T("47.842 reservas (cada cuadradito ≈ 48)", 28, BLANCO).next_to(puntos, UP, buff=0.35)
        self.play(FadeIn(puntos, lag_ratio=0.002, scale=0.5), FadeIn(etiqueta),
                  run_time=2.2)
        self.hasta(2)
        coloreados = puntos.copy()
        for i, p in enumerate(coloreados):
            p.set_fill(ROJO if i in canceladas else AZUL)
        self.play(Transform(puntos, coloreados), run_time=1.2)
        leyenda = VGroup(
            VGroup(Square(0.22, fill_color=ROJO, fill_opacity=1, stroke_width=0), T("se canceló: 41,7 %", 28)).arrange(RIGHT),
            VGroup(Square(0.22, fill_color=AZUL, fill_opacity=1, stroke_width=0), T("se ejecutó: 58,3 %", 28)).arrange(RIGHT),
        ).arrange(RIGHT, buff=0.8).next_to(puntos, DOWN, buff=0.35)
        self.play(FadeIn(leyenda), run_time=0.8)

        # i3: TP2 frente a TP3
        self.seg("i3")
        self.limpiar()
        tp2 = VGroup(T("TP2", 40, GRIS, weight=BOLD), T("¿qué modelo elijo?", 32, BLANCO)).arrange(DOWN, buff=0.3)
        modelos = VGroup(*[tarjeta(T(m, 24), buff=0.18) for m in ["Naive Bayes", "SVM", "KNN", "Random Forest"]])
        modelos.arrange(DOWN, buff=0.18).next_to(tp2, DOWN, buff=0.4)
        izq = VGroup(tp2, modelos).move_to(LEFT * 3.6)
        self.play(FadeIn(izq, shift=RIGHT * 0.3), run_time=1.2)
        self.hasta(1)
        rf = modelos[3].copy()
        self.play(modelos[3][0].animate.set_stroke(VERDE, 3), run_time=0.6)
        self.hasta(2)
        tp3 = T("TP3", 40, AMARILLO, weight=BOLD).move_to(RIGHT * 3.4 + UP * 1.6)
        self.play(FadeIn(tp3), rf.animate.move_to(RIGHT * 3.4 + UP * 0.6), run_time=1.0)
        self.hasta(3)
        p1 = T("¿por qué se equivoca?", 34, BLANCO).next_to(rf, DOWN, buff=0.5)
        self.play(Write(p1), run_time=1.0)
        self.hasta(4)
        p2 = T("¿qué hago para que se equivoque menos?", 30, BLANCO).next_to(p1, DOWN, buff=0.3)
        self.play(Write(p2), run_time=1.4)

        # i4: mapa de los cinco pasos
        self.seg("i4")
        self.limpiar()
        nombres = ["Validar", "Diagnosticar", "Analizar errores", "Optimizar", "Producción"]
        clases = ["clase 11", "clase 11", "clase 11", "clase 12", "clase 12"]
        circulos = VGroup(*[Circle(0.45, color=AMARILLO, stroke_width=3).set_fill(TARJETA, 1) for _ in nombres])
        circulos.arrange(RIGHT, buff=2.0).move_to(UP * 0.3)
        nodos = VGroup()
        for i, (n, c) in enumerate(zip(nombres, clases)):
            circ = circulos[i]
            numero = T(str(i + 1), 34, AMARILLO, weight=BOLD).move_to(circ)
            nombre = T(n, 26, BLANCO).next_to(circ, DOWN, buff=0.25)
            clase = T(c, 20, GRIS).move_to(circ.get_bottom() + DOWN * 1.05)
            nodos.add(VGroup(circ, numero, nombre, clase))
        lineas = VGroup(*[Line(circulos[i].get_right(), circulos[i + 1].get_left(), color=GRIS_OSCURO)
                          for i in range(4)])
        titulo = T("Teoría nueva + nuestra resolución", 40, BLANCO, weight=BOLD).to_edge(UP, buff=1.0)
        self.play(FadeIn(titulo), run_time=0.8)
        self.hasta(1)
        self.play(LaggedStart(*[FadeIn(n, shift=UP * 0.2) for n in nodos], lag_ratio=0.35),
                  LaggedStart(*[Create(l) for l in lineas], lag_ratio=0.35), run_time=self.resto(0.6))
        self.terminar()
