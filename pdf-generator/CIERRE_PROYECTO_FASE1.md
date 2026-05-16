# CIERRE DE PROYECTO — Diagnóstico Electoral Tuxtla 2027
**Cliente:** Lic. Francisco Chácon Sánchez · Candidatura MORENA
**Consultor:** Baldemar Maza León — BaldemarMaza.com
**Fecha de cierre Fase 1:** 15 de mayo de 2026

---

## ESTADO ACTUAL

### Producto entregado
- **Archivo:** `Diagnostico_Electoral_Tuxtla_v8.pdf`
- **Tamaño:** 639 KB (639,268 bytes)
- **Páginas:** 49
- **Formato:** Apaisado 13.33 × 10 pulg (ratio 4:3, óptimo para tablet/laptop)

### Estructura final del documento — 9 partes

| Parte | Contenido | Página |
|---|---|---|
| Portada + sub-portada + índice + resumen ejecutivo | 1-4 |
| I | Contexto territorial | 5 |
| II | Historia política 1998-2024 | 8 |
| III | Análisis de la elección 2024 | 13 |
| IV | Listado nominal y proyecciones | 19 |
| V | Escenarios electorales 2027 | 23 |
| VI | Indicadores complementarios (11 indicadores) | 28 |
| VII | Conclusiones y recomendaciones | 39 |
| VIII | Anexos, metodología y glosario | 44 |
| IX | Cierre estratégico — preguntas para el candidato | 47 |
| Contraportada | 49 |

### Los 11 indicadores complementarios de Parte VI
1. Mapa de calor de participación territorial (p29)
2. Tendencia electoral por sección 2018-2024 — sparklines (p30)
3. Crecimiento poblacional Tuxtla 1990-2027 (p31)
4. Evolución de coaliciones ganadoras — timeline (p32)
5. Radar de fortalezas territoriales 3 fuerzas (p33)
6. Top 10 secciones MORENA con margen estrecho — riesgo (p34)
7. Mapa de calor del partido ganador 2024 (p35)
8. Desagregación del voto coalición 2024 (p36)
9. Bastión histórico 1998-2024 (10 elecciones) (p37)
10. Voto cruzado municipal vs gubernatura 2024 (p38)

### Las 4 preguntas estratégicas (Parte IX)
1. ¿Quién es mi votante? — Perfil por densidad de sección
2. ¿Cuánto necesito para ganar? — Umbral de victoria 2027
3. ¿Quién es mi competidor real? — Escenario coalición opositora
4. ¿Cómo mido el éxito de la gestión? — Framework post-elección

---

## HALLAZGOS ESTRATÉGICOS CLAVE

### Sobre el bastión MORENA
- **207 de 264 secciones (78.4%)** ganadas por MORENA en 2024.
- **175 secciones** son izquierda histórica desde 1998 — no hay "moda MORENA", hay continuidad ideológica con PRD/PT/Convergencia.
- Voto MORENA efectivo Tuxtla 2024: **115,930 votos** (vs oposición consolidada 92,493).

### Sobre los riesgos
- **73 secciones MORENA tienen margen <15%**, y **10 ganaron por menos de 3%**. La sección 1754 fue por UN solo voto.
- **61 secciones dependen del arrastre estatal** (MORENA gubernatura > MORENA municipal). Vulnerables en 2027 sin concurrencia.
- Sin aliados (PVEM + PT), MORENA perdería **23,726 votos (20.5%)** de su coalición 2024.

### Sobre la oposición
- **57 secciones PAN históricas** coinciden con las 56 actuales: voto **estructural** del oriente residencial, no coyuntural.
- **33 secciones priistas históricas** son hoy zonas de votante huérfano — universo natural de captación MORENA.
- MC es **tercera fuerza** sin ganar ninguna sección, pero con concentración en centro urbano.

### Sobre la marca propia local
- MORENA municipal (44.7%) ≈ MORENA gubernatura (43.3%): **el candidato municipal sí tiene marca propia**, no depende del arrastre Sheinbaum.

### Umbrales de victoria 2027
- **Mínimo:** 104,646 votos (35% del voto válido, oposición fragmentada)
- **Esperado:** 88,321 (promedio últimas 3 elecciones)
- **Blindaje:** 134,545 (45% del voto válido, ganar sin sustos)

---

## ARCHIVOS DEL PROYECTO

Directorio: `/home/claude/proyecto/`

