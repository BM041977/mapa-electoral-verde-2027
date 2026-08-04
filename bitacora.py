"""
bitacora.py — Registro de accesos para mapa-electoral-v2
──────────────────────────────────────────────────────────
Implementa la Cláusula Octava del contrato de licencia (medida III:
bitácora de accesos) y sirve de respaldo probatorio para el escenario
que ninguna medida visual puede bloquear (foto de celular a la pantalla).

Backend: Turso vía HTTP puro (protocolo Hrana sobre HTTP), usando
solo `requests` — SIN el paquete `libsql` (causó un crash de
Tokio/Rust en producción el 03-ago-2026 por el modelo de workers
`fork` de gunicorn) y SIN `turso_serverless` (demasiado nuevo/sin
probar). Cada llamada es un POST HTTP normal, sin runtime persistente
ni hilos — el mismo modelo que ya usa `requests` en el resto del
proyecto.

Integración en app.py (SIN CAMBIOS respecto a la versión SQLite):

    from bitacora import init_bitacora, registrar_acceso

    app = Flask(__name__)
    init_bitacora(app)

    @app.before_request
    def _log_acceso():
        registrar_acceso()

Requiere que el login ya guarde el usuario en `session['usuario']`
(como en el sistema de auth SQLite existente).

Variables de entorno requeridas (ya deben existir en Render):
    TURSO_DATABASE_URL   ej. libsql://bitacora-chiapas-2027-<org>.turso.io
    TURSO_AUTH_TOKEN     token Bearer de la base de datos

Variable de entorno opcional (para distinguir el sitio en la BD
compartida entre v2/MORENA/PAN/VERDE sin tocar app.py):
    BITACORA_SITIO       "v2" (default), "morena", "pan" o "verde"
"""

import os
import requests
from datetime import datetime
from flask import request, session

TURSO_DATABASE_URL = os.environ.get("TURSO_DATABASE_URL", "")
TURSO_AUTH_TOKEN = os.environ.get("TURSO_AUTH_TOKEN", "")
SITIO = os.environ.get("BITACORA_SITIO", "verde")

# Timeouts cortos a propósito: registrar_acceso() corre en CADA
# request vía before_request — si Turso tarda o no responde, el sitio
# no debe quedarse colgado esperando.
TIMEOUT_ESCRITURA = 3   # segundos, para registrar_acceso()
TIMEOUT_LECTURA = 8     # segundos, para consultas de panel de admin

