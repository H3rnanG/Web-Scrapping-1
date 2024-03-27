import bs4
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
from funciones import getContenedor,getTituloEnlace

def AntaminaScrap():
    # Necesario instalar 'pip install html5lib'  para que funcione la siguiente línea de código

    URL = 'https://mastalento.antamina.com'
    URL_BASE = URL + '/search'

    contenedor = getContenedor(URL_BASE,'tbody')
    data_rows = contenedor.find_all('tr', class_='data-row')

    # Crear una lista para almacenar los datos de cada trabajo
    trabajos_data = []

    for row in data_rows:
        titulo, enlace = getTituloEnlace(row,URL,'jobTitle-link')

        # Encontrar el contenedor principal
        info = getContenedor(enlace,'span','jobdescription').find('div')

        # Construir la descripción HTML del trabajo
        descripcion_html = ""
        for seccion in info:
            titulo_seccion = seccion.find('h2').get_text(strip=True)
            contenido_seccion = seccion.find_all('span', attrs={'style': 'font-size:14.0px'})

            descripcion_html += f"<h3>{titulo_seccion}</h3>"
            for contenido_elemento in contenido_seccion:
                # Limpiar el texto y eliminar los espacios adicionales representados como &nbsp;
                texto_limpio = re.sub(r'\s+', ' ', contenido_elemento.get_text(strip=True).replace('\xa0', ' '))
                descripcion_html += f"<p>{texto_limpio}</p>"
        
        # Agregar los datos del trabajo a la lista
        trabajos_data.append({
            'title': titulo,
            'description': descripcion_html,
            'url': enlace,
            'category': '85',
            'department': 'Ancash',
            'province': 'Huari',
            'district': 'San Marcos',
            'company': 'Antamina'
        })

    # Crear un DataFrame de Pandas con los datos de los trabajos
    df = pd.DataFrame(trabajos_data)

    # Guardar el DataFrame en un archivo CSV
    df.to_csv('CSV/trabajos_antamina.csv', index=False)

    print("Archivo 'trabajos_antamina.csv' creado satisfactoriamente.")

AntaminaScrap()