### Código fuente (Python)
- `brand.py` — Paleta de colores, fuentes, dimensiones, colores institucionales (MORENA #8B1E3F, PAN #0066CC, MC #FF8C00, PRI #E53935)
- `page_system.py` — Sistema base: new_page, page_ax, draw_header, draw_footer (con logo), draw_insight (altura adaptativa), draw_card
- `components.py` — render_part_page, render_numbered_card, render_data_card, render_table
- `pages_part1.py` — Páginas 1-18 (portada, índice, resumen, partes I-III)
- `pages_part2.py` — Páginas 19-27 + Conclusiones + Anexos (partes IV, V, VII, VIII)
- `pages_indicadores.py` — Indicadores 1-5 (Parte VI primera mitad)
- `pages_indicadores_extra.py` — Indicadores 6-10 + Glosario + Divisor IX + Preguntas estratégicas
- `build_pdf.py` — Orquestador que ensambla las 49 páginas

### Scripts de cálculo
- `calc_indicadores.py` — Pre-cálculo de indicadores 1-5
- `calc_indicadores_nuevos.py` — Pre-cálculo de indicadores 6-9
- `calc_indicador_10.py` — Bastión histórico 1998-2024

### Datos consolidados (JSON)
- `datos_tuxtla.json` — Datos base de Tuxtla (LN, secciones, top 10s, historial alcaldes)
- `datos_indicadores.json` — Datos calculados de los 10 indicadores
- `datos_estrategicas.json` — Datos para las 4 preguntas finales

### Insumos
- Excel maestro: `/mnt/user-data/uploads/POWERBI2023xlsx.xlsx` (93 hojas, 116 MB)
- Logo: `/home/claude/proyecto/logo_clean.png`

---

## CONVENCIONES TÉCNICAS ESTABLECIDAS

1. **Tipografía:** Lora (serif para títulos y números), Liberation Sans (sans-serif para texto). NUNCA usar glifos → ni ▸ — las fuentes no los tienen. Usar `-`, `•` o `|`.
2. **Sistema visual:** zonas verticales con gaps, insight box de altura adaptativa, footer con logo no texto.
3. **Colores:** Crema fondo #FBF9F4, tinta #1A1A1A, accent #2D2D2D. Colores de partido institucionales fijos.
4. **Honestidad de datos:** todo cálculo declarado del Excel. Heurísticas marcadas con nota metodológica al pie.
5. **Naming:** secciones electorales se nombran SIN la palabra "Sección" en columnas tabulares (solo el número).

---

## PRÓXIMOS PASOS — FASES PENDIENTES

### Opción A — Fase 2: Parametrización para 124 municipios
**Objetivo:** convertir el código para que reciba parámetro `municipio` y genere PDFs distintos para cada uno de los 124 municipios de Chiapas.

**Tiempo estimado:** 2-3 sesiones (~3-4 horas total).

**Beneficio:** catálogo comercial de 124 productos para ofrecer a candidatos de cualquier municipio. Te diferencia como consultor con producto escalable.

**Pasos:**
1. Refactorizar `datos_tuxtla.json` → función parametrizada `cargar_datos_municipio(nombre)`.
2. Adaptar pre-cálculos para cualquier municipio.
3. Validar con 2-3 municipios piloto (ej. Berriozábal, San Cristóbal).
4. Generar batch de 124 PDFs (30-60 min de procesamiento).
5. Subir a GitHub `BM041977/mapa-electoral-v2` para distribución.

### Opción B — Fase 3: Dashboard web `/datos-secciones`
**Objetivo:** página interactiva en `mapa-electoral-v2.onrender.com` con tabla buscable, filtrable y descargable de las secciones de Tuxtla (o de los 124 municipios si ya se hizo Fase 2).

**Tiempo estimado:** 2 sesiones (~3 horas).

**Beneficio:** complementa el PDF resolviendo la observación de que el PDF muestra solo top 10 (4% del territorio). El usuario consulta las 264 secciones online.

**Pasos:**
1. Diseñar endpoint Flask `/datos-secciones` en `mapa-electoral-v2`.
2. Cargar `datos_indicadores.json` en backend.
3. Frontend con DataTables.js — buscador, filtros por distrito/partido, exportación CSV.
4. Deploy en Render Free.

### Opción C — Cierre comercial del entregable actual
**Objetivo:** preparar el documento como entregable formal al cliente.

**Tiempo estimado:** 1 sesión (~1 hora).

**Beneficio:** profesionalización del entregable. Genera prestigio para tu marca.

**Pasos:**
1. Agregar nombre de Francisco Chácon en sub-portada (página 2).
2. Crear documento ejecutivo de 1 hoja con los 5 hallazgos top + recomendación operativa.
3. Preparar paquete: PDF principal + ejecutivo + carta de presentación.

---

## CREDENCIALES Y URLS DEL PROYECTO

- **Sistema web:** https://mapa-electoral-v2.onrender.com (Render Free, Flask)
- **GitHub repo:** github.com/BM041977/mapa-electoral-v2 (privado)
- **Usuario:** Baldemar
- **Password:** Victoria@Ever

---

## MI RECOMENDACIÓN HONESTA DE ORDEN

Si tu prioridad es **valor comercial inmediato**: empezar por **Opción C** (1 sesión rápida que ya te deja entregable formal para Francisco Chácon esta semana), después **Opción A** (parametrización para vender el mismo producto a otros candidatos).

Si tu prioridad es **escalar el producto antes de vender**: ir directo a **Opción A**, luego **Opción B**, y la **Opción C** al final con el producto ya completo.

Si quieres **completar la plataforma técnica** antes de pensar en clientes: **Opción B** primero para tener el dashboard listo, después **Opción A** para alimentarlo con los 124 municipios.

---

## PARA RETOMAR EN NUEVA CONVERSACIÓN

Si abres una nueva sesión con otro Claude, simplemente comparte este documento y di:

> "Continuemos con el proyecto Diagnóstico Electoral Tuxtla. Adjunto el cierre de la Fase 1. Quiero arrancar con la **Opción [A/B/C]**."

Todo el contexto está en este archivo. El código está en `/home/claude/proyecto/` (aunque cada sesión nueva resetea el filesystem, así que necesitarás re-subir el Excel `POWERBI2023xlsx.xlsx` y el logo).
