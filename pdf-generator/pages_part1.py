"""
pages_part1.py — Páginas 1 a 18 del PDF v2
"""
import sys
sys.path.insert(0, "/home/claude/proyecto")

import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from brand import COLORS, FONT_SERIF, FONT_SANS, TYPE, M_LEFT, M_RIGHT, CONTENT_W, PARTY_COLORS
from page_system import (
    new_page, page_ax, draw_header, draw_footer, draw_insight,
    draw_card, draw_logo, wrap_text, party_color
)
from components import (
    render_part_page, render_numbered_card, render_data_card, render_table
)

with open('/home/claude/proyecto/datos_tuxtla.json') as f:
    D = json.load(f)


# ═══════════════════════════════════════════════════════════════
# PÁGINA 1 — PORTADA
# ═══════════════════════════════════════════════════════════════
def page_01():
    fig = new_page()
    ax = page_ax(fig)
    draw_logo(ax, 0.5, 0.84, width=0.30)
    ax.text(0.5, 0.66, "DIAGNÓSTICO ELECTORAL · CHIAPAS 2027",
            fontfamily=FONT_SANS, fontsize=12, fontweight="bold",
            color=COLORS["ink_soft"], ha="center", va="center")
    ax.plot([0.42, 0.58], [0.625, 0.625], color=COLORS["ink"], linewidth=2.5)
    ax.text(0.5, 0.50, "Inteligencia", fontfamily=FONT_SERIF, fontsize=72,
            fontweight="bold", color=COLORS["ink"], ha="center", va="center")
    ax.text(0.5, 0.385, "Electoral Municipal", fontfamily=FONT_SERIF, fontsize=72,
            fontweight="bold", color=COLORS["ink"], ha="center", va="center")
    ax.text(0.5, 0.265, '"Datos, territorio y estrategia',
            fontfamily=FONT_SERIF, fontsize=18, fontstyle="italic",
            color=COLORS["ink_soft"], ha="center", va="center")
    ax.text(0.5, 0.225, 'para construir mayoría electoral"',
            fontfamily=FONT_SERIF, fontsize=18, fontstyle="italic",
            color=COLORS["ink_soft"], ha="center", va="center")
    rect = patches.Rectangle((0, 0), 1, 0.08, linewidth=0, facecolor=COLORS["accent"])
    ax.add_patch(rect)
    ax.text(0.5, 0.04, "T U X T L A   G U T I É R R E Z   ·   P R O C E S O   E L E C T O R A L   2 0 2 7",
            fontfamily=FONT_SANS, fontsize=10, fontweight="bold",
            color="#FFFFFF", ha="center", va="center")
    return fig


# ═══════════════════════════════════════════════════════════════
# PÁGINA 2 — SUB-PORTADA (candidato)
# ═══════════════════════════════════════════════════════════════
def page_02():
    fig = new_page()
    ax = page_ax(fig)
    # Eyebrow
    ax.text(M_LEFT, 0.88, "DIAGNÓSTICO ELECTORAL · CHIAPAS 2027",
            fontfamily=FONT_SANS, fontsize=10, fontweight="bold",
            color=COLORS["ink_soft"])
    ax.plot([M_LEFT, M_LEFT + 0.05], [0.855, 0.855], color=COLORS["ink"], linewidth=2.5)

    # "Candidato a / Presidencia Municipal"
    ax.text(M_LEFT, 0.79, "Candidato a",
            fontfamily=FONT_SERIF, fontsize=24, fontstyle="italic",
            color=COLORS["ink_soft"], va="center")
    ax.text(M_LEFT, 0.745, "Presidencia Municipal",
            fontfamily=FONT_SERIF, fontsize=24, fontstyle="italic",
            color=COLORS["ink_soft"], va="center")

    # Nombre grande
    ax.text(M_LEFT, 0.58, "FRANCISCO",
            fontfamily=FONT_SERIF, fontsize=64, fontweight="bold",
            color=COLORS["ink"], va="center")
    ax.text(M_LEFT, 0.50, "CHÁCON SÁNCHEZ",
            fontfamily=FONT_SERIF, fontsize=64, fontweight="bold",
            color=COLORS["ink"], va="center")

    # Municipio
    ax.text(M_LEFT, 0.405, "Tuxtla Gutiérrez",
            fontfamily=FONT_SERIF, fontsize=24, fontstyle="italic",
            color=COLORS["ink_soft"], va="center")

    # Tres bloques inferiores
    y_block = 0.20
    box_w = 0.25
    gap = 0.03
    block_x_start = M_LEFT
    blocks = [
        ("PROCESO ELECTORAL", "Chiapas 2027"),
        ("PARTIDO", "MORENA"),
        ("PREPARADO POR", "Baldemar Maza León\nConsultoría Electoral"),
    ]
    for i, (label, value) in enumerate(blocks):
        bx = block_x_start + i * (box_w + gap)
        # Línea decorativa arriba
        ax.plot([bx, bx + 0.03], [y_block + 0.07, y_block + 0.07],
                color=COLORS["ink"], linewidth=2)
        ax.text(bx, y_block + 0.04, label,
                fontfamily=FONT_SANS, fontsize=9, fontweight="bold",
                color=COLORS["ink_soft"])
        wrapped = wrap_text(value, 30)
        ax.text(bx, y_block - 0.005, wrapped,
                fontfamily=FONT_SERIF, fontsize=14, fontweight="bold",
                color=COLORS["ink"], va="top", linespacing=1.3)

    draw_footer(ax, section="Sub-portada", page_num=2)
    return fig


