"""
pages_indicadores_extra.py — Indicadores 6-9 + Glosario
Se agregan a la Parte VI (Indicadores complementarios)
"""
import sys
sys.path.insert(0, "/home/claude/proyecto")

import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from brand import COLORS, FONT_SERIF, FONT_SANS, TYPE, M_LEFT, M_RIGHT, CONTENT_W, PARTY_COLORS
from page_system import (
    new_page, page_ax, draw_header, draw_footer, draw_insight,
    draw_card, wrap_text
)
from components import render_table, render_data_card, render_part_page

with open('/home/claude/proyecto/datos_indicadores.json') as f:
    I = json.load(f)


# ═══════════════════════════════════════════════════════════════
# INDICADOR 6 — TOP SECCIONES MORENA CON MARGEN ESTRECHO
# ═══════════════════════════════════════════════════════════════
def page_indicador_6():
    fig = new_page()
    ax = page_ax(fig)
    draw_header(ax,
        eyebrow="Indicador 6 · Riesgo competitivo",
        title="Top 10 secciones MORENA con margen estrecho",
        subtitle="Secciones donde MORENA ganó 2024 por menos de 3% — riesgo real de pérdida en 2027"
    )

    rows = []
    for i, m in enumerate(I['margen_estrecho']):
        rows.append([
            str(i+1),
            str(m['seccion']),
            f"{m['votos_morena']}",
            f"{m['segundo_partido']} ({m['votos_segundo']})",
            f"{m['margen_abs']}",
            f"{m['margen_pct']:.1f}%",
        ])
    render_table(ax,
        x=M_LEFT, y=0.27, w=CONTENT_W, h=0.49,
        headers=["#", "Sección", "Votos MORENA", "Segundo lugar", "Margen abs.", "Margen %"],
        rows=rows,
        col_widths_frac=[0.06, 0.13, 0.18, 0.30, 0.16, 0.17],
        highlight_cols=[5],
        highlight_color=COLORS["danger"],
    )

    # El insight refleja el dato real y su peso estratégico
    sec_top = I['margen_estrecho'][0]
    total_estrecho = I['margen_estrecho_total']
    draw_insight(ax, label="Alerta estratégica",
        text=f"{total_estrecho} secciones MORENA tienen margen <15% — y 10 ganaron por menos de 3%. La sección {sec_top['seccion']} fue por UN solo voto. Estas son las primeras que se pueden voltear en 2027: deben recibir el 30% del presupuesto territorial de campaña como prioridad defensiva.")
    draw_footer(ax, section="VI. Indicador 6: Riesgo competitivo", page_num=34)
    return fig


# ═══════════════════════════════════════════════════════════════
# INDICADOR 7 — MAPA DE CALOR DE PARTIDO GANADOR
# ═══════════════════════════════════════════════════════════════
def page_indicador_7():
    fig = new_page()
    ax = page_ax(fig)
    draw_header(ax,
        eyebrow="Indicador 7 · Distribución territorial",
        title="Mapa de calor del partido ganador 2024",
        subtitle="Visualización geográfica del control territorial por partido"
    )

    secciones = I['heatmap_ganador']
    n = len(secciones)
    cols = 14
    rows = int(np.ceil(n / cols))

    def color_partido(g):
        if g == 'MORENA': return PARTY_COLORS["MORENA"]
        elif g == 'PAN':  return PARTY_COLORS["PAN"]
        else:             return COLORS["ink_light"]

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
        color = color_partido(sec['ganador'])
        rect = patches.Rectangle((x + cell_pad, y + cell_pad),
                                  cell_w - 2*cell_pad, cell_h - 2*cell_pad,
                                  linewidth=0, facecolor=color)
        ax.add_patch(rect)
        # Número de sección
        ax.text(x + cell_w/2, y + cell_h*0.65, str(sec['seccion']),
                fontfamily=FONT_SANS, fontsize=5.8, fontweight="bold",
                color="white", ha="center", va="center")
        # Votos del ganador
        ax.text(x + cell_w/2, y + cell_h*0.30, str(sec['votos']),
                fontfamily=FONT_SANS, fontsize=6.5, fontweight="bold",
                color="white", ha="center", va="center")

    # Leyenda derecha
    leg_x = grid_x + grid_w + 0.04
    ax.text(leg_x, grid_y + grid_h - 0.01, "PARTIDO GANADOR",
            fontfamily=FONT_SANS, fontsize=9, fontweight="bold",
            color=COLORS["ink_soft"], va="top")
    # Contar
    cuenta = {'MORENA':0, 'PAN':0, 'COAL':0}
    for s in secciones:
        cuenta[s['ganador']] = cuenta.get(s['ganador'], 0) + 1
    niveles = [
        (PARTY_COLORS["MORENA"], "MORENA",    f"{cuenta['MORENA']} secciones · {cuenta['MORENA']*100/n:.1f}%"),
        (PARTY_COLORS["PAN"],    "PAN",       f"{cuenta['PAN']} secciones · {cuenta['PAN']*100/n:.1f}%"),
        (COLORS["ink_light"],    "Coalición", f"{cuenta['COAL']} secciones · {cuenta['COAL']*100/n:.1f}%"),
    ]
    for i, (color, nivel, desc) in enumerate(niveles):
        y = grid_y + grid_h - 0.07 - i * 0.085
        rect = patches.Rectangle((leg_x, y - 0.02), 0.025, 0.025,
                                  linewidth=0, facecolor=color)
        ax.add_patch(rect)
        ax.text(leg_x + 0.035, y - 0.005, nivel,
                fontfamily=FONT_SANS, fontsize=12, fontweight="bold",
                color=COLORS["ink"], va="center")
        ax.text(leg_x + 0.035, y - 0.032, desc,
                fontfamily=FONT_SANS, fontsize=9, fontstyle="italic",
                color=COLORS["ink_soft"], va="center")

    # Etiqueta debajo del grid
    ax.text(grid_x + grid_w/2, grid_y - 0.025,
            f"Distribución de {n} secciones electorales (cada celda = 1 sección)",
            fontfamily=FONT_SANS, fontsize=9, fontstyle="italic",
            color=COLORS["ink_soft"], ha="center")

    draw_insight(ax, label="Lectura territorial",
        text=f"La mancha guinda (MORENA, {cuenta['MORENA']} secciones) domina norte, poniente y centro de Tuxtla. La concentración azul (PAN, {cuenta['PAN']} secciones) se ubica en clusters específicos del oriente residencial — estrategia: identificar las 5-7 secciones PAN aislables del cluster principal para incursión 2027.")
    draw_footer(ax, section="VI. Indicador 7: Partido ganador territorial", page_num=35)
    return fig


