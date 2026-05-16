"""
calc_indicadores_nuevos.py — Datos para indicadores 6-9
"""
import pandas as pd, json, warnings
warnings.filterwarnings('ignore')

XLSX = '/mnt/user-data/uploads/POWERBI2023xlsx.xlsx'

# Cargar JSON existente y EXTENDER
with open('/home/claude/proyecto/datos_indicadores.json') as f:
    data = json.load(f)


# ════════════════════════════════════════════════════════════════
# INDICADOR 6: Top secciones MORENA por MARGEN ESTRECHO
# ════════════════════════════════════════════════════════════════
print("Indicador 6: Margen estrecho MORENA...")
df_ay = pd.read_excel(XLSX, sheet_name='AYUNTAMIENTO 2024')
tx = df_ay[df_ay['MUNICIPIO']=='TUXTLA GUTIERREZ'].copy()

# Para cada sección, calcular votos por partido y margen
partidos = ['PAN','PRI','PRD','PVEM','PT','MC','PCHU','MORENA','PMCH','PPCH','PES','RSP','FXM']
# Coaliciones que contienen MORENA — sumarlas al voto MORENA "efectivo"
coal_morena = [c for c in tx.columns if isinstance(c, str) and 'MORENA' in c]

# Agregar a nivel sección
agg = tx.groupby('SECCION').agg({p: 'sum' for p in partidos}).reset_index()
agg = agg[agg['SECCION'] > 0]

# Para cada sección, identificar ganador y segundo lugar
def calc_margen(row):
    votos = {p: row[p] for p in partidos}
    sorted_p = sorted(votos.items(), key=lambda x: -x[1])
    ganador, votos_g = sorted_p[0]
    segundo, votos_s = sorted_p[1]
    total = sum(votos.values())
    margen_abs = votos_g - votos_s
    margen_pct = (margen_abs / max(total, 1)) * 100
    return pd.Series({
        'ganador': ganador,
        'votos_ganador': int(votos_g),
        'segundo': segundo,
        'votos_segundo': int(votos_s),
        'margen_abs': int(margen_abs),
        'margen_pct': round(margen_pct, 1),
        'total_votos': int(total),
    })

agg_calc = agg.apply(calc_margen, axis=1)
agg = pd.concat([agg[['SECCION']], agg_calc], axis=1)

# Filtrar secciones donde MORENA ganó con margen estrecho (margen_pct < 10%)
margen_estrecho_morena = agg[(agg['ganador']=='MORENA') & (agg['margen_pct'] < 15)].copy()
margen_estrecho_morena = margen_estrecho_morena.sort_values('margen_pct').head(10)
print(f"  Secciones MORENA con margen <15%: {len(agg[(agg['ganador']=='MORENA') & (agg['margen_pct'] < 15)])}")
print(f"  Top 10 más ajustadas:")
data['margen_estrecho'] = []
for _, r in margen_estrecho_morena.iterrows():
    data['margen_estrecho'].append({
        'seccion': int(r['SECCION']),
        'votos_morena': int(r['votos_ganador']),
        'segundo_partido': r['segundo'],
        'votos_segundo': int(r['votos_segundo']),
        'margen_abs': int(r['margen_abs']),
        'margen_pct': float(r['margen_pct']),
    })
    print(f"    Sec {int(r['SECCION'])}: MORENA {int(r['votos_ganador'])} vs {r['segundo']} {int(r['votos_segundo'])} ({r['margen_pct']:.1f}%)")

# Stats adicionales
data['margen_estrecho_total'] = int(len(agg[(agg['ganador']=='MORENA') & (agg['margen_pct'] < 15)]))


# ════════════════════════════════════════════════════════════════
# INDICADOR 7: Mapa de calor PARTIDO GANADOR 2024
# ════════════════════════════════════════════════════════════════
print("\nIndicador 7: Mapa partido ganador...")
df_gp = pd.read_excel(XLSX, sheet_name='GANADOR PARTIDO 2024')
tx_gp = df_gp[df_gp['MUNICIPIO']=='TUXTLA GUTIERREZ'].copy()
tx_gp = tx_gp.sort_values('SECCION')

data['heatmap_ganador'] = [
    {'seccion': int(r['SECCION']),
     'ganador': r['Partido Ganador'] if r['Partido Ganador'] in ['MORENA','PAN'] else 'COAL',
     'votos': int(r['Votacion Maxima'])}
    for _, r in tx_gp.iterrows()
]
print(f"  {len(data['heatmap_ganador'])} secciones con ganador identificado")

# Voto nulo total Tuxtla — para card adicional
tx_ay_nulos = tx['  VOTOS NULOS'].sum() if '  VOTOS NULOS' in tx.columns else 0
tx_ay_total = tx['TOTAL VOTOS'].sum() if 'TOTAL VOTOS' in tx.columns else 1
data['votos_nulos_total'] = int(tx_ay_nulos)
data['votos_nulos_pct'] = round((tx_ay_nulos / tx_ay_total) * 100, 1) if tx_ay_total > 0 else 0
print(f"  Voto nulo Tuxtla 2024: {tx_ay_nulos:,.0f} ({data['votos_nulos_pct']}%)")