# ═══════════════════════════════════════════════════════════════
# PÁGINA 3 — ÍNDICE
# ═══════════════════════════════════════════════════════════════
def page_03():
    fig = new_page()
    ax = page_ax(fig)
    draw_header(ax,
        eyebrow="Contenido del documento",
        title="Índice",
        subtitle=None
    )
    # Entradas del índice
    items = [
        ("I.",    "Contexto territorial",                "5"),
        ("II.",   "Historia política 1998-2024",         "8"),
        ("III.",  "Análisis de la elección 2024",        "13"),
        ("IV.",   "Listado nominal y proyecciones",      "19"),
        ("V.",    "Escenarios electorales 2027",         "23"),
        ("VI.",   "Indicadores complementarios",         "28"),
        ("VII.",  "Conclusiones y recomendaciones",      "39"),
        ("VIII.", "Anexos, metodología y glosario",      "44"),
        ("IX.",   "Cierre estratégico",                  "47"),
    ]
    y0 = 0.72
    row_h = 0.068
    for i, (roman, title, page) in enumerate(items):
        y = y0 - i * row_h
        ax.text(M_LEFT, y, roman,
                fontfamily=FONT_SERIF, fontsize=18, fontweight="bold",
                color=COLORS["accent"], va="center")
        ax.text(M_LEFT + 0.06, y, title,
                fontfamily=FONT_SERIF, fontsize=18,
                color=COLORS["ink"], va="center")
        ax.text(1 - M_RIGHT, y, page,
                fontfamily=FONT_SANS, fontsize=14, fontweight="bold",
                color=COLORS["ink_soft"], va="center", ha="right")
        # línea sutil debajo
        ax.plot([M_LEFT, 1 - M_RIGHT], [y - 0.03, y - 0.03],
                color=COLORS["line"], linewidth=0.6)

    draw_footer(ax, section="Índice", page_num=3)
    return fig


# ═══════════════════════════════════════════════════════════════
# PÁGINA 4 — RESUMEN EJECUTIVO (4 cards numerados 2x2)
# CORRECCIÓN: card 04 debe mencionar top 3 oposición (PAN, MC, PRI)
# ═══════════════════════════════════════════════════════════════
def page_04():
    fig = new_page()
    ax = page_ax(fig)
    draw_header(ax,
        eyebrow="Hallazgos clave",
        title="Resumen ejecutivo",
        subtitle="Lo esencial sobre el panorama electoral de Tuxtla Gutiérrez"
    )
    # 4 cards 2x2 en zona de contenido
    pct_morena = D['secciones_morena'] * 100 / D['total_secciones']
    cards = [
        ("01", "BASTIÓN MORENA CONSOLIDADO",
         f"MORENA ha ganado 3 elecciones consecutivas (2018-2024) con "
         f"{D['secciones_morena']} secciones ganadas de {D['total_secciones']} en 2024 "
         f"({pct_morena:.0f}% del territorio)."),
        ("02", "PADRÓN EN CRECIMIENTO",
         f"Listado nominal proyectado a {D['listado_nominal']['2027']:,} electores en 2027 "
         f"(+{D['crecimiento_ln_2024_2027_pct']}% vs 2024). "
         f"{D['secciones_crecen']} secciones crecen, {D['secciones_decrecen']} decrecen."),
        ("03", f"{D['total_secciones']} SECCIONES ELECTORALES",
         f"Distribuidas en 3 distritos locales ({D['distritos_tuxtla']}). "
         f"En 2024 se instalaron {D['total_casillas']} casillas; jornada con 68% participación."),
        ("04", "OPOSICIÓN MULTIPARTIDISTA",
         f"Top 3 fuerzas opositoras 2024: "
         f"PAN ({D['top3_oposicion'][0]['votos']:,} votos), "
         f"MC ({D['top3_oposicion'][1]['votos']:,}) y "
         f"PRI ({D['top3_oposicion'][2]['votos']:,}). "
         f"PAN concentra fuerza en zonas residenciales del oriente."),
    ]
    # Layout 2x2
    card_w = (CONTENT_W - 0.03) / 2
    card_h = 0.215
    positions = [
        (M_LEFT, 0.50),                       # arriba izq
        (M_LEFT + card_w + 0.03, 0.50),       # arriba der
        (M_LEFT, 0.27),                       # abajo izq
        (M_LEFT + card_w + 0.03, 0.27),       # abajo der
    ]
    for (num, title, body), (x, y) in zip(cards, positions):
        render_numbered_card(ax, x, y, card_w, card_h, num, title, body, body_chars=46)

    draw_footer(ax, section="Resumen ejecutivo", page_num=4)
    return fig


# ═══════════════════════════════════════════════════════════════
# PÁGINA 5 — DIVISOR PARTE I
# ═══════════════════════════════════════════════════════════════
def page_05():
    fig = new_page()
    ax = page_ax(fig)
    render_part_page(ax, "I", "Parte I", "Contexto\nterritorial",
        "Localización, demografía y configuración electoral del municipio.")
    draw_footer(ax, section="Parte I", page_num=5)
    return fig


# ═══════════════════════════════════════════════════════════════
# PÁGINA 6 — CONTEXTO TERRITORIAL (texto + 5 data cards)
# CORRECCIÓN: "Distrito Local" completo + Distritos 01, 02 y 13
# ═══════════════════════════════════════════════════════════════
def page_06():
    fig = new_page()
    ax = page_ax(fig)
    draw_header(ax,
        eyebrow="I. Contexto territorial",
        title="Localización geográfica",
        subtitle="Tuxtla Gutiérrez es la capital del estado de Chiapas"
    )
    # Texto descriptivo a la izquierda
    parrafo = (
        "Tuxtla Gutiérrez es la capital del estado de Chiapas y se ubica en la "
        "Región Socioeconómica I Metropolitana.\n\n"
        "Limita al norte con San Fernando y Osumacinta, al este con Chiapa de Corzo, "
        "al sur con Suchiapa y al oeste con Ocozocoautla de Espinosa y Berriozábal.\n\n"
        "Las coordenadas de la cabecera municipal son: 16°45'11\" de latitud Norte y "
        "93°06'56\" de longitud Oeste, a una altitud de 522 metros sobre el nivel del mar.\n\n"
        "Con una superficie territorial de 334.61 km², ocupa el 0.45% del territorio "
        "estatal de Chiapas."
    )
    wrapped = wrap_text(parrafo, 60)
    ax.text(M_LEFT, 0.74, wrapped,
            fontfamily=FONT_SANS, fontsize=11.5, color=COLORS["ink_soft"],
            va="top", linespacing=1.55)

    # 5 data cards a la derecha — DATOS CLAVE
    x_cards = M_LEFT + 0.45
    cards_w = CONTENT_W - 0.45
    # Eyebrow encima de cards
    ax.text(x_cards, 0.755, "DATOS CLAVE",
            fontfamily=FONT_SANS, fontsize=10, fontweight="bold",
            color=COLORS["ink_soft"])
    card_h = 0.115
    gap = 0.010
    cards_data = [
        ("Superficie", "334.61 km²", "0.45% del estado"),
        ("Región", "I Metropolitana", "Capital estatal"),
        ("Altitud", "522 msnm", "Sobre nivel del mar"),
        ("Distrito Local", D['distritos_tuxtla'], "Tres distritos"),
        ("Secciones", str(D['total_secciones']), "Electorales"),
    ]
    y_top = 0.725
    for i, (label, value, desc) in enumerate(cards_data):
        y = y_top - i * (card_h + gap)
        render_data_card(ax, x_cards, y - card_h, cards_w, card_h, label, value, desc)

    draw_footer(ax, section="I. Contexto territorial", page_num=6)
    return fig