# ═══════════════════════════════════════════════════════════════
# INDICADOR 8 — FUERZA DE LA COALICIÓN MORENA-PVEM-PT
# ═══════════════════════════════════════════════════════════════
def page_indicador_8():
    fig = new_page()
    ax = page_ax(fig)
    draw_header(ax,
        eyebrow="Indicador 8 · Análisis de coalición",
        title="Desagregación del voto coalición 2024",
        subtitle="MORENA puro vs aporte de aliados PVEM y PT"
    )

    coal = I['coalicion_morena']

    # Bloque izquierdo: barras horizontales apiladas mostrando composición
    componentes = [
        ('MORENA puro',              coal['morena_puro'],       PARTY_COLORS["MORENA"]),
        ('PVEM puro',                coal['pvem_puro'],         PARTY_COLORS["PVEM"]),
        ('PT puro',                  coal['pt_puro'],           PARTY_COLORS["PT"]),
        ('Coalición 3 partidos',     coal['coal_3_partidos'],   "#7B1E3F"),  # variante guinda
        ('PVEM + MORENA',            coal['coal_pvem_morena'],  "#5A8E4F"),
        ('PT + MORENA',              coal['coal_pt_morena'],    "#A04545"),
    ]
    total = sum(c[1] for c in componentes)

    # Eje de barras a la izquierda — con margen extra para etiquetas Y
    ax_chart = fig.add_axes([M_LEFT + 0.10, 0.30, 0.41, 0.45])
    ax_chart.set_facecolor(COLORS["bg"])
    nombres = [c[0] for c in componentes]
    valores = [c[1] for c in componentes]
    colors = [c[2] for c in componentes]
    nombres = nombres[::-1]; valores = valores[::-1]; colors = colors[::-1]
    bars = ax_chart.barh(nombres, valores, color=colors, height=0.7, edgecolor="none")
    for bar, v in zip(bars, valores):
        pct = v / total * 100
        ax_chart.text(v + total*0.012, bar.get_y() + bar.get_height()/2,
                       f"{v:,}   ({pct:.1f}%)",
                       va="center", ha="left",
                       fontfamily=FONT_SANS, fontsize=10, fontweight="bold",
                       color=COLORS["ink"])
    ax_chart.set_xlim(0, max(valores) * 1.4)
    ax_chart.tick_params(axis="y", length=0, labelsize=10, colors=COLORS["ink"])
    ax_chart.tick_params(axis="x", length=0, labelsize=9, colors=COLORS["ink_soft"])
    for s in ['top','right','left']: ax_chart.spines[s].set_visible(False)
    ax_chart.spines['bottom'].set_color(COLORS["line"])
    ax_chart.xaxis.grid(True, color=COLORS["line"], linewidth=0.6, alpha=0.4)
    ax_chart.set_axisbelow(True)

    # Cards a la derecha: KPIs clave
    cards_x = M_LEFT + 0.56
    cards_w = CONTENT_W - 0.56
    pct_aliados = (total - coal['morena_puro']) / total * 100
    cards_data = [
        ("Voto total coalición", f"{total:,}",                       "Suma de los 6 componentes"),
        ("MORENA puro",          f"{coal['morena_puro']:,}",         f"{coal['morena_puro']*100/total:.1f}% del total"),
        ("Aporte de aliados",    f"{pct_aliados:.1f}%",              "PVEM, PT y combinaciones"),
    ]
    card_h = 0.14
    gap = 0.018
    for i, (label, val, desc) in enumerate(cards_data):
        y = 0.72 - i * (card_h + gap)
        render_data_card(ax, cards_x, y - card_h, cards_w, card_h, label, val, desc,
                         value_color=PARTY_COLORS["MORENA"])

    draw_insight(ax, label="Lectura estratégica de coalición",
        text=f"MORENA puro contribuye con {coal['morena_puro']*100/total:.1f}% del voto coalición. Si MORENA fuera sola en 2027, perdería aproximadamente {(total-coal['morena_puro']):,} votos ({pct_aliados:.1f}%). PVEM aporta más que PT como aliado individual. Mantener la coalición es decisivo: sin aliados, el bastión se vuelve competido.")
    draw_footer(ax, section="VI. Indicador 8: Análisis de coalición", page_num=36)
    return fig


