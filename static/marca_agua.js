/*
 * marca_agua.js — Cláusula Octava del contrato: marca discreta permanente
 * + refuerzo ante intento de captura/impresión.
 *
 * Integración: incluir este script al final de mapa_ligero.html y
 * mapa_por_partido.html, después de que la plantilla renderice las
 * variables `usuario`, `ip_cliente` (pasada desde Flask con request headers)
 * y `municipio`.
 *
 * En la plantilla Jinja, antes de este <script>, definir:
 *   <script>
 *     window.SESION = {
 *       usuario: "{{ usuario }}",
 *       ip: "{{ ip_cliente }}",
 *       municipio: "{{ municipio }}"
 *     };
 *   </script>
 */

(function () {
  const sesion = window.SESION || { usuario: "usuario", ip: "0.0.0.0", municipio: "" };

  // Convierte "ocozocoautla de espinosa" -> "Ocozocoautla de Espinosa".
  // Solo afecta el TEXTO MOSTRADO en las marcas; sesion.usuario no se toca.
  function formatearNombreMunicipio(texto) {
    const conectores = ["de", "del", "la", "las", "los", "y"];
    return String(texto || "")
      .toLowerCase()
      .split(" ")
      .map((palabra, i) => {
        if (i > 0 && conectores.includes(palabra)) return palabra;
        return palabra.charAt(0).toUpperCase() + palabra.slice(1);
      })
      .join(" ");
  }

  // ---------- CAPA 1: marca discreta permanente (esquina) ----------
  function crearMarcaDiscreta() {
    const marca = document.createElement("div");
    marca.id = "marca-discreta";
    marca.textContent = formatearNombreMunicipio(sesion.usuario);
    marca.style.cssText = [
      "position: fixed",
      "bottom: 90px",
      "left: 10px",
      "font-size: 18px",
      "color: rgba(90,90,90,0.65)",
      "text-shadow: 0 0 3px rgba(255,255,255,0.6), 0 1px 2px rgba(255,255,255,0.6)",
      "font-family: sans-serif",
      "pointer-events: none",
      "z-index: 9998",
      "user-select: none",
    ].join(";");
    document.body.appendChild(marca);
  }

  // ---------- CAPA 2: refuerzo ante intento de captura/impresión ----------
  function crearMarcaReforzada() {
    const overlay = document.createElement("div");
    overlay.id = "marca-reforzada";
    overlay.style.cssText = [
      "position: fixed",
      "inset: 0",
      "pointer-events: none",
      "z-index: 9999",
      "display: none",
      "background: repeating-linear-gradient(-28deg, transparent 0 120px, rgba(0,0,0,0.05) 120px 121px)",
    ].join(";");

    const fecha = () => new Date().toLocaleString("es-MX");
    const texto = `${formatearNombreMunicipio(sesion.usuario)} · ${sesion.ip} · ${fecha()}`;

    // Rejilla de textos repetidos, similar a la maqueta mostrada
    for (let i = 0; i < 6; i++) {
      const t = document.createElement("div");
      t.textContent = texto;
      t.style.cssText = [
        "position: absolute",
        `top: ${15 + (i % 3) * 30}%`,
        `left: ${10 + (i % 2) * 45}%`,
        "transform: rotate(-28deg)",
        "font-size: 12px",
        "color: rgba(90,90,90,0.5)",
        "font-family: sans-serif",
        "white-space: nowrap",
      ].join(";");
      overlay.appendChild(t);
    }
    document.body.appendChild(overlay);
    return overlay;
  }

  let overlayReforzado = null;
  let ocultarTimeout = null;

  function activarRefuerzo() {
    if (!overlayReforzado) overlayReforzado = crearMarcaReforzada();
    overlayReforzado.style.display = "block";
    clearTimeout(ocultarTimeout);
    // se mantiene visible unos segundos tras recuperar el foco,
    // por si la captura ocurrió justo al volver
    ocultarTimeout = setTimeout(() => {
      overlayReforzado.style.display = "none";
    }, 4000);
  }

  // Pérdida de foco de la ventana o cambio de pestaña
  window.addEventListener("blur", activarRefuerzo);
  document.addEventListener("visibilitychange", () => {
    if (document.hidden) activarRefuerzo();
  });

  // ---------- Bloqueo de impresión ----------
  window.print = function () {
    console.warn("Impresión deshabilitada por la licencia de uso.");
  };
  window.addEventListener("keydown", (e) => {
    const esImprimir = (e.ctrlKey || e.metaKey) && (e.key === "p" || e.key === "P");
    if (esImprimir) {
      e.preventDefault();
      activarRefuerzo();
    }
  });
  window.addEventListener("beforeprint", (e) => {
    activarRefuerzo();
  });

  // Init
  document.addEventListener("DOMContentLoaded", crearMarcaDiscreta);
})();
