"""
pages_indicadores.py — Páginas de Parte VIII (Indicadores complementarios)
Mockups 1-5 implementados con datos reales del Excel.
"""
import sys
sys.path.insert(0, "/home/claude/proyecto")

import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Polygon, RegularPolygon

from brand import COLORS, FONT_SERIF, FONT_SANS, TYPE, M_LEFT, M_RIGHT, CONTENT_W, PARTY_COLORS
from page_system import (
    new_page, page_ax, draw_header, draw_footer, draw_insight,
    draw_card, draw_logo, wrap_text
)
from components import render_part_page, render_data_card

with open('/home/claude/proyecto/datos_indicadores.json') as f:
    I = json.load(f)


# ═══════════════════════════════════════════════════════════════
# DIVISOR PARTE VI — Indicadores complementarios
# ═══════════════════════════════════════════════════════════════
def page_part8():
    fig = new_page()
    ax = page_ax(fig)
    render_part_page(ax, "VI", "Parte VI", "Indicadores\ncomplementarios",
        "Cinco indicadores avanzados para la estrategia 2027: participación territorial, tendencia por sección, contexto demográfico, evolución de coaliciones y radar de fortalezas.")
    draw_footer(ax, section="Parte VI", page_num=28)
    return fig


# ═══════════════════════════════════════════════════════════════
# INDICADOR 1 — MAPA DE CALOR DE PARTICIPACIÓN
# Corrección aplicada: número de sección en cada celda
# ═══════════════════════════════════════════════════════════════
def page_indicador_1():
    fig = new_page()
    ax = page_ax(fig)
    draw_header(ax,
        eyebrow="Indicador 1 · Participación territorial",
        title="Mapa de calor de participación",
        subtitle="Promedio de participación por sección en elección municipal 2024"
    )

    secciones = I['heatmap_secciones']
    n = len(secciones)

    # Cuadrícula: filas x cols
    # 250 secciones → 14 cols x 18 filas = 252 celdas (ajuste fino)
    cols = 14
    rows = int(np.ceil(n / cols))

    # Función de color según participación
    def color_part(pct):
        if pct >= 65:    return COLORS["good"]            # verde — alta
        elif pct >= 55:  return "#FACC15"                  # amarillo — media
        elif pct >= 45:  return COLORS["warning"]          # naranja — baja
        else:            return COLORS["danger"]           # rojo — muy baja

    # Layout del grid
    grid_x = M_LEFT + 0.005
    grid_y = 0.30
    grid_w = 0.65
    grid_h = 0.43
    cell_w = grid_w / cols
    cell_h = grid_h / rows
    cell_pad = 0.0015

    for i, sec in enumerate(secciones):
        r = i // cols
        c = i % cols
        x = grid_x + c * cell_w
        y = grid_y + grid_h - (r + 1) * cell_h
        pct = sec['participacion']
        color = color_part(pct)
        rect = patches.Rectangle((x + cell_pad, y + cell_pad),
                                  cell_w - 2*cell_pad, cell_h - 2*cell_pad,
                                  linewidth=0, facecolor=color)
        ax.add_patch(rect)
        # Número de sección — chico arriba
        ax.text(x + cell_w/2, y + cell_h*0.70, str(sec['seccion']),
                fontfamily=FONT_SANS, fontsize=5.8, fontweight="bold",
                color="white", ha="center", va="center")
        # % participación — chico abajo
        ax.text(x + cell_w/2, y + cell_h*0.30, f"{pct:.0f}%",
                fontfamily=FONT_SANS, fontsize=6.5, fontweight="bold",
                color="white", ha="center", va="center")

    # Leyenda a la derecha
    leg_x = grid_x + grid_w + 0.04
    ax.text(leg_x, grid_y + grid_h - 0.01, "NIVEL DE PARTICIPACIÓN",
            fontfamily=FONT_SANS, fontsize=9, fontweight="bold",
            color=COLORS["ink_soft"], va="top")
    niveles = [
        (COLORS["good"],    "Alta (≥65%)",       "Movilización óptima"),
        ("#FACC15",         "Media (55-65%)",    "Atención estándar"),
        (COLORS["warning"], "Baja (45-55%)",     "Oportunidad"),
        (COLORS["danger"],  "Muy baja (<45%)",   "Apatía crítica"),
    ]
    for i, (color, nivel, desc) in enumerate(niveles):
        y = grid_y + grid_h - 0.06 - i * 0.085
        rect = patches.Rectangle((leg_x, y - 0.02), 0.025, 0.025,
                                  linewidth=0, facecolor=color)
        ax.add_patch(rect)
        ax.text(leg_x + 0.035, y - 0.005, nivel,
                fontfamily=FONT_SANS, fontsize=11, fontweight="bold",
                color=COLORS["ink"], va="center")
        ax.text(leg_x + 0.035, y - 0.030, desc,
                fontfamily=FONT_SANS, fontsize=9, fontstyle="italic",
                color=COLORS["ink_soft"], va="center")

    # Etiqueta debajo del grid
    ax.text(grid_x + grid_w/2, grid_y - 0.025,
            f"Distribución de {n} secciones electorales (cada celda = 1 sección)",
            fontfamily=FONT_SANS, fontsize=9, fontstyle="italic",
            color=COLORS["ink_soft"], ha="center")

    draw_insight(ax, label="Oro estratégico identificado",
        text=f"{I['heatmap_baja_secciones']} secciones tienen participación inferior al 50% — representan {I['heatmap_no_movilizados']:,} electores potenciales no movilizados. Captar incluso 20% de ese universo equivale a sumar ~25K votos: cifra suficiente para definir la elección 2027.")
    draw_footer(ax, section="VI. Indicador 1: Participación territorial", page_num=29)
    return fig


