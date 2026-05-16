"""
brand.py — Sistema de marca BaldemarMaza.com
Paleta de colores, tipografías y constantes de layout.
"""

# ─────────────────────────────────────────────────────────────────
# PALETA DE MARCA (no cambiar)
# ─────────────────────────────────────────────────────────────────
COLORS = {
    "bg":         "#FBF9F4",   # fondo crema
    "card":       "#FFFFFF",   # blanco
    "ink":        "#1A1A1A",   # tinta principal
    "ink_soft":   "#5A5A5A",   # tinta secundaria
    "ink_light":  "#888888",   # tinta clara
    "line":       "#E8E4DC",   # líneas/bordes
    "accent":     "#2D2D2D",   # acento grafito (para insight box)
    "good":       "#16A34A",   # verde positivo
    "warning":    "#D97706",   # naranja atención
    "danger":     "#B91C1C",   # rojo riesgo
    "row_alt":    "#F5F2EC",   # fila alterna en tablas
}

# ─────────────────────────────────────────────────────────────────
# COLORES PARTIDISTAS OFICIALES (NUNCA cambiar)
# ─────────────────────────────────────────────────────────────────
PARTY_COLORS = {
    "MORENA":  "#8B1E3F",  # guinda
    "PVEM":    "#00A65A",  # verde
    "PT":      "#D32F2F",  # rojo oscuro
    "PAN":     "#0066CC",  # azul
    "PRI":     "#E53935",  # rojo
    "MC":      "#FF8C00",  # naranja
    "PRD":     "#FFD600",  # amarillo
    "PCHU":    "#4FC3F7",  # celeste
    "PMCH":    "#6A1B9A",  # morado
    "RSP":     "#757575",  # gris
    "PES":     "#9C27B0",  # violeta
    "PPCH":    "#80CBC4",  # turquesa pálido
    "FXM":     "#EC407A",  # rosa
    "COAL":    "#888888",  # gris neutro para coaliciones
    "UNIDAD":  "#FF7043",  # naranja-rojo
}

# ─────────────────────────────────────────────────────────────────
# TIPOGRAFÍA
# ─────────────────────────────────────────────────────────────────
FONT_SERIF = "Lora"             # títulos editorial
FONT_SANS  = "Liberation Sans"  # cuerpo de texto y datos

# Escala tipográfica (en puntos)
TYPE = {
    "eyebrow":   10,   # texto pequeño mayúsculas arriba del título
    "h1":        38,   # título grande de página
    "h2":        24,   # título de sección
    "h3":        16,   # subtítulo
    "subtitle":  14,   # bajada italic
    "body":      11,   # cuerpo principal
    "small":     9,    # texto fino
    "footer":    8.5,  # texto del footer
    "insight_label": 9, # etiqueta del insight box
    "insight_text":  11, # texto del insight box
    "big_number":    72, # números enormes (cards de escenario)
    "card_label":    9,  # etiqueta de card
    "card_value":    20, # valor numérico en card
}

# ─────────────────────────────────────────────────────────────────
# DIMENSIONES DE PÁGINA
# Formato horizontal tipo presentación editorial
# ─────────────────────────────────────────────────────────────────
PAGE_W = 13.33  # pulgadas (1280 px @ 96 dpi)
PAGE_H = 10.0   # pulgadas (960 px @ 96 dpi)

# Márgenes (fracción del área total)
M_LEFT   = 0.065
M_RIGHT  = 0.065
M_TOP    = 0.06
M_BOTTOM = 0.06

# Zonas verticales (en fracción 0-1, donde 0 es abajo, 1 es arriba)
# IMPORTANTE: estas zonas garantizan no overlap entre header / contenido / insight / footer
ZONE_FOOTER_TOP   = 0.055   # el footer va de 0 a 0.055
ZONE_INSIGHT_TOP  = 0.20    # el insight box va de 0.07 a 0.20 (espacio ~0.13)
ZONE_CONTENT_BOTTOM = 0.22  # contenido principal empieza arriba de 0.22 (gap de 0.02)
ZONE_CONTENT_TOP  = 0.78    # contenido principal termina abajo de 0.78
ZONE_HEADER_BOTTOM = 0.80   # header empieza arriba de 0.80 (gap de 0.02)

# Anchos
CONTENT_W = 1 - M_LEFT - M_RIGHT  # 0.87 del ancho de página

# Insight box (proporciones internas)
INSIGHT_PAD_X = 0.025  # padding horizontal interno
INSIGHT_PAD_Y = 0.025  # padding vertical interno