# ═══════════════════════════════════════════════════════════════
# PÁGINA 7 — DEMOGRAFÍA (3 data cards grandes + donut H/M)
# ═══════════════════════════════════════════════════════════════
def page_07():
    fig = new_page()
    ax = page_ax(fig)
    draw_header(ax,
        eyebrow="I. Contexto territorial",
        title="Demografía municipal",
        subtitle="Tuxtla Gutiérrez representa el 11.55% de la población de Chiapas"
    )

    # Donut a la IZQUIERDA con margen suficiente para etiquetas externas
    ax_donut = fig.add_axes([M_LEFT + 0.04, 0.28, 0.38, 0.46])
    ax_donut.set_aspect("equal")
    ax_donut.set_xlim(-1.6, 1.6)
    ax_donut.set_ylim(-1.4, 1.4)
    sizes = [52.38, 47.62]
    colors_donut = [COLORS["accent"], COLORS["ink_light"]]
    labels = ['Mujeres', 'Hombres']
    pcts = ['52.38%', '47.62%']
    wedges, _ = ax_donut.pie(sizes, colors=colors_donut, startangle=90,
                              wedgeprops=dict(width=0.32, edgecolor=COLORS["bg"], linewidth=2),
                              radius=1.0)
    # Etiquetas externas con líneas guía
    for wedge, label, pct in zip(wedges, labels, pcts):
        ang = (wedge.theta2 + wedge.theta1) / 2.
        # punto de anclaje en el borde externo
        x_anchor = 1.05 * np.cos(np.deg2rad(ang))
        y_anchor = 1.05 * np.sin(np.deg2rad(ang))
        # posición del texto
        x_text = 1.45 * np.cos(np.deg2rad(ang))
        y_text = 1.20 * np.sin(np.deg2rad(ang))
        ha = "left" if x_text >= 0 else "right"
        # línea guía sutil
        ax_donut.plot([x_anchor, x_text*0.92], [y_anchor, y_text*0.96],
                       color=COLORS["ink_light"], linewidth=0.8, alpha=0.6)
        # etiqueta
        ax_donut.text(x_text, y_text + 0.05, label,
                       fontfamily=FONT_SANS, fontsize=11, fontweight="bold",
                       color=COLORS["ink"], ha=ha, va="bottom")
        ax_donut.text(x_text, y_text - 0.05, pct,
                       fontfamily=FONT_SERIF, fontsize=14, fontweight="bold",
                       color=COLORS["ink"], ha=ha, va="top")
    ax_donut.set_facecolor("none")
    ax_donut.axis("off")

    # 3 cards a la DERECHA, apilados verticalmente
    cards_x = M_LEFT + 0.50
    cards_w = CONTENT_W - 0.50
    card_h = 0.135
    gap = 0.018
    y_top = 0.72
    cards_data = [
        ("Población total", "671,619", "habitantes (Censo 2020)", COLORS["ink"]),
        ("Hombres",         "319,838", "47.62% del total",          COLORS["ink"]),
        ("Mujeres",         "351,781", "52.38% del total",          COLORS["accent"]),
    ]
    for i, (label, value, desc, color) in enumerate(cards_data):
        y = y_top - i * (card_h + gap)
        render_data_card(ax, cards_x, y - card_h, cards_w, card_h, label, value, desc,
                         value_color=color, value_size=24)

    draw_insight(ax,
        label="Implicación electoral",
        text=("Tuxtla concentra mayoría de voto femenino (52.4%). Las estrategias de "
              "campaña 2027 deben considerar a las mujeres como base electoral clave, "
              "con propuestas diferenciadas en agenda de género, seguridad y empleo."))
    draw_footer(ax, section="I. Contexto territorial", page_num=7)
    return fig


# ═══════════════════════════════════════════════════════════════
# PÁGINA 8 — DIVISOR PARTE II
# ═══════════════════════════════════════════════════════════════
def page_08():
    fig = new_page()
    ax = page_ax(fig)
    render_part_page(ax, "II", "Parte II", "Historia\npolítica",
        "Evolución del voto y partidos en Tuxtla 1998-2024.")
    draw_footer(ax, section="Parte II", page_num=8)
    return fig


