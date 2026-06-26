"""
calc_indicadores.py — Pre-calcula datos para los indicadores 1-5.
Refactor Fase 2: parametrizado por MUNICIPIO_KEY (env var MUNICIPIO).

Salidas:
- datos_indicadores[_<municipio>].json  → indicadores 1, 2, 3, 5
                                          + votos_historicos (1998-2024)
                                          + ln_total_municipio
                                          + total_secciones_municipio
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pandas as pd, json, warnings
warnings.filterwarnings('ignore')

from municipio_config import (
    MUNICIPIO_KEY, XLSX_PATH, archivo_indicadores, presentacion, info
)

info()
XLSX = XLSX_PATH
data = {}

# Persistir el municipio dentro del JSON
data['municipio_key'] = MUNICIPIO_KEY
data['municipio_presentacion'] = presentacion()


# ════════════════════════════════════════════════════════════════
# INDICADOR 1: Mapa de calor de participación
# ════════════════════════════════════════════════════════════════
print(f"\nIndicador 1: Mapa de calor de participación...")
df = pd.read_excel(XLSX, sheet_name='PARTICIPACION 2024')
mun = df[df['MUNICIPIO']==MUNICIPIO_KEY].copy()
mun = mun[mun['% VOTACION'] > 0]
mun = mun.sort_values('SECCION')
data['heatmap_secciones'] = [
    {'seccion': int(r['SECCION']),
     'participacion': float(round(r['% VOTACION']*100, 1)),
     'ln': int(r['LISTADO NOMINAL'])}
    for _, r in mun.iterrows()
]
baja = mun[mun['% VOTACION'] < 0.50]
data['heatmap_baja_secciones'] = int(len(baja))
data['heatmap_baja_ln'] = int(baja['LISTADO NOMINAL'].sum())
data['heatmap_no_movilizados'] = int((baja['LISTADO NOMINAL'] * (1 - baja['% VOTACION'])).sum())

# NUEVO Fase 2: antes hardcoded (`/ 264`, `ln_total = 467347`).
data['total_secciones_municipio'] = int(len(mun))
data['ln_total_municipio'] = int(mun['LISTADO NOMINAL'].sum())

print(f"  {len(mun)} secciones con datos válidos")
print(f"  LN total: {data['ln_total_municipio']:,}")
print(f"  {len(baja)} secciones con participación <50% ({data['heatmap_no_movilizados']:,} electores no movilizados)")


# ════════════════════════════════════════════════════════════════
# INDICADOR 2: Tendencia por sección con sparklines (MORENA 2018→2024)
# ════════════════════════════════════════════════════════════════
print("\nIndicador 2: Tendencia por sección (sparklines)...")

def pct_morena_por_seccion(hoja, año, col_morena):
    df = pd.read_excel(XLSX, sheet_name=hoja)
    sub = df[df['MUNICIPIO']==MUNICIPIO_KEY].copy()
    if len(sub) == 0:
        return pd.DataFrame(columns=['SECCION', f'pct_{año}'])
    metadata = {'CVE-DTO','CABECERA DISTRITAL','  CABECERA DISTRITAL','CVE-MPIO','MUNICIPIO','AÑO',
                'SECCION','CASILLA','LISTA NOMINAL','TIPO CASILLA','ID CASILLA','EXT CONTIGUA',
                'URNA ELECTRONICA','CIRCUNSCRIPCION','ID ESTADO','NOMBRE ESTADO','ID DISTRITO LOCAL',
                'CABECERA DISTRITAL LOCAL','ID MUNICIPIO','ESTADO','ACTA CASILLA MEC','LISTANOMINAL',
                '  VOTOS VALIDOS',' NO REGISTRADOS','  VOTOS NULOS','TOTAL VOTOS','% VOTACION',
                'GANADOR','PARTIDO GANADOR','ESTATUS ACTA','TRIBUNAL','OBSERVACIONES','RUTA ACTA',
                'VOTOS VALIDOS','NO REGISTRADOS','VOTOS NULOS','TOTAL DE VOTOS'}
    voto_cols = [c for c in sub.columns if c not in metadata and sub[c].dtype in ['float64','int64']]
    sub['TOTAL'] = sub[voto_cols].fillna(0).sum(axis=1)
    if col_morena not in sub.columns:
        sub[col_morena] = 0
    agg = sub.groupby('SECCION').agg(
        morena=(col_morena, lambda x: x.fillna(0).sum()),
        total=('TOTAL','sum')
    ).reset_index()
    agg[f'pct_{año}'] = (agg['morena'] / agg['total'].replace(0,1)) * 100
    return agg[['SECCION', f'pct_{año}']]

df18 = pct_morena_por_seccion('AYUNTAMIENTO 2018', 2018, 'MORENA')
df21 = pct_morena_por_seccion('AYUNTAMIENTO 2021', 2021, ' MORENA')
df24 = pct_morena_por_seccion('AYUNTAMIENTO 2024', 2024, 'MORENA')
hist = df18.merge(df21, on='SECCION', how='outer').merge(df24, on='SECCION', how='outer')

if len(hist) == 0:
    print(f"  ⚠️  Sin datos históricos para MORENA en {MUNICIPIO_KEY}")
    data['sparklines_muestra'] = []
    data['sparklines_distribucion'] = {}
else:
    hist['SECCION'] = hist['SECCION'].astype(int)

    def clasificar(row):
        v18, v21, v24 = row['pct_2018'], row['pct_2021'], row['pct_2024']
        if pd.isna(v18) or pd.isna(v21) or pd.isna(v24):
            return 'RE-SECCIONADA'
        delta_total = v24 - v18
        rango = max(v18, v21, v24) - min(v18, v21, v24)
        if delta_total >= 18:
            return 'CRECIENTE'
        elif delta_total >= 8:
            return 'CONSOLIDADA'
        elif delta_total <= -5:
            return 'EN RETROCESO'
        elif rango > 18:
            return 'ERRÁTICA'
        else:
            return 'ESTABLE'

    hist['delta'] = hist['pct_2024'] - hist['pct_2018']
    hist['clasif'] = hist.apply(clasificar, axis=1)
    hist = hist[hist['SECCION'] > 0].copy()

    clasificaciones_a_mostrar = ['CONSOLIDADA','CONSOLIDADA','CRECIENTE','CRECIENTE',
                                  'ESTABLE','RE-SECCIONADA']
    muestra = []
    for clas in clasificaciones_a_mostrar:
        sub = hist[hist['clasif']==clas]
        ya_tomados = {x['seccion'] for x in muestra}
        sub = sub[~sub['SECCION'].isin(ya_tomados)]
        if len(sub) > 0:
            if clas == 'EN RETROCESO':
                r = sub.sort_values('delta').iloc[0]
            elif clas in ('CONSOLIDADA','CRECIENTE'):
                r = sub.sort_values('delta', ascending=False).iloc[0]
            elif clas == 'RE-SECCIONADA':
                sub_nuevas = sub[sub['pct_2024'].notna() & sub['pct_2018'].isna()]
                r = sub_nuevas.iloc[0] if len(sub_nuevas) > 0 else sub.iloc[0]
            else:
                r = sub.iloc[0]
            muestra.append({
                'seccion': int(r['SECCION']),
                'v18': None if pd.isna(r['pct_2018']) else round(float(r['pct_2018']), 1),
                'v21': None if pd.isna(r['pct_2021']) else round(float(r['pct_2021']), 1),
                'v24': None if pd.isna(r['pct_2024']) else round(float(r['pct_2024']), 1),
                'delta': None if pd.isna(r['delta']) else round(float(r['delta']), 1),
                'clasif': clas,
            })
    data['sparklines_muestra'] = muestra
    dist = hist['clasif'].value_counts().to_dict()
    data['sparklines_distribucion'] = {k: int(v) for k, v in dist.items()}
    print(f"  Distribución: {data['sparklines_distribucion']}")


# ════════════════════════════════════════════════════════════════
# INDICADOR 3: Crecimiento poblacional 1990-2027
# ════════════════════════════════════════════════════════════════
print("\nIndicador 3: Crecimiento poblacional...")

def cargar_poblacion(municipio_key):
    if municipio_key == 'TUXTLA GUTIERREZ':
        return [
            {'año': 1990, 'pob': 295615},
            {'año': 1995, 'pob': 367033},
            {'año': 2000, 'pob': 434143},
            {'año': 2005, 'pob': 503320},
            {'año': 2010, 'pob': 553374},
            {'año': 2015, 'pob': 598710},
            {'año': 2020, 'pob': 671619},
            {'año': 2025, 'pob': 695200},
            {'año': 2027, 'pob': 715400},
        ]

    # Intentar leer hoja específica (POBLACION CHIAPAS 1990-2020 — formato variable)
    serie_directa = []
    try:
        dfp = pd.read_excel(XLSX, sheet_name='POBLACION CHIAPAS 1990-2020')
        cols = list(dfp.columns)
        col_mun = next((c for c in cols if 'MUNI' in str(c).upper()), None)
        if col_mun is not None:
            sub = dfp[dfp[col_mun].astype(str).str.upper().str.strip()==municipio_key]
            if len(sub):
                for c in cols:
                    try:
                        año = int(str(c).strip())
                        if 1990 <= año <= 2030:
                            val = sub[c].iloc[0]
                            if pd.notna(val):
                                serie_directa.append({'año': año, 'pob': int(val)})
                    except (ValueError, TypeError):
                        continue
    except Exception:
        pass

    if serie_directa:
        serie_directa.sort(key=lambda x: x['año'])
        # Proyección 2025/2027 si no existe
        años_existentes = {s['año'] for s in serie_directa}
        if 2020 in años_existentes and len(serie_directa) >= 2:
            s_ant = [s for s in serie_directa if s['año'] < 2020][-1]
            s_2020 = next(s for s in serie_directa if s['año'] == 2020)
            delta_años = 2020 - s_ant['año']
            tasa_anual = (s_2020['pob'] - s_ant['pob']) / max(delta_años, 1) if delta_años > 0 else 0
            if 2025 not in años_existentes:
                serie_directa.append({'año': 2025, 'pob': int(s_2020['pob'] + tasa_anual * 5)})
            if 2027 not in años_existentes:
                base_2025 = next((s['pob'] for s in serie_directa if s['año']==2025), s_2020['pob'])
                serie_directa.append({'año': 2027, 'pob': int(base_2025 + tasa_anual * 2)})
        serie_directa.sort(key=lambda x: x['año'])
        return serie_directa

    # FALLBACK: sintetizar serie a partir del Censo 2020 (hoja DEMOGRAFICOS)
    # con tasas de crecimiento típicas históricas de municipios de Chiapas.
    try:
        df_dem = pd.read_excel(XLSX, sheet_name='DEMOGRAFICOS')
        sub = df_dem[df_dem['MUNICIPIO'].astype(str).str.upper().str.strip() == municipio_key]
        if len(sub) == 0:
            return []
        pob_2020 = int(sub.iloc[0]['HABITANTES'])
    except Exception:
        return []

    # Tasas anuales históricas aproximadas Chiapas
    #   1990-1995: 3.5% / 1995-2000: 2.8% / 2000-2005: 2.0% / 2005-2010: 1.6%
    #   2010-2015: 1.4% / 2015-2020: 1.6% / 2020-2025: 1.2% / 2025-2027: 1.2%
    # Hacia atrás desde 2020:
    factores_atras = {1990: 0.563, 1995: 0.668, 2000: 0.767,
                       2005: 0.847, 2010: 0.918, 2015: 0.984}
    serie = []
    for año, factor in factores_atras.items():
        serie.append({'año': año, 'pob': int(pob_2020 * factor)})
    serie.append({'año': 2020, 'pob': pob_2020})
    # Hacia adelante (extrapolación a tasa 1.2%):
    serie.append({'año': 2025, 'pob': int(pob_2020 * (1.012 ** 5))})
    serie.append({'año': 2027, 'pob': int(pob_2020 * (1.012 ** 7))})
    serie.sort(key=lambda x: x['año'])
    print(f"  Serie poblacional sintetizada desde DEMOGRAFICOS (pob 2020 = {pob_2020:,})")
    return serie

data['poblacion_municipio'] = cargar_poblacion(MUNICIPIO_KEY)
# Alias legacy: pages_indicadores.py v8 lee 'poblacion_tuxtla'
data['poblacion_tuxtla'] = data['poblacion_municipio']
print(f"  Serie poblacional: {len(data['poblacion_municipio'])} puntos")


# ════════════════════════════════════════════════════════════════
# INDICADOR 5: Radar de fortalezas (4 dimensiones REALES, por partidos
# relevantes dinámicos del municipio — top 3 ó 4 según hoja 2024 B)
#
# Refactor Fase 2: se eliminaron las dimensiones inventadas
# "Crecimiento histórico" y "Penetración urbana" (hardcoded 92/38/65 y
# 72/65/45) y la dimensión duplicada "Bastiones seguros" (= cobertura).
# Las 4 que quedan son todas derivables del Excel sin heurísticas.
# ════════════════════════════════════════════════════════════════
print("\nIndicador 5: Radar de fortalezas (4 dims, partidos relevantes)...")

import partidos_relevantes as PR_mod  # noqa
partidos_rel = PR_mod.obtener_partidos_relevantes(MUNICIPIO_KEY, XLSX)

df_gp = pd.read_excel(XLSX, sheet_name='GANADOR PARTIDO 2024')
mun_gp = df_gp[df_gp['MUNICIPIO'].astype(str).str.strip()==MUNICIPIO_KEY].copy()
mun_gp = mun_gp.drop_duplicates(subset=['SECCION'])

df_ay = pd.read_excel(XLSX, sheet_name='AYUNTAMIENTO 2024')
mun_ay = df_ay[df_ay['MUNICIPIO'].astype(str).str.strip()==MUNICIPIO_KEY].copy()

# Mapeo clave corta → posibles nombres de columna en AYUNTAMIENTO 2024
COL_AY = {
    'MORENA': ['MORENA'], 'PAN': ['PAN'], 'PRI': ['PRI'], 'PRD': ['PRD'],
    'PT': ['PT'], 'PVEM': ['PVEM'], 'MC': ['MC'],
    'CHIAPAS UNIDO':   ['CHIAPAS UNIDO', 'PARTIDO CHIAPAS UNIDO'],
    'MOVER A CHIAPAS': ['MOVER A CHIAPAS', 'PARTIDO MOVER A CHIAPAS'],
    'PES': ['PES', 'PARTIDO ENCUENTRO SOLIDARIO'],
    'PPC': ['PPC', 'PARTIDO POPULAR CHIAPANECO'],
    'RSP': ['RSP', 'REDES SOCIALES PROGRESISTAS'],
    'FXM': ['FXM', 'FUERZA POR MEXICO'],
}


def col_de(clave):
    for nombre in COL_AY.get(clave, [clave]):
        if nombre in mun_ay.columns:
            return nombre
    return None


ln_total = data['ln_total_municipio']
total_votos_mun = PR_mod.obtener_total_votos(MUNICIPIO_KEY, XLSX)

# Total de secciones: tomar el de mun_gp (deduplicado) que es consistente
# con el conteo "secciones_por_partido" de calc_datos_base.
total_secciones = int(len(mun_gp))

# Mapeo de "Partido Ganador" (nombres cortos en GANADOR PARTIDO 2024) → clave canónica
NORM = {
    'MORENA':'MORENA','PVEM':'PVEM','PAN':'PAN','PRI':'PRI','PRD':'PRD',
    'PT':'PT','MC':'MC',
}


def secs_ganadas(clave):
    return int(sum(
        1 for g in mun_gp['Partido Ganador'].astype(str).str.strip().str.upper()
        if NORM.get(g) == clave
    ))


def margen_en_bastiones(clave):
    """En las secciones donde el partido ganó, qué % promedio del voto válido sacó.
    Se calcula como votos_partido / suma_votos_relevantes en la sección."""
    col = col_de(clave)
    if col is None:
        return 0.0
    # Secciones donde gana
    secs_ganadas_set = set(
        int(r['SECCION'])
        for _, r in mun_gp.iterrows()
        if NORM.get(str(r['Partido Ganador']).strip().upper()) == clave
    )
    if not secs_ganadas_set:
        return 0.0
    # Total de votos válidos por sección (sum de las columnas de partidos relevantes)
    cols_rel = list({col_de(p['clave']) for p in partidos_rel if col_de(p['clave'])})
    if not cols_rel or col not in cols_rel:
        cols_rel = list(set(cols_rel + [col]))
    por_seccion = mun_ay.groupby('SECCION')[cols_rel].sum()
    por_seccion = por_seccion[por_seccion.index.isin(secs_ganadas_set)]
    if len(por_seccion) == 0:
        return 0.0
    total_rel = por_seccion[cols_rel].sum(axis=1)
    mask = total_rel > 0
    if not mask.any():
        return 0.0
    pct = (por_seccion.loc[mask, col] / total_rel[mask]) * 100
    return float(pct.mean())


radar = {}
raw = {}
for p in partidos_rel:
    clave = p['clave']
    votos = p['votos']
    pct_mun = p['pct_total']
    sg = secs_ganadas(clave)
    cobertura = (sg / max(total_secciones, 1)) * 100
    movilizacion = (votos / max(ln_total, 1)) * 100
    bastion_pct = margen_en_bastiones(clave)

    radar[clave] = {
        'Cobertura territorial': round(cobertura, 1),
        '% del voto total':      round(pct_mun, 1),
        'Movilización padrón':   round(movilizacion, 1),
        'Margen en bastiones':   round(bastion_pct, 1),
    }
    raw[clave] = {
        'votos': votos,
        'secs_ganadas': sg,
        'pct_total': pct_mun,
        'cobertura_pct': round(cobertura, 1),
        'movilizacion_pct': round(movilizacion, 1),
        'margen_bastiones_pct': round(bastion_pct, 1),
    }

data['radar'] = radar
data['radar_raw'] = raw
data['radar_partidos'] = [p['clave'] for p in partidos_rel]
print(f"  Radar calculado para: {data['radar_partidos']}")
for clave in data['radar_partidos']:
    r = raw[clave]
    print(f"    {clave:<18}  votos={r['votos']:>7,}  "
          f"cob={r['cobertura_pct']:>5.1f}%  "
          f"voto={r['pct_total']:>5.1f}%  "
          f"mov={r['movilizacion_pct']:>5.1f}%  "
          f"bastiones={r['margen_bastiones_pct']:>5.1f}%")


# ════════════════════════════════════════════════════════════════
# NUEVO Fase 2: Votación histórica 1998-2024 (antes hardcoded en pages_part1.py)
# Para cada elección se identifica el partido/coalición ganador y su voto.
# ════════════════════════════════════════════════════════════════
print("\nVotación histórica 1998-2024 (cálculo del Excel)...")

ELECCIONES_HIST = {
    1998: ('AYUNTAMIENTO 1998', 2),
    2001: ('AYUNTAMIENTO 2001', 2),
    2004: ('AYUNTAMIENTO 2004', 2),
    2007: ('AYUNTAMIENTO 2007', 2),
    2010: ('AYUNTAMIENTO 2010', 2),
    2012: ('AYUNTAMIENTO 2012', 2),
    2015: ('AYUNTAMIENTO 2015', 0),
    2018: ('AYUNTAMIENTO 2018', 0),
    2021: ('AYUNTAMIENTO 2021', 0),
    2024: ('AYUNTAMIENTO 2024', 0),
}

METADATA_COLS_HIST = {
    'Unnamed: 0','Unnamed: 1','CVE-DTO','CABECERA DISTRITAL','  CABECERA DISTRITAL',
    'CVE-MPIO','MUNICIPIO','AÑO','Columna1','SECCION','CASILLA','LISTA NOMINAL',
    'TIPO CASILLA','ID CASILLA','EXT CONTIGUA','URNA ELECTRONICA','CIRCUNSCRIPCION',
    'ID ESTADO','NOMBRE ESTADO','ID DISTRITO LOCAL','CABECERA DISTRITAL LOCAL',
    'ID MUNICIPIO','ESTADO','LISTANOMINAL','ACTA CASILLA MEC',
    'NO REGISTRADOS',' NO REGISTRADOS',
    'VOTOS VALIDOS','  VOTOS VALIDOS','VOTOS NULOS','  VOTOS NULOS',
    'TOTAL VOTOS','TOTAL DE VOTOS','VOTACION TOTAL','VOTAC1ION TOTAL',
    '% VOTACION','% PARTICIPACIÓN','% PARTICIPACION',
    'GANADOR','PARTIDO GANADOR','ESTATUS ACTA','TRIBUNAL',
    'OBSERVACIONES','RUTA ACTA','JUSTA',
    # Agregadoras detectadas en AYUNTAMIENTO 2018/2021 que NO son partidos:
    'VOTACION MAXIMA','Votacion Maxima',
}

def familia_partido(nombre):
    """
    Mapea el nombre de un partido/coalición a su sigla corta.
    Para coaliciones, identifica el partido dominante usando la misma
    lógica de prioridad que generar_historico_secciones.py del mapa.
    Así los votos y partidos cuadran entre PDF y plataforma web.
    """
    n = str(nombre).upper().strip()

    PRIORIDAD = [
        ('MORENA',  ['MORENA']),
        ('PAN',     ['ACCION NACIONAL', ' PAN ', 'PAN-', '-PAN']),
        ('PRI',     ['REVOLUCIONARIO INSTITUCIONAL', ' PRI ', 'PRI-', '-PRI', 'PRI -']),
        ('PRD',     ['REVOLUCION DEMOCRATICA', ' PRD ', 'PRD-', '-PRD']),
        ('PT',      ['PARTIDO DEL TRABAJO', ' PT ', 'PT-', '-PT']),
        ('MC',      ['MOVIMIENTO CIUDADANO', 'CONVERGENCIA', ' MC ', 'MC-', '-MC']),
        ('PCHU',    ['CHIAPAS UNIDO', ' PCHU', ' PCU']),
        ('PMCH',    ['MOVER A CHIAPAS', 'PMCH']),
        ('PPCH',    ['POPULAR CHIAPANECO', 'PPCH', ' PPC']),
        ('PES',     ['ENCUENTRO SOLIDARIO', 'ENCUENTRO SOCIAL', ' PES']),
        ('RSP',     ['REDES SOCIALES', ' RSP']),
        ('FXM',     ['FUERZA POR MEXICO', ' FXM']),
        ('PVEM',    ['VERDE ECOLOGISTA', 'PVEM']),
        ('PANAL',   ['NUEVA ALIANZA', 'PANAL', ' NA ']),
        ('INDEP',   ['INDEPENDIENTE', 'CANDIDATO IND']),
    ]

    es_coalicion = (' - ' in n or
                    'UNIDOS POR CHIAPAS' in n or
                    'UNIDAD POR CHIAPAS' in n or
                    'COALICION' in n or
                    'JUNTOS' in n or
                    'FRENTE AMPLIO' in n or
                    'COMPROMISO' in n)

    if es_coalicion:
        for sigla, tokens in PRIORIDAD:
            for tok in tokens:
                if tok in n:
                    return sigla
        return 'COAL'

    for sigla, tokens in PRIORIDAD:
        for tok in tokens:
            if tok in n:
                return sigla

    return n[:6] if n else 'N/D'

# Cargar catálogo oficial de ganadores desde GANADORES AYUNTAMIENTO
try:
    df_gan = pd.read_excel(XLSX, sheet_name='GANADORES AYUNTAMIENTO')
    # Normalizar nombre del municipio
    col_mun_gan = next((c for c in df_gan.columns if 'MUNICIPIO' in str(c).upper()), None)
    col_ano_gan = next((c for c in df_gan.columns if 'AÑO' in str(c).upper() or 'ANO' in str(c).upper() or 'ELECCION' in str(c).upper()), None)
    col_par_gan = next((c for c in df_gan.columns if 'PARTIDO' in str(c).upper()), None)
    ganadores_oficiales = {}
    if col_mun_gan and col_ano_gan and col_par_gan:
        sub_gan = df_gan[df_gan[col_mun_gan].astype(str).str.upper().str.strip() == MUNICIPIO_KEY]
        for _, row in sub_gan.iterrows():
            try:
                ano = int(row[col_ano_gan])
                partido = str(row[col_par_gan]).strip()
                ganadores_oficiales[ano] = partido
            except:
                continue
except Exception as e:
    print(f"  ⚠️  No se pudo leer GANADORES AYUNTAMIENTO: {e}")
    ganadores_oficiales = {}

votacion_historica = []
for año, (hoja, hdr) in ELECCIONES_HIST.items():
    try:
        df_h = pd.read_excel(XLSX, sheet_name=hoja, header=hdr)
    except Exception as e:
        print(f"  ⚠️  No se pudo leer {hoja}: {e}")
        continue
    if 'MUNICIPIO' not in df_h.columns:
        continue
    sub = df_h[df_h['MUNICIPIO']==MUNICIPIO_KEY].copy()
    if len(sub) == 0:
        continue
    voto_cols = [c for c in sub.columns if c not in METADATA_COLS_HIST
                 and sub[c].dtype in ['float64','int64']]
    if not voto_cols:
        continue

    # Sumar votos por familia de partido (agrupa partido solo + todas sus coaliciones)
    totales_raw = sub[voto_cols].fillna(0).sum()
    totales_familia = {}
    for col, votos in totales_raw.items():
        if votos <= 0:
            continue
        fam = familia_partido(col)
        totales_familia[fam] = totales_familia.get(fam, 0) + int(votos)

    if not totales_familia:
        continue

    # Votos del ganador = mayor total entre todas las familias
    votos_ganador = max(totales_familia.values())

    # Partido ganador = fuente oficial GANADORES AYUNTAMIENTO
    if año in ganadores_oficiales:
        partido_oficial = ganadores_oficiales[año]
        # Convertir nombre largo a sigla si es necesario
        ganador_fam = familia_partido(partido_oficial)
    else:
        ganador_fam = max(totales_familia, key=totales_familia.get)

    votacion_historica.append({
        'año': año,
        'votos': votos_ganador,
        'partido': ganador_fam,
        'col_ganadora': ganador_fam,
    })

data['votacion_historica'] = votacion_historica
print(f"  Histórico ganador por elección ({len(votacion_historica)} elecciones):")
for v in votacion_historica:
    print(f"    {v['año']}: {v['votos']:>6,} votos · {v['partido']} ({v['col_ganadora']})")


# ════════════════════════════════════════════════════════════════
# PARTICIPACIÓN MUNICIPAL HISTÓRICA 2015-2024
# Calcula desde hoja PROYECCION VOTACION 2027 (LN × participación)
# ════════════════════════════════════════════════════════════════
print("\nParticipación municipal histórica 2015-2024...")
data['participacion_municipal'] = []
# FIX (v11.3): la hoja PROYECCION VOTACION 2027 tiene datos desalineados o ceros
# para muchos municipios. La fuente confiable son las hojas AYUNTAMIENTO_<año>
# donde sumamos TOTAL VOTOS / LISTA NOMINAL a nivel municipio.
HOJAS_PART = [
    (2015, 'AYUNTAMIENTO 2015'),
    (2018, 'AYUNTAMIENTO 2018'),
    (2021, 'AYUNTAMIENTO 2021'),
    (2024, 'AYUNTAMIENTO 2024'),
]
for año, hoja in HOJAS_PART:
    try:
        df_ay = pd.read_excel(XLSX, sheet_name=hoja)
        sub = df_ay[df_ay['MUNICIPIO'].astype(str).str.upper().str.strip() == MUNICIPIO_KEY]
        if len(sub) == 0:
            continue
        # Buscar columnas tolerando variaciones de nombre
        ln_col = next((c for c in df_ay.columns if 'NOMINAL' in str(c).upper()), None)
        votos_col = next((c for c in df_ay.columns
                          if 'TOTAL VOTOS' in str(c).upper() or 'VOTACION TOTAL' in str(c).upper()), None)
        if not ln_col or not votos_col:
            print(f"  ⚠️  {año}: no se encontraron columnas LN/votos en {hoja}")
            continue
        ln_tot = pd.to_numeric(sub[ln_col], errors='coerce').fillna(0).sum()
        votos_tot = pd.to_numeric(sub[votos_col], errors='coerce').fillna(0).sum()
        if ln_tot > 0:
            pct = round(votos_tot / ln_tot * 100, 1)
            data['participacion_municipal'].append({'año': año, 'pct': pct})
            print(f"  {año}: LN={ln_tot:,.0f}, votos={votos_tot:,.0f} → participación {pct}%")
    except Exception as e:
        print(f"  ⚠️  {año}: error leyendo {hoja}: {e}")


# ════════════════════════════════════════════════════════════════
# Guardar
# ════════════════════════════════════════════════════════════════
out_path = archivo_indicadores()
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
print(f"\n✓ Datos indicadores guardados en {out_path}")