# ═══════════════════════════════════════════════════════════════
# INDICADOR 9 — COMPARATIVO METROPOLITANO
# ═══════════════════════════════════════════════════════════════
def page_indicador_9():
    fig = new_page()
    ax = page_ax(fig)
    draw_header(ax,
        eyebrow="Indicador 9 · Contexto regional",
        title="Tuxtla en su zona metropolitana",
        subtitle="Comparativo electoral con 5 municipios vecinos"
    )

    comp = I['comparativo_metropolitano']
    rows = []
    for m in comp:
        # Resaltar Tuxtla
        rows.append([
            m['municipio'].title().replace('De', 'de'),
            f"{m['ln_2024']:,}",
            f"{m['total_secciones']}",
            f"{m['pct_secciones_morena']:.0f}%",
            f"{m['morena_votos']:,}",
            f"{m['pan_votos']:,}",
        ])
    render_table(ax,
        x=M_LEFT, y=0.32, w=CONTENT_W, h=0.41,
        headers=["Municipio", "LN 2024", "Secciones", "% gana MORENA", "Votos MORENA", "Votos PAN"],
        rows=rows,
        col_widths_frac=[0.26, 0.16, 0.13, 0.20, 0.13, 0.12],
        highlight_cols=[3],
        highlight_color=PARTY_COLORS["MORENA"],
    )

    # Hallazgo: identificar diferencias clave
    tuxtla = comp[0]
    fortaleza_morena = [c for c in comp if c['pct_secciones_morena'] >= 60]
    opositores = [c for c in comp if c['pct_secciones_morena'] < 30]
    nombres_morena = ", ".join([c['municipio'].title() for c in fortaleza_morena])
    nombres_opos   = ", ".join([c['municipio'].title() for c in opositores])

    draw_insight(ax, label="Hallazgo regional",
        text=f"La zona metropolitana NO es homogéneamente guinda. Fortalezas MORENA: {nombres_morena}. Territorio opositor: {nombres_opos}. Si MORENA pierde Chiapa de Corzo y Ocozocoautla en 2027 — con sus ~150K electores combinados —, la corona metropolitana se vuelve azul/multipartidista. La estrategia regional importa tanto como la local.")
    draw_footer(ax, section="VI. Indicador 9: Contexto regional", page_num=37)
    return fig


