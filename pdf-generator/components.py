"""
components.py — Componentes visuales reutilizables
"""
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import textwrap

from brand import COLORS, FONT_SERIF, FONT_SANS, TYPE, M_LEFT, M_RIGHT, CONTENT_W, PARTY_COLORS
from page_system import draw_card, wrap_text


# ═══════════════════════════════════════════════════════════════
# PÁGINA DE PARTE (número romano grande + título de sección)
# ═══════════════════════════════════════════════════════════════

def render_part_page(ax, roman, part_label, title, subtitle):
    """
    Página de divisor de parte. Muy minimalista:
    - Número romano enorme arriba izquierda
    - Eyebrow "PARTE X"
    - Título grande serif
    - Subtítulo italic
    """
    # Romano enorme decorativo (esquina superior izquierda)
    ax.text(M_LEFT, 0.82, roman,
            fontfamily=FONT_SERIF, fontsize=160, fontweight="bold",
            color=COLORS["accent"], va="top", alpha=0.95)

    # Eyebrow
    ax.text(M_LEFT, 0.46, part_label.upper(),
            fontfamily=FONT_SANS, fontsize=11, fontweight="bold",
            color=COLORS["ink_soft"])

    # Línea decorativa (entre eyebrow y título)
    ax.plot([M_LEFT, M_LEFT + 0.05], [0.435, 0.435],
            color=COLORS["ink"], linewidth=2.5)

    # Título
    ax.text(M_LEFT, 0.345, title,
            fontfamily=FONT_SERIF, fontsize=54, fontweight="bold",
            color=COLORS["ink"], va="center")

    # Subtítulo
    sub_wrapped = wrap_text(subtitle, 80)
    ax.text(M_LEFT, 0.22, sub_wrapped,
            fontfamily=FONT_SERIF, fontsize=16, fontstyle="italic",
            color=COLORS["ink_soft"], va="top", linespacing=1.4)


# ═══════════════════════════════════════════════════════════════
# CARD NUMERADO (para resumen ejecutivo, conclusiones, etc.)
# ═══════════════════════════════════════════════════════════════

def render_numbered_card(ax, x, y, w, h, num, title, body, body_chars=58):
    """Card con número grande a la izquierda, título y body wrappeado."""
    draw_card(ax, x, y, w, h, lw=0.8, radius=0.012)

    pad = 0.018
    # Número grande
    ax.text(x + pad + 0.008, y + h/2, num,
            fontfamily=FONT_SERIF, fontsize=42, fontweight="bold",
            color=COLORS["accent"], va="center")

    # Título
    text_x = x + pad + 0.07
    ax.text(text_x, y + h - pad - 0.012, title.upper(),
            fontfamily=FONT_SANS, fontsize=11, fontweight="bold",
            color=COLORS["ink"], va="top")

    # Body wrappeado
    wrapped = wrap_text(body, body_chars)
    ax.text(text_x, y + h - pad - 0.045, wrapped,
            fontfamily=FONT_SANS, fontsize=10,
            color=COLORS["ink_soft"], va="top", linespacing=1.45)


# ═══════════════════════════════════════════════════════════════
# CARD DE DATO CLAVE (label arriba + valor grande + descripción)
# ═══════════════════════════════════════════════════════════════

def render_data_card(ax, x, y, w, h, label, value, desc, value_color=None, value_size=22):
    """Card con label arriba, valor grande al centro, descripción abajo.
    Las posiciones internas son relativas al alto, evitando encimado en cards bajos."""
    draw_card(ax, x, y, w, h, lw=0.8, radius=0.012)
    value_color = value_color or COLORS["ink"]
    # Posiciones proporcionales al alto del card — siempre dejan aire
    label_y = y + h * 0.82
    value_y = y + h * 0.50
    desc_y  = y + h * 0.18
    # Label
    ax.text(x + w/2, label_y, label.upper(),
            fontfamily=FONT_SANS, fontsize=9, fontweight="bold",
            color=COLORS["ink_soft"], va="center", ha="center")
    # Valor
    ax.text(x + w/2, value_y, value,
            fontfamily=FONT_SERIF, fontsize=value_size, fontweight="bold",
            color=value_color, va="center", ha="center")
    # Descripción
    ax.text(x + w/2, desc_y, desc,
            fontfamily=FONT_SANS, fontsize=9,
            color=COLORS["ink_light"], va="center", ha="center")


# ═══════════════════════════════════════════════════════════════
# FILA DE TABLA CON HEADER
# ═══════════════════════════════════════════════════════════════

def render_table(ax, x, y, w, h, headers, rows, col_widths_frac=None,
                 header_bg=None, header_fg="#FFFFFF",
                 highlight_cols=None, highlight_color=None):
    """
    Tabla horizontal con header en color y filas alternadas.
    headers: lista de strings
    rows: lista de listas
    col_widths_frac: lista de fracciones que suman 1.0 (si None, equiparte)
    highlight_cols: lista de índices de columna a colorear con highlight_color
    """
    header_bg = header_bg or COLORS["accent"]
    highlight_color = highlight_color or COLORS["good"]
    n_cols = len(headers)
    n_rows = len(rows)
    if col_widths_frac is None:
        col_widths_frac = [1/n_cols] * n_cols
    col_widths = [cw * w for cw in col_widths_frac]
    col_x = [x]
    for cw in col_widths[:-1]:
        col_x.append(col_x[-1] + cw)

    # Header bar
    header_h = h * 0.13
    rect = patches.Rectangle((x, y + h - header_h), w, header_h,
                              linewidth=0, facecolor=header_bg)
    ax.add_patch(rect)
    for i, htext in enumerate(headers):
        ax.text(col_x[i] + 0.012, y + h - header_h/2, htext.upper(),
                fontfamily=FONT_SANS, fontsize=9, fontweight="bold",
                color=header_fg, va="center")

    # Rows
    row_h = (h - header_h) / n_rows
    for r, row in enumerate(rows):
        y_row = y + h - header_h - (r + 1) * row_h
        # Alterna fondo
        if r % 2 == 1:
            rect = patches.Rectangle((x, y_row), w, row_h,
                                       linewidth=0, facecolor=COLORS["row_alt"])
            ax.add_patch(rect)
        for c, cell in enumerate(row):
            color = COLORS["ink"]
            weight = "normal"
            if highlight_cols and c in highlight_cols:
                color = highlight_color
                weight = "bold"
            ax.text(col_x[c] + 0.012, y_row + row_h/2, str(cell),
                    fontfamily=FONT_SANS, fontsize=10,
                    fontweight=weight, color=color, va="center")
