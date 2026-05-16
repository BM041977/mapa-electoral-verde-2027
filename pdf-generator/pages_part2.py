"""
pages_part2.py — Páginas 19 a 35 del PDF v2
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
    draw_card, draw_logo, wrap_text
)
from components import (
    render_part_page, render_numbered_card, render_data_card, render_table
)

with open('/home/claude/proyecto/datos_tuxtla.json') as f:
    D = json.load(f)


# ═══════════════════════════════════════════════════════════════
# PÁGINA 19 — DIVISOR PARTE IV
# ═══════════════════════════════════════════════════════════════
def page_19():
    fig = new_page()
    ax = page_ax(fig)
    render_part_page(ax, "IV", "Parte IV", "Listado nominal\ny proyecciones",
        "Evolución del padrón electoral y secciones de oportunidad.")
    draw_footer(ax, section="Parte IV", page_num=19)
    return fig


# ═══════════════════════════════════════════════════════════════
# PÁGINA 20 — EVOLUCIÓN DEL PADRÓN ELECTORAL (barras)
# ═══════════════════════════════════════════════════════════════
def page_20():
    fig = new_page()
    ax = page_ax(fig)
    draw_header(ax,
        eyebrow="IV. Listado nominal y proyecciones",
        title="Evolución del padrón electoral",
        subtitle="Tuxtla Gutiérrez 2015-2027 (proyectado)"
    )
    años  = [2015, 2018, 2021, 2024, 2027]
    valor = [D['listado_nominal'][str(a)] for a in años]
    # Colores: histórico ink_light, proyección accent (neutro, no MORENA)
    colors = [COLORS["ink_light"]] * 4 + [COLORS["accent"]]

    ax_chart = fig.add_axes([M_LEFT + 0.01, 0.275, CONTENT_W - 0.02, 0.48])
    ax_chart.set_facecolor(COLORS["bg"])
    x_pos = np.arange(len(años))
    bars = ax_chart.bar(x_pos, valor, color=colors, width=0.6, edgecolor="none")
    # La última barra (proyección) lleva patrón diagonal para diferenciarla
    bars[-1].set_hatch("///")
    bars[-1].set_edgecolor(COLORS["bg"])
    bars[-1].set_linewidth(0)
    for bar, v in zip(bars, valor):
        ax_chart.text(bar.get_x() + bar.get_width()/2, v + 10000, f"{v:,}",
                       ha="center", va="bottom",
                       fontfamily=FONT_SANS, fontsize=11, fontweight="bold",
                       color=COLORS["ink"])
    # Etiqueta PROYECCIÓN sobre la última barra
    ax_chart.text(4, valor[-1]/2, "PROYECCIÓN", ha="center", va="center",
                   fontfamily=FONT_SANS, fontsize=9, fontweight="bold",
                   color="#FFFFFF", rotation=90)
    ax_chart.set_xticks(x_pos)
    ax_chart.set_xticklabels(años, fontsize=12, fontweight="bold", color=COLORS["ink"])
    ax_chart.tick_params(axis="x", length=0, pad=8)
    ax_chart.set_yticks([100000, 200000, 300000, 400000, 500000])
    ax_chart.set_yticklabels(["100K","200K","300K","400K","500K"], fontsize=9, color=COLORS["ink_soft"])
    ax_chart.tick_params(axis="y", length=0)
    ax_chart.set_ylim(0, 540000)
    ax_chart.yaxis.grid(True, color=COLORS["line"], linewidth=0.6)
    ax_chart.set_axisbelow(True)
    for s in ax_chart.spines.values(): s.set_visible(False)

    crec_total = ((valor[-1] - valor[0]) / valor[0]) * 100
    draw_insight(ax, label="Crecimiento sostenido",
        text=f"El padrón crece +{crec_total:.0f}% en 12 años (2015-2027). En 2027 se esperan {valor[-1]:,} electores potenciales en Tuxtla — mercado electoral en expansión que demanda estrategia de captación temprana.")
    draw_footer(ax, section="IV. Listado nominal", page_num=20)
    return fig


# ═══════════════════════════════════════════════════════════════
# PÁGINA 21 — TOP 10 SECCIONES MÁS POBLADAS 2027 (tabla)
# ═══════════════════════════════════════════════════════════════
def page_21():
    fig = new_page()
    ax = page_ax(fig)
    draw_header(ax,
        eyebrow="IV. Listado nominal y proyecciones",
        title="Top 10 secciones más pobladas 2027",
        subtitle="Secciones con mayor listado nominal proyectado — máxima prioridad estratégica"
    )
    rows = []
    for i, s in enumerate(D['top10_pobladas']):
        rows.append([
            str(i+1),
            str(s['seccion']),
            f"{s['ln_2024']:,}",
            f"{s['ln_2027']:,}",
            f"+{s['crecimiento_pct']:.1f}%",
        ])
    render_table(ax,
        x=M_LEFT, y=0.27, w=CONTENT_W, h=0.49,
        headers=["#", "Sección", "LN 2024", "LN 2027 (proyectado)", "Crecimiento"],
        rows=rows,
        col_widths_frac=[0.08, 0.28, 0.20, 0.28, 0.16],
        highlight_cols=[4],
    )
    suma_top10 = sum(s['ln_2027'] for s in D['top10_pobladas'])
    pct_total = suma_top10 * 100 / D['listado_nominal']['2027']
    lider = D['top10_pobladas'][0]
    draw_insight(ax, label="Concentración geográfica",
        text=f"Las 10 secciones más pobladas concentran ~{suma_top10:,} electores ({pct_total:.0f}% del total municipal). Sección {lider['seccion']} lidera con {lider['ln_2027']:,} electores proyectados — prioridad #1 estratégica.")
    draw_footer(ax, section="IV. Listado nominal", page_num=21)
    return fig


# ═══════════════════════════════════════════════════════════════
# PÁGINA 22 — TOP 10 SECCIONES CON MAYOR CRECIMIENTO (tabla)
# ═══════════════════════════════════════════════════════════════
def page_22():
    fig = new_page()
    ax = page_ax(fig)
    draw_header(ax,
        eyebrow="IV. Listado nominal y proyecciones",
        title="Top 10 secciones con mayor crecimiento",
        subtitle="Crecimiento porcentual proyectado 2024-2027 — nuevos electores"
    )
    rows = []
    for i, s in enumerate(D['top10_creciendo']):
        rows.append([
            str(i+1),
            str(s['seccion']),
            f"{s['ln_2024']:,}",
            f"{s['ln_2027']:,}",
            f"+{s['nuevos_electores']:,}",
            f"+{s['crecimiento_pct']:.1f}%",
        ])
    render_table(ax,
        x=M_LEFT, y=0.27, w=CONTENT_W, h=0.49,
        headers=["#", "Sección", "LN 2024", "LN 2027", "Nuevos electores", "Crecimiento"],
        rows=rows,
        col_widths_frac=[0.07, 0.22, 0.16, 0.16, 0.22, 0.17],
        highlight_cols=[4, 5],
    )
    top3 = ", ".join([str(s['seccion']) for s in D['top10_creciendo'][:3]])
    rng_pct = (D['top10_creciendo'][2]['crecimiento_pct'], D['top10_creciendo'][0]['crecimiento_pct'])
    draw_insight(ax, label="Oportunidad estratégica",
        text=f"Secciones {top3} lideran crecimiento (+{rng_pct[0]:.0f}% a +{rng_pct[1]:.0f}%). Son zonas en desarrollo urbano con votantes jóvenes nuevos. Captarlos temprano es decisivo para 2027.")
    draw_footer(ax, section="IV. Listado nominal", page_num=22)
    return fig


# ═══════════════════════════════════════════════════════════════
# PÁGINA 23 — DIVISOR PARTE V
# CORRECCIÓN: revisar ortografía
# ═══════════════════════════════════════════════════════════════
def page_23():
    fig = new_page()
    ax = page_ax(fig)
    render_part_page(ax, "V", "Parte V", "Escenarios\n2027",
        "Tres proyecciones electorales y estrategia recomendada.")
    draw_footer(ax, section="Parte V", page_num=23)
    return fig


# ═══════════════════════════════════════════════════════════════
# Helper para páginas de escenario (24, 25, 26)
# ═══════════════════════════════════════════════════════════════
def _render_escenario(page_num, titulo, subtitulo, votos, pct_ln,
                       condiciones, recomendacion, color, section_label):
    fig = new_page()
    ax = page_ax(fig)
    draw_header(ax,
        eyebrow="V. Escenarios electorales 2027",
        title=titulo,
        subtitle=None,
    )
    # Layout: 2 cards lado a lado (votos / condiciones)
    card_w = (CONTENT_W - 0.04) / 2
    card_h = 0.42
    y = 0.32

    # Card izquierda: votos estimados
    draw_card(ax, M_LEFT, y, card_w, card_h, lw=0.8)
    ax.text(M_LEFT + card_w/2, y + card_h - 0.04, "VOTOS ESTIMADOS",
            fontfamily=FONT_SANS, fontsize=10, fontweight="bold",
            color=COLORS["ink_soft"], ha="center", va="top")
    # Subtítulo italic
    ax.text(M_LEFT + card_w/2, y + card_h - 0.08, subtitulo,
            fontfamily=FONT_SERIF, fontsize=12, fontstyle="italic",
            color=COLORS["ink_soft"], ha="center", va="top")
    # Número grande
    ax.text(M_LEFT + card_w/2, y + card_h/2 - 0.01, f"{votos:,}",
            fontfamily=FONT_SERIF, fontsize=68, fontweight="bold",
            color=color, ha="center", va="center")
    # % del listado nominal
    ax.text(M_LEFT + card_w/2, y + 0.08, f"{pct_ln}% del listado nominal",
            fontfamily=FONT_SERIF, fontsize=12, fontstyle="italic",
            color=COLORS["ink_soft"], ha="center")
    ax.text(M_LEFT + card_w/2, y + 0.04, "Participación estimada: ~70%",
            fontfamily=FONT_SANS, fontsize=10, color=COLORS["ink_light"],
            ha="center")

    # Card derecha: condiciones
    cx = M_LEFT + card_w + 0.04
    draw_card(ax, cx, y, card_w, card_h, lw=0.8)
    ax.text(cx + 0.02, y + card_h - 0.04, "CONDICIONES DEL ESCENARIO",
            fontfamily=FONT_SANS, fontsize=10, fontweight="bold",
            color=COLORS["ink_soft"], va="top")
    # Lista de condiciones
    cond_y = y + card_h - 0.10
    for i, cond in enumerate(condiciones):
        # Bullet
        ax.text(cx + 0.025, cond_y - i * 0.07, "•",
                fontfamily=FONT_SANS, fontsize=16, fontweight="bold",
                color=color, va="center")
        wrapped = wrap_text(cond, 42)
        ax.text(cx + 0.05, cond_y - i * 0.07, wrapped,
                fontfamily=FONT_SANS, fontsize=11, color=COLORS["ink"],
                va="center", linespacing=1.45)

    # Insight box con color del escenario
    draw_insight(ax, label="Estrategia recomendada",
        text=recomendacion, color=color)
    draw_footer(ax, section=section_label, page_num=page_num)
    return fig


# ═══════════════════════════════════════════════════════════════
# PÁGINA 24 — ESCENARIO BASE
# ═══════════════════════════════════════════════════════════════
def page_24():
    return _render_escenario(
        page_num=24,
        titulo="Escenario BASE",
        subtitulo="Escenario más probable — continuidad MORENA",
        votos=98500, pct_ln=30,
        condiciones=[
            "Participación electoral ~68% (similar a 2024)",
            "Voto MORENA estable en zonas fortaleza",
            "Sin coalición opositora articulada",
            "Continuidad de gestión municipal favorable",
        ],
        recomendacion="Mantener movilización de bases. Operación territorial sólida en 150 secciones de fortaleza. Defender 57 secciones en competencia con margen estrecho.",
        color=COLORS["accent"],
        section_label="V. Escenario BASE",
    )


# ═══════════════════════════════════════════════════════════════
# PÁGINA 25 — ESCENARIO FAVORABLE
# ═══════════════════════════════════════════════════════════════
def page_25():
    return _render_escenario(
        page_num=25,
        titulo="Escenario FAVORABLE",
        subtitulo="Crecimiento de voto MORENA sobre 2024",
        votos=115000, pct_ln=35,
        condiciones=[
            "Participación supera 70%",
            "Crecimiento en zonas residenciales",
            "Captación efectiva de nuevos electores",
            "Programa de gobierno bien recibido",
        ],
        recomendacion="Aprovechar tendencia favorable. Penetrar 20-25 secciones PAN en oriente. Consolidar liderazgo regional con miras a 2030.",
        color=COLORS["good"],
        section_label="V. Escenario FAVORABLE",
    )


# ═══════════════════════════════════════════════════════════════
# PÁGINA 26 — ESCENARIO DESFAVORABLE
# ═══════════════════════════════════════════════════════════════
def page_26():
    return _render_escenario(
        page_num=26,
        titulo="Escenario DESFAVORABLE",
        subtitulo="Riesgo de erosión de la base electoral",
        votos=82000, pct_ln=25,
        condiciones=[
            "Participación cae a ~60%",
            "Coalición opositora articulada (PAN-MC-PRI)",
            "Crisis interna de MORENA en Chiapas",
            "Crisis económica o social local",
        ],
        recomendacion="Defensa intensa. Activar redes de movilización inmediatas. Comunicación de crisis. Riesgo de pérdida de 30-40 secciones en zonas de competencia.",
        color=COLORS["danger"],
        section_label="V. Escenario DESFAVORABLE",
    )


# ═══════════════════════════════════════════════════════════════
# PÁGINA 27 — ESTRATEGIA RECOMENDADA (4 filas distribución %)
# ═══════════════════════════════════════════════════════════════
def page_27():
    fig = new_page()
    ax = page_ax(fig)
    draw_header(ax,
        eyebrow="V. Escenarios electorales 2027",
        title="Estrategia recomendada",
        subtitle="Distribución óptima del esfuerzo de campaña según escenarios"
    )
    items = [
        ("MOVILIZAR",    "Fortaleza MORENA — Mantener voto duro",        "60%", COLORS["good"]),
        ("DEFENDER",     "Competencia — Evitar pérdida por margen estrecho", "25%", COLORS["warning"]),
        ("INCURSIONAR",  "Riesgo — Penetración selectiva PAN",            "10%", COLORS["danger"]),
        ("PROYECTAR",    "Nuevos electores — Captación temprana",         "5%",  PARTY_COLORS["PAN"]),
    ]
    card_h = 0.105
    gap = 0.018
    y_start = 0.70
    for i, (label, sub, pct, color) in enumerate(items):
        y = y_start - i * (card_h + gap)
        draw_card(ax, M_LEFT, y - card_h, CONTENT_W, card_h, lw=0.8)
        # Label
        ax.text(M_LEFT + 0.025, y - 0.03, label,
                fontfamily=FONT_SANS, fontsize=14, fontweight="bold",
                color=color, va="center")
        # Sublabel
        ax.text(M_LEFT + 0.025, y - 0.065, sub,
                fontfamily=FONT_SANS, fontsize=10.5, fontstyle="italic",
                color=COLORS["ink_soft"], va="center")
        # Porcentaje grande a la derecha
        ax.text(1 - M_RIGHT - 0.025, y - card_h/2, pct,
                fontfamily=FONT_SERIF, fontsize=52, fontweight="bold",
                color=color, va="center", ha="right")

    draw_insight(ax, label="Recomendación final",
        text="Concentrar 85% del esfuerzo en mantener y defender el voto MORENA actual. Invertir 15% en estrategia de crecimiento futuro (jóvenes y nuevos electores).")
    draw_footer(ax, section="V. Escenarios 2027", page_num=27)
    return fig


# ═══════════════════════════════════════════════════════════════
# PÁGINA 28 — DIVISOR PARTE VI
# ═══════════════════════════════════════════════════════════════
def page_28():
    fig = new_page()
    ax = page_ax(fig)
    render_part_page(ax, "VII", "Parte VII", "Conclusiones\ny recomendaciones",
        "Síntesis estratégica y plan de acción para 2027.")
    draw_footer(ax, section="Parte VII", page_num=39)
    return fig


# ═══════════════════════════════════════════════════════════════
# PÁGINA 29 — CONCLUSIONES ESTRATÉGICAS (5 cards numerados verticales)
# ═══════════════════════════════════════════════════════════════
def page_29():
    fig = new_page()
    ax = page_ax(fig)
    draw_header(ax,
        eyebrow="VII. Conclusiones y recomendaciones",
        title="Conclusiones estratégicas",
        subtitle=None
    )
    pct_morena = D['secciones_morena']*100/D['total_secciones']
    cards = [
        ("01", "BASTIÓN CONSOLIDADO",
         f"MORENA mantiene hegemonía en Tuxtla con 3 victorias consecutivas (2018-2024) y {pct_morena:.0f}% de secciones ganadas en 2024."),
        ("02", "PADRÓN EN CRECIMIENTO",
         f"Listado nominal proyectado a {D['listado_nominal']['2027']:,} electores en 2027 (+{D['crecimiento_ln_2024_2027_pct']}% vs 2024). {D['secciones_crecen']} secciones crecen, {D['secciones_decrecen']} decrecen."),
        ("03", "OPOSICIÓN MULTIPARTIDISTA",
         f"PAN ({D['top3_oposicion'][0]['votos']:,} votos), MC ({D['top3_oposicion'][1]['votos']:,}) y PRI ({D['top3_oposicion'][2]['votos']:,}) conforman las 3 fuerzas opositoras. PAN concentrado en oriente residencial."),
        ("04", "PARTICIPACIÓN AL ALZA",
         "Participación 2024 alcanzó 68.2% — récord histórico. Tendencia favorable para consolidación electoral."),
        ("05", "OPORTUNIDAD EN NUEVOS ELECTORES",
         "~15,000 nuevos electores esperados entre 2024-2027. Concentrados en secciones de crecimiento urbano (2017, 2022, 1748)."),
    ]
    card_h = 0.087
    gap = 0.013
    y_start = 0.72
    for i, (num, title, body) in enumerate(cards):
        y = y_start - i * (card_h + gap)
        render_numbered_card(ax, M_LEFT, y - card_h, CONTENT_W, card_h, num, title, body, body_chars=110)

    draw_footer(ax, section="VII. Conclusiones", page_num=40)
    return fig


# ═══════════════════════════════════════════════════════════════
# PÁGINA 30 — RECOMENDACIONES OPERATIVAS (6 cards 2x3)
# ═══════════════════════════════════════════════════════════════
def page_30():
    fig = new_page()
    ax = page_ax(fig)
    draw_header(ax,
        eyebrow="VII. Conclusiones y recomendaciones",
        title="Recomendaciones operativas",
        subtitle="Plan de acción priorizado para campaña 2027"
    )
    recs = [
        ("TERRITORIAL", "Mantener movilización en las 150 secciones de fortaleza MORENA. Establecer estructura de representantes por sección."),
        ("JÓVENES",     "Diseñar programa específico para nuevos electores (~15K esperados). Concentrar en secciones de crecimiento urbano."),
        ("DEFENSIVA",   "Reforzar presencia en 57 secciones de competencia con margen estrecho. Riesgo de pérdida si no se atiende oportunamente."),
        ("OFENSIVA",    "Incursionar selectivamente en zonas residenciales del oriente (56 secciones PAN) con propuesta económica diferenciada."),
        ("NARRATIVA",   "Construir narrativa de continuidad del proyecto MORENA, con énfasis en gestión local y resultados visibles del trienio 2024-2027."),
        ("OPERACIÓN",   f"Capacitar {D['total_casillas']} representantes de casilla. Establecer protocolos PREP/cómputo para evitar disputas postelectorales."),
    ]
    card_w = (CONTENT_W - 0.04) / 3
    card_h = 0.22
    for i, (label, body) in enumerate(recs):
        row = i // 3
        col = i % 3
        x = M_LEFT + col * (card_w + 0.02)
        y = 0.54 - row * (card_h + 0.02)
        draw_card(ax, x, y, card_w, card_h, lw=0.8)
        # Label color accent
        ax.text(x + 0.018, y + card_h - 0.025, label,
                fontfamily=FONT_SANS, fontsize=11, fontweight="bold",
                color=COLORS["accent"], va="top")
        # Línea separadora
        ax.plot([x + 0.018, x + 0.05], [y + card_h - 0.045, y + card_h - 0.045],
                color=COLORS["accent"], linewidth=1.5)
        # Body
        wrapped = wrap_text(body, 38)
        ax.text(x + 0.018, y + card_h - 0.065, wrapped,
                fontfamily=FONT_SANS, fontsize=10,
                color=COLORS["ink_soft"], va="top", linespacing=1.45)

    draw_footer(ax, section="VII. Recomendaciones", page_num=41)
    return fig


# ═══════════════════════════════════════════════════════════════
# PÁGINA 31 — PLAN DE ACCIÓN PRIORIZADO (4 fases cronológicas)
# ═══════════════════════════════════════════════════════════════
def page_31():
    fig = new_page()
    ax = page_ax(fig)
    draw_header(ax,
        eyebrow="VII. Conclusiones y recomendaciones",
        title="Plan de acción priorizado",
        subtitle="Roadmap operativo de campaña — 12 meses previos a elección"
    )
    fases = [
        ("Q3 2026", "PRE-CAMPAÑA",  "Estructura territorial · Coordinadores por sección · Diagnóstico base de electores · Construcción de base de datos"),
        ("Q4 2026", "CONSTRUCCIÓN", "Reuniones vecinales · Identificación de líderes locales · Operadores barriales · Mapeo de demandas ciudadanas"),
        ("Q1 2027", "ARRANQUE",     "Posicionamiento del candidato · Programa de gobierno · Lanzamiento de campaña · Definición de coalición partidista"),
        ("Q2 2027", "CAMPAÑA",      "Recorridos territoriales · Eventos masivos · Defensa de propuestas · Cierre y jornada electoral"),
    ]
    card_h = 0.11
    gap = 0.018
    y_start = 0.72
    for i, (quarter, fase, body) in enumerate(fases):
        y = y_start - i * (card_h + gap)
        draw_card(ax, M_LEFT, y - card_h, CONTENT_W, card_h, lw=0.8)
        # Quarter pequeño
        ax.text(M_LEFT + 0.025, y - 0.025, quarter,
                fontfamily=FONT_SANS, fontsize=10, fontweight="bold",
                color=COLORS["ink_light"], va="top")
        # Fase
        ax.text(M_LEFT + 0.025, y - 0.058, fase,
                fontfamily=FONT_SANS, fontsize=14, fontweight="bold",
                color=PARTY_COLORS["MORENA"], va="center")
        # Body
        wrapped = wrap_text(body, 100)
        ax.text(M_LEFT + 0.20, y - card_h/2, wrapped,
                fontfamily=FONT_SANS, fontsize=10.5,
                color=COLORS["ink_soft"], va="center", linespacing=1.5)

    draw_footer(ax, section="VII. Plan de acción", page_num=42)
    return fig


# ═══════════════════════════════════════════════════════════════
# PÁGINA 32 — CALENDARIO ELECTORAL 2026-2027 (timeline vertical)
# ═══════════════════════════════════════════════════════════════
def page_32():
    fig = new_page()
    ax = page_ax(fig)
    draw_header(ax,
        eyebrow="VII. Conclusiones y recomendaciones",
        title="Calendario electoral 2026-2027",
        subtitle="Hitos clave del proceso electoral local Chiapas 2027"
    )
    hitos = [
        ("Octubre 2026",  "Inicio del proceso electoral local",     "IEPC instala consejos distritales y municipales"),
        ("Diciembre 2026","Registro de candidaturas",                "Plazo de registro ante partidos políticos"),
        ("Enero 2027",    "Aprobación de candidaturas",              "Resolución del IEPC"),
        ("Febrero 2027",  "Inicio de campañas",                       "60 días de campaña electoral"),
        ("Mayo 2027",     "Jornada electoral",                        "6 de junio (probable)"),
        ("Junio 2027",    "Cómputos y entrega de constancias",       "Validación oficial de resultados"),
        ("Octubre 2027",  "Toma de protesta",                         "Inicio del nuevo gobierno municipal"),
    ]
    row_h = 0.085
    y_start = 0.72
    for i, (fecha, hito, desc) in enumerate(hitos):
        y = y_start - i * row_h
        # Punto en timeline
        circle = patches.Circle((M_LEFT + 0.018, y), 0.012,
                                  linewidth=0, facecolor=PARTY_COLORS["MORENA"])
        ax.add_patch(circle)
        # Línea vertical (excepto último)
        if i < len(hitos) - 1:
            ax.plot([M_LEFT + 0.018, M_LEFT + 0.018], [y - 0.012, y - row_h + 0.012],
                    color=COLORS["line"], linewidth=2)
        # Fecha
        ax.text(M_LEFT + 0.05, y, fecha,
                fontfamily=FONT_SANS, fontsize=11, fontweight="bold",
                color=PARTY_COLORS["MORENA"], va="center")
        # Hito
        ax.text(M_LEFT + 0.22, y + 0.012, hito,
                fontfamily=FONT_SERIF, fontsize=14, fontweight="bold",
                color=COLORS["ink"], va="center")
        # Desc
        ax.text(M_LEFT + 0.22, y - 0.015, desc,
                fontfamily=FONT_SANS, fontsize=10, fontstyle="italic",
                color=COLORS["ink_soft"], va="center")

    draw_footer(ax, section="VII. Calendario electoral", page_num=43)
    return fig


# ═══════════════════════════════════════════════════════════════
# PÁGINA 33 — DIVISOR PARTE VII
# ═══════════════════════════════════════════════════════════════
def page_33():
    fig = new_page()
    ax = page_ax(fig)
    render_part_page(ax, "VIII", "Parte VIII", "Anexos\ny metodología",
        "Fuentes, metodología utilizada y glosario electoral.")
    draw_footer(ax, section="Parte VIII", page_num=44)
    return fig


# ═══════════════════════════════════════════════════════════════
# PÁGINA 34 — METODOLOGÍA Y FUENTES
# ═══════════════════════════════════════════════════════════════
def page_34():
    fig = new_page()
    ax = page_ax(fig)
    draw_header(ax,
        eyebrow="VIII. Anexos y metodología",
        title="Metodología y fuentes",
        subtitle=None
    )
    secciones = [
        ("FUENTES DE DATOS",
         "El presente análisis se construyó sobre las siguientes fuentes oficiales:",
         [
            "Instituto Electoral y de Participación Ciudadana de Chiapas (IEPC)",
            "Instituto Nacional Electoral (INE) — Listado Nominal y Padrón Electoral",
            "Resultados electorales históricos del Sistema PREP 1998-2024",
            "Censo Nacional de Población y Vivienda 2020 (INEGI)",
            "Base de datos propia de BaldemarMaza — Inteligencia Electoral",
         ]),
        ("METODOLOGÍA DE PROYECCIÓN 2027",
         "Las proyecciones del listado nominal 2027 se calcularon mediante:",
         [
            "Análisis de tendencias históricas 2015-2024 (4 elecciones)",
            "Modelo de crecimiento poblacional INEGI-CONAPO",
            "Ajustes por densidad de desarrollo urbano por sección",
            "Validación cruzada con datos de empadronamiento INE",
         ]),
        ("LIMITACIONES Y SUPUESTOS",
         None,
         [
            "Proyecciones sujetas a actualización con datos preelectorales 2027",
            "Modelos asumen continuidad de tendencias demográficas observadas",
            "Análisis territorial basado en información disponible al cierre 2024",
         ]),
    ]
    y = 0.75
    for label, intro, items in secciones:
        # Label
        ax.text(M_LEFT, y, label,
                fontfamily=FONT_SANS, fontsize=11, fontweight="bold",
                color=COLORS["accent"], va="top")
        y -= 0.035
        if intro:
            ax.text(M_LEFT, y, intro,
                    fontfamily=FONT_SANS, fontsize=10.5,
                    color=COLORS["ink_soft"], va="top")
            y -= 0.030
        for item in items:
            ax.text(M_LEFT + 0.015, y, "•",
                    fontfamily=FONT_SANS, fontsize=11, fontweight="bold",
                    color=COLORS["ink_soft"], va="top")
            wrapped = wrap_text(item, 110)
            ax.text(M_LEFT + 0.030, y, wrapped,
                    fontfamily=FONT_SANS, fontsize=10.5,
                    color=COLORS["ink"], va="top", linespacing=1.45)
            y -= 0.028 + (wrapped.count('\n') * 0.020)
        y -= 0.018

    draw_footer(ax, section="VIII. Metodología", page_num=45)
    return fig


# ═══════════════════════════════════════════════════════════════
# PÁGINA 35 — CONTRAPORTADA
# CORRECCIÓN: usar logo real (no texto "BaldemarMaza.com")
# ═══════════════════════════════════════════════════════════════
def page_35():
    fig = new_page()
    ax = page_ax(fig)
    # Logo grande arriba (igual que portada)
    draw_logo(ax, 0.5, 0.78, width=0.30)

    # Línea decorativa
    ax.plot([0.45, 0.55], [0.62, 0.62], color=COLORS["ink"], linewidth=2.5)

    # Bloque CONTACTO
    ax.text(0.5, 0.55, "CONTACTO",
            fontfamily=FONT_SANS, fontsize=11, fontweight="bold",
            color=COLORS["ink_soft"], ha="center")
    ax.text(0.5, 0.49, "Baldemar Maza León",
            fontfamily=FONT_SERIF, fontsize=28, fontweight="bold",
            color=COLORS["ink"], ha="center", va="center")
    ax.text(0.5, 0.42, "Consultoría & Capacitación Empresarial",
            fontfamily=FONT_SERIF, fontsize=14, fontstyle="italic",
            color=COLORS["ink_soft"], ha="center")

    # Datos de contacto
    ax.text(0.5, 0.33, "baldemarmaza@gmail.com",
            fontfamily=FONT_SANS, fontsize=13,
            color=COLORS["ink"], ha="center")
    ax.text(0.5, 0.29, "961 217 0091",
            fontfamily=FONT_SANS, fontsize=13,
            color=COLORS["ink"], ha="center")

    # Banda inferior con aviso de derechos
    rect = patches.Rectangle((0, 0), 1, 0.10, linewidth=0, facecolor=COLORS["accent"])
    ax.add_patch(rect)
    ax.text(0.5, 0.05,
            "Queda prohibida la reproducción total o parcial sin el consentimiento expreso del autor.",
            fontfamily=FONT_SERIF, fontsize=11, fontstyle="italic",
            color="#FFFFFF", ha="center", va="center")
    return fig
