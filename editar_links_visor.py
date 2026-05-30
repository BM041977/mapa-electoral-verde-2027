content = open('templates/diagnosticos.html', 'r', encoding='utf-8').read()

# Cambiar link directo al PDF por el visor
content = content.replace(
    'href="{{ muni.url }}"',
    'href="/ver-pdf/{{ muni.archivo | replace(\'Diagnostico_Electoral_\', \'\') | replace(\'_v8.pdf\', \'\') }}"'
)

# Cambiar texto del boton
content = content.replace('Ver diagn&#243;stico', 'Ver diagn&#243;stico →')

open('templates/diagnosticos.html', 'w', encoding='utf-8').write(content)
print('OK - links actualizados al visor')