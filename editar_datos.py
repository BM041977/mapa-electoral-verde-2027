content = open('templates/datos_secciones.html', 'r', encoding='utf-8').read()

# 1. Logo en lugar de BaldemarMaza.com
content = content.replace(
    '<span class="brand-mark"></span>\n        <span class="brand-name">BaldemarMaza<span class="brand-tld">.com</span></span>',
    '<img src="/static/logo.png" alt="Baldemar Maza León" style="height:48px;width:auto;">'
)

# 2. Quitar boton exportar CSV
content = content.replace(
    "{ extend: 'csv', text: 'Exportar CSV', filename: 'secciones_chiapas_2024',\n                  exportOptions: { columns: [0,1,2,3,4,5,6,7,8,9] } }  // sin bot\xc3\xb3n Detalle",
    ""
)

open('templates/datos_secciones.html', 'w', encoding='utf-8').write(content)
print('OK - datos_secciones.html actualizado')