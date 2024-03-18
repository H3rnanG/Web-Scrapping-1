import bs4
from bs4 import BeautifulSoup
import requests

URL_BASE = 'https://mastalento.antamina.com/search'
pedido_obtenido = requests.get(URL_BASE)
html_obtenido = pedido_obtenido.text

soup = BeautifulSoup(html_obtenido, "html.parser")

# Encontrar todos los elementos td con la clase 'colTitle'
colTitle = soup.find_all('td', class_='colTitle')

for elemento in colTitle:

    # Extraer el título
    titulo_elemento = elemento.find('span', class_='jobTitle').find('a', class_='jobTitle-link')
    titulo = titulo_elemento.text.strip() if titulo_elemento else None
    
    # Extraer la fecha
    fecha = elemento.find('span', class_='jobDate').text.strip()
    
    # Encontrar el país dentro del mismo contenedor del título
    pais_elemento = elemento.find_next_sibling('td', class_='colLocation').find('span', class_='jobLocation')
    pais = pais_elemento.text.strip() if pais_elemento else None
    
    # Extraer el enlace de mas informacion
    enlace = URL_BASE[0:-7] + titulo_elemento['href'] if titulo_elemento else None

    #  Obtenemos el Html de la pagina del enlace
    pedido_enlace = requests.get(enlace)
    html_enlace = pedido_enlace.text

    soupInfo = BeautifulSoup(html_enlace, "html.parser")

    # Encontrar el contenedor principal
    info = soupInfo.find('span', class_='jobdescription').find('div')

    # Verificar Divs
    # for i in info:
    #     print(i)
    #     print('\n\n\n')

    # Crear un diccionario para almacenar los datos extraídos
    datos = {}

    print("Título:", titulo)
    print("Enlace:", enlace)
    print("Fecha:", fecha)
    print("País:", pais)

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

    print('--------------------------------------------------------------------------------------')

