from bs4 import BeautifulSoup
import pandas as pd
import requests
from funciones import getContenedor,getTituloEnlace
import cloudscraper

from bs4 import BeautifulSoup
import pandas as pd
import requests
import cloudscraper

def CerroVerdeScrap():
    URL = 'https://freeport.bumeran.com.pe/'
    URL_BASE = URL + 'listadoofertas.bum'

    # Evitar CloudFlare
    scraper = cloudscraper.create_scraper()
    response = scraper.get(URL_BASE)
    html = response.text
    
    soup = BeautifulSoup(html, "html5lib")
    contenedor = soup.find('table',class_='grid')
    # Los corchetes son para ignorar el encabezado
    data_rows = contenedor.find_all('tr')[1:]

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
        soup = BeautifulSoup(html_enlace,"html5lib") 
        detalle = soup.find('div',class_='detalle')
        descripcion_html = detalle.find_all('div')[-1]

        # Agregar los datos del trabajo a la lista
        trabajos_data.append({
            'title': titulo,
            'description': descripcion_html,
            'url': enlace,
            'category': '85',
            'department': 'Arequipa',
            'province': 'Arequipa',
            'district': '',
            'company': 'Cerro Verde'
        })
    
    # Crear un DataFrame de Pandas con los datos de los trabajos
    df = pd.DataFrame(trabajos_data)

    # Guardar el DataFrame en un archivo CSV
    df.to_csv('CSV/trabajos_cerroVerde.csv', index=False)

    print("Archivo 'trabajos_cerroVerde.csv' creado satisfactoriamente.")

CerroVerdeScrap()
