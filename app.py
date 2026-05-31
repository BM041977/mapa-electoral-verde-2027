from flask import Flask, render_template, request, redirect, session, jsonify, send_file
from functools import wraps
import os
import json
 
def _cargar_usuarios():
    try:
        with open("usuarios.json", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}
 
import hmac
from datetime import timedelta
 
app = Flask(__name__)
 
# CONFIGURACIÓN
app.secret_key = os.environ.get("SECRET_KEY", "clave_super_segura")
 
# SESIÓN DE 20 MINUTOS
app.permanent_session_lifetime = timedelta(minutes=20)
 
# SEGURIDAD DE COOKIES
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"]   = os.environ.get("HTTPS", "0") == "1"
 
# PROPIETARIO
OWNER             = "Baldemar Maza León"
TELEFONO          = "961 217 0091"
AVISO_PROPIEDAD   = f"Este sistema es un desarrollo independiente propiedad de {OWNER} · {TELEFONO}"
 
# USUARIO Y PASSWORD
USER     = os.environ.get("APP_USER", "Baldemar")
PASSWORD = os.environ.get("APP_PASSWORD", "Victoria@Ever")
 
# RUTAS DE ARCHIVOS
BASE_DIR            = os.path.dirname(os.path.abspath(__file__))
MAPA_HTML           = os.path.join(BASE_DIR, "templates", "mapa_ligero.html")
MAPA_PARTIDOS_HTML  = os.path.join(BASE_DIR, "templates", "mapa_por_partido.html")
GEOJSON_PATH        = os.path.join(BASE_DIR, "secciones_simplificado.geojson")
SECCIONES_JSON_PATH = os.path.join(BASE_DIR, "secciones.json")
 
# CACHE DEL GEOJSON
_geojson_cache = None
 
def _cargar_geojson():
    global _geojson_cache
    if _geojson_cache is None:
        with open(GEOJSON_PATH, "r", encoding="utf-8") as f:
            _geojson_cache = json.load(f)
    return _geojson_cache
 
# CACHE DEL DATASET DE SECCIONES
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
        "owner":           OWNER,
        "telefono":        TELEFONO,
        "aviso_propiedad": AVISO_PROPIEDAD,
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
    nombre = archivo.replace("Diagnostico_Electoral_", "").replace("_v8.pdf", "")
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
 
# LOGIN
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
            session.permanent = True
            return redirect("/inicio")
        usuarios_muni = _cargar_usuarios()
        if usuario in usuarios_muni:
            if hmac.compare_digest(password, usuarios_muni[usuario]["password"]):
                session["logged_in"] = True
                session["es_maestro"] = False
                session["municipio"] = usuarios_muni[usuario]["municipio"]
                session.permanent = True
                muni_url = usuarios_muni[usuario]["municipio"].replace(" ", "_")
                return redirect(f"/ver-pdf/{muni_url}")
        return render_template("login.html", error="Usuario o contraseña incorrectos")
    return render_template("login.html")
 
# INICIO
@app.route("/inicio")
@login_required
def inicio():
    return render_template("index.html")
 
# MAPA SECCIÓN
@app.route("/mapa")
@login_required
def mapa():
    return send_file(MAPA_HTML)    
es_maestro = session.get("es_maestro", True)
    municipio_filtro = "" if es_maestro else session.get("municipio", "")
    return render_template("mapa_ligero.html", municipio_filtro=municipio_filtro)
 
# MAPA POR PARTIDO
@app.route("/mapa-partidos")
@login_required
def mapa_partidos():
    return send_file(MAPA_PARTIDOS_HTML)
    es_maestro = session.get("es_maestro", True)
    municipio_filtro = "" if es_maestro else session.get("municipio", "")
    return render_template("mapa_por_partido.html", municipio_filtro=municipio_filtro)
 
@app.route("/diagnosticos")
@login_required
def diagnosticos():
    pdf_dir = os.path.join(app.static_folder, "pdfs")
    archivos = sorted([f for f in os.listdir(pdf_dir) if f.endswith(".pdf")])
    es_maestro = session.get("es_maestro", True)
    municipio_sesion = session.get("municipio", "")
    if not es_maestro and municipio_sesion:
        archivos = [f for f in archivos if municipio_sesion.replace(" ", "_") in f]
    municipios = [
        {
            "archivo": f,
            "nombre": nombre_bonito(f),
            "url": f"/static/pdfs/{f}"
        }
        for f in archivos
    ]
    return render_template("diagnosticos.html", municipios=municipios, owner=OWNER)
 
@app.route("/ver-pdf/<municipio>")
@login_required
def ver_pdf(municipio):
    pdf_dir = os.path.join(app.static_folder, "pdfs")
    archivos = [f for f in os.listdir(pdf_dir) if f.endswith(".pdf")]
    archivo = next((f for f in archivos if municipio in f), None)
    if not archivo:
        return "PDF no encontrado", 404
    return render_template("visor_pdf.html", municipio=municipio.replace("_", " "), owner=OWNER)
 
# GEOJSON
@app.route("/geojson/secciones")
@login_required
def geojson_secciones():
    return jsonify(_cargar_geojson())
 
# DATOS POR SECCIÓN
@app.route("/datos-secciones")
@login_required
def datos_secciones():
    data = _cargar_secciones()
    es_maestro = session.get("es_maestro", True)
    municipio_filtro = "" if es_maestro else session.get("municipio", "")
    return render_template("datos_secciones.html", meta=data["meta"], municipio_filtro=municipio_filtro)
 
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
 
# LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
 
if __name__ == "__main__":
    app.run(debug=True)
