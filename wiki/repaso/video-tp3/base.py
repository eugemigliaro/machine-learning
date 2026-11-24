"""Estilo común y sincronización con la narración."""

import json
import os
from pathlib import Path

from manim import (
    BOLD, DOWN, DR, LEFT, RIGHT, UL, UP, FadeIn, FadeOut, Line, MarkupText, RoundedRectangle, Scene, Text,
    VGroup, config,
)

AQUI = Path(__file__).resolve().parent
BUILD = Path(os.environ.get("VIDEO_BUILD", AQUI / "build"))
AUDIO = BUILD / "audio"

FUENTE = "P052"
MONO = "Ubuntu Mono"

FONDO = "#0B0D10"
TARJETA = "#161B22"
BORDE = "#30363D"
BLANCO = "#ECEFF1"
GRIS = "#9AA0A6"
GRIS_OSCURO = "#5F6368"
AZUL = "#58C4DD"  # se ejecuta, train
ROJO = "#FC6255"  # se cancela, errores
AMARILLO = "#F4D345"  # validación al azar
TURQUESA = "#5CD0B3"  # validación agrupada
NARANJA = "#FF862F"  # región elegida
VERDE = "#83C167"  # adoptado, correcto
VIOLETA = "#B189D8"  # gradient boosting

config.background_color = FONDO


def T(texto, tam=32, color=BLANCO, **kw):
    return Text(texto, font=FUENTE, font_size=tam, color=color, **kw)


def M(markup, tam=32, color=BLANCO, **kw):
    return MarkupText(markup, font=FUENTE, font_size=tam, color=color, **kw)


def C(texto, tam=28, color=BLANCO, **kw):
    return Text(texto, font=MONO, font_size=tam, color=color, **kw)


def num(valor, decimales=3):
    """Formatea con coma decimal."""
    return f"{valor:.{decimales}f}".replace(".", ",")


def tarjeta(contenido, ancho=None, alto=None, color=BORDE, relleno=TARJETA, buff=0.35, radio=0.15):
    ancho = ancho or contenido.width + 2 * buff
    alto = alto or contenido.height + 2 * buff
    caja = RoundedRectangle(width=ancho, height=alto, corner_radius=radio, stroke_color=color, stroke_width=2,
                            fill_color=relleno, fill_opacity=1)
    caja.move_to(contenido)
    return VGroup(caja, contenido)


def tachar(mob, color=ROJO):
    return Line(mob.get_left() + LEFT * 0.1, mob.get_right() + RIGHT * 0.1, color=color, stroke_width=4)


class Escena(Scene):
    """Escena con narración: cada `seg` arranca un audio y espera a que termine el anterior."""

    CAPITULO = None

    def setup(self):
        self.info = json.loads((AUDIO / "duraciones.json").read_text())
        self._fin = None
        self._inicio = 0.0
        self._oraciones = [0.0]
        self._fuente = None
        self.cap = None
        if self.CAPITULO:
            self.cap = T(self.CAPITULO, 24, GRIS).to_corner(UL, buff=0.35)
            self.add(self.cap)

    # tiempo -------------------------------------------------------------
    def ahora(self):
        return self.renderer.time

    def seg(self, clave):
        self.cerrar()
        datos = self.info[clave]
        self.add_sound(str(AUDIO / f"{clave}.wav"))
        self._inicio = self.ahora()
        self._fin = self._inicio + datos["duracion"]
        self._oraciones = datos["oraciones"]
        self._poner_fuente(datos["fuente"])

    def hasta(self, oracion):
        """Espera a que empiece la oración `oracion` (desde 0) del segmento actual."""
        oracion = min(oracion, len(self._oraciones) - 1)
        objetivo = self._inicio + self._oraciones[oracion]
        if objetivo - self.ahora() > 0.02:
            self.wait(objetivo - self.ahora())

    def resto(self, fraccion=1.0, minimo=0.3):
        """Tiempo que queda del segmento actual, escalado."""
        return max(minimo, (self._fin - self.ahora()) * fraccion)

    def cerrar(self):
        if self._fin is not None and self._fin - self.ahora() > 0.02:
            self.wait(self._fin - self.ahora())

    # pantalla ------------------------------------------------------------
    def _poner_fuente(self, texto):
        nueva = T(texto, 18, GRIS_OSCURO).to_corner(DR, buff=0.25)
        if self._fuente is not None:
            self.remove(self._fuente)
        self.add(nueva)
        self._fuente = nueva

    def fijos(self):
        return [m for m in (self.cap, self._fuente) if m is not None]

    def limpiar(self, tiempo=0.6):
        objetos = [m for m in self.mobjects if m not in self.fijos()]
        if objetos:
            self.play(*[FadeOut(m) for m in objetos], run_time=tiempo)

    def titulo(self, texto, tam=44):
        t = T(texto, tam, BLANCO, weight=BOLD).to_edge(UP, buff=0.7)
        return t

    def terminar(self):
        self.cerrar()
        objetos = [m for m in self.mobjects]
        if objetos:
            self.play(*[FadeOut(m) for m in objetos], run_time=0.8)
        self.wait(0.3)


__all__ = [
    "AMARILLO", "AUDIO", "AZUL", "BLANCO", "BORDE", "C", "Escena", "FONDO", "FUENTE", "GRIS", "GRIS_OSCURO", "M",
    "MONO", "NARANJA", "ROJO", "T", "TARJETA", "TURQUESA", "VERDE", "VIOLETA", "num", "tachar", "tarjeta",
]
