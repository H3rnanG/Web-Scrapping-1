import pandas as pd
from funciones import getContenedor

def YanacochaScrap():
    # Obtener contenedor
    URL = 'https://jobs.newmont.com'
    URL_BASE = URL + '/go/Business-Professionals/7986400/'

    contenedorPaginacion = getContenedor(URL_BASE,'ul',clase='pagination')
    paginacion = contenedorPaginacion.findAll('li')[1:-1]

    # Crear una lista para el dataframe
    trabajos_data = []

    for pagina in paginacion:
        enlacePaginacion = URL + pagina.find('a')['href']

        contenedor = getContenedor(enlacePaginacion,'tbody')
        data_rows = contenedor.find_all('tr', class_='data-row')

        for row in data_rows:
            # Titulo
            titulo_elemento = row.find('a',class_='jobTitle-link')
            titulo = titulo_elemento.text.strip() if titulo_elemento else None

            # Enlace
            enlace = URL + titulo_elemento['href'] if titulo_elemento else None

            descripcion_html = getContenedor(url=enlace,etiqueta='span',clase='jobdescription')
            
            # Agregar los datos del trabajo a la lista
            trabajos_data.append({
                'title': titulo,
                'description': descripcion_html,
                'url': enlace,
                'category': '85',
                'department': 'Cajamarca',
                'province': '',
                'district': '',
                'company': 'Minera Yanacocha'
            })

        # Eliminar este Brake para que se obtenga todos los trabajos de todas las páginas
        break

    # Crear un DataFrame de 'trabajos_data' y crear un csv
    df = pd.DataFrame(trabajos_data)
    df.to_csv('CSV/trabajos_yanacocha.csv', index=False)

    print("Archivo 'trabajos_yanacocha.csv' creado satisfactoriamente.")

YanacochaScrap()