RUTAS_EXCLUIDAS_PREFIJOS = ("/static/", "/favicon.ico", "/healthz")

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS accesos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT,
    ip TEXT,
    user_agent TEXT,
    ruta TEXT,
    metodo TEXT,
    fecha_hora TEXT,
    sitio TEXT
);
"""


def _pipeline_url():
    """Convierte TURSO_DATABASE_URL (libsql://...) al endpoint HTTP /v2/pipeline."""
    base = TURSO_DATABASE_URL
    if base.startswith("libsql://"):
        base = "https://" + base[len("libsql://"):]
    return base.rstrip("/") + "/v2/pipeline"


def _tipar(valor):
    """Convierte un valor Python al formato tipado que exige Hrana sobre HTTP."""
    if valor is None:
        return {"type": "null"}
    if isinstance(valor, bool):
        # bool antes que int (bool es subclase de int en Python)
        return {"type": "integer", "value": str(int(valor))}
    if isinstance(valor, int):
        return {"type": "integer", "value": str(valor)}
    if isinstance(valor, float):
        return {"type": "float", "value": str(valor)}
    return {"type": "text", "value": str(valor)}


def _destipar(celda):
    """Convierte una celda tipada de la respuesta de Hrana a un valor Python normal."""
    if celda is None:
        return None
    tipo = celda.get("type")
    valor = celda.get("value")
    if tipo == "null" or valor is None:
        return None
    if tipo == "integer":
        return int(valor)
    if tipo == "float":
        return float(valor)
    return valor  # text / blob


def _ejecutar(sql, args=None, timeout=TIMEOUT_LECTURA):
    """
    Ejecuta una sola sentencia SQL contra Turso vía HTTP (pipeline de un solo
    'execute' + 'close', conexión efímera — no mantiene estado entre llamadas).
    Devuelve una lista de dicts (una por fila) usando los nombres de columna.
    Lanza una excepción si algo falla (la maneja quien llama, según el caso).
    """
    stmt = {"sql": sql}
    if args:
        stmt["args"] = [_tipar(a) for a in args]

    payload = {
        "requests": [
            {"type": "execute", "stmt": stmt},
            {"type": "close"},
        ]
    }
    headers = {
        "Authorization": f"Bearer {TURSO_AUTH_TOKEN}",
        "Content-Type": "application/json",
    }

    resp = requests.post(_pipeline_url(), headers=headers, json=payload, timeout=timeout)
    resp.raise_for_status()
    data = resp.json()

    resultados = data.get("results", [])
    if not resultados or resultados[0].get("type") != "ok":
        error = resultados[0].get("error") if resultados else {"message": "respuesta vacía de Turso"}
        raise RuntimeError(f"Turso HTTP error: {error}")

    result = resultados[0]["response"]["result"]
    cols = [c["name"] for c in result.get("cols", [])]
    filas = []
    for fila in result.get("rows", []):
        valores = [_destipar(celda) for celda in fila]
        filas.append(dict(zip(cols, valores)))
    return filas


def init_bitacora(app):
    """
    Crea la tabla `accesos` en Turso si no existe. Llamar una vez al iniciar la app.

    Envuelto en try/except: si Turso no responde durante el arranque
    (deploy, cold start, incidente momentáneo), el sitio debe seguir
    levantando igual — la bitácora simplemente queda inactiva hasta el
    próximo intento, en vez de tumbar el servicio completo (como pasó
    con el crash de Tokio/libsql).
    """
    try:
        _ejecutar(SCHEMA_SQL, timeout=TIMEOUT_LECTURA)
        app.logger.info(f"Bitácora (Turso/HTTP) inicializada — sitio={SITIO}")
    except Exception as e:
        app.logger.warning(f"bitacora: no se pudo inicializar contra Turso: {e}")


def _get_ip():
    """
    Obtiene la IP real del visitante. En Render (y la mayoría de plataformas
    detrás de proxy), la IP real viaja en X-Forwarded-For, no en request.remote_addr.
    """
    forwarded = request.headers.get("X-Forwarded-For", "")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.remote_addr or "desconocida"


def registrar_acceso():
    """Registra el request actual en la bitácora. Llamar desde @app.before_request.

    Envuelto en try/except a propósito: un problema de la base de datos
    (red, timeout, bloqueo, etc.) nunca debe tumbar el sitio -- en el peor
    caso, ese acceso específico simplemente no queda registrado.
    """
    ruta = request.path
    if ruta.startswith(RUTAS_EXCLUIDAS_PREFIJOS):
        return

    usuario = session.get("usuario", "anonimo")
    ip = _get_ip()
    user_agent = request.headers.get("User-Agent", "")[:255]
    metodo = request.method
    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        _ejecutar(
            "INSERT INTO accesos (usuario, ip, user_agent, ruta, metodo, fecha_hora, sitio) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (usuario, ip, user_agent, ruta, metodo, fecha_hora, SITIO),
            timeout=TIMEOUT_ESCRITURA,
        )
    except Exception as e:
        try:
            from flask import current_app
            current_app.logger.warning(f"bitacora: no se pudo registrar el acceso: {e}")
        except Exception:
            pass


def detectar_sesiones_simultaneas(usuario, minutos=5):
    """
    Devuelve True si el mismo usuario aparece con más de una IP distinta
    dentro de la ventana de tiempo indicada — señal de credencial compartida.
    Llamar periódicamente (ej. en una ruta de admin) o tras cada login.

    Si Turso no responde, devuelve False (no bloquea al usuario ni tumba
    la ruta que llame a esta función) y deja constancia en el log.
    """
    try:
        filas = _ejecutar(
            """
            SELECT DISTINCT ip FROM accesos
            WHERE usuario = ?
            AND fecha_hora >= datetime('now', ?)
            """,
            (usuario, f"-{minutos} minutes"),
        )
        ips = {f["ip"] for f in filas}
        return len(ips) > 1
    except Exception as e:
        try:
            from flask import current_app
            current_app.logger.warning(f"bitacora: no se pudo consultar sesiones simultáneas: {e}")
        except Exception:
            pass
        return False


def detectar_uso_multisitio(usuario, minutos=30):
    """
    Devuelve True si el mismo usuario aparece activo en más de un `sitio`
    (v2 / morena / pan / verde) dentro de la ventana de tiempo indicada —
    señal de credencial compartida entre los sitios de partido, algo que
    `detectar_sesiones_simultaneas()` no puede ver porque solo mira IPs
    dentro de un mismo sitio.

    Requiere que los 4 repos escriban a la MISMA base de datos Turso
    (misma TURSO_DATABASE_URL/TURSO_AUTH_TOKEN en los 4 servicios de
    Render), cada uno con su propio BITACORA_SITIO.

    Si Turso no responde, devuelve False y deja constancia en el log.
    """
    try:
        filas = _ejecutar(
            """
            SELECT DISTINCT sitio FROM accesos
            WHERE usuario = ?
            AND fecha_hora >= datetime('now', ?)
            """,
            (usuario, f"-{minutos} minutes"),
        )
        sitios = {f["sitio"] for f in filas}
        return len(sitios) > 1
    except Exception as e:
        try:
            from flask import current_app
            current_app.logger.warning(f"bitacora: no se pudo consultar uso multisitio: {e}")
        except Exception:
            pass
        return False


def consultar_bitacora(usuario=None, limite=200):
    """Para el panel de administración: devuelve los últimos accesos, opcionalmente filtrados por usuario.

    Si Turso no responde, devuelve una lista vacía (el panel se ve vacío,
    no se cae) y deja constancia en el log.
    """
    try:
        if usuario:
            return _ejecutar(
                "SELECT * FROM accesos WHERE usuario = ? ORDER BY id DESC LIMIT ?",
                (usuario, limite),
            )
        return _ejecutar(
            "SELECT * FROM accesos ORDER BY id DESC LIMIT ?",
            (limite,),
        )
    except Exception as e:
        try:
            from flask import current_app
            current_app.logger.warning(f"bitacora: no se pudo consultar la bitácora: {e}")
        except Exception:
            pass
        return []
