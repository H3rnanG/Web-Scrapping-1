import bs4
from bs4 import BeautifulSoup
import requests
import re

# Necesario instalar 'pip install html5lib'  para que funcione la siguiente línea de código

URL_BASE = 'https://careers.mmg.com/caw/es/filter/?work-type=&location=&category=&search-keyword=&job-mail-subscribe-privacy=agree'
pedido_obtenido = requests.get(URL_BASE)
html_obtenido = pedido_obtenido.text

soup = BeautifulSoup(html_obtenido, "html5lib")

# Encontrar todos los elementos con la clase 'search-result'
data_rows = soup.find('div',id='recent-jobs-content').find_all('div', class_ = 'search-result')

# Verificar datos
# for div_trabajo in data_rows:
#     print(div_trabajo)
#     print('\n\n\n')

# Crear una cadena de caracteres para almacenar todo el contenido HTML
contenido_html = ""

for row in data_rows:
    # Extraer el titulo
    titulo_elemento = row.find('h3').find('a',class_='job-link')
    titulo = titulo_elemento.text.strip() if titulo_elemento else None

    # Extraer Subtitulo
    subtitulo = row.find('p',class_='result-sub-heading')

    # Extraer Ubicacion y Tipo de Trabajo
    ubicacion = subtitulo.find('span',class_="location").text.strip()
    tipoTrabajo = subtitulo.find('span',class_='work-type tiempo-completo').text.strip()

    # Extraer resumen
    resumen = row.find('p',class_='result-description').text.strip()
    
    # Nota
    nota = row.find('p',class_='result-note').text.strip()

print("Archivo 'contenido.html' creado satisfactoriamente.")
