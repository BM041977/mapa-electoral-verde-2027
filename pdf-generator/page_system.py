"""
page_system.py — Sistema base de plantilla de página
────────────────────────────────────────────────────────────────
Componentes reutilizables que garantizan consistencia y resuelven
el bug sistémico de "textos encimados" del PDF v1.

Diseño:
- Cada página es una Figure de matplotlib con dimensiones fijas.
- El layout usa ZONAS VERTICALES claramente separadas que NUNCA
  se sobreponen: header, content, insight, footer.
- El insight box tiene altura calculada según contenido, no fija.
- Todo texto largo pasa por wrap dinámico (textwrap).
- El footer es una banda completa con marca + sección + paginación.
"""

import textwrap
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.image import imread
import numpy as np

from brand import (
    COLORS, FONT_SERIF, FONT_SANS, TYPE,
    PAGE_W, PAGE_H, M_LEFT, M_RIGHT, M_TOP, M_BOTTOM,
    ZONE_FOOTER_TOP, ZONE_INSIGHT_TOP, ZONE_CONTENT_BOTTOM,
    ZONE_CONTENT_TOP, ZONE_HEADER_BOTTOM, CONTENT_W,
    INSIGHT_PAD_X, INSIGHT_PAD_Y
)

LOGO_PATH = "/home/claude/proyecto/logo_clean.png"


# ═══════════════════════════════════════════════════════════════
# FIGURE Y AXES BASE
# ═══════════════════════════════════════════════════════════════

def new_page():
    """Crea una nueva figura con dimensiones y fondo de marca."""
    fig = plt.figure(figsize=(PAGE_W, PAGE_H), facecolor=COLORS["bg"])
    return fig


def page_ax(fig):
    """
    Devuelve un Axes que cubre toda la página, sin marcos ni ticks.
    Coordenadas: (0,0) abajo-izquierda, (1,1) arriba-derecha.
    """
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_facecolor(COLORS["bg"])
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    return ax


# ═══════════════════════════════════════════════════════════════
# WRAP DINÁMICO DE TEXTO
# ═══════════════════════════════════════════════════════════════

def wrap_text(text, max_chars):
    """
    Hace wrap de texto largo en líneas de máximo `max_chars` caracteres.
    Conserva saltos de línea explícitos (\n).
    """
    if not text:
        return ""
    lines = []
    for para in text.split("\n"):
        if not para.strip():
            lines.append("")
            continue
        wrapped = textwrap.wrap(para, width=max_chars, break_long_words=False)
        if wrapped:
            lines.extend(wrapped)
        else:
            lines.append(para)
    return "\n".join(lines)


def count_lines(text):
    """Cuenta cuántas líneas tendrá el texto al renderizarse."""
    if not text:
        return 0
    return len(text.split("\n"))


# ═══════════════════════════════════════════════════════════════
# HEADER (eyebrow + título + línea decorativa + subtítulo)
# ═══════════════════════════════════════════════════════════════

def draw_header(ax, eyebrow, title, subtitle=None,
                y_eyebrow=0.945, y_title=0.885, y_line=0.842, y_subtitle=0.815,
                title_size=None):
    """
    Dibuja el header estándar:
      - eyebrow (texto pequeño mayúsculas)
      - título principal en serif
      - línea decorativa corta bajo el título
      - subtitle en italic (opcional)
    """
    x = M_LEFT
    title_size = title_size or TYPE["h1"]

    # Eyebrow
    if eyebrow:
        ax.text(x, y_eyebrow, eyebrow.upper(),
                fontfamily=FONT_SANS, fontsize=TYPE["eyebrow"],
                fontweight="bold", color=COLORS["ink_soft"])

    # Título
    if title:
        ax.text(x, y_title, title,
                fontfamily=FONT_SERIF, fontsize=title_size,
                fontweight="bold", color=COLORS["ink"],
                va="center")

    # Línea decorativa corta
    ax.plot([x, x + 0.05], [y_line, y_line],
            color=COLORS["ink"], linewidth=2.5, solid_capstyle="butt")

    # Subtítulo
    if subtitle:
        ax.text(x, y_subtitle, subtitle,
                fontfamily=FONT_SERIF, fontsize=TYPE["subtitle"],
                fontstyle="italic", color=COLORS["ink_soft"])


