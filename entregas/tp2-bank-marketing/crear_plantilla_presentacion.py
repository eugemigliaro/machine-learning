"""Crea la plantilla de pandoc usada por la presentación del TP2.

Parte de la plantilla por defecto de pandoc y cambia sólo dos cosas:
- en el diseño "Two Content", la columna izquierda (gráficos) ocupa ~65 % del ancho
  y el texto de las columnas baja a 14 pt;
- títulos y cuerpo usan fuentes más chicas, para que entren texto y números.
"""

import re
import subprocess
import zipfile
from pathlib import Path

OUTPUT = Path(__file__).parent / "plantilla_presentacion.pptx"

MARGIN = 320040
TITLE = (MARGIN, 120000, 8503920, 640000)
BODY = (MARGIN, 860000, 8503920, 4050000)
LEFT = (MARGIN, 860000, 5760720, 4050000)
RIGHT = (6217920, 860000, 2606040, 4050000)


def set_geometry(shape, geometry):
    x, y, cx, cy = geometry
    shape = re.sub(r'<a:off x="\d+" y="\d+"/>', f'<a:off x="{x}" y="{y}"/>', shape, count=1)
    return re.sub(r'<a:ext cx="\d+" cy="\d+"/>', f'<a:ext cx="{cx}" cy="{cy}"/>', shape, count=1)


def update_shapes(xml, placeholders):
    def replace(match):
        shape = match.group(0)
        for marker, geometry in placeholders.items():
            if marker in shape:
                return set_geometry(shape, geometry)
        return shape
    return re.sub(r"<p:sp>.*?</p:sp>", replace, xml, flags=re.S)


def update_master(xml):
    xml = update_shapes(xml, {'<p:ph type="title"/>': TITLE, '<p:ph type="body" idx="1"/>': BODY})
    title_style = re.search(r"<p:titleStyle>.*?</p:titleStyle>", xml, re.S).group(0)
    xml = xml.replace(title_style, title_style.replace('sz="3300"', 'sz="2600"'))
    body_style = re.search(r"<p:bodyStyle>.*?</p:bodyStyle>", xml, re.S).group(0)
    smaller = body_style
    for old, new in [('sz="2400"', 'sz="1500"'), ('sz="2100"', 'sz="1350"'), ('sz="1800"', 'sz="1200"')]:
        smaller = smaller.replace(old, new)
    return xml.replace(body_style, smaller)


def update_two_content(xml):
    xml = update_shapes(xml, {'<p:ph sz="half" idx="1"/>': LEFT, '<p:ph sz="half" idx="2"/>': RIGHT})
    sizes = {"1": "1400", "2": "1250", "3": "1100"}
    return re.sub(
        r'<a:lvl([123])pPr><a:defRPr sz="\d+"/>',
        lambda match: f'<a:lvl{match.group(1)}pPr><a:defRPr sz="{sizes[match.group(1)]}"/>',
        xml,
    )


default = subprocess.run(
    ["pandoc", "--print-default-data-file", "reference.pptx"], check=True, capture_output=True
).stdout
source = OUTPUT.with_suffix(".tmp")
source.write_bytes(default)
with zipfile.ZipFile(source) as original, zipfile.ZipFile(OUTPUT, "w", zipfile.ZIP_DEFLATED) as result:
    for item in original.infolist():
        data = original.read(item.filename)
        if item.filename == "ppt/slideMasters/slideMaster1.xml":
            data = update_master(data.decode()).encode()
        elif item.filename == "ppt/slideLayouts/slideLayout4.xml":
            data = update_two_content(data.decode()).encode()
        result.writestr(item, data)
source.unlink()
print(f"Plantilla creada en {OUTPUT}")
