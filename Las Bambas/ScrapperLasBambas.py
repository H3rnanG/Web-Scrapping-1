import bs4
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd

def LasBambasScrap():
    # Necesario instalar 'pip install html5lib'  para que funcione la siguiente línea de código

    URL_BASE = 'https://careers.mmg.com/caw/es/filter/?work-type=&location=&category=&search-keyword=&job-mail-subscribe-privacy=agree'
    pedido_obtenido = requests.get(URL_BASE)
    html_obtenido = pedido_obtenido.text

    soup = BeautifulSoup(html_obtenido, "html5lib")

    # Encontrar todos los elementos con la clase 'search-result'
    data_rows = soup.find('div', id='recent-jobs-content').find_all('div', class_='search-result')

    # Crear una lista para el dataframe
    trabajos_data = []

    for row in data_rows:
        # Extraer el titulo
        titulo_elemento = row.find('h3').find('a', class_='job-link')
        titulo = titulo_elemento.text.strip() if titulo_elemento else None
        
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

        # Concatenar el HTML de cada trabajo sin las comas innecesarias y corchetes
        descripcion_html = ''.join([str(tag) for tag in info if 'ProducimosCobreProducimosTalento' not in str(tag) and '<a class="apply-link button"' not in str(tag)])

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
    df.to_csv('Las Bambas/trabajos_mmg.csv', index=False)

    print("Archivo 'trabajos_mmg.csv' creado satisfactoriamente.")
