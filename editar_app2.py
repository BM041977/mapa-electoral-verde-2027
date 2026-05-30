content = open('app.py', 'r', encoding='utf-8').read()

ruta = '\n@app.route("/diagnosticos")\n@login_required\ndef diagnosticos():\n    pdf_dir = os.path.join(app.static_folder, "pdfs")\n    archivos = sorted([f for f in os.listdir(pdf_dir) if f.endswith(".pdf")])\n    municipios = [\n        {\n            "archivo": f,\n            "nombre": nombre_bonito(f),\n            "url": f"/static/pdfs/{f}"\n        }\n        for f in archivos\n    ]\n    return render_template("diagnosticos.html", municipios=municipios, owner=OWNER)\n\n'

marca = '# -----------------------------\n# GEOJSON'
content = content.replace(marca, ruta + marca)
open('app.py', 'w', encoding='utf-8').write(content)
print('OK - ruta agregada')