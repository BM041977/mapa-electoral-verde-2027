# ── diagnosticos.html: logo + quitar descarga ──
content = open('templates/diagnosticos.html', 'r', encoding='utf-8').read()

# Reemplazar brand por logo
viejo_brand = '''    <div class="brand">
        <span class="brand-mark"></span>
        <span class="brand-name">BaldemarMaza<span class="brand-tld">.com</span></span>
    </div>'''

nuevo_brand = '''    <div class="brand">
        <img src="/static/logo.png" alt="Baldemar Maza León" style="height:48px;width:auto;">
    </div>'''

content = content.replace(viejo_brand, nuevo_brand)

# Quitar atributo download y cambiar texto
content = content.replace('download="{{ muni.archivo }}"', '')
content = content.replace('Descargar PDF', 'Ver diagn&#243;stico')

open('templates/diagnosticos.html', 'w', encoding='utf-8').write(content)
print('OK - diagnosticos.html actualizado')

# ── index.html: logo ──
content2 = open('templates/index.html', 'r', encoding='utf-8').read()

viejo_brand2 = '''    <div class="brand">
        <span class="brand-mark"></span>
        <span class="brand-name">BaldemarMaza<span class="brand-tld">.com</span></span>
    </div>'''

nuevo_brand2 = '''    <div class="brand">
        <img src="/static/logo.png" alt="Baldemar Maza León" style="height:48px;width:auto;">
    </div>'''

content2 = content2.replace(viejo_brand2, nuevo_brand2)
open('templates/index.html', 'w', encoding='utf-8').write(content2)
print('OK - index.html actualizado')