content = open('app.py', 'r', encoding='utf-8').read()
content = content.replace('# 👤 PROPIETARIO', '# PROPIETARIO')
open('app.py', 'w', encoding='utf-8').write(content)
print('OK')