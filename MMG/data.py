import bs4
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd

# Necesario instalar 'pip install html5lib'  para que funcione la siguiente línea de código

URL_BASE = 'https://careers.mmg.com/caw/es/filter/?work-type=&location=&category=&search-keyword=&job-mail-subscribe-privacy=agree'
pedido_obtenido = requests.get(URL_BASE)
html_obtenido = pedido_obtenido.text

soup = BeautifulSoup(html_obtenido, "html5lib")

# Encontrar todos los elementos con la clase 'search-result'
data_rows = soup.find('div', id='recent-jobs-content').find_all('div', class_='search-result')

# Crear una cadena de caracteres para almacenar todo el contenido HTML
contenido_html = ""
trabajos_data = []

for row in data_rows:
    # Extraer el titulo
    titulo_elemento = row.find('h3').find('a', class_='job-link')
    titulo = titulo_elemento.text.strip() if titulo_elemento else None

    # Extraer Subtitulo
    subtitulo = row.find('p', class_='result-sub-heading')

    # Extraer Ubicacion y Tipo de Trabajo
    ubicacion = subtitulo.find('span', class_="location").text.strip()
    tipoTrabajo = subtitulo.find('span', class_='work-type tiempo-completo').text.strip()

    # Extraer resumen
    resumen = row.find('p', class_='result-description').text.strip()

    # Nota
    nota = row.find('p', class_='result-note').text.strip()

    # Extraer el enlace de mas informacion
    enlace = URL_BASE[0:23] + titulo_elemento['href'] if titulo_elemento else None

    #  Obtenemos el Html de la pagina del enlace
    pedido_enlace = requests.get(enlace)
    html_enlace = pedido_enlace.text

    soupInfo = BeautifulSoup(html_enlace, "html5lib")

    # Encuentra el contenido dentro del div 'job-content'
    job_content_div = soupInfo.find('div', id='job-content')

    # Excluye las imágenes dentro del contenido
    for img in job_content_div.find_all('img'):
        img.extract()

    # Encuentra todos los elementos <p> y <ul> dentro del div 'job-content' después de excluir las imágenes
    info = job_content_div.find_all(['p', 'ul'])

    # Construir el HTML de cada trabajo
    trabajo_html = f"""
    <div class="trabajo">
        <h2>{titulo}</h2>
        <p>Enlace: <a href="{enlace}">{enlace}</a></p>
        <p>Resumen: {resumen}</p>
        <p>País: {nota}</p>
    """

    # Concatenar el HTML de cada trabajo sin las comas innecesarias y corchetes
    descripcion_html = ''.join([str(tag) for tag in info if 'ProducimosCobreProducimosTalento' not in str(tag) and '<a class="apply-link button"' not in str(tag)])
    trabajo_html += descripcion_html

    trabajo_html += "</div>"

    contenido_html += trabajo_html
    contenido_html += '\n--------------------------------------------------------------------------------------\n'

    # Agregar los datos del trabajo a la lista
    trabajos_data.append({
        'title': titulo,
        'description': descripcion_html,
        'url': enlace,
        'category': 'null',
        'department': 'null',
        'province': 'null',
        'district': 'null',
        'company': 'null'
    })

# Crear un DataFrame de Pandas con los datos de los trabajos
df = pd.DataFrame(trabajos_data)

# Guardar el DataFrame en un archivo CSV
df.to_csv('MMG/trabajos_mmg.csv', index=False)

# Escribir el contenido HTML en un archivo HTML
# with open("MMG/contenido.html", "w", encoding="utf-8") as file:
#     file.write(contenido_html)

print("Archivo 'trabajos_mmg.html' creado satisfactoriamente.")
