import bs4
from bs4 import BeautifulSoup
import requests
import pandas as pd
from funciones import getContenedor,getTituloEnlace

def LasBambasScrap():
    # Necesario instalar 'pip install html5lib'  para que funcione la siguiente línea de código

    URL = 'https://careers.mmg.com'
    URL_BASE = URL + '/caw/es/listing'

    contenedor = getContenedor(URL_BASE,'div',ide='recent-jobs-content')
    data_rows = contenedor.find_all('div', class_='search-result')

    # Crear una lista para el dataframe
    trabajos_data = []

    for row in data_rows:
        titulo, enlace = getTituloEnlace(row, URL, 'job-link')

        descripcion_html = getContenedor(enlace,'div',ide='job-content')

        # Excluye las imágenes dentro del contenido
        for img in descripcion_html.find_all('img'):
            img.extract()

        # Encuentra todos los elementos <p> y <ul>
        descripcion_html = descripcion_html.find_all(['p', 'ul'])

        # Concatenar el HTML de cada trabajo sin las comas innecesarias y corchetes
        descripcion_html = ''.join([str(tag) for tag in descripcion_html if 'ProducimosCobreProducimosTalento' not in str(tag) and '<a class="apply-link button"' not in str(tag)])

        # Agregar los datos del trabajo a la lista
        trabajos_data.append({
            'title': titulo,
            'description': descripcion_html,
            'url': enlace,
            'category': '85',
            'department': 'Apurímac',
            'province': 'Cotabambas, Grau',
            'district': 'Challhuahuacho, Tambobamb, Coyllurqui, Progreso',
            'company': 'Las Bambas'
        })

    # Crear un DataFrame de Pandas con los datos de los trabajos
    df = pd.DataFrame(trabajos_data)

    # Guardar el DataFrame en un archivo CSV
    df.to_csv('CSV/trabajos_mmg.csv', index=False)

    print("Archivo 'trabajos_mmg.csv' creado satisfactoriamente.")

LasBambasScrap()