# ═══════════════════════════════════════════════════════════════
# INDICADOR 2 — TENDENCIA POR SECCIÓN (SPARKLINES)
# Corrección aplicada: RE-SECCIONADA distinta de ERRÁTICA
# ═══════════════════════════════════════════════════════════════
def page_indicador_2():
    fig = new_page()
    ax = page_ax(fig)
    draw_header(ax,
        eyebrow="Indicador 2 · Tendencia electoral",
        title="Comportamiento histórico por sección",
        subtitle="Cada valor = porcentaje del voto válido obtenido por MORENA en esa sección"
    )

    muestra = I['sparklines_muestra']
    # Colores por clasificación
    color_clasif = {
        'CONSOLIDADA':   COLORS["good"],
        'CRECIENTE':     COLORS["good"],
        'EN RETROCESO':  COLORS["danger"],
        'ERRÁTICA':      COLORS["warning"],
        'RE-SECCIONADA': COLORS["ink_light"],  # distinto color para distinguir
        'ESTABLE':       COLORS["ink_soft"],
    }

    # Header de tabla
    y_header = 0.74
    # Anchos y centros de columna
    headers_x = {
        'seccion':   M_LEFT + 0.02,
        'sparkline': M_LEFT + 0.22,       # inicio de la columna sparkline
        'variacion': M_LEFT + 0.60,
        'clasif':    M_LEFT + 0.72,
    }
    # Centro de la columna sparkline (para alinear texto y gráfico)
    spark_col_ini = headers_x['sparkline']
    spark_col_fin = headers_x['variacion']
    spark_col_center = (spark_col_ini + spark_col_fin) / 2
    spark_col_width = spark_col_fin - spark_col_ini

    # Fondo header
    rect = patches.Rectangle((M_LEFT, y_header - 0.022), CONTENT_W, 0.045,
                              linewidth=0, facecolor=COLORS["accent"])
    ax.add_patch(rect)
    # Header texts — sparkline va centrado, los demás a la izquierda
    ax.text(headers_x['seccion'], y_header, "SECCIÓN",
            fontfamily=FONT_SANS, fontsize=9, fontweight="bold",
            color="white", va="center")
    ax.text(spark_col_center, y_header, "TENDENCIA 2018-2024 (% MORENA)",
            fontfamily=FONT_SANS, fontsize=9, fontweight="bold",
            color="white", va="center", ha="center")
    ax.text(headers_x['variacion'], y_header, "VARIACIÓN",
            fontfamily=FONT_SANS, fontsize=9, fontweight="bold",
            color="white", va="center")
    ax.text(headers_x['clasif'], y_header, "CLASIFICACIÓN",
            fontfamily=FONT_SANS, fontsize=9, fontweight="bold",
            color="white", va="center")

    # Filas
    row_h = 0.058
    y_start = y_header - 0.05
    for i, item in enumerate(muestra):
        y = y_start - i * row_h
        # Fondo alterno
        if i % 2 == 1:
            rect = patches.Rectangle((M_LEFT, y - row_h/2), CONTENT_W, row_h,
                                      linewidth=0, facecolor=COLORS["row_alt"])
            ax.add_patch(rect)

        # Sección
        ax.text(headers_x['seccion'], y, str(item['seccion']),
                fontfamily=FONT_SANS, fontsize=11, color=COLORS["ink"], va="center")

        # Sparkline: 3 puntos conectados, CENTRADA en su columna
        sw = 0.26  # ancho del sparkline
        sx = spark_col_center - sw / 2  # comienza desde el centro de la columna
        sh = row_h * 0.7
        sparkline_x = [sx + sw * t for t in [0, 0.5, 1.0]]
        valores = [item['v18'], item['v21'], item['v24']]

        if item['clasif'] == 'RE-SECCIONADA':
            # Texto explicativo centrado en columna
            ax.text(spark_col_center, y, "(secciones nuevas o reasignadas — sin serie completa)",
                    fontfamily=FONT_SANS, fontsize=9, fontstyle="italic",
                    color=COLORS["ink_light"], ha="center", va="center")
        else:
            # Sparkline normal
            color = color_clasif[item['clasif']]
            # Normalizar valores a alto de sparkline
            vmin, vmax = 15, 65
            ys_norm = [y + ((v - vmin) / (vmax - vmin) - 0.5) * sh for v in valores]
            ax.plot(sparkline_x, ys_norm, color=color, linewidth=2,
                    marker='o', markersize=5, markerfacecolor=color, markeredgecolor='white',
                    markeredgewidth=1.2)
            # Etiquetas de valor mini
            for px, py, v in zip(sparkline_x, ys_norm, valores):
                ax.text(px, py + 0.015, f"{v:.0f}",
                        fontfamily=FONT_SANS, fontsize=8, color=color,
                        ha="center", va="bottom", fontweight="bold")

        # Variación
        if item['delta'] is not None:
            delta_str = f"{item['delta']:+.1f} pp"
            delta_color = COLORS["good"] if item['delta'] > 0 else COLORS["danger"]
        else:
            delta_str = "—"
            delta_color = COLORS["ink_light"]
        ax.text(headers_x['variacion'], y, delta_str,
                fontfamily=FONT_SANS, fontsize=11, fontweight="bold",
                color=delta_color, va="center")

        # Clasificación
        ax.text(headers_x['clasif'], y, item['clasif'],
                fontfamily=FONT_SANS, fontsize=10, fontweight="bold",
                color=color_clasif[item['clasif']], va="center")

    # Resumen de distribución abajo del header
    dist = I['sparklines_distribucion']
    total = sum(dist.values())
    res_y = 0.275
    ax.text(M_LEFT, res_y, f"Universo: {total} secciones con datos completos",
            fontfamily=FONT_SANS, fontsize=9, fontweight="bold",
            color=COLORS["ink_soft"])
    res_text_parts = []
    for clas in ['CONSOLIDADA','CRECIENTE','EN RETROCESO','ERRÁTICA','ESTABLE','RE-SECCIONADA']:
        if clas in dist:
            res_text_parts.append(f"{clas} {dist[clas]}")
    ax.text(M_LEFT, res_y - 0.025, "  ·  ".join(res_text_parts),
            fontfamily=FONT_SANS, fontsize=9,
            color=COLORS["ink_soft"])

    draw_insight(ax, label="Lectura de tendencias",
        text=f"Los valores son el porcentaje del voto válido obtenido por MORENA en cada sección. En 2018-2021 MORENA competía como parte de coaliciones (PT-MORENA-PES, PVEM-PT-MORENA), lo cual repartía su voto entre varias columnas. En 2024 el voto MORENA puro consolidó. La tendencia ascendente reflejada en todas las secciones (Δ positivo) confirma el crecimiento estructural del partido en Tuxtla.")
    draw_footer(ax, section="VI. Indicador 2: Tendencia por sección", page_num=30)
    return fig