# ════════════════════════════════════════════════════════════════
# INDICADOR 8: Fuerza de la coalición MORENA-PVEM en 2024
# ════════════════════════════════════════════════════════════════
print("\nIndicador 8: Coalición MORENA-PVEM...")
# Voto MORENA puro
morena_puro = tx['MORENA'].sum()
# Voto PVEM puro
pvem_puro = tx['PVEM'].sum()
# Voto PT puro
pt_puro = tx['PT'].sum()
# Voto de las coaliciones de los 3 partidos (combinaciones)
# Las columnas con todos los 3: PVEM+PT+MORENA y similares
coal_3 = [c for c in tx.columns if isinstance(c,str)
          and 'PVEM' in c and 'PT' in c and 'MORENA' in c]
coal_3_total = tx[coal_3].fillna(0).sum().sum() if coal_3 else 0
# Coaliciones binarias PVEM-MORENA, PT-MORENA, PVEM-PT
coal_pvem_morena_solo = tx['PVEM MORENA'].sum() if 'PVEM MORENA' in tx.columns else 0
coal_pt_morena_solo = tx['PT MORENA'].sum() if 'PT MORENA' in tx.columns else 0
coal_pvem_pt_solo = tx['PVEM PT'].sum() if 'PVEM PT' in tx.columns else 0
# Voto total atribuible a MORENA (incluye coalición)
voto_morena_efectivo = morena_puro + coal_3_total + coal_pvem_morena_solo + coal_pt_morena_solo

data['coalicion_morena'] = {
    'morena_puro':       int(morena_puro),
    'pvem_puro':         int(pvem_puro),
    'pt_puro':           int(pt_puro),
    'coal_3_partidos':   int(coal_3_total),
    'coal_pvem_morena':  int(coal_pvem_morena_solo),
    'coal_pt_morena':    int(coal_pt_morena_solo),
    'coal_pvem_pt':      int(coal_pvem_pt_solo),
    'voto_morena_efectivo': int(voto_morena_efectivo),
    'aporte_aliados_pct': round(((coal_3_total + coal_pvem_morena_solo + coal_pt_morena_solo + pvem_puro + pt_puro) / voto_morena_efectivo) * 100, 1),
}
print(f"  MORENA puro: {morena_puro:,.0f}")
print(f"  PVEM puro:   {pvem_puro:,.0f}")
print(f"  PT puro:     {pt_puro:,.0f}")
print(f"  Coalición 3 partidos: {coal_3_total:,.0f}")
print(f"  Bi PVEM-MORENA: {coal_pvem_morena_solo:,.0f}")
print(f"  Bi PT-MORENA:   {coal_pt_morena_solo:,.0f}")
print(f"  Voto MORENA efectivo: {voto_morena_efectivo:,.0f}")


# ════════════════════════════════════════════════════════════════
# INDICADOR 9: Comparativo Tuxtla vs municipios vecinos metropolitanos
# ════════════════════════════════════════════════════════════════
print("\nIndicador 9: Comparativo metropolitano...")
vecinos = ['TUXTLA GUTIERREZ', 'BERRIOZABAL', 'CHIAPA DE CORZO',
           'SUCHIAPA', 'OCOZOCOAUTLA DE ESPINOSA', 'SAN FERNANDO']

# Datos por municipio: secciones, voto MORENA, partido ganador
df_pr = pd.read_excel(XLSX, sheet_name='PROYECCION VOTACION 2027')

comparativo = []
for mun in vecinos:
    sub_pr = df_pr[df_pr['MUNICIPIO']==mun]
    sub_ay = df_ay[df_ay['MUNICIPIO']==mun]
    sub_gp = df_gp[df_gp['MUNICIPIO']==mun]

    if len(sub_pr) == 0:
        continue
    ln_2024 = int(sub_pr['LISTADO NOMINAL 2024'].sum())
    ln_2027 = int(sub_pr['LISTADO NOMINAL 2027 PROYECCIÓN'].sum())
    crecimiento_pct = round(((ln_2027 - ln_2024) / max(ln_2024,1)) * 100, 1)
    morena_votos = int(sub_ay['MORENA'].sum()) if 'MORENA' in sub_ay.columns else 0
    pan_votos = int(sub_ay['PAN'].sum()) if 'PAN' in sub_ay.columns else 0
    total_secciones = len(sub_gp)
    secciones_morena = int((sub_gp['Partido Ganador']=='MORENA').sum())
    pct_secciones_morena = round((secciones_morena / max(total_secciones,1)) * 100, 1) if total_secciones > 0 else 0
    comparativo.append({
        'municipio': mun.replace('OCOZOCOAUTLA DE ESPINOSA', 'OCOZOCOAUTLA'),
        'ln_2024': ln_2024,
        'ln_2027': ln_2027,
        'crecimiento_pct': crecimiento_pct,
        'morena_votos': morena_votos,
        'pan_votos': pan_votos,
        'total_secciones': total_secciones,
        'secciones_morena': secciones_morena,
        'pct_secciones_morena': pct_secciones_morena,
    })
data['comparativo_metropolitano'] = comparativo
for c in comparativo:
    print(f"  {c['municipio']:25s}: LN24={c['ln_2024']:>7,}  secciones={c['total_secciones']:>3}  %MORENA secciones={c['pct_secciones_morena']:>5.1f}%")

# Guardar
with open('/home/claude/proyecto/datos_indicadores.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
print("\n✓ Datos extendidos guardados")
