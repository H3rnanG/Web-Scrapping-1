import bs4
from bs4 import BeautifulSoup
import requests
import re

URL_BASE = 'https://mastalento.antamina.com/search'
pedido_obtenido = requests.get(URL_BASE)
html_obtenido = pedido_obtenido.text

soup = BeautifulSoup(html_obtenido, "html.parser")

# Encontrar todos los elementos con la clase 'data-row'
data_rows = soup.find_all('tr', class_='data-row')

# Crear una cadena de caracteres para almacenar todo el contenido HTML
contenido_html = ""

for row in data_rows:
    # Extraer el título
    titulo_elemento = row.find('span', class_='jobTitle').find('a', class_='jobTitle-link')
    titulo = titulo_elemento.text.strip() if titulo_elemento else None
    
    # Extraer la fecha
    fecha = row.find('span', class_='jobDate').text.strip()
    
    # Encontrar el país dentro del mismo contenedor del título
    pais_elemento = row.find('td', class_='colLocation').find('span', class_='jobLocation')
    pais = pais_elemento.text.strip() if pais_elemento else None
    
    # Extraer el enlace de mas informacion
    enlace = URL_BASE[0:-7] + titulo_elemento['href'] if titulo_elemento else None

    #  Obtenemos el Html de la pagina del enlace
    pedido_enlace = requests.get(enlace)
    html_enlace = pedido_enlace.text

    soupInfo = BeautifulSoup(html_enlace, "html.parser")

    # Encontrar el contenedor principal
    info = soupInfo.find('span', class_='jobdescription').find('div')

    # Crear un diccionario para almacenar los datos extraídos
    datos = {'ubigeo': 'Ancash'}

    # Construir el HTML de cada trabajo
    trabajo_html = f"""
    <div class="trabajo">
        <h2>{titulo}</h2>
        <p>Enlace: <a href="{enlace}">{enlace}</a></p>
        <p>Fecha: {fecha}</p>
        <p>País: {pais}</p>
    """

    for seccion in info:
        titulo_seccion = seccion.find('h2').get_text(strip=True)
        contenido_seccion = seccion.find_all('span', attrs={'style': 'font-size:14.0px'})

        trabajo_html += f"<h3>{titulo_seccion}</h3>"
        for contenido_elemento in contenido_seccion:
            # Limpiar el texto y eliminar los espacios adicionales representados como &nbsp;
            texto_limpio = re.sub(r'\s+', ' ', contenido_elemento.get_text(strip=True).replace('\xa0', ' '))
            trabajo_html += f"<p>{texto_limpio}</p>"

    trabajo_html += "</div>"

    # Agregar el HTML del trabajo al contenido total
    contenido_html += trabajo_html

    contenido_html += '\n--------------------------------------------------------------------------------------\n'

# Escribir el contenido HTML en el archivo "contenido.html"
with open("contenido.html", "w", encoding="utf-8") as file:
    file.write(contenido_html)

print("Archivo 'contenido.html' creado satisfactoriamente.")
