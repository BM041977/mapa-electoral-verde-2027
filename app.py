from flask import Flask, render_template, request, redirect, session, jsonify, send_file, Response
from functools import wraps
import os
import json
import re
import unicodedata

def _cargar_usuarios():
    try:
        with open("usuarios.json", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

import hmac
from datetime import timedelta
from bitacora import init_bitacora, registrar_acceso

app = Flask(__name__)
init_bitacora(app)

@app.before_request
def _log_acceso():
    registrar_acceso()

app.secret_key = os.environ.get("SECRET_KEY", "clave_super_segura")
app.permanent_session_lifetime = timedelta(minutes=20)
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"]   = os.environ.get("HTTPS", "0") == "1"

OWNER             = "Baldemar Maza León"
TELEFONO          = "961 217 0091"
AVISO_PROPIEDAD   = f"Este sistema es un desarrollo independiente propiedad de {OWNER} · {TELEFONO}"

USER     = os.environ.get("APP_USER", "Baldemar")
PASSWORD = os.environ.get("APP_PASSWORD", "Victoria@Ever")

BASE_DIR            = os.path.dirname(os.path.abspath(__file__))
MAPA_HTML           = os.path.join(BASE_DIR, "templates", "mapa_ligero.html")
MAPA_PARTIDOS_HTML  = os.path.join(BASE_DIR, "templates", "mapa_por_partido.html")
HISTORICO_HTML      = os.path.join(BASE_DIR, "templates", "historico.html")
GEOJSON_PATH        = os.path.join(BASE_DIR, "secciones_simplificado.geojson")
SECCIONES_JSON_PATH = os.path.join(BASE_DIR, "secciones.json")

_geojson_cache = None

def _cargar_geojson():
    global _geojson_cache
    if _geojson_cache is None:
        with open(GEOJSON_PATH, "r", encoding="utf-8") as f:
            _geojson_cache = json.load(f)
    return _geojson_cache

_secciones_cache = None

def _cargar_secciones():
    global _secciones_cache
    if _secciones_cache is None:
        with open(SECCIONES_JSON_PATH, "r", encoding="utf-8") as f:
            _secciones_cache = json.load(f)
    return _secciones_cache

@app.context_processor
def inject_owner():
    return {
        "owner": OWNER,
        "telefono": TELEFONO,
        "aviso_propiedad": AVISO_PROPIEDAD,
        "usuario": session.get("usuario", "usuario"),
        "ip_cliente": _ip_cliente(),
        "municipio": session.get("municipio", ""),
    }

@app.after_request
def no_cache(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"]        = "no-cache"
    response.headers["Expires"]       = "0"
    return response

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect("/")
        return f(*args, **kwargs)
    return wrapper

def nombre_bonito(archivo):
    nombre = archivo.replace("Diagnostico_Electoral_Municipio_de_", "").replace("Diagnostico_Electoral_", "")
    nombre = nombre.replace("_v8.pdf", "").replace(".pdf", "")
    palabras = nombre.split("_")
    minusculas = {"De", "Del", "La", "Las", "Los", "El", "Y", "A"}
    resultado = []
    for i, p in enumerate(palabras):
        if i == 0:
            resultado.append(p.capitalize())
        elif p in minusculas:
            resultado.append(p.lower())
        else:
            resultado.append(p.capitalize())
    return " ".join(resultado)

@app.route("/", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        usuario  = request.form.get("usuario", "").strip()
        password = request.form.get("password", "").strip()
        usuario_ok  = hmac.compare_digest(usuario,  USER)
        password_ok = hmac.compare_digest(password, PASSWORD)
        if usuario_ok and password_ok:
            session["logged_in"] = True
            session["es_maestro"] = True
            session["usuario"] = usuario
            session.permanent = True
            return redirect("/inicio")
        usuarios_muni = _cargar_usuarios()
        if usuario in usuarios_muni:
            if hmac.compare_digest(password, usuarios_muni[usuario]["password"]):
                session["logged_in"] = True
                session["es_maestro"] = False
                session["municipio"] = usuarios_muni[usuario]["municipio"]
                session["usuario"] = usuario
                session.permanent = True
                muni_url = usuarios_muni[usuario]["municipio"].replace(" ", "_")
                return redirect("/inicio")
        return render_template("login.html", error="Usuario o contraseña incorrectos")
    return render_template("login.html")

@app.route("/inicio")
@login_required
def inicio():
    return render_template("index.html")

def _ip_cliente():
    forwarded = request.headers.get("X-Forwarded-For", "")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.remote_addr or "desconocida"

def _inyectar_sesion(html, cierre, usuario, ip_cliente, municipio):
    bloque = (
        f'<script>\n'
        f'  window.SESION = {{\n'
        f'    usuario: "{usuario}",\n'
        f'    ip: "{ip_cliente}",\n'
        f'    municipio: "{municipio}"\n'
        f'  }};\n'
        f'</script>\n'
        f'<script src="/static/marca_agua.js"></script>\n'
        f'{cierre}'
    )
    return html.replace(cierre, bloque, 1)

@app.route("/mapa")
@login_required
def mapa():
    with open(MAPA_HTML, encoding="utf-8") as f:
        html = f.read()
    html = _inyectar_sesion(
        html,
        "</html>",
        session.get("usuario", "usuario"),
        _ip_cliente(),
        session.get("municipio", ""),
    )
    return Response(html, mimetype="text/html")

@app.route("/mapa-partidos")
@login_required
def mapa_partidos():
    with open(MAPA_PARTIDOS_HTML, encoding="utf-8") as f:
        html = f.read()
    html = _inyectar_sesion(
        html,
        "</body>",
        session.get("usuario", "usuario"),
        _ip_cliente(),
        session.get("municipio", ""),
    )
    return Response(html, mimetype="text/html")

@app.route("/api/mi-municipio")
@login_required
def api_mi_municipio():
    es_maestro = session.get("es_maestro", True)
    municipio = "" if es_maestro else session.get("municipio", "")
    return jsonify({"municipio": municipio})

@app.route("/diagnosticos")
@login_required
def diagnosticos():
    # static/pdfs/ no se sube a este repo a propósito (los diagnósticos de
    # este sitio se entregan de forma impresa) — por eso NO usamos
    # os.listdir directo: si la carpeta no existe, os.listdir lanza
    # FileNotFoundError y tumba la ruta con un 500. isdir() la evita y deja
    # que la plantilla muestre la leyenda correspondiente con municipios=[].
    pdf_dir = os.path.join(app.static_folder, "pdfs")
    if os.path.isdir(pdf_dir):
        archivos = sorted([f for f in os.listdir(pdf_dir) if f.endswith(".pdf")])
    else:
        archivos = []
    es_maestro = session.get("es_maestro", True)
    municipio_sesion = session.get("municipio", "")
    if not es_maestro and municipio_sesion:
        archivos = [f for f in archivos if municipio_sesion.replace(" ", "_") in f]
    municipios = [{"archivo": f, "nombre": nombre_bonito(f), "url": f"/static/pdfs/{f}"} for f in archivos]
    return render_template("diagnosticos.html", municipios=municipios, owner=OWNER)

@app.route("/ver-pdf/<municipio>")
@login_required
def ver_pdf(municipio):
    pdf_dir = os.path.join(app.static_folder, "pdfs")
    archivos = [f for f in os.listdir(pdf_dir) if f.endswith(".pdf")]
    archivo = next((f for f in archivos if municipio in f), None)
    if not archivo:
        return "PDF no encontrado", 404
    es_maestro = session.get("es_maestro", True)
    return render_template("visor_pdf.html", municipio=municipio.replace("_", " "), owner=OWNER, es_maestro=es_maestro, archivo=archivo)

@app.route("/geojson/secciones")
@login_required
def geojson_secciones():
    return jsonify(_cargar_geojson())

@app.route("/datos-secciones")
@login_required
def datos_secciones():
    data = _cargar_secciones()
    es_maestro = session.get("es_maestro", True)
    municipio_filtro = "" if es_maestro else session.get("municipio", "")
    return render_template("datos_secciones.html", meta=data["meta"], municipio_filtro=municipio_filtro, es_maestro=es_maestro)

@app.route("/api/secciones")
@login_required
def api_secciones():
    data = _cargar_secciones()
    return jsonify(data["secciones"])

@app.route("/api/meta")
@login_required
def api_meta():
    data = _cargar_secciones()
    return jsonify(data["meta"])

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/historico")
@login_required
def historico():
    es_maestro = session.get("es_maestro", True)
    municipio_usuario = "" if es_maestro else session.get("municipio", "")
    return render_template(
        "historico.html",
        es_master=es_maestro,
        municipio_usuario=municipio_usuario
    )

# ════════════════════════════════════════════════════════════════
# PRESIDENTES MUNICIPALES HISTÓRICOS — datos del pipeline de PDFs
# ════════════════════════════════════════════════════════════════
# ⚠️ Estas rutas viven fuera de este repo (paquete_v11_final no está
# en git ni se despliega a Render). Funciona en local; en producción
# devolverá 404 hasta que se decida cómo sincronizar esos JSON.
PIPELINE_DATOS_DIR = os.environ.get(
    "PIPELINE_DATOS_DIR",
    r"C:\Users\Baldemar Maza\Documents\chiapas_2027\paquete-v11.13-CHIAPAS-2027\paquete_v11_final",
)

def _slug_municipio(municipio_key):
    """'TUXTLA GUTIERREZ' -> 'tuxtla_gutierrez' (mismo slug que municipio_config.py)."""
    return municipio_key.title().replace(' ', '_').lower()

def _archivo_datos_pipeline(municipio_key):
    if municipio_key == "TUXTLA GUTIERREZ":
        return os.path.join(PIPELINE_DATOS_DIR, "datos_tuxtla.json")
    return os.path.join(PIPELINE_DATOS_DIR, f"datos_{_slug_municipio(municipio_key)}.json")

def _archivo_estrategicas_pipeline(municipio_key):
    if municipio_key == "TUXTLA GUTIERREZ":
        return os.path.join(PIPELINE_DATOS_DIR, "datos_estrategicas.json")
    return os.path.join(PIPELINE_DATOS_DIR, f"datos_estrategicas_{_slug_municipio(municipio_key)}.json")

_candidatos_cache = None
def _cargar_candidatos():
    global _candidatos_cache
    if _candidatos_cache is None:
        path = os.path.join(app.static_folder, 'data', 'historico_candidatos.json')
        with open(path, 'r', encoding='utf-8') as f:
            _candidatos_cache = json.load(f)
    return _candidatos_cache
@app.route('/candidatos')
@login_required
def candidatos():
    es_maestro = session.get("es_maestro", True)
    return render_template('candidatos.html', es_maestro=es_maestro)
@app.route('/api/candidatos/buscar')
@login_required
def api_buscar_candidatos():
    es_maestro = session.get("es_maestro", True)
    if not es_maestro:
        return jsonify({"error": "no autorizado"}), 403
    q = request.args.get('q', '').strip().upper()
    if len(q) < 3:
        return jsonify({"resultados": []})
    data = _cargar_candidatos()
    resultados = []
    for nombre in data['perfiles'].keys():
        if q in nombre:
            resultados.append(nombre)
            if len(resultados) >= 20:
                break
    return jsonify({"resultados": sorted(resultados)})
@app.route('/api/candidatos/perfil')
@login_required
def api_perfil_candidato():
    es_maestro = session.get("es_maestro", True)
    nombre = request.args.get('nombre', '').strip().upper()
    data = _cargar_candidatos()
    perfil = data['perfiles'].get(nombre)
    if not perfil:
        return jsonify({"error": "no encontrado"}), 404
    if not es_maestro:
        municipio_sesion = session.get("municipio", "").strip().upper()
        if municipio_sesion not in perfil.get('municipios', []):
            return jsonify({"error": "no autorizado"}), 403
    return jsonify(perfil)
@app.route('/api/candidatos/municipio/<municipio>')
@login_required
def api_candidatos_municipio(municipio):
    es_maestro = session.get("es_maestro", True)
    municipio_sesion = session.get("municipio", "")
    municipio_norm = municipio.strip().upper().replace('_', ' ')
    if not es_maestro and municipio_norm != municipio_sesion.strip().upper():
        return jsonify({"error": "no autorizado"}), 403
    data = _cargar_candidatos()
    resultado = []
    for nombre, perfil in data['perfiles'].items():
        if 'CANCELADO' in nombre.upper():
            continue
        if municipio_norm in perfil['municipios'] and perfil['total_participaciones'] > 1:
            anos_en_municipio = sorted({
                h.get('ano') for h in perfil.get('historial', [])
                if str(h.get('municipio', '')).strip().upper() == municipio_norm
            })
            historial_en_municipio = sorted(
                [
                    {
                        'ano': h.get('ano'),
                        'cargo': h.get('cargo'),
                        'partido': h.get('partido'),
                        'gano': h.get('gano', False),
                        'es_presidente': h.get('es_presidente', False),
                    }
                    for h in perfil.get('historial', [])
                    if str(h.get('municipio', '')).strip().upper() == municipio_norm
                ],
                key=lambda h: h['ano'],
                reverse=True,
            )
            resultado.append({
                'nombre': nombre,
                'total_participaciones': perfil['total_participaciones'],
                'anos': perfil['anos'],
                'anos_en_municipio': anos_en_municipio,
                'historial_en_municipio': historial_en_municipio,
                'partidos': perfil['partidos'],
                'veces_gano_presidente': perfil['veces_gano_presidente'],
                'veces_candidato_presidente': perfil['veces_candidato_presidente'],
                'posible_homonimo': perfil.get('posible_homonimo', False),
            })
    resultado.sort(key=lambda x: -x['total_participaciones'])
    return jsonify({"candidatos": resultado})

@app.route('/api/candidatos/presidentes/<municipio>')
@login_required
def api_presidentes_municipio(municipio):
    es_maestro = session.get("es_maestro", True)
    municipio_sesion = session.get("municipio", "")
    municipio_norm = municipio.strip().upper().replace('_', ' ')
    if not es_maestro and municipio_norm != municipio_sesion.strip().upper():
        return jsonify({"error": "no autorizado"}), 403

    ruta_datos = _archivo_datos_pipeline(municipio_norm)
    if not os.path.exists(ruta_datos):
        return jsonify({"error": "municipio no encontrado"}), 404

    try:
        with open(ruta_datos, encoding='utf-8') as f:
            datos_base = json.load(f)
    except (json.JSONDecodeError, OSError):
        return jsonify({"error": "municipio no encontrado"}), 404

    presidentes_hist = datos_base.get('presidentes_historicos', [])

    margen_2024_votos = None
    margen_2024_pct = None
    ruta_estr = _archivo_estrategicas_pipeline(municipio_norm)
    if os.path.exists(ruta_estr):
        try:
            with open(ruta_estr, encoding='utf-8') as f:
                datos_estr = json.load(f)
            margen_2024_votos = datos_estr.get('margen_2024_votos')
            margen_2024_pct = datos_estr.get('margen_2024_pct')
        except (json.JSONDecodeError, OSError):
            pass  # margen queda en None si el archivo de estratégicas falla

    presidentes = []
    for p in presidentes_hist:
        anio = p.get('anio')
        es_2024 = (anio == 2024)
        presidentes.append({
            'anio': anio,
            'candidato': p.get('candidato'),
            'partido': p.get('partido'),
            'margen_votos': margen_2024_votos if es_2024 else None,
            'margen_pct': margen_2024_pct if es_2024 else None,
        })

    presidentes.sort(key=lambda x: x['anio'] or 0, reverse=True)

    return jsonify({"municipio": municipio_norm, "presidentes": presidentes})

# ════════════════════════════════════════════════════════════════
# PLANILLA POR AÑO/MUNICIPIO/PARTIDO — quién compitió y planilla completa
# ════════════════════════════════════════════════════════════════
def _normalizar_nombre(nombre):
    """Mayúsculas, sin acentos, espacios colapsados — para matchear nombres
    entre presidentes_historicos (Title Case, acentos inconsistentes) y
    historico_candidatos.json (MAYÚSCULAS)."""
    nfkd = unicodedata.normalize('NFKD', str(nombre or ''))
    sin_acentos = ''.join(c for c in nfkd if not unicodedata.combining(c))
    return re.sub(r'\s+', ' ', sin_acentos.strip().upper())

def _title_case_nombre(nombre):
    return str(nombre or '').title()

def _formatear_cargo(cargo):
    """Similar a _title_case_nombre pero corrige el efecto secundario de
    .title() sobre sufijos de ordinal pegados a números: "1ER"->"1Er" (mal)
    se corrige a "1er" (bien). El resto del texto (Presidente, Sindico,
    Regidor, Propietario, Suplente, "(A)") ya sale correcto con .title()."""
    texto = str(cargo or '').title()
    return re.sub(r'(\d+)([A-Za-z]+)', lambda m: m.group(1) + m.group(2).lower(), texto)

def _rango_cargo(cargo):
    """Cargo (str) -> (es_suplente, numero) para ordenar una planilla:
    Presidente(0) < Sindico(1) < 1er Regidor(2) < 2do Regidor(3) < ...,
    con todos los suplentes agrupados al final."""
    c = str(cargo or '').strip().upper()
    es_suplente = 'SUPLENTE' in c

    if c.startswith('PRESIDENTE'):
        numero = 0
    elif c.startswith('SINDICO') or c.startswith('SÍNDICO'):
        numero = 1
    elif 'REGIDOR' in c:
        m = re.match(r'^(\d+)[A-Z]*\s+REGIDOR', c)
        numero = (1 + int(m.group(1))) if m else 100
    else:
        numero = 999

    return (es_suplente, numero)

_indice_planillas = None
def _construir_indice_planillas():
    """Índice perezoso: (anio, municipio) -> [{nombre, cargo, partido}, ...],
    construido una sola vez a partir de historico_candidatos.json (ya cacheado
    por _cargar_candidatos()) y reutilizado en todos los requests siguientes."""
    global _indice_planillas
    if _indice_planillas is not None:
        return _indice_planillas
    data = _cargar_candidatos()
    indice = {}
    for nombre, perfil in data['perfiles'].items():
        for h in perfil.get('historial', []):
            anio = h.get('ano')
            municipio = str(h.get('municipio', '')).strip().upper()
            if anio is None or not municipio:
                continue
            indice.setdefault((anio, municipio), []).append({
                'nombre': nombre,
                'cargo': h.get('cargo'),
                'partido': h.get('partido'),
            })
    _indice_planillas = indice
    return _indice_planillas

@app.route('/api/candidatos/planilla/<municipio>/<int:ano>/<partido>')
@login_required
def api_planilla_candidato(municipio, ano, partido):
    es_maestro = session.get("es_maestro", True)
    municipio_sesion = session.get("municipio", "")
    municipio_norm = municipio.strip().upper().replace('_', ' ')
    if not es_maestro and municipio_norm != municipio_sesion.strip().upper():
        return jsonify({"error": "no autorizado"}), 403

    indice = _construir_indice_planillas()
    entradas = indice.get((ano, municipio_norm), [])

    # Resolver el partido real del ganador cruzando presidentes_historicos
    # (nombre, Title Case) con las entradas de historico_candidatos.json
    # (MAYÚSCULAS) para este año/municipio — el <partido> de la URL puede
    # venir en formato distinto (ej. coalición) al que usa cada candidato
    # individualmente en su historial.
    partido_resuelto = partido
    ruta_datos = _archivo_datos_pipeline(municipio_norm)
    if os.path.exists(ruta_datos):
        try:
            with open(ruta_datos, encoding='utf-8') as f:
                datos_base = json.load(f)
            ganador = next(
                (p.get('candidato') for p in datos_base.get('presidentes_historicos', [])
                 if p.get('anio') == ano),
                None
            )
            if ganador:
                objetivo = _normalizar_nombre(ganador)
                match = next(
                    (e for e in entradas
                     if str(e.get('cargo', '')).strip().upper().startswith('PRESIDENTE')
                     and _normalizar_nombre(e['nombre']) == objetivo),
                    None
                )
                if match:
                    partido_resuelto = match['partido']
        except (json.JSONDecodeError, OSError):
            pass  # si falla la lectura, seguimos con el partido de la URL

    compitio_contra = [
        {'nombre': _title_case_nombre(e['nombre']), 'cargo': _formatear_cargo(e['cargo']), 'partido': e['partido']}
        for e in entradas
        if str(e.get('cargo', '')).strip().upper().startswith('PRESIDENTE')
        and e.get('partido') != partido_resuelto
    ]

    planilla_ordenada = sorted(
        (e for e in entradas if e.get('partido') == partido_resuelto),
        key=lambda e: _rango_cargo(e.get('cargo'))
    )
    planilla = [{'nombre': _title_case_nombre(e['nombre']), 'cargo': _formatear_cargo(e['cargo'])} for e in planilla_ordenada]

    return jsonify({
        "municipio": municipio_norm,
        "anio": ano,
        "partido": partido,
        "compitio_contra": compitio_contra,
        "planilla": planilla,
    })

if __name__ == "__main__":
    app.run(debug=True)
