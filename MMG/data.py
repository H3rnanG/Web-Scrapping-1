import bs4
from bs4 import BeautifulSoup
import requests
import re

# Necesario instalar 'pip install html5lib'  para que funcione la siguiente línea de código

URL_BASE = 'https://careers.mmg.com/caw/es/filter/?work-type=&location=&category=&search-keyword=&job-mail-subscribe-privacy=agree'
pedido_obtenido = requests.get(URL_BASE)
html_obtenido = pedido_obtenido.text

soup = BeautifulSoup(html_obtenido, "html5lib")

data_rows = soup.find_all('div', class_ = 'search-result')

# Verificar Divs
for i in data_rows:
    print(i)
    print('\n\n\n')

print("Archivo 'contenido.html' creado satisfactoriamente.")