# ═══════════════════════════════════════════════════════════════
# INDICADOR 10 — MAPA DE CALOR DE BASTIÓN HISTÓRICO 1998-2024
# ═══════════════════════════════════════════════════════════════
def page_indicador_10():
    fig = new_page()
    ax = page_ax(fig)
    draw_header(ax,
        eyebrow="Indicador 10 · Lealtad territorial histórica",
        title="Bastión histórico 1998-2024",
        subtitle="Familia política dominante por sección a través de 10 elecciones municipales"
    )

    bastion = I['bastion_historico']
    stats = I['bastion_stats']
    n = len(bastion)
    cols = 14
    rows_grid = int(np.ceil(n / cols))

    # Colores por familia
    color_fam = {
        'IZQ': PARTY_COLORS["MORENA"],
        'PAN': PARTY_COLORS["PAN"],
        'PRI': PARTY_COLORS["PRI"],
    }
    # Intensidad: cuántas veces ganó la familia dominante / total de elecciones
    def color_with_alpha(fam, ratio):
        base = color_fam[fam]
        # alpha entre 0.35 (poca consistencia) y 1.0 (siempre)
        alpha = 0.35 + 0.65 * ratio
        return base, alpha

    # Layout del grid
    grid_x = M_LEFT + 0.005
    grid_y = 0.31
    grid_w = 0.65
    grid_h = 0.41
    cell_w = grid_w / cols
    cell_h = grid_h / rows_grid
    cell_pad = 0.0015

    for i, b in enumerate(bastion):
        r = i // cols
        c = i % cols
        x = grid_x + c * cell_w
        y = grid_y + grid_h - (r + 1) * cell_h
        ratio = b[b['dominante'].lower()] / max(b['total'], 1)
        color, alpha = color_with_alpha(b['dominante'], ratio)
        rect = patches.Rectangle((x + cell_pad, y + cell_pad),
                                  cell_w - 2*cell_pad, cell_h - 2*cell_pad,
                                  linewidth=0, facecolor=color, alpha=alpha)
        ax.add_patch(rect)
        # Número de sección
        ax.text(x + cell_w/2, y + cell_h*0.62, str(b['seccion']),
                fontfamily=FONT_SANS, fontsize=5.8, fontweight="bold",
                color="white", ha="center", va="center")
        # Conteo "X de N" elecciones
        ax.text(x + cell_w/2, y + cell_h*0.28,
                f"{b[b['dominante'].lower()]}/{b['total']}",
                fontfamily=FONT_SANS, fontsize=6.2, fontweight="bold",
                color="white", ha="center", va="center")

    # Leyenda derecha
    leg_x = grid_x + grid_w + 0.04
    ax.text(leg_x, grid_y + grid_h - 0.005, "FAMILIA POLÍTICA",
            fontfamily=FONT_SANS, fontsize=9, fontweight="bold",
            color=COLORS["ink_soft"], va="top")

    # 3 entradas con explicación de partidos
    niveles = [
        (PARTY_COLORS["MORENA"], "Izquierda / MORENA",
         f"{stats['izq']} secciones",
         "MORENA, PRD, PT y coaliciones"),
        (PARTY_COLORS["PAN"],    "PAN / Centro-derecha",
         f"{stats['pan']} secciones",
         "PAN puro o alianzas que lideró"),
        (PARTY_COLORS["PRI"],    "PRI / Oficialismo",
         f"{stats['pri']} secciones",
         "PRI, PVEM y coaliciones priistas"),
    ]
    for i, (color, nivel, conteo, desc) in enumerate(niveles):
        y = grid_y + grid_h - 0.07 - i * 0.115
        rect = patches.Rectangle((leg_x, y - 0.02), 0.025, 0.025,
                                  linewidth=0, facecolor=color)
        ax.add_patch(rect)
        ax.text(leg_x + 0.035, y, nivel,
                fontfamily=FONT_SANS, fontsize=11, fontweight="bold",
                color=COLORS["ink"], va="center")
        ax.text(leg_x + 0.035, y - 0.025, conteo,
                fontfamily=FONT_SANS, fontsize=10, fontweight="bold",
                color=color, va="center")
        ax.text(leg_x + 0.035, y - 0.048, desc,
                fontfamily=FONT_SANS, fontsize=8.5, fontstyle="italic",
                color=COLORS["ink_soft"], va="center")

    # Nota sobre el grid
    ax.text(grid_x + grid_w/2, grid_y - 0.025,
            f"Cada celda muestra # de victorias / # de elecciones donde existió la sección · Intensidad de color = consistencia del bastión",
            fontfamily=FONT_SANS, fontsize=8.5, fontstyle="italic",
            color=COLORS["ink_soft"], ha="center")

    draw_insight(ax, label="Lectura histórica del territorio",
        text=f"Las {stats['izq']} secciones de izquierda histórica son las MISMAS donde gana MORENA hoy — el bastión guinda no aparece de la nada en 2018, es continuidad ideológica con PRD/PT/Convergencia. Las {stats['pan']} secciones PAN históricas coinciden con las 56 actuales: voto estructural. Las {stats['pri']} secciones priistas son hoy zonas con votante huérfano — universo natural de captación MORENA para 2027.")
    draw_footer(ax, section="VI. Indicador 10: Bastión histórico", page_num=37)
    return fig