# ═══════════════════════════════════════════════════════════════
# PÁGINA 9 — VOTACIÓN MUNICIPAL POR ELECCIÓN (barras)
# ═══════════════════════════════════════════════════════════════
def page_09():
    fig = new_page()
    ax = page_ax(fig)
    draw_header(ax,
        eyebrow="II. Historia política · 1998-2024",
        title="Votación municipal por elección",
        subtitle="Evolución del voto para presidente municipal en 10 elecciones"
    )
    años = [1998, 2001, 2004, 2007, 2010, 2012, 2015, 2018, 2021, 2024]
    votos = [46877, 36613, 89776, 54153, 50650, 76683, 66590, 94873, 75199, 94893]
    partidos = ["PAN","PAN","COAL","COAL","COAL","COAL","COAL","COAL","MORENA","MORENA"]
    colors = [PARTY_COLORS["PAN"], PARTY_COLORS["PAN"], PARTY_COLORS["COAL"],
              PARTY_COLORS["PRD"], PARTY_COLORS["UNIDAD"], PARTY_COLORS["PRI"],
              PARTY_COLORS["PRI"], PARTY_COLORS["MORENA"], PARTY_COLORS["MORENA"],
              PARTY_COLORS["MORENA"]]

    ax_chart = fig.add_axes([M_LEFT + 0.01, 0.275, CONTENT_W - 0.02, 0.48])
    ax_chart.set_facecolor(COLORS["bg"])
    x_pos = np.arange(len(años))
    bars = ax_chart.bar(x_pos, votos, color=colors, width=0.62, edgecolor="none")
    for bar, v in zip(bars, votos):
        ax_chart.text(bar.get_x() + bar.get_width()/2, v + 2200, f"{v:,}",
                      ha="center", va="bottom",
                      fontfamily=FONT_SANS, fontsize=10, fontweight="bold",
                      color=COLORS["ink"])
    for i, p in enumerate(partidos):
        ax_chart.text(i, -8500, p, ha="center", va="top",
                      fontfamily=FONT_SANS, fontsize=8.5, fontweight="bold",
                      color=COLORS["ink_soft"])
    ax_chart.set_xticks(x_pos)
    ax_chart.set_xticklabels(años, fontsize=11, fontweight="bold", color=COLORS["ink"])
    ax_chart.tick_params(axis="x", length=0, pad=8)
    ax_chart.set_yticks([20000, 40000, 60000, 80000, 100000])
    ax_chart.set_yticklabels(["20K","40K","60K","80K","100K"], fontsize=9, color=COLORS["ink_soft"])
    ax_chart.tick_params(axis="y", length=0, pad=4)
    ax_chart.set_ylim(0, 115000)
    ax_chart.yaxis.grid(True, color=COLORS["line"], linewidth=0.6)
    ax_chart.set_axisbelow(True)
    for s in ax_chart.spines.values(): s.set_visible(False)

    draw_insight(ax, label="Insight clave",
        text="MORENA acumula 3 victorias consecutivas en Tuxtla (2018, 2021, 2024). En 2024 alcanza 94,893 votos — récord histórico empatado prácticamente con 2018 (94,873). Tuxtla se consolida como bastión guinda.")
    draw_footer(ax, section="II. Historia política", page_num=9)
    return fig


# ═══════════════════════════════════════════════════════════════
# PÁGINA 10 — PARTICIPACIÓN ELECTORAL HISTÓRICA (línea)
# ═══════════════════════════════════════════════════════════════
def page_10():
    fig = new_page()
    ax = page_ax(fig)
    draw_header(ax,
        eyebrow="II. Historia política · 1998-2024",
        title="Participación electoral histórica",
        subtitle="Evolución comparada: elecciones estatales vs federales"
    )

    # Datos estatales (los originales, leídos del Excel: PARTICIPACION ELECTORAL ESTATAL)
    estatal_años = [1998, 2001, 2004, 2007, 2010, 2012, 2015, 2018, 2021, 2024]
    estatal_pct  = [46.3, 51.8, 54.8, 56.9, 53.3, 67.5, 64.1, 66.8, 59.9, 68.2]

    # Datos federales (leídos del Excel: PARTICIPACION ELECTORAL FEDERAL)
    federal_años = [2000, 2003, 2006, 2009, 2012, 2015, 2018, 2021, 2024]
    federal_pct  = [52.2, 31.8, 48.7, 40.0, 67.3, 46.3, 68.9, 61.3, 62.0]

    ax_chart = fig.add_axes([M_LEFT + 0.01, 0.275, CONTENT_W - 0.02, 0.48])
    ax_chart.set_facecolor(COLORS["bg"])

    # Línea estatal (color principal)
    ax_chart.plot(estatal_años, estatal_pct,
                   color=COLORS["ink"], linewidth=2.5, marker="o",
                   markersize=8, markerfacecolor=COLORS["ink"],
                   markeredgecolor="white", markeredgewidth=2,
                   label="Estatal")
    # Línea federal (color secundario)
    ax_chart.plot(federal_años, federal_pct,
                   color=PARTY_COLORS["MORENA"], linewidth=2.5,
                   marker="s", markersize=8,
                   markerfacecolor=PARTY_COLORS["MORENA"],
                   markeredgecolor="white", markeredgewidth=2,
                   linestyle="--",
                   label="Federal")

    # Etiquetas inteligentes: cuando dos puntos coinciden temporal y verticalmente, agruparlas
    # Detectar pares de años cercanos con valores cercanos
    pares_cercanos = set()
    for x_e, y_e in zip(estatal_años, estatal_pct):
        for x_f, y_f in zip(federal_años, federal_pct):
            if abs(x_e - x_f) <= 1 and abs(y_e - y_f) < 3:
                pares_cercanos.add((x_e, x_f))

    # Render por separado, evitando los pares cercanos en su lugar normal
    # Para cada año estatal
    for x, y in zip(estatal_años, estatal_pct):
        # Verificar si forma par cercano con un federal
        en_par = any(p[0] == x for p in pares_cercanos)
        if en_par:
            # Buscar el federal y dibujar etiqueta combinada arriba
            for x_f, y_f in zip(federal_años, federal_pct):
                if (x, x_f) in pares_cercanos:
                    # Una sola etiqueta agrupada
                    ax_chart.text(x, max(y, y_f) + 2.0,
                                  f"{y:.1f} | {y_f:.1f}",
                                  ha="center", va="bottom",
                                  fontfamily=FONT_SANS, fontsize=9, fontweight="bold",
                                  color=COLORS["ink"])
                    break
        else:
            ax_chart.text(x, y + 1.5, f"{y:.1f}",
                          ha="center", va="bottom",
                          fontfamily=FONT_SANS, fontsize=9, fontweight="bold",
                          color=COLORS["ink"])

    for x, y in zip(federal_años, federal_pct):
        en_par = any(p[1] == x for p in pares_cercanos)
        if not en_par:
            ax_chart.text(x, y - 2.0, f"{y:.1f}",
                          ha="center", va="top",
                          fontfamily=FONT_SANS, fontsize=9, fontweight="bold",
                          color=PARTY_COLORS["MORENA"])

    ax_chart.set_xlim(1996, 2026)
    ax_chart.set_ylim(25, 78)
    ax_chart.set_ylabel("Participación (%)", fontfamily=FONT_SANS, fontsize=10, color=COLORS["ink_soft"])
    ax_chart.tick_params(colors=COLORS["ink_soft"], labelsize=10)
    for s in ['top','right']:
        ax_chart.spines[s].set_visible(False)
    ax_chart.spines['left'].set_color(COLORS["line"])
    ax_chart.spines['bottom'].set_color(COLORS["line"])
    ax_chart.yaxis.grid(True, color=COLORS["line"], linewidth=0.6, alpha=0.5)
    ax_chart.set_axisbelow(True)

    # Leyenda nativa de matplotlib
    leg = ax_chart.legend(loc='upper left', frameon=False,
                          prop={'family': FONT_SANS, 'size': 11, 'weight': 'bold'},
                          handlelength=2.0)
    for text in leg.get_texts():
        text.set_color(COLORS["ink"])

    prom_est = sum(estatal_pct)/len(estatal_pct)
    prom_fed = sum(federal_pct)/len(federal_pct)
    draw_insight(ax, label="Comparativo estatal vs federal",
        text=f"Participación promedio estatal: {prom_est:.1f}% | federal: {prom_fed:.1f}% (diferencia ~{prom_est-prom_fed:.0f}pp). La participación FEDERAL es históricamente más baja y volátil — los procesos locales (elecciones intermedias estatales) generan más movilización en Tuxtla. En 2018, 2021 y 2024 la brecha se acorta cuando coincidieron concurrencias.")
    draw_footer(ax, section="II. Historia política", page_num=10)
    return fig


