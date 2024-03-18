import bs4
from bs4 import BeautifulSoup
import requests

URL_BASE = 'https://mastalento.antamina.com/job/PRACTICANTE-DE-MEJORA-DE-NEGOCIO/636187819/'
pedido_obtenido = requests.get(URL_BASE)
html_obtenido = pedido_obtenido.text

# Crear el objeto BeautifulSoup
soup = BeautifulSoup(html_obtenido, "html.parser")

# Encontrar el contenedor principal
info = soup.find('span', class_='jobdescription').find('div')

# Verificar Divs
for i in info:
    print(i)
    print('\n\n\n')

# Crear un diccionario para almacenar los datos extraídos
datos = {}

for seccion in info:
    titulo = seccion.find('h2')
    contenido = seccion.find_all('span',attrs={'style':'font-size:14.0px'})

    if len(contenido) == 1:
        print(titulo.get_text(strip=True))
        print(contenido[0].get_text(strip=True)+'\n')
    elif len(contenido) > 1:
        print(f'{titulo.get_text(strip=True)}:')
        for elemento in contenido:
            print('- ' + elemento.get_text(strip=True))
        print('\n')