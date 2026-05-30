content = open('app.py', 'r', encoding='utf-8').read()

funcion = '\ndef nombre_bonito(archivo):\n    nombre = archivo.replace("Diagnostico_Electoral_", "").replace("_v8.pdf", "")\n    palabras = nombre.split("_")\n    minusculas = {"De", "Del", "La", "Las", "Los", "El", "Y", "A"}\n    resultado = []\n    for i, p in enumerate(palabras):\n        if i == 0:\n            resultado.append(p.capitalize())\n        elif p in minusculas:\n            resultado.append(p.lower())\n        else:\n            resultado.append(p.capitalize())\n    return " ".join(resultado)\n\n'

marca = '# -----------------------------\n# LOGIN'
content = content.replace(marca, funcion + marca)
open('app.py', 'w', encoding='utf-8').write(content)
print('OK - funcion agregada')