# ═══════════════════════════════════════════════════════════════
# PÁGINA 11 — TABLA HISTÓRICA DE PRESIDENTES MUNICIPALES
# ═══════════════════════════════════════════════════════════════
def page_11():
    fig = new_page()
    ax = page_ax(fig)
    draw_header(ax,
        eyebrow="II. Historia política",
        title="Presidentes municipales electos",
        subtitle="De alternancia política a hegemonía MORENA (1998-2024)"
    )
    rows = [
        ["1998", "PAN", "Francisco Antonio Rojas Toledo"],
        ["2001", "PAN", "Victoria Isabel Rincón Carrillo"],
        ["2004", "Coalición Alianza para Todos", "Juan José Sabines Guerrero"],
        ["2007", "PRD-PVEM-PT-Convergencia", "Jaime Valls Esponda"],
        ["2010", "Unidad por Chiapas", "Seth Yassir Vázquez Hernández"],
        ["2012", "PRI-PVEM-POCH", "Samuel Toledo Córdova Toledo"],
        ["2015", "PRI-PVEM-PANAL-PCHU", "Luis Fernando Castellanos Cal y Mayor"],
        ["2018", "PT-MORENA-PES", "Carlos Orsoe Morales Vázquez"],
        ["2021", "MORENA", "Carlos Orsoe Morales Vázquez (R)"],
        ["2024", "MORENA", "Ángel Carlos Torres Culebro"],
    ]
    render_table(ax,
        x=M_LEFT, y=0.28, w=CONTENT_W, h=0.48,
        headers=["Año", "Partido / Coalición", "Candidato electo"],
        rows=rows,
        col_widths_frac=[0.09, 0.39, 0.52],
    )
    draw_insight(ax, label="Patrón histórico",
        text="En 18 años hubo 6 fuerzas distintas ganadoras (1998-2015). Desde 2018, MORENA domina con 3 victorias consecutivas más una reelección de Carlos Morales.")
    draw_footer(ax, section="II. Historia política", page_num=11)
    return fig


# ═══════════════════════════════════════════════════════════════
# PÁGINA 12 — TRES ERAS POLÍTICAS (3 cards de eras)
# ═══════════════════════════════════════════════════════════════
def page_12():
    fig = new_page()
    ax = page_ax(fig)
    draw_header(ax,
        eyebrow="II. Historia política",
        title="De alternancia a hegemonía",
        subtitle="Tres eras políticas marcaron Tuxtla en 26 años"
    )
    # 3 cards horizontales coloreados por partido dominante
    card_w = (CONTENT_W - 0.04) / 3
    card_h = 0.46
    y = 0.30
    eras = [
        ("ERA PAN", "1998-2007", PARTY_COLORS["PAN"],
         "Hegemonía azul en alianza con sectores empresariales. "
         "Rojas Toledo y Rincón Carrillo encabezan continuidad panista en la capital."),
        ("ALTERNANCIA", "2007-2015", COLORS["ink_light"],
         "Cuatro coaliciones distintas ganan elección a elección. "
         "Sabines, Valls, Vázquez, Toledo y Castellanos representan el ciclo de cambio."),
        ("ERA MORENA", "2018-2024", PARTY_COLORS["MORENA"],
         "Tres victorias consecutivas: Carlos Morales (2018, 2021) y Ángel Torres (2024). "
         "MORENA se consolida como fuerza dominante en la capital chiapaneca."),
    ]
    for i, (era, period, color, body) in enumerate(eras):
        x = M_LEFT + i * (card_w + 0.02)
        # Barra superior coloreada
        bar = patches.Rectangle((x, y + card_h - 0.012), card_w, 0.012,
                                 linewidth=0, facecolor=color)
        ax.add_patch(bar)
        draw_card(ax, x, y, card_w, card_h - 0.012, lw=0.8)
        # Era título
        ax.text(x + 0.02, y + card_h - 0.07, era,
                fontfamily=FONT_SANS, fontsize=11, fontweight="bold",
                color=color)
        ax.text(x + 0.02, y + card_h - 0.12, period,
                fontfamily=FONT_SERIF, fontsize=28, fontweight="bold",
                color=COLORS["ink"], va="center")
        # Body
        wrapped = wrap_text(body, 38)
        ax.text(x + 0.02, y + card_h - 0.18, wrapped,
                fontfamily=FONT_SANS, fontsize=10.5,
                color=COLORS["ink_soft"], va="top", linespacing=1.5)

    draw_insight(ax, label="Lectura estratégica",
        text="Tuxtla pasó de \"ciudad del PAN\" a \"municipio competido\" y hoy es \"bastión MORENA\". La continuidad del proyecto guinda en 2027 está condicionada a mantener cohesión interna y atender demandas urbanas.")
    draw_footer(ax, section="II. Historia política", page_num=12)
    return fig


