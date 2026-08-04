"""
bitacora.py — Registro de accesos para mapa-electoral-v2
──────────────────────────────────────────────────────────
Implementa la Cláusula Octava del contrato de licencia (medida III:
bitácora de accesos) y sirve de respaldo probatorio para el escenario
que ninguna medida visual puede bloquear (foto de celular a la pantalla).

Integración en app.py:

    from bitacora import init_bitacora, registrar_acceso

    app = Flask(__name__)
    init_bitacora(app)

    @app.before_request
    def _log_acceso():
        registrar_acceso()

Requiere que el login ya guarde el usuario en `session['usuario']`
(como en el sistema de auth SQLite existente).
"""

import sqlite3
import os
from datetime import datetime
from flask import request, session, g

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bitacora.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS accesos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
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


def init_bitacora(app):
    """Crea la base de datos y la tabla si no existen. Llamar una vez al iniciar la app."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute(SCHEMA)
    conn.commit()
    conn.close()
    app.logger.info(f"Bitácora inicializada en {DB_PATH}")


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
    """Registra el request actual en la bitácora. Llamar desde @app.before_request."""
    ruta = request.path
    if ruta.startswith(RUTAS_EXCLUIDAS_PREFIJOS):
        return

    usuario = session.get("usuario", "anonimo")
    ip = _get_ip()
    user_agent = request.headers.get("User-Agent", "")[:255]
    metodo = request.method
    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO accesos (usuario, ip, user_agent, ruta, metodo, fecha_hora) VALUES (?, ?, ?, ?, ?, ?)",
        (usuario, ip, user_agent, ruta, metodo, fecha_hora),
    )
    conn.commit()
    conn.close()


def detectar_sesiones_simultaneas(usuario, minutos=5):
    """
    Devuelve True si el mismo usuario aparece con más de una IP distinta
    dentro de la ventana de tiempo indicada — señal de credencial compartida.
    Llamar periódicamente (ej. en una ruta de admin) o tras cada login.
    """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.execute(
        """
        SELECT DISTINCT ip FROM accesos
        WHERE usuario = ?
        AND fecha_hora >= datetime('now', ?)
        """,
        (usuario, f"-{minutos} minutes"),
    )
    ips = [row[0] for row in cur.fetchall()]
    conn.close()
    return len(ips) > 1


def consultar_bitacora(usuario=None, limite=200):
    """Para el panel de administración: devuelve los últimos accesos, opcionalmente filtrados por usuario."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    if usuario:
        cur = conn.execute(
            "SELECT * FROM accesos WHERE usuario = ? ORDER BY id DESC LIMIT ?",
            (usuario, limite),
        )
    else:
        cur = conn.execute("SELECT * FROM accesos ORDER BY id DESC LIMIT ?", (limite,))
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows
