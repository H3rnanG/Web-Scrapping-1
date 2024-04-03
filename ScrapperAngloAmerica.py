import bs4
from bs4 import BeautifulSoup
import requests
import pandas as pd
from funciones import getContenedor,getTituloEnlace
import cloudscraper
import json
import re

def corregir_description(cleaned_description):
    # Definir el patrón para buscar y reemplazar las comillas dobles dentro de "description"
    patron = r'("description":")(.*?)(",\s*"industry")'

    # Definir una función de reemplazo personalizada
    def reemplazo(match):
        # Extraer la parte de la cadena que está entre las comillas dobles
        parte_interior = match.group(2)
        # Reemplazar las comillas dobles con comillas simples
        parte_interior_corregida = parte_interior.replace('"', "“")
        # Devolver la cadena modificada con las comillas dobles corregidas
        return match.group(1) + parte_interior_corregida + match.group(3)

    # Aplicar el reemplazo utilizando el patrón y la función de reemplazo
    descripcion_corregida = re.sub(patron, reemplazo, cleaned_description)

    return descripcion_corregida

def AngloAmericanScrap():
    URL = 'https://www.angloamerican.com'
    URL_BASE = URL + '/careers/job-opportunities/apply'

    # Evitar CloudFlare
    scraper = cloudscraper.create_scraper()
    response = scraper.get(URL_BASE)
    html = response.text

    soup = BeautifulSoup(html, "html5lib")
    contenedor = soup.find('div',class_='hidden-joblist')
    
    data_rows = contenedor.find_all('li')

    # Crear una lista para el dataframe
    trabajos_data = []

    for row in data_rows:
        # Obtener titulo
        titulo_elemento = row.find('a')
        titulo = titulo_elemento.text.strip() if titulo_elemento else None

        # Obtener enlace
        enlace = URL + titulo_elemento['href'] if titulo_elemento else None

        # Evitar CloudFlare
        response_enlace = scraper.get(enlace)
        html_enlace = response_enlace.text

        # Obtener descripcion
        soup_descripcion = BeautifulSoup(html_enlace, "html.parser")
        script_element = soup_descripcion.find("script", {"type": "application/ld+json"})

        # Obtener el contenido del script
        script_content = script_element.string

        # Limpiar el JSON eliminando caracteres de control
        cleaned_json = re.sub(r'[\x00-\x1F\x7F-\x9F]', '', script_content)
        cleaned_description = corregir_description(cleaned_json)

        job_data = json.loads(cleaned_description)
    
        # Obtener la descripción del trabajo
        descripcion_trabajo = job_data.get('description', None)

        # Agregar los datos del trabajo a la lista
        trabajos_data.append({
            'title': titulo,
            'description': descripcion_trabajo,
            'url': enlace,
            'category': '85',
            'department': '',
            'province': '',
            'district': '',
            'company': 'Anglo American'
        })

    # Crear un DataFrame de Pandas con los datos de los trabajos
    df = pd.DataFrame(trabajos_data)

    # Guardar el DataFrame en un archivo CSV
    df.to_csv('CSV/trabajos_cerroVerde.csv', index=False)

    print("Archivo 'trabajos_cerroVerde.csv' creado satisfactoriamente.")

AngloAmericanScrap()