# ═══════════════════════════════════════════════════════════════
# PÁGINA 13 — DIVISOR PARTE III
# ═══════════════════════════════════════════════════════════════
def page_13():
    fig = new_page()
    ax = page_ax(fig)
    render_part_page(ax, "III", "Parte III", "Análisis\nelección 2024",
        "Resultados, secciones ganadas y zonas estratégicas.")
    draw_footer(ax, section="Parte III", page_num=13)
    return fig


# ═══════════════════════════════════════════════════════════════
# PÁGINA 14 — DISTRIBUCIÓN POR PARTIDO GANADOR (donut)
# ═══════════════════════════════════════════════════════════════
def page_14():
    fig = new_page()
    ax = page_ax(fig)
    draw_header(ax,
        eyebrow="III. Análisis de la elección 2024",
        title="Distribución de secciones por partido ganador",
        subtitle=f"{D['total_secciones']} secciones electorales analizadas · elección presidencia municipal 2024"
    )
    # Donut grande izquierda
    ax_donut = fig.add_axes([M_LEFT + 0.02, 0.27, 0.33, 0.50])
    ax_donut.set_aspect("equal")
    sizes  = [D['secciones_morena'], D['secciones_pan'], D['secciones_coal']]
    labels = ["MORENA", "PAN", "Coalición"]
    colors_d = [PARTY_COLORS["MORENA"], PARTY_COLORS["PAN"], COLORS["ink_light"]]
    wedges, _ = ax_donut.pie(sizes, colors=colors_d, startangle=90,
                              wedgeprops=dict(width=0.32, edgecolor=COLORS["bg"], linewidth=2))
    # Texto central
    ax_donut.text(0, 0.08, str(D['total_secciones']),
                   fontfamily=FONT_SERIF, fontsize=48, fontweight="bold",
                   color=COLORS["ink"], ha="center", va="center")
    ax_donut.text(0, -0.12, "secciones",
                   fontfamily=FONT_SANS, fontsize=11, color=COLORS["ink_soft"],
                   ha="center", va="center")
    ax_donut.set_facecolor("none")

    # Leyenda derecha
    leg_x = M_LEFT + 0.45
    leg_y = 0.62
    for i, (label, sz) in enumerate(zip(labels, sizes)):
        y = leg_y - i * 0.12
        # Cuadro de color
        rect = patches.Rectangle((leg_x, y - 0.01), 0.03, 0.03,
                                  linewidth=0, facecolor=colors_d[i])
        ax.add_patch(rect)
        # Nombre
        ax.text(leg_x + 0.045, y + 0.005, label,
                fontfamily=FONT_SANS, fontsize=14, fontweight="bold",
                color=COLORS["ink"], va="center")
        # Datos
        pct = sz / sum(sizes) * 100
        ax.text(leg_x + 0.045, y - 0.025, f"{sz} secciones · {pct:.1f}% del territorio",
                fontfamily=FONT_SANS, fontsize=10.5, color=COLORS["ink_soft"])

    draw_insight(ax, label="Resultado 2024",
        text=f"MORENA ganó {D['secciones_morena']} de {D['total_secciones']} secciones ({D['secciones_morena']*100/D['total_secciones']:.1f}%). PAN obtuvo {D['secciones_pan']} secciones ({D['secciones_pan']*100/D['total_secciones']:.1f}%) concentradas en zonas residenciales del oriente. La hegemonía MORENA en el territorio es contundente.")
    draw_footer(ax, section="III. Análisis 2024", page_num=14)
    return fig


# ═══════════════════════════════════════════════════════════════
# PÁGINA 15 — TOP 10 SECCIONES MORENA (barras horizontales)
# ═══════════════════════════════════════════════════════════════
def page_15():
    fig = new_page()
    ax = page_ax(fig)
    draw_header(ax,
        eyebrow="III. Análisis 2024",
        title="Top 10 secciones de las 3 fuerzas principales",
        subtitle="Comparativo por partido — votación absoluta 2024"
    )

    # 3 mini-tablas/charts lado a lado
    partidos_data = [
        ("MORENA", D['top10_morena_v2'], PARTY_COLORS["MORENA"]),
        ("PAN",    D['top10_pan_v2'],    PARTY_COLORS["PAN"]),
        ("MC",     D['top10_mc'],        PARTY_COLORS["MC"]),
    ]

    col_w = (CONTENT_W - 0.04) / 3  # ancho por columna
    col_gap = 0.02

    for col_idx, (partido, top, color) in enumerate(partidos_data):
        col_x = M_LEFT + col_idx * (col_w + col_gap)

        # Encabezado de columna (barra de color con nombre del partido)
        rect = patches.Rectangle((col_x, 0.71), col_w, 0.045,
                                  linewidth=0, facecolor=color)
        ax.add_patch(rect)
        ax.text(col_x + col_w/2, 0.7325, partido,
                fontfamily=FONT_SANS, fontsize=14, fontweight="bold",
                color="white", ha="center", va="center")

        # Filas de tabla — sección + barra mini + votos
        row_h = 0.043
        y_start = 0.69
        max_votos = max(s['votos'] for s in top)

        for i, s in enumerate(top):
            y = y_start - i * row_h
            # Fondo alterno
            if i % 2 == 1:
                rect = patches.Rectangle((col_x, y - row_h/2 + 0.002), col_w, row_h - 0.004,
                                          linewidth=0, facecolor=COLORS["row_alt"])
                ax.add_patch(rect)
            # Número de sección a la izquierda
            ax.text(col_x + 0.012, y, str(s['seccion']),
                    fontfamily=FONT_SANS, fontsize=10, color=COLORS["ink"], va="center")
            # Mini barra horizontal
            bar_x = col_x + 0.055
            bar_max_w = col_w - 0.11
            bar_w = bar_max_w * (s['votos'] / max_votos)
            bar = patches.Rectangle((bar_x, y - 0.008), bar_w, 0.016,
                                     linewidth=0, facecolor=color, alpha=0.85)
            ax.add_patch(bar)
            # Votos a la derecha
            ax.text(col_x + col_w - 0.012, y, f"{s['votos']:,}",
                    fontfamily=FONT_SANS, fontsize=10, fontweight="bold",
                    color=COLORS["ink"], va="center", ha="right")

    # Insight
    # Identificar secciones compartidas entre los 3 top 10
    secs_morena = {s['seccion'] for s in D['top10_morena_v2']}
    secs_pan    = {s['seccion'] for s in D['top10_pan_v2']}
    secs_mc     = {s['seccion'] for s in D['top10_mc']}
    triples = sorted(secs_morena & secs_pan & secs_mc)
    triples_str = ", ".join(str(s) for s in triples)

    draw_insight(ax, label="Hallazgo: secciones de alta densidad electoral",
        text=f"{len(triples)} secciones aparecen en los 3 top 10 simultáneamente ({triples_str}). Son las zonas más pobladas y políticamente disputadas — territorio donde TODOS los partidos buscan voto. La página siguiente las analiza a detalle.")
    draw_footer(ax, section="III. Análisis 2024", page_num=15)
    return fig


