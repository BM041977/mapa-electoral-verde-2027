for filename in ['templates/mapa_ligero.html', 'templates/mapa_por_partido.html']:
    content = open(filename, 'r', encoding='utf-8').read()
    # Reducir tiempo de espera de 3000ms a 500ms y reintentos de 40 a 20
    content = content.replace(
        'setTimeout(() => intentarFiltro(40), 3000);',
        'setTimeout(() => intentarFiltro(20), 500);'
    )
    open(filename, 'w', encoding='utf-8').write(content)
    print('OK - ' + filename)
