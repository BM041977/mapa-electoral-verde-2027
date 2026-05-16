# INSTRUCCIONES PARA RETOMAR EL PROYECTO

## PASO 1 — Archivos a subir en la nueva conversación

Sube estos archivos cuando abras la nueva sesión:

1. **`POWERBI2023xlsx.xlsx`** — Tu Excel maestro (116 MB, 93 hojas)
2. **`Diagnostico_Electoral_Tuxtla_v8.pdf`** — El PDF entregado (referencia visual)
3. **`CIERRE_PROYECTO_FASE1.md`** — Documento técnico de cierre con detalle de código y hallazgos
4. **Tu logo** — `logo_clean.png` o similar (si no lo tienes guardado, lo recreamos)

## PASO 2 — Mensaje para pegar (copia el texto completo de abajo)

---

Hola, vengo a continuar el proyecto de diagnóstico electoral para Tuxtla Gutiérrez. Soy Baldemar Maza León, consultor electoral en Chiapas. Mi cliente es el Lic. Francisco Chácon Sánchez (candidatura MORENA Tuxtla 2027).

**Contexto:** En sesiones anteriores con Claude construimos un PDF de diagnóstico electoral de 49 páginas con datos reales del Excel POWERBI2023xlsx. El documento está completo en su Fase 1: cubre 9 partes (Contexto territorial, Historia política 1998-2024, Análisis 2024, Listado nominal, Escenarios 2027, 11 Indicadores complementarios, Conclusiones, Anexos y Cierre estratégico con 4 preguntas para el candidato).

**Lo que adjunto:**
- `POWERBI2023xlsx.xlsx` — Excel maestro con los datos electorales de Chiapas
- `Diagnostico_Electoral_Tuxtla_v8.pdf` — PDF entregado (referencia)
- `CIERRE_PROYECTO_FASE1.md` — Documento técnico con el detalle del código, hallazgos, archivos del proyecto y plan de continuación
- `logo_clean.png` — Mi logo (para mantener consistencia visual)

**Lo que quiero hacer ahora:** [ELEGIR UNA OPCIÓN]

→ **Opción A — Cierre comercial del entregable** (1 sesión)
   Personalizar el PDF con el nombre de mi cliente en sub-portada, crear un resumen ejecutivo de 1 hoja con los 5 hallazgos top, y preparar el paquete listo para entregar (PDF + ejecutivo + carta de presentación).

→ **Opción B — Parametrización para 124 municipios** (2-3 sesiones)
   Convertir el código actual para que reciba parámetro `municipio` y genere PDFs distintos para cada uno de los 124 municipios de Chiapas. Crear catálogo comercial escalable.

→ **Opción C — Dashboard web `/datos-secciones`** (2 sesiones)
   Crear una página interactiva en mapa-electoral-v2.onrender.com con tabla buscable y filtrable de todas las secciones de Tuxtla.

Mi elección: **[ESCRIBIR A, B o C aquí]**

**Preferencias de trabajo:**
- Comunicación en español casual
- Un objetivo por sesión, calidad sobre velocidad
- Avisar si la calidad puede bajar o si un dato no se puede calcular
- Resumen matutino al iniciar conversación (mundo, deportes, finanzas y política México)

---

## PASO 3 — Lo que la nueva conversación va a hacer

El nuevo Claude debe:
1. Leer el `CIERRE_PROYECTO_FASE1.md` para entender el estado completo del proyecto.
2. Inspeccionar el PDF v8 para entender el resultado actual.
3. Confirmar contigo cuál opción atacar.
4. Empezar a trabajar.

**IMPORTANTE:** El código del proyecto vivía en `/home/claude/proyecto/` pero cada sesión nueva resetea el filesystem. Eso significa que:

- Si elegiste **Opción A** (cierre comercial): se reconstruye desde cero solo lo necesario (modificar 1-2 páginas, crear ejecutivo). Tiempo razonable.
- Si elegiste **Opción B o C**: necesitarás reconstruir el código base (3-4 horas adicionales) ANTES de poder parametrizar o crear dashboard. Considera esto al elegir.

**Atajo opcional:** Si tienes acceso al GitHub `BM041977/mapa-electoral-v2`, puedes subir el código de `/home/claude/proyecto/` allí para tenerlo persistente. Pregúntale al nuevo Claude cómo hacerlo si te interesa.

## PASO 4 — Datos críticos del proyecto para referencia

- **Cliente:** Lic. Francisco Chácon Sánchez
- **Municipio:** Tuxtla Gutiérrez, Chiapas
- **Elección objetivo:** 2027 (intermedia estatal, sin gubernatura concurrente)
- **Partido:** MORENA
- **Sistema web existente:** mapa-electoral-v2.onrender.com (usuario: Baldemar, password: Victoria@Ever)
- **GitHub:** BM041977/mapa-electoral-v2 (privado)

### Hallazgos clave del diagnóstico (para que el nuevo Claude los tenga a la mano)
- MORENA gana 207 de 264 secciones (78.4%) en 2024
- 175 secciones son izquierda histórica desde 1998 (continuidad, no moda)
- 73 secciones MORENA tienen margen <15% — riesgo defensivo prioritario
- 61 secciones dependen del arrastre estatal (vulnerables sin gubernatura concurrente en 2027)
- Voto MORENA municipal 2024: 115,930 (con coalición); oposición unida 92,493
- Umbral seguro 2027: ~134,545 votos (45% del voto válido)
- Promedio histórico últimas 3 elecciones: 88,321 votos