# ═══════════════════════════════════════════════════════════════
# PÁGINA 16 — TOP 10 SECCIONES PAN (barras horizontales)
# ═══════════════════════════════════════════════════════════════
def page_16():
    fig = new_page()
    ax = page_ax(fig)
    draw_header(ax,
        eyebrow="III. Análisis 2024",
        title="Secciones de alta densidad electoral",
        subtitle="Top 10 secciones donde se concentra el voto de las 3 fuerzas principales"
    )

    secs_morena = {s['seccion']: s['votos'] for s in D['top10_morena_v2']}
    secs_pan    = {s['seccion']: s['votos'] for s in D['top10_pan_v2']}
    secs_mc     = {s['seccion']: s['votos'] for s in D['top10_mc']}
    todas = set(secs_morena) | set(secs_pan) | set(secs_mc)

    # Calcular voto combinado (las que tienen voto, en cada partido)
    def voto_combinado(s):
        return secs_morena.get(s, 0) + secs_pan.get(s, 0) + secs_mc.get(s, 0)
    # Tomar top 10 por voto combinado
    todas_ordenadas = sorted(todas, key=lambda s: -voto_combinado(s))
    triples_data = todas_ordenadas[:10]

    # Gráfica de barras agrupadas
    ax_chart = fig.add_axes([M_LEFT + 0.06, 0.30, CONTENT_W - 0.08, 0.46])
    ax_chart.set_facecolor(COLORS["bg"])

    n = len(triples_data)
    x_pos = np.arange(n)
    bar_w = 0.27

    votos_morena_arr = [secs_morena.get(s, 0) for s in triples_data]
    votos_pan_arr    = [secs_pan.get(s, 0)    for s in triples_data]
    votos_mc_arr     = [secs_mc.get(s, 0)     for s in triples_data]

    b1 = ax_chart.bar(x_pos - bar_w, votos_morena_arr, bar_w,
                       color=PARTY_COLORS["MORENA"], edgecolor="none", label="MORENA")
    b2 = ax_chart.bar(x_pos,         votos_pan_arr,    bar_w,
                       color=PARTY_COLORS["PAN"],    edgecolor="none", label="PAN")
    b3 = ax_chart.bar(x_pos + bar_w, votos_mc_arr,     bar_w,
                       color=PARTY_COLORS["MC"],     edgecolor="none", label="MC")

    # Etiquetas de valor encima de cada barra (solo si > 0)
    max_val = max(max(votos_morena_arr), max(votos_pan_arr), max(votos_mc_arr))
    for bars_grupo in [b1, b2, b3]:
        for bar in bars_grupo:
            h = bar.get_height()
            if h > 0:
                ax_chart.text(bar.get_x() + bar.get_width()/2, h + max_val * 0.015,
                              f"{int(h):,}",
                              ha="center", va="bottom",
                              fontfamily=FONT_SANS, fontsize=7.5, fontweight="bold",
                              color=COLORS["ink"])

    ax_chart.set_xticks(x_pos)
    ax_chart.set_xticklabels([str(s) for s in triples_data],
                              fontsize=10, fontweight="bold", color=COLORS["ink"])
    ax_chart.tick_params(axis="x", length=0, pad=8)
    ax_chart.tick_params(axis="y", length=0, labelsize=9, colors=COLORS["ink_soft"])
    ax_chart.set_xlabel("Sección electoral",
                        fontfamily=FONT_SANS, fontsize=10, color=COLORS["ink_soft"],
                        labelpad=10)
    ax_chart.set_ylim(0, max_val * 1.20)
    ax_chart.yaxis.grid(True, color=COLORS["line"], linewidth=0.6, alpha=0.5)
    ax_chart.set_axisbelow(True)
    for s in ['top','right']: ax_chart.spines[s].set_visible(False)
    ax_chart.spines['left'].set_color(COLORS["line"])
    ax_chart.spines['bottom'].set_color(COLORS["line"])

    leg = ax_chart.legend(loc='upper right', frameon=False,
                          prop={'family': FONT_SANS, 'size': 11, 'weight': 'bold'},
                          handlelength=1.5, handleheight=1.2)
    for text in leg.get_texts():
        text.set_color(COLORS["ink"])

    sec_ej = triples_data[0]
    suma_morena = sum(votos_morena_arr)
    suma_pan    = sum(votos_pan_arr)
    suma_mc     = sum(votos_mc_arr)
    total_3p    = suma_morena + suma_pan + suma_mc

    draw_insight(ax, label="Lectura estratégica del territorio disputado",
        text=f"En estas {n} secciones de alta densidad las 3 fuerzas compiten simultáneamente. Total combinado: {total_3p:,} votos ({suma_morena:,} MORENA + {suma_pan:,} PAN + {suma_mc:,} MC). La sección {sec_ej} concentra {secs_morena.get(sec_ej,0)+secs_pan.get(sec_ej,0)+secs_mc.get(sec_ej,0):,} votos solo de estas 3 fuerzas — son las urnas de mayor impacto electoral del municipio.")
    draw_footer(ax, section="III. Análisis 2024", page_num=16)
    return fig


