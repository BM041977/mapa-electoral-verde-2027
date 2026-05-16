"""
build_pdf.py — Orquestador: genera las 35 páginas y arma el PDF v2
"""
import sys, os
sys.path.insert(0, "/home/claude/proyecto")

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

from brand import COLORS
import pages_part1 as P1
import pages_part2 as P2
import pages_indicadores as PI
import pages_indicadores_extra as PIE

OUT_PDF = "/home/claude/proyecto/Diagnostico_Electoral_Tuxtla_v8.pdf"
PREVIEW_DIR = "/home/claude/proyecto/preview_v8"
os.makedirs(PREVIEW_DIR, exist_ok=True)

# Mapa página → función
# Estructura: 8 partes. Indicadores en Parte VI (28-37, ahora 10 indicadores en lugar de 5)
PAGES = [
    # Páginas 1-4: portada, sub-portada, índice, resumen ejecutivo
    (1,  P1.page_01), (2,  P1.page_02), (3,  P1.page_03), (4,  P1.page_04),
    # Parte I — Contexto territorial (5-7)
    (5,  P1.page_05), (6,  P1.page_06), (7,  P1.page_07),
    # Parte II — Historia política (8-12)
    (8,  P1.page_08), (9,  P1.page_09), (10, P1.page_10), (11, P1.page_11), (12, P1.page_12),
    # Parte III — Análisis 2024 (13-18)
    (13, P1.page_13), (14, P1.page_14), (15, P1.page_15), (16, P1.page_16),
    (17, P1.page_17), (18, P1.page_18),
    # Parte IV — Listado nominal (19-22)
    (19, P2.page_19), (20, P2.page_20), (21, P2.page_21), (22, P2.page_22),
    # Parte V — Escenarios 2027 (23-27)
    (23, P2.page_23), (24, P2.page_24), (25, P2.page_25), (26, P2.page_26),
    (27, P2.page_27),
    # Parte VI — Indicadores complementarios (28-37) — 10 indicadores (sin el comparativo metropolitano)
    (28, PI.page_part8),               # Divisor Parte VI
    (29, PI.page_indicador_1),         # Mapa calor participación
    (30, PI.page_indicador_2),         # Sparklines
    (31, PI.page_indicador_3),         # Crecimiento poblacional
    (32, PI.page_indicador_4),         # Coaliciones timeline
    (33, PI.page_indicador_5),         # Radar
    (34, PIE.page_indicador_6),        # Margen estrecho
    (35, PIE.page_indicador_7),        # Mapa partido ganador 2024
    (36, PIE.page_indicador_8),        # Análisis coalición
    # — eliminado: (37, PIE.page_indicador_9) Comparativo metropolitano —
    (37, PIE.page_indicador_10),       # Bastión histórico 1998-2024
    (38, PIE.page_indicador_11),       # Voto cruzado muni vs gub
    # Parte VII — Conclusiones (39-43)
    (39, P2.page_28),
    (40, P2.page_29),
    (41, P2.page_30),
    (42, P2.page_31),
    (43, P2.page_32),
    # Parte VIII — Anexos (44-46)
    (44, P2.page_33),                  # Divisor
    (45, P2.page_34),                  # Metodología
    (46, PIE.page_glosario),           # Glosario
    # Parte IX — Cierre estratégico (47-48)
    (47, PIE.page_part9),              # NUEVO: Divisor Parte IX
    (48, PIE.page_preguntas_estrategicas),
    # Contraportada
    (49, P2.page_35),
]

PREVIEW_PAGES = {3, 47, 48, 49}

print(f"Generando {len(PAGES)} páginas...")
with PdfPages(OUT_PDF) as pdf:
    for num, fn in PAGES:
        fig = fn()
        pdf.savefig(fig, facecolor=COLORS["bg"], bbox_inches=None)
        if num in PREVIEW_PAGES:
            fig.savefig(f"{PREVIEW_DIR}/p{num:02d}.png",
                        dpi=140, facecolor=COLORS["bg"], bbox_inches=None)
        plt.close(fig)
        print(f"  ✓ Página {num:02d}")

print(f"\n✓ PDF generado: {OUT_PDF}")
print(f"  Tamaño: {os.path.getsize(OUT_PDF):,} bytes")
