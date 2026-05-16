# Diagnóstico Electoral PDF Generator

Sistema de generación de diagnóstico electoral en PDF para municipios de Chiapas.
Versión actual: **v8 — Tuxtla Gutiérrez 2027** (49 páginas)

**Cliente:** Lic. Francisco Chácon Sánchez — Candidatura MORENA Tuxtla 2027
**Consultor:** Baldemar Maza León — BaldemarMaza.com

---

## Estructura de archivos

### Sistema de generación de páginas
- `brand.py` — Paleta de colores, tipografía, dimensiones, colores de partidos
- `page_system.py` — Sistema base: new_page, draw_header, draw_footer (con logo), draw_insight, draw_card
- `components.py` — Componentes reutilizables: render_part_page, render_data_card, render_table, render_numbered_card
- `pages_part1.py` — Páginas 1-18 (portada, índice, resumen, partes I, II, III)
- `pages_part2.py` — Páginas 19-27 + Conclusiones + Anexos (partes IV, V, VII, VIII)
- `pages_indicadores.py` — Indicadores 1-5 (primera mitad de Parte VI)
- `pages_indicadores_extra.py` — Indicadores 6-10, Glosario, Divisor IX y Preguntas estratégicas
- `build_pdf.py` — **Orquestador principal** — ensambla las 49 páginas

### Scripts de pre-cálculo de datos
- `calc_indicadores.py` — Pre-calcula indicadores 1-5 desde el Excel
- `calc_indicadores_nuevos.py` — Pre-calcula indicadores 6-9
- `calc_indicador_10.py` — Bastión histórico 1998-2024 (10 elecciones)

### Datos consolidados (output de los scripts de cálculo)
- `datos_tuxtla.json` — Datos base de Tuxtla
- `datos_indicadores.json` — Datos calculados de los 10 indicadores
- `datos_estrategicas.json` — Datos para las preguntas finales del candidato

### Recursos visuales
- `logo_clean.png` — Logo de Baldemar Maza León con transparencia

### Documentación
- `CIERRE_PROYECTO_FASE1.md` — Documento técnico completo del proyecto
- `INSTRUCCIONES_NUEVA_CONVERSACION.md` — Cómo retomar el proyecto en sesión nueva

### Testing
- `test_pages.py` — Suite de pruebas visuales (legacy, no crítico)

---

## Cómo usar el código

### Pre-requisitos
- Python 3.10+
- Librerías: `matplotlib`, `pandas`, `openpyxl`, `numpy`
- Excel maestro: `POWERBI2023xlsx.xlsx` (debe estar en `/mnt/user-data/uploads/` o ajustar rutas)
- Logo: `logo_clean.png` en el mismo directorio del código

### Generar el PDF completo
```bash
# 1. Pre-calcular datos (si cambiaron los inputs)
python3 calc_indicadores.py
python3 calc_indicadores_nuevos.py
python3 calc_indicador_10.py

# 2. Ensamblar el PDF
python3 build_pdf.py
```

Output: `Diagnostico_Electoral_Tuxtla_v8.pdf` (~640 KB, 49 páginas)

---

## Convenciones técnicas establecidas

### Tipografía
- **Serif:** Lora (títulos, números grandes, fechas)
- **Sans-serif:** Liberation Sans (texto de cuerpo, etiquetas)
- **NUNCA usar** los glifos `→` ni `▸` — las fuentes no los soportan. Usar `-`, `•` o `|`.

### Colores institucionales
| Elemento | Hex | Uso |
|---|---|---|
| Fondo crema | `#FBF9F4` | Background del documento |
| Tinta principal | `#1A1A1A` | Títulos, texto principal |
| Accent | `#2D2D2D` | Detalles, líneas, proyecciones neutras |
| MORENA | `#8B1E3F` | Color institucional guinda |
| PAN | `#0066CC` | Color institucional azul |
| MC | `#FF8C00` | Color institucional naranja |
| PRI | `#E53935` | Color institucional rojo |

### Sistema visual
- Dimensiones del PDF: 13.33 × 10 pulg (apaisado, ratio 4:3)
- Zonas verticales separadas con gaps de seguridad
- Insight box de altura adaptativa (no fija) — clave para evitar overlap
- Footer con logo no texto, posición fija
- Header con eyebrow + título serif grande + subtítulo italic

### Datos y honestidad
- Todo cálculo declarado del Excel POWERBI2023
- Heurísticas marcadas con nota metodológica al pie (ver Indicador 5 Radar)
- Secciones electorales se nombran SIN la palabra "Sección" en columnas tabulares

---

## Hallazgos clave del diagnóstico Tuxtla 2027

1. **207 de 264 secciones (78.4%)** ganadas por MORENA en 2024
2. **175 secciones** son izquierda histórica desde 1998 — continuidad ideológica
3. **73 secciones MORENA con margen <15%** — riesgo defensivo prioritario
4. **61 secciones dependen del arrastre estatal** — vulnerables sin gubernatura concurrente en 2027
5. Voto MORENA municipal 2024: **115,930** (con coalición); oposición unida: **92,493**
6. **Umbral seguro 2027:** ~134,545 votos (45% del voto válido)
7. Promedio histórico últimas 3 elecciones: **88,321 votos**

---

## Roadmap

- ✅ **Fase 1:** PDF completo Tuxtla v8 (49 páginas, 11 indicadores, 9 partes)
- ⏳ **Fase 2:** Parametrización para 124 municipios de Chiapas
- ⏳ **Fase 3:** Dashboard web `/datos-secciones` en mapa-electoral-v2.onrender.com

---

## Licencia
Uso interno — Consultoría Baldemar Maza León. Todos los derechos reservados.
