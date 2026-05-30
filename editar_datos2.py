content = open('templates/datos_secciones.html', 'r', encoding='utf-8').read()

# Buscar y eliminar el boton exportar CSV
import re
content = re.sub(
    r"\{ extend: 'csv'.*?exportOptions:.*?\}.*?\}",
    "",
    content,
    flags=re.DOTALL
)

open('templates/datos_secciones.html', 'w', encoding='utf-8').write(content)
print('OK - Exportar CSV eliminado')