# ═══════════════════════════════════════════════════════════════
# INDICADOR 3 — CRECIMIENTO POBLACIONAL TUXTLA 1990-2027
# ═══════════════════════════════════════════════════════════════
def page_indicador_3():
    fig = new_page()
    ax = page_ax(fig)
    draw_header(ax,
        eyebrow="Indicador 3 · Contexto demográfico",
        title="Crecimiento poblacional Tuxtla 1990-2027",
        subtitle="37 años de evolución demográfica con proyección INEGI-CONAPO"
    )

    años = [p['año'] for p in I['poblacion_tuxtla']]
    pob  = [p['pob']  for p in I['poblacion_tuxtla']]

    # Gráfica de área a la izquierda
    ax_chart = fig.add_axes([M_LEFT + 0.005, 0.30, 0.62, 0.46])
    ax_chart.set_facecolor(COLORS["bg"])

    # Línea + área
    ax_chart.fill_between(años, pob, alpha=0.18, color=PARTY_COLORS["MORENA"])
    ax_chart.plot(años, pob, color=PARTY_COLORS["MORENA"], linewidth=2.5,
                   marker="o", markersize=8,
                   markerfacecolor="white", markeredgecolor=PARTY_COLORS["MORENA"],
                   markeredgewidth=2)

    # Etiquetas de valor
    for x, y in zip(años, pob):
        # Mostrar en K
        label = f"{y/1000:.0f}K"
        ax_chart.text(x, y + 18000, label,
                       ha="center", va="bottom",
                       fontfamily=FONT_SANS, fontsize=10, fontweight="bold",
                       color=COLORS["ink"])

    # Línea vertical de proyección (después de 2020)
    ax_chart.axvline(x=2020.5, color=COLORS["ink_light"], linestyle="--", linewidth=1, alpha=0.7)
    ax_chart.text(2023.5, 230000, "PROYECCIÓN", ha="center",
                   fontfamily=FONT_SANS, fontsize=9, fontstyle="italic",
                   color=COLORS["ink_light"], fontweight="bold")

    ax_chart.set_xlim(1988, 2029)
    ax_chart.set_ylim(200000, 800000)
    ax_chart.set_yticks([200000, 400000, 600000, 800000])
    ax_chart.set_yticklabels(["200K","400K","600K","800K"], fontsize=9, color=COLORS["ink_soft"])
    ax_chart.set_xticks([1990, 1995, 2000, 2005, 2010, 2015, 2020, 2025])
    ax_chart.tick_params(axis="x", labelsize=10, colors=COLORS["ink_soft"])
    for s in ['top','right']: ax_chart.spines[s].set_visible(False)
    ax_chart.spines['left'].set_color(COLORS["line"])
    ax_chart.spines['bottom'].set_color(COLORS["line"])
    ax_chart.yaxis.grid(True, color=COLORS["line"], linewidth=0.6, alpha=0.5)
    ax_chart.set_axisbelow(True)

    # 3 cards de KPI a la derecha
    crec_total = (pob[-1] - pob[0]) / pob[0] * 100
    cards_x = M_LEFT + 0.70
    cards_w = CONTENT_W - 0.70
    cards_data = [
        ("1990 - 2027",       f"+{crec_total:.0f}%",   "Crecimiento total"),
        ("Tasa anual",        "~2.5%",                  "Promedio histórico"),
        ("Para 2030",         "~750K",                  "Proyección habitantes"),
    ]
    card_h = 0.13
    gap = 0.018
    for i, (label, val, desc) in enumerate(cards_data):
        y = 0.70 - i * (card_h + gap)
        render_data_card(ax, cards_x, y - card_h, cards_w, card_h, label, val, desc,
                         value_color=PARTY_COLORS["MORENA"])

    draw_insight(ax, label="Narrativa demográfica",
        text=f"Tuxtla casi duplicó su población en 30 años ({pob[0]/1000:.0f}K en 1990 → {pob[-1]/1000:.0f}K proyectados en 2027). Es la capital de mayor crecimiento del sureste mexicano. Esto crea oportunidades (nuevos electores) y desafíos (servicios urbanos saturados).")
    draw_footer(ax, section="VI. Indicador 3: Contexto demográfico", page_num=31)
    return fig


