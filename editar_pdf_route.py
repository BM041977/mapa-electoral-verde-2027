content = open('app.py', 'r', encoding='utf-8').read()

ruta = '''
@app.route("/ver-pdf/<municipio>")
@login_required
def ver_pdf(municipio):
    pdf_dir = os.path.join(app.static_folder, "pdfs")
    archivos = [f for f in os.listdir(pdf_dir) if f.endswith(".pdf")]
    archivo = next((f for f in archivos if municipio in f), None)
    if not archivo:
        return "PDF no encontrado", 404
    return render_template("visor_pdf.html", municipio=municipio.replace("_", " "), owner=OWNER)

'''

marca = '# -----------------------------\n# GEOJSON'
content = content.replace(marca, ruta + marca)
open('app.py', 'w', encoding='utf-8').write(content)
print('OK - ruta ver_pdf agregada')