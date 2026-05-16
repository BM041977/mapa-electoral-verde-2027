"""
calc_indicador_10.py — Mapa de calor de bastión histórico 1998-2024
"""
import pandas as pd, json, warnings
warnings.filterwarnings('ignore')

XLSX = '/mnt/user-data/uploads/POWERBI2023xlsx.xlsx'

def familia(nombre):
    n = str(nombre).upper().strip()
    if 'MORENA' in n: return 'IZQ'
    if 'PRD' in n or n.startswith('PT') or 'PARTIDO DEL TRABAJO' in n: return 'IZQ'
    if 'CONVERGENCIA' in n: return 'IZQ'
    if 'ACCION NACIONAL' in n or n == 'PAN' or n.startswith('PAN '): return 'PAN'
    if 'REVOLUCIONARIO INSTITUCIONAL' in n or n == 'PRI' or n.startswith('PRI ')\
        or 'PVEM' in n or 'VERDE' in n: return 'PRI'
    if 'UNIDAD' in n or 'UNIDOS' in n: return 'PRI'
    return None

elecciones = {
    1998: ('AYUNTAMIENTO 1998', 2), 2001: ('AYUNTAMIENTO 2001', 2),
    2004: ('AYUNTAMIENTO 2004', 2), 2007: ('AYUNTAMIENTO 2007', 2),
    2010: ('AYUNTAMIENTO 2010', 2), 2012: ('AYUNTAMIENTO 2012', 2),
    2015: ('AYUNTAMIENTO 2015', 0), 2018: ('AYUNTAMIENTO 2018', 0),
    2021: ('AYUNTAMIENTO 2021', 0), 2024: ('AYUNTAMIENTO 2024', 0),
}

METADATA_COLS = {'Unnamed: 0','Unnamed: 1','CVE-DTO','CABECERA DISTRITAL','  CABECERA DISTRITAL',
                 'CVE-MPIO','MUNICIPIO','AÑO','Columna1','SECCION','CASILLA','LISTA NOMINAL',
                 'TIPO CASILLA','ID CASILLA','EXT CONTIGUA','URNA ELECTRONICA','CIRCUNSCRIPCION',
                 'ID ESTADO','NOMBRE ESTADO','ID DISTRITO LOCAL','CABECERA DISTRITAL LOCAL',
                 'ID MUNICIPIO','ESTADO','LISTANOMINAL','ACTA CASILLA MEC',
                 'NO REGISTRADOS',' NO REGISTRADOS',
                 'VOTOS VALIDOS','  VOTOS VALIDOS','VOTOS NULOS','  VOTOS NULOS',
                 'TOTAL VOTOS','TOTAL DE VOTOS','VOTACION TOTAL','VOTAC1ION TOTAL',
                 '% VOTACION','GANADOR','PARTIDO GANADOR','ESTATUS ACTA','TRIBUNAL',
                 'OBSERVACIONES','RUTA ACTA','JUSTA'}

historico = {}
for año, (hoja, hdr) in elecciones.items():
    df = pd.read_excel(XLSX, sheet_name=hoja, header=hdr)
    if 'MUNICIPIO' not in df.columns: continue
    tx = df[df['MUNICIPIO']=='TUXTLA GUTIERREZ'].copy()
    voto_cols = [c for c in tx.columns if c not in METADATA_COLS and tx[c].dtype in ['float64','int64']]
    tx_grp = tx.groupby('SECCION')[voto_cols].sum().reset_index()
    tx_grp = tx_grp[tx_grp['SECCION'] > 0]
    for _, row in tx_grp.iterrows():
        sec = int(row['SECCION'])
        votos = {c: row[c] for c in voto_cols if row[c] > 0}
        if not votos: continue
        ganador = max(votos.items(), key=lambda x: x[1])[0]
        fam = familia(ganador)
        if fam is None: continue
        historico.setdefault(sec, []).append((año, fam))

# Para cada sección: familia dominante y conteo
bastion = []
for sec in sorted(historico.keys()):
    hist = historico[sec]
    fams = [h[1] for h in hist]
    counts = {'IZQ': fams.count('IZQ'), 'PAN': fams.count('PAN'), 'PRI': fams.count('PRI')}
    # familia dominante: la que más veces ganó (desempate: izq > pan > pri por simplicidad)
    max_count = max(counts.values())
    if counts['IZQ'] == max_count:
        dom = 'IZQ'
    elif counts['PAN'] == max_count:
        dom = 'PAN'
    else:
        dom = 'PRI'
    bastion.append({
        'seccion': sec,
        'dominante': dom,
        'izq': counts['IZQ'],
        'pan': counts['PAN'],
        'pri': counts['PRI'],
        'total': len(hist),
    })

# Cargar y extender
with open('/home/claude/proyecto/datos_indicadores.json') as f:
    data = json.load(f)
data['bastion_historico'] = bastion

# Stats
from collections import Counter
cnt = Counter(b['dominante'] for b in bastion)
data['bastion_stats'] = {
    'total_secciones': len(bastion),
    'izq': cnt.get('IZQ', 0),
    'pan': cnt.get('PAN', 0),
    'pri': cnt.get('PRI', 0),
    'elecciones_analizadas': 10,
}
# Secciones perfectas (que SIEMPRE ganó la misma familia)
perfectas = {'IZQ':0, 'PAN':0, 'PRI':0}
for b in bastion:
    if b['total'] >= 7:  # con al menos 7 elecciones
        if b[b['dominante'].lower()] == b['total']:
            perfectas[b['dominante']] = perfectas.get(b['dominante'], 0) + 1
data['bastion_perfectas'] = perfectas
print(f"Bastion histórico calculado: {len(bastion)} secciones")
print(f"  IZQ: {cnt.get('IZQ',0)}, PAN: {cnt.get('PAN',0)}, PRI: {cnt.get('PRI',0)}")
print(f"  Perfectas (siempre misma familia): {perfectas}")

with open('/home/claude/proyecto/datos_indicadores.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
print("\n✓ Datos guardados")