# ═══════════════════════════════════════════════════════════════
# FOOTER (línea separadora + marca + sección + paginación)
# ═══════════════════════════════════════════════════════════════

def draw_footer(ax, section, page_num, total_pages=49, show_logo=True):
    """
    Footer consistente. Banda fija arriba del borde inferior.
    Línea horizontal separadora arriba del footer.
    Marca a la izquierda como LOGO (no texto), para proteger marca personal.
    """
    y_line   = 0.045  # línea separadora
    y_text   = 0.022  # texto del footer

    # Línea separadora sutil
    ax.plot([M_LEFT, 1 - M_RIGHT], [y_line, y_line],
            color=COLORS["line"], linewidth=0.8)

    # Marca a la izquierda — LOGO pequeño (no texto)
    if show_logo:
        # logo width = 0.085 de la página; alto se calcula manteniendo aspect
        # Lo centramos verticalmente en la mitad de la zona del footer (entre 0 y y_line)
        logo_w = 0.085
        try:
            img = imread(LOGO_PATH)
            aspect = img.shape[0] / img.shape[1]
            logo_h_frac = (logo_w * PAGE_W * aspect) / PAGE_H
        except Exception:
            logo_h_frac = 0.030
        logo_x = M_LEFT
        # Centrar en mitad de la zona del footer (entre 0 y y_line)
        logo_y = (y_line / 2) - logo_h_frac / 2
        ax_logo = ax.figure.add_axes([logo_x, logo_y, logo_w, logo_h_frac], zorder=10)
        try:
            ax_logo.imshow(imread(LOGO_PATH))
        except Exception:
            pass
        ax_logo.set_xticks([]); ax_logo.set_yticks([])
        for s in ax_logo.spines.values():
            s.set_visible(False)
        ax_logo.patch.set_alpha(0)
    else:
        # Fallback: texto (no debería usarse normalmente)
        ax.text(M_LEFT, y_text, "Baldemar Maza León",
                fontfamily=FONT_SANS, fontsize=TYPE["footer"],
                fontweight="bold", color=COLORS["ink"], va="center")

    # Sección al centro
    if section:
        ax.text(0.5, y_text, section,
                fontfamily=FONT_SERIF, fontsize=TYPE["footer"],
                fontstyle="italic", color=COLORS["ink_soft"],
                va="center", ha="center")

    # Paginación a la derecha
    ax.text(1 - M_RIGHT, y_text, f"{page_num} / {total_pages}",
            fontfamily=FONT_SANS, fontsize=TYPE["footer"],
            color=COLORS["ink_soft"], va="center", ha="right")


# ═══════════════════════════════════════════════════════════════
# INSIGHT BOX (banda grafito con label + texto)
# ═══════════════════════════════════════════════════════════════