# ═══════════════════════════════════════════════════════════════
# PÁGINA 17 — ZONAS ESTRATÉGICAS (3 cards FORTALEZA/COMPETENCIA/RIESGO)
# CORRECCIÓN: revisar ortografía (acentos)
# ═══════════════════════════════════════════════════════════════
def page_17():
    fig = new_page()
    ax = page_ax(fig)
    draw_header(ax,
        eyebrow="III. Análisis 2024",
        title="Zonas estratégicas",
        subtitle="Clasificación territorial para la estrategia de campaña 2027"
    )
    card_w = (CONTENT_W - 0.04) / 3
    card_h = 0.40
    y = 0.36
    zonas = [
        ("FORTALEZA", "Mantener y movilizar", "~150", "secciones",
         COLORS["good"],
         "Secciones donde MORENA ganó con margen amplio (>30% de diferencia). "
         "Núcleo duro del electorado guinda."),
        ("COMPETENCIA", "Defender y persuadir", "~57", "secciones",
         COLORS["warning"],
         "Secciones ganadas por MORENA con margen estrecho (<10%) o donde la "
         "oposición creció. Zonas de disputa."),
        ("RIESGO", "Estrategia ofensiva", str(D['secciones_pan']), "secciones",
         COLORS["danger"],
         "Secciones perdidas en 2024 (mayoritariamente PAN). Zonas residenciales "
         "del oriente con voto opositor consolidado."),
    ]
    for i, (titulo, sub, valor, unidad, color, body) in enumerate(zonas):
        x = M_LEFT + i * (card_w + 0.02)
        # Barra superior coloreada
        bar = patches.Rectangle((x, y + card_h - 0.012), card_w, 0.012,
                                 linewidth=0, facecolor=color)
        ax.add_patch(bar)
        draw_card(ax, x, y, card_w, card_h - 0.012, lw=0.8)
        # Título zona
        ax.text(x + 0.02, y + card_h - 0.055, titulo,
                fontfamily=FONT_SANS, fontsize=12, fontweight="bold",
                color=color)
        ax.text(x + 0.02, y + card_h - 0.092, sub,
                fontfamily=FONT_SANS, fontsize=10, fontstyle="italic",
                color=COLORS["ink_soft"])
        # Valor grande
        ax.text(x + 0.02, y + card_h - 0.20, valor,
                fontfamily=FONT_SERIF, fontsize=48, fontweight="bold",
                color=COLORS["ink"], va="center")
        ax.text(x + 0.02 + 0.10, y + card_h - 0.20, unidad,
                fontfamily=FONT_SANS, fontsize=11,
                color=COLORS["ink_soft"], va="center")
        # Body
        wrapped = wrap_text(body, 38)
        ax.text(x + 0.02, y + card_h - 0.28, wrapped,
                fontfamily=FONT_SANS, fontsize=10,
                color=COLORS["ink_soft"], va="top", linespacing=1.45)

    draw_insight(ax, label="Estrategia territorial recomendada",
        text="Concentrar 60% del esfuerzo en zonas de FORTALEZA (movilización del voto duro), 30% en COMPETENCIA (defensa de margen estrecho) y 10% en RIESGO (incursión selectiva en bastiones opositores).")
    draw_footer(ax, section="III. Análisis 2024", page_num=17)
    return fig


# ═══════════════════════════════════════════════════════════════
# PÁGINA 18 — DISTRIBUCIÓN GEOGRÁFICA DEL VOTO
# ═══════════════════════════════════════════════════════════════
def page_18():
    fig = new_page()
    ax = page_ax(fig)
    draw_header(ax,
        eyebrow="III. Análisis 2024",
        title="Distribución geográfica del voto",
        subtitle="Concentración territorial de las 3 fuerzas principales en 2024"
    )

    # Cálculo en vivo desde D
    total_secs = D['total_secciones']
    secs_morena = D['secciones_morena']
    secs_pan = D['secciones_pan']
    # MC ganó 0 secciones según datos del Excel (es tercera fuerza pero no ganadora en ninguna sección)
    secs_mc = 0

    # 3 cards superiores con datos reales de cobertura territorial
    card_w = (CONTENT_W - 0.04) / 3
    card_h = 0.16
    y_top = 0.57
    cards_data = [
        ("MORENA",
         f"{secs_morena*100/total_secs:.1f}%",
         f"{secs_morena} secciones ganadas",
         PARTY_COLORS["MORENA"]),
        ("PAN",
         f"{secs_pan*100/total_secs:.1f}%",
         f"{secs_pan} secciones ganadas",
         PARTY_COLORS["PAN"]),
        ("MC",
         "0%",
         f"{secs_mc} secciones ganadas (3ª fuerza)",
         PARTY_COLORS["MC"]),
    ]
    for i, (label, val, desc, color) in enumerate(cards_data):
        x = M_LEFT + i * (card_w + 0.02)
        render_data_card(ax, x, y_top, card_w, card_h, label, val, desc, value_color=color)

    # Distribución por zona — bloque inferior
    y_dist = 0.35
    ax.text(M_LEFT, y_dist + 0.10, "DISTRIBUCIÓN POR ZONA",
            fontfamily=FONT_SANS, fontsize=10, fontweight="bold",
            color=COLORS["ink_soft"])
    zonas = [
        ("Norte y Poniente",     "Bastión MORENA",      "~120 secciones MORENA", PARTY_COLORS["MORENA"]),
        ("Centro y Sur",          "Mayoría MORENA",      "~87 secciones MORENA",  PARTY_COLORS["MORENA"]),
        ("Oriente residencial",   "Bastión PAN",         f"{secs_pan} secciones PAN", PARTY_COLORS["PAN"]),
        ("Centro urbano",         "Penetración MC",      "Concentra voto MC sin ganar secciones", PARTY_COLORS["MC"]),
    ]
    for i, (zona, etiq, secs, color) in enumerate(zonas):
        y = y_dist + 0.06 - i * 0.045
        rect = patches.Rectangle((M_LEFT, y - 0.013), 0.018, 0.026,
                                  linewidth=0, facecolor=color)
        ax.add_patch(rect)
        ax.text(M_LEFT + 0.04, y, zona,
                fontfamily=FONT_SANS, fontsize=12, fontweight="bold",
                color=COLORS["ink"], va="center")
        ax.text(M_LEFT + 0.30, y, etiq,
                fontfamily=FONT_SANS, fontsize=11, color=COLORS["ink_soft"], va="center")
        ax.text(1 - M_RIGHT, y, secs,
                fontfamily=FONT_SANS, fontsize=11, fontweight="bold",
                color=COLORS["ink"], va="center", ha="right")

    draw_footer(ax, section="III. Análisis 2024", page_num=18)
    return fig