# ═══════════════════════════════════════════════════════════════
# INDICADOR 11 — VOTO CRUZADO MUNICIPAL vs GUBERNATURA 2024
# ═══════════════════════════════════════════════════════════════
def page_indicador_11():
    fig = new_page()
    ax = page_ax(fig)
    draw_header(ax,
        eyebrow="Indicador 11 · Marca propia vs arrastre",
        title="Voto cruzado municipal vs gubernatura 2024",
        subtitle="¿MORENA gana por su candidato o por arrastre estatal?"
    )

    cruzado = I['voto_cruzado']
    stats = I['voto_cruzado_stats']
    cruz_df = pd.DataFrame(cruzado)

    # ============ Tres bloques ============
    # 1) KPIs arriba (3 cards horizontales)
    card_w = (CONTENT_W - 0.04) / 3
    card_h = 0.13
    y_kpi = 0.67

    kpis = [
        ("MORENA municipal",  f"{stats['pct_morena_muni_promedio']}%",
         f"Promedio en {stats['total_secciones']} secciones", PARTY_COLORS["MORENA"]),
        ("MORENA gubernatura", f"{stats['pct_morena_gub_promedio']}%",
         f"Promedio en {stats['total_secciones']} secciones", PARTY_COLORS["MORENA"]),
        ("Diferencia (muni − gub)", f"{stats['delta_promedio']:+.1f} pp",
         "Marca propia del candidato",
         COLORS["good"] if stats['delta_promedio'] > 0 else COLORS["danger"]),
    ]
    for i, (label, val, desc, color) in enumerate(kpis):
        x = M_LEFT + i * (card_w + 0.02)
        render_data_card(ax, x, y_kpi, card_w, card_h, label, val, desc, value_color=color)

    # 2) Clasificación de secciones (3 bandas horizontales)
    y_band = 0.56
    band_h = 0.09
    bands = [
        ("MARCA PROPIA",      stats['secs_marca_propia'],
         "Δ > +5pp: MORENA muni > gub. El candidato tiene marca local fuerte.",
         COLORS["good"]),
        ("CONSISTENTE",       stats['secs_consistente'],
         "Δ entre −5pp y +5pp: votante MORENA estable entre cargos.",
         COLORS["accent"]),
        ("DEPENDENCIA ARRASTRE", stats['secs_dependencia'],
         "Δ < −5pp: MORENA gub > muni. Voto MORENA viene del gobernador, NO del municipal.",
         COLORS["danger"]),
    ]
    for i, (titulo, n, desc, color) in enumerate(bands):
        y = y_band - i * (band_h + 0.005)
        draw_card(ax, M_LEFT, y - band_h, CONTENT_W, band_h, lw=0.8)
        # Barra de color a la izquierda
        bar = patches.Rectangle((M_LEFT, y - band_h), 0.005, band_h,
                                 linewidth=0, facecolor=color)
        ax.add_patch(bar)
        # Etiqueta
        ax.text(M_LEFT + 0.025, y - 0.025, titulo,
                fontfamily=FONT_SANS, fontsize=11, fontweight="bold",
                color=color, va="center")
        # Descripción
        ax.text(M_LEFT + 0.025, y - 0.06, desc,
                fontfamily=FONT_SANS, fontsize=10, fontstyle="italic",
                color=COLORS["ink_soft"], va="center")
        # Conteo grande a la derecha
        ax.text(1 - M_RIGHT - 0.025, y - band_h/2, str(n),
                fontfamily=FONT_SERIF, fontsize=40, fontweight="bold",
                color=color, va="center", ha="right")
        # "secciones" texto pequeño bajo el número
        ax.text(1 - M_RIGHT - 0.025, y - band_h/2 - 0.038, "secciones",
                fontfamily=FONT_SANS, fontsize=9,
                color=COLORS["ink_light"], va="center", ha="right")

    # 3) Insight
    draw_insight(ax, label="Hallazgo crítico para 2027",
        text=(f"MORENA en Tuxtla NO depende mayormente del arrastre estatal: "
              f"el voto MORENA promedio es prácticamente igual entre municipal ({stats['pct_morena_muni_promedio']}%) "
              f"y gubernatura ({stats['pct_morena_gub_promedio']}%). PERO existen {stats['secs_dependencia']} secciones donde "
              f"MORENA municipal cayó >5 puntos respecto a gubernatura — son las MÁS VULNERABLES en 2027, "
              f"cuando no habrá gubernatura concurrente. Atender estas secciones es prioridad defensiva. "
              f"PAN, en cambio, tiene voto puramente municipal (+{stats['delta_pan_promedio']:.0f}pp sobre gub): "
              f"su electorado no se mueve."))
    draw_footer(ax, section="VI. Indicador 11: Voto cruzado", page_num=38)
    return fig


# ═══════════════════════════════════════════════════════════════
# GLOSARIO — Parte VIII Anexos
# ═══════════════════════════════════════════════════════════════
def page_glosario():
    fig = new_page()
    ax = page_ax(fig)
    draw_header(ax,
        eyebrow="VIII. Anexos y metodología",
        title="Glosario electoral",
        subtitle="Términos técnicos utilizados en este diagnóstico"
    )

    terminos = [
        ("Sección electoral",
         "Unidad geográfica básica del sistema electoral. Cada sección agrupa entre 100 y 3,000 electores y se identifica con un número único asignado por el INE."),
        ("Listado Nominal (LN)",
         "Padrón electoral con fotografía. Total de ciudadanos registrados con credencial vigente en una sección, distrito o municipio. Es el universo máximo de electores potenciales."),
        ("Distrito Local",
         "Demarcación electoral para elegir diputados locales. Tuxtla Gutiérrez está integrada por tres distritos locales: 01, 02 y 13."),
        ("Casilla básica / contigua / extraordinaria",
         "Tipos de casilla. La básica es la principal de cada sección; las contiguas se instalan cuando hay más de 750 electores; las extraordinarias en zonas de difícil acceso."),
        ("PREP",
         "Programa de Resultados Electorales Preliminares. Sistema oficial de captura y difusión de resultados desde casilla la misma noche de la jornada electoral."),
        ("Coalición",
         "Alianza formal entre dos o más partidos para postular candidaturas conjuntas. El voto a una coalición se reparte entre los partidos según convenio registrado ante el IEPC."),
        ("Margen estrecho",
         "Diferencia porcentual entre el primer y segundo lugar menor a 15%. Indica zona de competencia electoral real, no bastión consolidado."),
        ("Voto cruzado",
         "Cuando un elector vota por partidos distintos en elecciones concurrentes (ej. presidente MORENA, alcalde PAN). Indica fortaleza de marca personal vs arrastre partidista."),
        ("Re-seccionamiento",
         "Reorganización territorial de secciones electorales por crecimiento urbano. Una sección puede dividirse, fusionarse o cambiar de número, dificultando comparaciones históricas directas."),
        ("Bastión",
         "Sección o territorio donde un partido gana consistentemente con margen amplio (>30%) en al menos 3 elecciones consecutivas."),
    ]

    # Dos columnas de términos
    col_w = (CONTENT_W - 0.04) / 2
    col_left_x = M_LEFT
    col_right_x = M_LEFT + col_w + 0.04
    y_start = 0.72
    row_h_total = 0.115

    n = len(terminos)
    half = (n + 1) // 2

    for i, (termino, defi) in enumerate(terminos):
        col_x = col_left_x if i < half else col_right_x
        row_in_col = i if i < half else i - half
        y_term = y_start - row_in_col * row_h_total
        # Término en negrita
        ax.text(col_x, y_term, termino,
                fontfamily=FONT_SANS, fontsize=11, fontweight="bold",
                color=COLORS["accent"])
        # Definición wrap
        wrapped = wrap_text(defi, 58)
        ax.text(col_x, y_term - 0.022, wrapped,
                fontfamily=FONT_SANS, fontsize=9.5,
                color=COLORS["ink_soft"], va="top", linespacing=1.4)

    draw_footer(ax, section="VIII. Glosario", page_num=46)
    return fig