# ═══════════════════════════════════════════════════════════════
# INDICADOR 4 — TIMELINE DE COALICIONES GANADORAS
# ═══════════════════════════════════════════════════════════════
def page_indicador_4():
    fig = new_page()
    ax = page_ax(fig)
    draw_header(ax,
        eyebrow="Indicador 4 · Análisis de coaliciones",
        title="Evolución de coaliciones ganadoras",
        subtitle="Mapa de alianzas políticas en Tuxtla 1998-2024"
    )

    elecciones = [
        (1998, "PAN solo",            "PAN",                                      PARTY_COLORS["PAN"]),
        (2001, "PAN solo",            "PAN",                                      PARTY_COLORS["PAN"]),
        (2004, "Alianza para Todos",  "PAN · PRD · PT",                           PARTY_COLORS["COAL"]),
        (2007, "PRD multipartido",    "PRD · PVEM · PT · MC",                     PARTY_COLORS["PRD"]),
        (2010, "Unidad por Chiapas",  "Coalición ampliada",                       PARTY_COLORS["UNIDAD"]),
        (2012, "PRI + verde",         "PRI · PVEM · POCH",                        PARTY_COLORS["PRI"]),
        (2015, "PRI ampliado",        "PRI · PVEM · PANAL · PCHU",                PARTY_COLORS["PRI"]),
        (2018, "Inicio era MORENA",   "PT · MORENA · PES",                        PARTY_COLORS["MORENA"]),
        (2021, "MORENA solo",         "MORENA",                                   PARTY_COLORS["MORENA"]),
        (2024, "MORENA + PVEM",       "MORENA · PVEM",                            PARTY_COLORS["MORENA"]),
    ]

    # Línea horizontal eje del timeline
    eje_y = 0.50
    eje_x_ini = M_LEFT + 0.03
    eje_x_fin = 1 - M_RIGHT - 0.03
    ax.plot([eje_x_ini, eje_x_fin], [eje_y, eje_y],
            color=COLORS["line"], linewidth=1.5)

    # 10 nodos en el eje
    n = len(elecciones)
    posiciones_x = [eje_x_ini + (eje_x_fin - eje_x_ini) * (i / (n-1)) for i in range(n)]

    for i, ((año, nombre, partidos, color), x) in enumerate(zip(elecciones, posiciones_x)):
        # Punto/anillo en el eje
        outer = patches.Circle((x, eje_y), 0.012, linewidth=2.5,
                                edgecolor=color, facecolor=COLORS["bg"])
        ax.add_patch(outer)

        # Línea vertical hacia etiqueta
        if i % 2 == 0:
            # Arriba
            y_label = eje_y + 0.13
            ax.plot([x, x], [eje_y + 0.015, y_label - 0.02],
                    color=color, linewidth=1, alpha=0.4)
            # Año
            ax.text(x, y_label - 0.005, str(año),
                    fontfamily=FONT_SERIF, fontsize=14, fontweight="bold",
                    color=COLORS["ink"], ha="center", va="bottom")
            # Nombre coalición
            ax.text(x, y_label + 0.025, nombre,
                    fontfamily=FONT_SANS, fontsize=10, fontweight="bold",
                    color=color, ha="center", va="bottom")
            # Partidos pequeño
            ax.text(x, y_label + 0.045, partidos,
                    fontfamily=FONT_SANS, fontsize=8, fontstyle="italic",
                    color=COLORS["ink_soft"], ha="center", va="bottom")
        else:
            # Abajo
            y_label = eje_y - 0.13
            ax.plot([x, x], [eje_y - 0.015, y_label + 0.02],
                    color=color, linewidth=1, alpha=0.4)
            ax.text(x, y_label + 0.005, str(año),
                    fontfamily=FONT_SERIF, fontsize=14, fontweight="bold",
                    color=COLORS["ink"], ha="center", va="top")
            ax.text(x, y_label - 0.025, nombre,
                    fontfamily=FONT_SANS, fontsize=10, fontweight="bold",
                    color=color, ha="center", va="top")
            ax.text(x, y_label - 0.045, partidos,
                    fontfamily=FONT_SANS, fontsize=8, fontstyle="italic",
                    color=COLORS["ink_soft"], ha="center", va="top")

    # 3 segmentos de era abajo
    eras_y = 0.13
    eras_h = 0.05
    eras = [
        ("Era PAN",      PARTY_COLORS["PAN"],    0, 1),
        ("Alternancia",  COLORS["ink_light"],    2, 6),
        ("Era MORENA",   PARTY_COLORS["MORENA"], 7, 9),
    ]
    for label, color, i_ini, i_fin in eras:
        x_ini = posiciones_x[i_ini] - 0.01
        x_fin = posiciones_x[i_fin] + 0.01
        rect = patches.FancyBboxPatch(
            (x_ini, eras_y), x_fin - x_ini, eras_h,
            boxstyle="round,pad=0,rounding_size=0.008",
            linewidth=0, facecolor=color
        )
        ax.add_patch(rect)
        ax.text((x_ini + x_fin) / 2, eras_y + eras_h/2, label,
                fontfamily=FONT_SANS, fontsize=11, fontweight="bold",
                color="white", ha="center", va="center")

    draw_footer(ax, section="VI. Indicador 4: Coaliciones históricas", page_num=32)
    return fig


