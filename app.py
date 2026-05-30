from flask import Flask, render_template, request, redirect, session, jsonify, send_file
from functools import wraps
import os
import json
import hmac
from datetime import timedelta

app = Flask(__name__)

# 🔐 CONFIGURACIÓN
app.secret_key = os.environ.get("SECRET_KEY", "clave_super_segura")

# ⏳ SESIÓN DE 20 MINUTOS
app.permanent_session_lifetime = timedelta(minutes=20)

# 🍪 SEGURIDAD DE COOKIES
app.config["SESSION_COOKIE_HTTPONLY"] = True                              # JS no puede leer la cookie
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"                             # mitiga CSRF
app.config["SESSION_COOKIE_SECURE"]   = os.environ.get("HTTPS", "0") == "1"  # solo HTTPS en producción

# 👤 PROPIETARIO
OWNER             = "Baldemar Maza León"
TELEFONO          = "961 217 0091"
AVISO_PROPIEDAD   = f"Este sistema es un desarrollo independiente propiedad de {OWNER} · {TELEFONO}"

# 🔐 USUARIO Y PASSWORD
USER     = os.environ.get("APP_USER", "Baldemar")
PASSWORD = os.environ.get("APP_PASSWORD", "Victoria@Ever")

# 📂 RUTAS DE ARCHIVOS
BASE_DIR            = os.path.dirname(os.path.abspath(__file__))
MAPA_HTML           = os.path.join(BASE_DIR, "templates", "mapa_ligero.html")
MAPA_PARTIDOS_HTML  = os.path.join(BASE_DIR, "templates", "mapa_por_partido.html")  # 🆕
GEOJSON_PATH        = os.path.join(BASE_DIR, "secciones_simplificado.geojson")
SECCIONES_JSON_PATH = os.path.join(BASE_DIR, "secciones.json")                       # 🆕 FASE 3

# 💾 CACHE DEL GEOJSON (se carga UNA vez, no en cada request)
_geojson_cache = None

def _cargar_geojson():
    global _geojson_cache
    if _geojson_cache is None:
        with open(GEOJSON_PATH, "r", encoding="utf-8") as f:
            _geojson_cache = json.load(f)
    return _geojson_cache

# 💾 CACHE DEL DATASET DE SECCIONES (FASE 3 — Dashboard)
_secciones_cache = None

def _cargar_secciones():
    """Carga secciones.json una sola vez al primer acceso."""
    global _secciones_cache
    if _secciones_cache is None:
        with open(SECCIONES_JSON_PATH, "r", encoding="utf-8") as f:
            _secciones_cache = json.load(f)
    return _secciones_cache

# 🌐 INYECTAR DATOS DE PROPIETARIO EN TODOS LOS TEMPLATES
# (en cualquier .html puedes usar {{ owner }}, {{ telefono }}, {{ aviso_propiedad }})
@app.context_processor
def inject_owner():
    return {
        "owner":           OWNER,
        "telefono":        TELEFONO,
        "aviso_propiedad": AVISO_PROPIEDAD,
    }

# 🔒 EVITAR CACHE DEL NAVEGADOR
@app.after_request
def no_cache(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"]        = "no-cache"
    response.headers["Expires"]       = "0"
    return response

# 🛡️ DECORADOR DE AUTENTICACIÓN
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

# -----------------------------
# LOGIN
# -----------------------------
@app.route("/", methods=["GET", "POST"])
def login():

    # 🔴 SIEMPRE PEDIR LOGIN AL ABRIR LA RAÍZ
    session.clear()

    if request.method == "POST":

        usuario  = request.form.get("usuario", "").strip()
        password = request.form.get("password", "").strip()

        # 🛡️ COMPARACIÓN A PRUEBA DE TIMING ATTACKS
        usuario_ok  = hmac.compare_digest(usuario,  USER)
        password_ok = hmac.compare_digest(password, PASSWORD)

        if usuario_ok and password_ok:

            session["logged_in"] = True
            session.permanent    = True   # ⚡ CLAVE: activa los 3 min del lado servidor

            return redirect("/inicio")    # 🔄 antes era /mapa, ahora va a la landing

        return render_template(
            "login.html",
            error="Usuario o contraseña incorrectos"
        )

    return render_template("login.html")

# -----------------------------
# 🆕 LANDING / INICIO (menú de mapas)
# -----------------------------
@app.route("/inicio")
@login_required
def inicio():
    return render_template("index.html")

# -----------------------------
# MAPA SECCIÓN (el que ya tenías)
# -----------------------------
@app.route("/mapa")
@login_required
def mapa():
    # ⚠️ NO usar render_template: el archivo pesa 16 MB y Jinja lo parsearía
    # en cada request. send_file lo manda crudo, sin tocar plantillas.
    return send_file(MAPA_HTML)

# -----------------------------
# 🆕 MAPA POR PARTIDO
# -----------------------------
@app.route("/mapa-partidos")
@login_required
def mapa_partidos():
    # Mismo razonamiento: 3.7 MB, mejor servirlo crudo sin Jinja.
    return send_file(MAPA_PARTIDOS_HTML)


@app.route("/diagnosticos")
@login_required
def diagnosticos():
    pdf_dir = os.path.join(app.static_folder, "pdfs")
    archivos = sorted([f for f in os.listdir(pdf_dir) if f.endswith(".pdf")])
    municipios = [
        {
            "archivo": f,
            "nombre": nombre_bonito(f),
            "url": f"/static/pdfs/{f}"
        }
        for f in archivos
    ]
    return render_template("diagnosticos.html", municipios=municipios, owner=OWNER)

# -----------------------------
# GEOJSON (protegido)
# -----------------------------
@app.route("/geojson/secciones")
@login_required
def geojson_secciones():
    return jsonify(_cargar_geojson())

# ════════════════════════════════════════════════════════════════
# 🆕 FASE 3 — DASHBOARD DE DATOS POR SECCIÓN
# ════════════════════════════════════════════════════════════════

@app.route("/datos-secciones")
@login_required
def datos_secciones():
    """Página HTML con tabla interactiva DataTables."""
    data = _cargar_secciones()
    return render_template("datos_secciones.html", meta=data["meta"])

@app.route("/api/secciones")
@login_required
def api_secciones():
    """Devuelve el dataset completo (2,278 secciones) en JSON.
    DataTables lo carga del lado del cliente."""
    data = _cargar_secciones()
    return jsonify(data["secciones"])

@app.route("/api/meta")
@login_required
def api_meta():
    """Metadatos: municipios, partidos individuales, total de secciones."""
    data = _cargar_secciones()
    return jsonify(data["meta"])

# -----------------------------
# LOGOUT
# -----------------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# -----------------------------
# EJECUCIÓN
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
