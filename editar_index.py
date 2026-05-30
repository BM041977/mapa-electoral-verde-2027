content = open('templates/index.html', 'r', encoding='utf-8').read()

card = '''
        <a class="card" href="/diagnosticos">
            <div class="card-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                    <polyline points="14 2 14 8 20 8"/>
                    <line x1="16" y1="13" x2="8" y2="13"/>
                    <line x1="16" y1="17" x2="8" y2="17"/>
                    <polyline points="10 9 9 9 8 9"/>
                </svg>
            </div>
            <div class="card-title">Diagn&#243;sticos</div>
            <p class="card-question">&#191;Qu&#233; dice el an&#225;lisis de mi municipio?</p>
            <p class="card-desc">123 diagn&#243;sticos municipales en PDF. An&#225;lisis completo por secci&#243;n, tendencia de voto, fortalezas y riesgos electorales de cara a 2027.</p>
            <div class="card-meta">
                <span class="tag">123 municipios</span>
                <span class="tag">Descarga PDF</span>
            </div>
            <div class="card-cta">
                Ver diagn&#243;sticos
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M5 12h14M13 5l7 7-7 7"/>
                </svg>
            </div>
        </a>

'''

content = content.replace('    </div>\n\n    <footer>', card + '    </div>\n\n    <footer>')
content = content.replace('grid-template-columns: repeat(3, 1fr);', 'grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));')
open('templates/index.html', 'w', encoding='utf-8').write(content)
print('OK - card agregado')