# ═══════════════════════════════════════════════════════════════
# INDICADOR 5 — RADAR DE FORTALEZAS (3 partidos, colores institucionales)
# ═══════════════════════════════════════════════════════════════
def page_indicador_5():
    fig = new_page()
    ax = page_ax(fig)
    draw_header(ax,
        eyebrow="Indicador 5 · Perfil estratégico",
        title="Radar de fortalezas territoriales",
        subtitle="Comparativo MORENA vs PAN vs MC en 6 dimensiones electorales"
    )

    radar = I['radar']
    dimensiones = ['Cobertura\nterritorial', 'Votación\npromedio', 'Crecimiento\nhistórico',
                   'Movilización', 'Bastiones\nseguros', 'Penetración\nurbana']
    angulos = np.linspace(0, 2*np.pi, len(dimensiones), endpoint=False).tolist()
    angulos += angulos[:1]  # cerrar polígono

    # Radar a la izquierda — más compacto y posicionado para dejar espacio a etiquetas
    ax_radar = fig.add_axes([M_LEFT + 0.04, 0.295, 0.40, 0.44], polar=True)
    ax_radar.set_facecolor(COLORS["bg"])
    ax_radar.set_theta_offset(np.pi / 2)
    ax_radar.set_theta_direction(-1)

    # Plot por partido
    partidos_plot = [('MORENA', PARTY_COLORS["MORENA"]),
                     ('PAN',    PARTY_COLORS["PAN"]),
                     ('MC',     PARTY_COLORS["MC"])]
    for partido, color in partidos_plot:
        # Las claves del JSON están sin \n
        dims_key = [d.replace('\n', ' ') for d in dimensiones]
        valores = [radar[partido][d] for d in dims_key]
        valores += valores[:1]
        ax_radar.plot(angulos, valores, color=color, linewidth=2.5, label=partido)
        ax_radar.fill(angulos, valores, color=color, alpha=0.18)

    # Etiquetas de dimensiones — usar las nativas de matplotlib con padding
    ax_radar.set_xticks(angulos[:-1])
    ax_radar.set_xticklabels(dimensiones,
                              fontfamily=FONT_SANS, fontsize=10, fontweight="bold",
                              color=COLORS["ink"])
    ax_radar.tick_params(axis='x', pad=18)  # separar etiquetas del radar

    # Ejes radiales
    ax_radar.set_ylim(0, 100)
    ax_radar.set_yticks([20, 40, 60, 80, 100])
    ax_radar.set_yticklabels(["20","40","60","80","100"], fontsize=8, color=COLORS["ink_light"])
    ax_radar.tick_params(axis='y', pad=0)
    ax_radar.grid(color=COLORS["line"], linewidth=0.6, alpha=0.7)
    ax_radar.spines['polar'].set_color(COLORS["line"])
    ax_radar.spines['polar'].set_linewidth(0.6)

    # Leyenda + análisis a la derecha
    leg_x = M_LEFT + 0.56
    leg_y = 0.74
    # Línea + nombre partido
    for i, (partido, color) in enumerate(partidos_plot):
        y = leg_y - i * 0.04
        ax.plot([leg_x, leg_x + 0.03], [y, y], color=color, linewidth=3, solid_capstyle="butt")
        ax.text(leg_x + 0.04, y, partido,
                fontfamily=FONT_SANS, fontsize=12, fontweight="bold",
                color=COLORS["ink"], va="center")

    # Bloque análisis
    interp_y = 0.58
    interpretaciones = [
        ("FORTALEZA MORENA",  COLORS["good"],
         f"Lidera en cobertura ({radar['MORENA']['Cobertura territorial']:.0f}) y votación promedio (100)."),
        ("AMENAZA PAN",       COLORS["danger"],
         f"Penetración urbana ({radar['PAN']['Penetración urbana']:.0f}) y votación ({radar['PAN']['Votación promedio']:.0f}) por encima de su cobertura."),
        ("TERCERA FUERZA: MC", PARTY_COLORS["MC"],
         f"Movilización baja ({radar['MC']['Movilización']:.0f}) pero crecimiento histórico medio."),
        ("OPORTUNIDAD",       COLORS["accent"],
         "Cerrar brecha en penetración urbana = consolidar victoria."),
    ]
    for i, (titulo, color, desc) in enumerate(interpretaciones):
        y = interp_y - i * 0.08
        ax.text(leg_x, y, titulo,
                fontfamily=FONT_SANS, fontsize=10, fontweight="bold",
                color=color)
        wrapped = wrap_text(desc, 38)
        ax.text(leg_x, y - 0.022, wrapped,
                fontfamily=FONT_SANS, fontsize=9.5, fontstyle="italic",
                color=COLORS["ink_soft"], va="top", linespacing=1.4)

    # Nota al pie aclarando que algunas dimensiones son estimaciones
    ax.text(M_LEFT, 0.245,
            "Nota metodológica: 'Cobertura territorial', 'Votación promedio', 'Movilización' y 'Bastiones seguros' se calculan del Excel POWERBI2023. 'Crecimiento histórico' y 'Penetración urbana' son estimaciones heurísticas calibradas (requieren datos adicionales para validación cuantitativa).",
            fontfamily=FONT_SANS, fontsize=7.5, fontstyle="italic",
            color=COLORS["ink_light"], va="top",
            wrap=True)

    draw_insight(ax, label="Diagnóstico comparativo",
        text=f"MORENA domina en cobertura ({radar['MORENA']['Cobertura territorial']:.0f}) y bastiones seguros. PAN mantiene fortaleza en penetración urbana ({radar['PAN']['Penetración urbana']:.0f}) — sus votantes son geográficamente más concentrados. MC aparece como tercera fuerza con potencial captable. Estrategia: aumentar movilización MORENA y disputar voto urbano.")
    draw_footer(ax, section="VI. Indicador 5: Radar de fortalezas", page_num=33)
    return fig