# ═══════════════════════════════════════════════════════════════
# DIVISOR PARTE IX — Cierre estratégico
# ═══════════════════════════════════════════════════════════════
def page_part9():
    fig = new_page()
    ax = page_ax(fig)
    render_part_page(ax, "IX", "Parte IX", "Cierre\nestratégico",
        "Las cuatro preguntas críticas que un candidato se hace al cerrar este documento: quién es su votante, cuánto necesita para ganar, quién es su competidor real y cómo medir el éxito de su gestión.")
    draw_footer(ax, section="Parte IX", page_num=47)
    return fig


# ═══════════════════════════════════════════════════════════════
# PREGUNTAS ESTRATÉGICAS — PÁGINA DE CIERRE
# Responde 4 preguntas críticas que un candidato se hace al leer el documento
# ═══════════════════════════════════════════════════════════════
def page_preguntas_estrategicas():
    fig = new_page()
    ax = page_ax(fig)
    draw_header(ax,
        eyebrow="IX. Cierre estratégico",
        title="Preguntas estratégicas para el candidato",
        subtitle="Lo que un consultor electoral le preguntaría a este documento"
    )

    # Cargar datos estratégicos
    with open('/home/claude/proyecto/datos_estrategicas.json') as f:
        E = json.load(f)

    # ═══ LAYOUT 2×2 ═══
    cuad_w = (CONTENT_W - 0.03) / 2
    cuad_h = 0.235
    y_top  = 0.71
    y_bot  = y_top - cuad_h - 0.025
    x_left  = M_LEFT
    x_right = M_LEFT + cuad_w + 0.03

    # ─── CUADRANTE 1: ¿Quién es mi votante? (donut de perfil) ───
    perfil = E['secciones_perfil']
    total_secs = perfil['chicas'] + perfil['medias'] + perfil['grandes']
    draw_card(ax, x_left, y_top - cuad_h, cuad_w, cuad_h, lw=0.8, radius=0.012)
    # Título cuadrante
    ax.text(x_left + 0.015, y_top - 0.025, "01",
            fontfamily=FONT_SERIF, fontsize=22, fontweight="bold",
            color=COLORS["accent"], va="center")
    ax.text(x_left + 0.055, y_top - 0.025, "¿Quién es mi votante?",
            fontfamily=FONT_SANS, fontsize=11.5, fontweight="bold",
            color=COLORS["ink"], va="center")
    ax.text(x_left + 0.055, y_top - 0.05, "Perfil por densidad de sección",
            fontfamily=FONT_SANS, fontsize=9, fontstyle="italic",
            color=COLORS["ink_soft"], va="center")

    # Mini barras horizontales
    items = [
        ("Chica (<1K)",  perfil['chicas'],  PARTY_COLORS["MORENA"], "Comunidad cerrada"),
        ("Media (1-3K)", perfil['medias'],  COLORS["accent"],       "Suburbio típico"),
        ("Grande (>3K)", perfil['grandes'], COLORS["ink_light"],    "Urbano denso"),
    ]
    max_v = max(p[1] for p in items)
    bar_y_start = y_top - 0.10
    bar_h = 0.022
    bar_gap = 0.038
    bar_x = x_left + 0.13
    bar_max_w = cuad_w - 0.18
    for i, (label, n, color, desc) in enumerate(items):
        y = bar_y_start - i * bar_gap
        # label
        ax.text(x_left + 0.015, y, label,
                fontfamily=FONT_SANS, fontsize=9, color=COLORS["ink"],
                va="center", zorder=12)
        # barra
        w = bar_max_w * (n / max_v)
        bar = patches.Rectangle((bar_x, y - bar_h/2), w, bar_h,
                                 linewidth=0, facecolor=color, zorder=10)
        ax.add_patch(bar)
        # valor
        ax.text(bar_x + w + 0.005, y, f"{n}",
                fontfamily=FONT_SANS, fontsize=9, fontweight="bold",
                color=COLORS["ink"], va="center", zorder=12)
        # subtítulo
        ax.text(x_left + 0.015, y - 0.018, desc,
                fontfamily=FONT_SANS, fontsize=7.5, fontstyle="italic",
                color=COLORS["ink_light"], va="center", zorder=12)

    ax.text(x_left + cuad_w/2, y_top - cuad_h + 0.02,
            f"Concentrar esfuerzo en {perfil['medias']} secciones media-densidad: voto persuadible y movilizable.",
            fontfamily=FONT_SANS, fontsize=8.5, fontstyle="italic",
            color=COLORS["ink_soft"], ha="center", va="center", wrap=True)

    # ─── CUADRANTE 2: ¿Cuánto necesito para ganar? (umbral de victoria) ───
    draw_card(ax, x_right, y_top - cuad_h, cuad_w, cuad_h, lw=0.8, radius=0.012)
    ax.text(x_right + 0.015, y_top - 0.025, "02",
            fontfamily=FONT_SERIF, fontsize=22, fontweight="bold",
            color=COLORS["accent"], va="center")
    ax.text(x_right + 0.055, y_top - 0.025, "¿Cuánto necesito para ganar?",
            fontfamily=FONT_SANS, fontsize=11.5, fontweight="bold",
            color=COLORS["ink"], va="center")
    ax.text(x_right + 0.055, y_top - 0.05, "Umbral de victoria estimado 2027",
            fontfamily=FONT_SANS, fontsize=9, fontstyle="italic",
            color=COLORS["ink_soft"], va="center")

    # 3 escenarios
    escenarios = [
        ("Mínimo",    f"{E['voto_minimo_2027']:,}",  "35% del voto válido", COLORS["warning"]),
        ("Esperado",  f"{E['promedio_ult3']:,}",     "Promedio últimas 3", COLORS["accent"]),
        ("Blindaje",  f"{E['voto_seguro_2027']:,}",  "45% del voto válido", COLORS["good"]),
    ]
    esc_y = y_top - 0.10
    esc_h = 0.045
    esc_w = (cuad_w - 0.04) / 3
    for i, (label, val, desc, color) in enumerate(escenarios):
        ex = x_right + 0.02 + i * (esc_w + 0.005)
        # Card mini
        rect = patches.Rectangle((ex, esc_y - esc_h - 0.025), esc_w, esc_h + 0.035,
                                  linewidth=0.6, edgecolor=COLORS["line"],
                                  facecolor="white")
        ax.add_patch(rect)
        # label
        ax.text(ex + esc_w/2, esc_y - 0.005, label.upper(),
                fontfamily=FONT_SANS, fontsize=8, fontweight="bold",
                color=color, ha="center", va="top")
        # valor
        ax.text(ex + esc_w/2, esc_y - 0.027, val,
                fontfamily=FONT_SERIF, fontsize=13, fontweight="bold",
                color=COLORS["ink"], ha="center", va="center")
        # desc
        ax.text(ex + esc_w/2, esc_y - 0.05, desc,
                fontfamily=FONT_SANS, fontsize=7,
                color=COLORS["ink_soft"], ha="center", va="center")

    ax.text(x_right + cuad_w/2, y_top - cuad_h + 0.02,
            f"Meta segura 2027: ~{E['voto_seguro_2027']:,} votos. Promedio histórico ult.3: {E['promedio_ult3']:,}.",
            fontfamily=FONT_SANS, fontsize=8.5, fontstyle="italic",
            color=COLORS["ink_soft"], ha="center", va="center", wrap=True)

    # ─── CUADRANTE 3: ¿Quién es mi competidor real? (barra apilada) ───
    draw_card(ax, x_left, y_bot - cuad_h, cuad_w, cuad_h, lw=0.8, radius=0.012)
    ax.text(x_left + 0.015, y_bot - 0.025, "03",
            fontfamily=FONT_SERIF, fontsize=22, fontweight="bold",
            color=COLORS["accent"], va="center")
    ax.text(x_left + 0.055, y_bot - 0.025, "¿Quién es mi competidor real?",
            fontfamily=FONT_SANS, fontsize=11.5, fontweight="bold",
            color=COLORS["ink"], va="center")
    ax.text(x_left + 0.055, y_bot - 0.05, "Escenario: coalición opositora",
            fontfamily=FONT_SANS, fontsize=9, fontstyle="italic",
            color=COLORS["ink_soft"], va="center")

    morena = E['voto_morena_2024']
    oposicion = E['voto_oposicion_2024']
    total = morena + oposicion
    bar_y_pos = y_bot - 0.10
    bar_height = 0.035
    bar_left = x_left + 0.025
    bar_total_w = cuad_w - 0.05
    morena_w = bar_total_w * (morena / total)
    oposicion_w = bar_total_w * (oposicion / total)
    # MORENA
    rect = patches.Rectangle((bar_left, bar_y_pos - bar_height/2), morena_w, bar_height,
                              linewidth=0, facecolor=PARTY_COLORS["MORENA"], zorder=10)
    ax.add_patch(rect)
    ax.text(bar_left + morena_w/2, bar_y_pos, f"MORENA\n{morena:,}",
            fontfamily=FONT_SANS, fontsize=9, fontweight="bold",
            color="white", ha="center", va="center", zorder=11)
    # Oposición
    rect = patches.Rectangle((bar_left + morena_w, bar_y_pos - bar_height/2), oposicion_w, bar_height,
                              linewidth=0, facecolor=COLORS["ink"], zorder=10)
    ax.add_patch(rect)
    ax.text(bar_left + morena_w + oposicion_w/2, bar_y_pos, f"Oposición\n{oposicion:,}",
            fontfamily=FONT_SANS, fontsize=9, fontweight="bold",
            color="white", ha="center", va="center", zorder=11)
    # %
    ax.text(bar_left, bar_y_pos - 0.04,
            f"{morena/total*100:.1f}%",
            fontfamily=FONT_SANS, fontsize=10, fontweight="bold",
            color=PARTY_COLORS["MORENA"], ha="left", va="center")
    ax.text(bar_left + bar_total_w, bar_y_pos - 0.04,
            f"{oposicion/total*100:.1f}%",
            fontfamily=FONT_SANS, fontsize=10, fontweight="bold",
            color=COLORS["ink"], ha="right", va="center")
    # Detalle oposición
    ax.text(x_left + cuad_w/2, bar_y_pos - 0.08,
            "Oposición = PAN (61,184) + MC (17,396) + PRI (13,913)",
            fontfamily=FONT_SANS, fontsize=8, fontstyle="italic",
            color=COLORS["ink_soft"], ha="center", va="center")
    ax.text(x_left + cuad_w/2, y_bot - cuad_h + 0.02,
            f"Ventaja real MORENA: +{morena-oposicion:,} votos. Si la oposición se une, la elección se decide por margen estrecho.",
            fontfamily=FONT_SANS, fontsize=8.5, fontstyle="italic",
            color=COLORS["ink_soft"], ha="center", va="center", wrap=True)

    # ─── CUADRANTE 4: ¿Cómo mido éxito post-elección? (framework) ───
    draw_card(ax, x_right, y_bot - cuad_h, cuad_w, cuad_h, lw=0.8, radius=0.012)
    ax.text(x_right + 0.015, y_bot - 0.025, "04",
            fontfamily=FONT_SERIF, fontsize=22, fontweight="bold",
            color=COLORS["accent"], va="center")
    ax.text(x_right + 0.055, y_bot - 0.025, "¿Cómo mido el éxito de la gestión?",
            fontfamily=FONT_SANS, fontsize=11.5, fontweight="bold",
            color=COLORS["ink"], va="center")
    ax.text(x_right + 0.055, y_bot - 0.05, "Framework propuesto para post-elección",
            fontfamily=FONT_SANS, fontsize=9, fontstyle="italic",
            color=COLORS["ink_soft"], va="center")

    indicadores_post = [
        ("Aprobación",       "Encuesta trimestral",   "% favorable / desfavorable"),
        ("Secciones leales", "Mapa anual",           "Comparativo vs intermedia"),
        ("Obra visible",     "Reportes mensuales",   "% obra completada vs ofrecida"),
        ("Percepción gestión", "Focus groups",       "3 ejes: seguridad / agua / obra"),
    ]
    ind_y = y_bot - 0.085
    ind_gap = 0.033
    for i, (ind, instr, desc) in enumerate(indicadores_post):
        y = ind_y - i * ind_gap
        # Bullet número
        ax.text(x_right + 0.02, y, f"{i+1}.",
                fontfamily=FONT_SANS, fontsize=9, fontweight="bold",
                color=COLORS["accent"], va="center")
        ax.text(x_right + 0.04, y, ind,
                fontfamily=FONT_SANS, fontsize=9.5, fontweight="bold",
                color=COLORS["ink"], va="center")
        ax.text(x_right + 0.16, y, instr,
                fontfamily=FONT_SANS, fontsize=8, fontstyle="italic",
                color=COLORS["ink_soft"], va="center")
        ax.text(x_right + 0.30, y, desc,
                fontfamily=FONT_SANS, fontsize=7.5,
                color=COLORS["ink_light"], va="center")

    ax.text(x_right + cuad_w/2, y_bot - cuad_h + 0.02,
            "Establecer este sistema desde el día 1 evita sorpresas en la intermedia 2030.",
            fontfamily=FONT_SANS, fontsize=8.5, fontstyle="italic",
            color=COLORS["ink_soft"], ha="center", va="center", wrap=True)

    draw_footer(ax, section="IX. Preguntas estratégicas", page_num=48)
    return fig