def draw_insight(ax, label, text, max_chars=145, color=None):
    """
    Insight box adaptativo:
    - Calcula la altura según el número de líneas del texto wrappeado.
    - Se posiciona exactamente entre el footer y el contenido.
    - Color de fondo por defecto: grafito (accent).
    """
    color = color or COLORS["accent"]

    # Wrap del texto
    wrapped = wrap_text(text, max_chars)
    n_lines = count_lines(wrapped)

    # Altura calculada
    # base = padding superior + label + gap + n_lines de texto + padding inferior
    line_height = 0.022  # alto en y por línea de texto
    base_top_pad = 0.025  # padding superior
    label_height = 0.022  # alto del label
    gap = 0.012           # gap entre label y texto
    base_bottom_pad = 0.022

    box_height = base_top_pad + label_height + gap + (n_lines * line_height) + base_bottom_pad
    # Mínimo de altura
    box_height = max(box_height, 0.10)

    # Posición: parte superior fija a ZONE_INSIGHT_TOP, crece hacia abajo
    y_top = ZONE_INSIGHT_TOP
    y_bot = y_top - box_height

    # Caja
    rect = patches.Rectangle(
        (M_LEFT, y_bot), CONTENT_W, box_height,
        linewidth=0, facecolor=color, zorder=2
    )
    ax.add_patch(rect)

    # Label (arriba dentro de la caja)
    y_label = y_top - base_top_pad - label_height / 2
    ax.text(M_LEFT + INSIGHT_PAD_X, y_label, label.upper(),
            fontfamily=FONT_SANS, fontsize=TYPE["insight_label"],
            fontweight="bold", color="#FFFFFF",
            va="center", zorder=3)

    # Texto principal (debajo del label)
    y_text_start = y_label - label_height / 2 - gap - line_height / 2
    ax.text(M_LEFT + INSIGHT_PAD_X, y_text_start, wrapped,
            fontfamily=FONT_SANS, fontsize=TYPE["insight_text"],
            color="#FFFFFF", va="top", zorder=3,
            linespacing=1.45)

    return y_bot  # devuelve y inferior para referencia


# ═══════════════════════════════════════════════════════════════
# CARDS (recuadros blancos con borde sutil)
# ═══════════════════════════════════════════════════════════════

def draw_card(ax, x, y, w, h, fill=None, edge=None, lw=0.8, radius=0.012, zorder=2):
    """Card blanca redondeada con borde sutil."""
    fill = fill or COLORS["card"]
    edge = edge or COLORS["line"]
    rect = patches.FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad=0,rounding_size={radius}",
        linewidth=lw, facecolor=fill, edgecolor=edge, zorder=zorder
    )
    ax.add_patch(rect)


# ═══════════════════════════════════════════════════════════════
# LOGO
# ═══════════════════════════════════════════════════════════════

def draw_logo(ax, x_center, y_center, width=0.30):
    """
    Inserta el logo PNG centrado en (x_center, y_center).
    width = ancho deseado en fracción de página.
    La altura se calcula manteniendo el aspect ratio.
    """
    try:
        img = imread(LOGO_PATH)
    except Exception:
        return  # falla silenciosamente si no hay logo

    aspect = img.shape[0] / img.shape[1]  # h/w
    # Convertir width (en fracción de página) a height (en fracción)
    # asumiendo que la página es PAGE_W x PAGE_H
    width_inches = width * PAGE_W
    height_inches = width_inches * aspect
    height_frac = height_inches / PAGE_H

    x_left = x_center - width / 2
    y_bot  = y_center - height_frac / 2

    ax_img = ax.figure.add_axes([x_left, y_bot, width, height_frac], zorder=10)
    ax_img.imshow(img)
    ax_img.set_xticks([])
    ax_img.set_yticks([])
    for s in ax_img.spines.values():
        s.set_visible(False)
    ax_img.set_facecolor("none")
    ax_img.patch.set_alpha(0)


# ═══════════════════════════════════════════════════════════════
# UTILIDADES VARIAS
# ═══════════════════════════════════════════════════════════════

def hline(ax, y, x1=None, x2=None, color=None, lw=0.8):
    """Línea horizontal en la zona de contenido."""
    x1 = x1 if x1 is not None else M_LEFT
    x2 = x2 if x2 is not None else 1 - M_RIGHT
    color = color or COLORS["line"]
    ax.plot([x1, x2], [y, y], color=color, linewidth=lw)


def party_color(name):
    """Devuelve el color institucional de un partido."""
    from brand import PARTY_COLORS
    return PARTY_COLORS.get(name.upper(), COLORS["ink_soft"])
