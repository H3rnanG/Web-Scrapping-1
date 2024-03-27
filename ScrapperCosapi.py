import bs4
from bs4 import BeautifulSoup 
import pandas as pd
from funciones import getContenedor,getTituloEnlace

def CosapiScrap():
    # Obtener contenedor
    URL = 'https://unete.cosapi.com.pe'
    URL_BASE = URL + '/search/?createNewAlert=false&q='

    contenedor = getContenedor(URL_BASE,'tbody')
    data_rows = contenedor.find_all('tr')

    # Crear una lista para el dataframe
    trabajos_data = []

    for row in data_rows:
        titulo, enlace = getTituloEnlace(row, URL, 'jobTitle-link')

        descripcion_html = getContenedor(enlace,'span','jobdescription').find('div')

        # Agregar los datos del trabajo a la lista
        trabajos_data.append({
            'title': titulo,
            'description': descripcion_html,
            'url': enlace,
            'category': '85',
            'department': 'Ica',
            'province': '',
            'district': '',
            'company': 'Cosapi'
        })

    # Crear un DataFrame de 'trabajos_data' y crear un csv
    df = pd.DataFrame(trabajos_data)
    df.to_csv('CSV/trabajos_cosapi.csv', index=False)

    print("Archivo 'trabajos_cosapi.csv' creado satisfactoriamente.")

CosapiScrap()