"""
bitacora.py — Registro de accesos para mapa-electoral-v2
──────────────────────────────────────────────────────────
Implementa la Cláusula Octava del contrato de licencia (medida III:
bitácora de accesos) y sirve de respaldo probatorio para el escenario
que ninguna medida visual puede bloquear (foto de celular a la pantalla).

Base de datos: Turso (libSQL en la nube), UNA sola base compartida entre
los 4 repos (v2 / MORENA / PAN / VERDE) -- el plan Free de Render no
soporta Persistent Disk, así que un SQLite local se borraba en cada
deploy y no servía como respaldo confiable. Cada sitio se distingue con
la columna `sitio`, tomada de la variable de entorno SITIO.

Integración en app.py (sin cambios respecto a la versión SQLite):

    from bitacora import init_bitacora, registrar_acceso

    app = Flask(__name__)
    init_bitacora(app)

    @app.before_request
    def _log_acceso():
        registrar_acceso()

Requiere que el login ya guarde el usuario en `session['usuario']`
(como en el sistema de auth existente), y estas variables de entorno
(configuradas en Render → Settings → Environment):

    TURSO_DATABASE_URL   -- URL de la base (turso db show <db> --url)
    TURSO_AUTH_TOKEN     -- token de acceso (turso db tokens create <db>)
    SITIO                -- "v2" / "morena" / "pan" / "verde" según el repo
                             (si no está definida, cae en "v2" por defecto)
"""

import os
from datetime import datetime
import libsql
from flask import request, session

TURSO_DATABASE_URL = os.environ.get("TURSO_DATABASE_URL", "")
TURSO_AUTH_TOKEN = os.environ.get("TURSO_AUTH_TOKEN", "")
SITIO = os.environ.get("SITIO", "v2")

SCHEMA = """
CREATE TABLE IF NOT EXISTS accesos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sitio TEXT,
    usuario TEXT,
    ip TEXT,
    user_agent TEXT,
    ruta TEXT,
    metodo TEXT,
    fecha_hora TEXT
);
"""

# Rutas que NO se registran para no llenar la bitácora de ruido
# (archivos estáticos, health checks, etc.)
RUTAS_EXCLUIDAS_PREFIJOS = ("/static/", "/favicon.ico", "/healthz")


def _conectar():
    """
    Abre una conexión nueva a Turso. Se crea una por operación -- igual
    patrón que antes con sqlite3.connect() -- para no lidiar con hilos de
    gunicorn compartiendo una sola conexión; el volumen de esta bitácora
    es bajo, así que el costo de reconectar en cada llamada es mínimo.
    """
    return libsql.connect(database=TURSO_DATABASE_URL, auth_token=TURSO_AUTH_TOKEN)


def init_bitacora(app):
    """Crea la tabla en Turso si no existe. Llamar una vez al iniciar la app.

    Envuelto en try/except: si Turso no responde al arrancar, la app debe
    seguir levantando igual -- sin bitácora es mejor que sin sitio.
    """
    try:
        conn = _conectar()
        conn.execute(SCHEMA)
        conn.commit()
        app.logger.info(f"Bitácora conectada a Turso (sitio={SITIO})")
    except Exception as e:
        app.logger.warning(f"bitacora: no se pudo inicializar la conexión a Turso: {e}")


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
    (red, timeout, Turso caído, etc.) nunca debe tumbar el sitio -- en el
    peor caso, ese acceso específico simplemente no queda registrado.
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
        conn = _conectar()
        conn.execute(
            "INSERT INTO accesos (sitio, usuario, ip, user_agent, ruta, metodo, fecha_hora) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (SITIO, usuario, ip, user_agent, ruta, metodo, fecha_hora),
        )
        conn.commit()
    except Exception as e:
        try:
            from flask import current_app
            current_app.logger.warning(f"bitacora: no se pudo registrar el acceso: {e}")
        except Exception:
            pass


def detectar_sesiones_simultaneas(usuario, minutos=5, entre_sitios=False):
    """
    Devuelve True si el mismo usuario aparece con más de una IP distinta
    dentro de la ventana de tiempo indicada -- señal de credencial compartida.

    Por defecto revisa solo dentro del sitio actual (SITIO), igual que
    antes de migrar a Turso. Como las cuentas municipales usan el mismo
    usuario/contraseña en los 4 repos de partido, pasa entre_sitios=True
    para revisar la actividad del usuario en TODOS los sitios a la vez
    (v2, MORENA, PAN, VERDE) -- útil para detectar el mismo municipio
    activo simultáneamente en más de un sitio, no solo en el mismo.

    Llamar periódicamente (ej. en una ruta de admin) o tras cada login.
    """
    conn = _conectar()
    if entre_sitios:
        cur = conn.execute(
            """
            SELECT DISTINCT ip FROM accesos
            WHERE usuario = ?
            AND fecha_hora >= datetime('now', ?)
            """,
            (usuario, f"-{minutos} minutes"),
        )
    else:
        cur = conn.execute(
            """
            SELECT DISTINCT ip FROM accesos
            WHERE usuario = ?
            AND sitio = ?
            AND fecha_hora >= datetime('now', ?)
            """,
            (usuario, SITIO, f"-{minutos} minutes"),
        )
    ips = [row[0] for row in cur.fetchall()]
    return len(ips) > 1


def detectar_uso_multisitio(usuario, minutos=5):
    """
    Devuelve la lista de sitios distintos (v2/morena/pan/verde) donde el
    mismo usuario ha tenido actividad dentro de la ventana de tiempo
    indicada. A diferencia de detectar_sesiones_simultaneas, esto no
    depende de la IP -- solo de en cuántos sitios distintos aparece. Como
    las cuentas municipales comparten usuario/contraseña en los 4 repos de
    partido, ver al mismo usuario activo en más de un sitio puede ser
    normal (alguien revisando varias vistas) o una señal a vigilar.
    """
    conn = _conectar()
    cur = conn.execute(
        """
        SELECT DISTINCT sitio FROM accesos
        WHERE usuario = ?
        AND fecha_hora >= datetime('now', ?)
        """,
        (usuario, f"-{minutos} minutes"),
    )
    return [row[0] for row in cur.fetchall()]


def consultar_bitacora(usuario=None, sitio=None, limite=200):
    """
    Para el panel de administración: devuelve los últimos accesos,
    opcionalmente filtrados por usuario y/o por sitio (v2/morena/pan/verde).
    Sin filtro de sitio, muestra accesos de los 4 sitios juntos (misma
    base de datos compartida).
    """
    conn = _conectar()
    columnas = ["id", "sitio", "usuario", "ip", "user_agent", "ruta", "metodo", "fecha_hora"]
    condiciones = []
    params = []
    if usuario:
        condiciones.append("usuario = ?")
        params.append(usuario)
    if sitio:
        condiciones.append("sitio = ?")
        params.append(sitio)
    where = f"WHERE {' AND '.join(condiciones)}" if condiciones else ""
    params.append(limite)
    cur = conn.execute(f"SELECT * FROM accesos {where} ORDER BY id DESC LIMIT ?", tuple(params))
    return [dict(zip(columnas, row)) for row in cur.fetchall()]
