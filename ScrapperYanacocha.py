import pandas as pd
from funciones import getContenedor
from funciones import getTituloEnlace

def YanacochaScrap():
    # Url inicial
    URL = 'https://jobs.newmont.com'
    URL_BASE = URL + '/go/Business-Professionals/7986400/'

    # Obtener elementos de la paginacion
    contenedorPaginacion = getContenedor(URL_BASE,'ul',clase='pagination')
    # Los corchetes son para ignorar los li  que son enlaces para acceder a la primera y ultima pagina 
    paginacion = contenedorPaginacion.findAll('li')[1:-1]

    # Crear una lista para el dataframe
    trabajos_data = []

    for pagina in paginacion:
        # Obtener enlace de la pagina
        enlacePaginacion = URL + pagina.find('a')['href']

        # Obtener tabla y hacer un array de todas las filas
        contenedor = getContenedor(enlacePaginacion,'tbody')
        data_rows = contenedor.find_all('tr', class_='data-row')

        # Iterar las filas para obtener los daots
        for row in data_rows:
            claseTitulo = 'jobTitle-link'
            titulo, enlace = getTituloEnlace(row,URL,claseTitulo)

            descripcion_html = getContenedor(enlace,'span','jobdescription')
            
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

        #Eliminar el break para obtener todos los trabajos de todas las paginas
        break

    # Crear un DataFrame de 'trabajos_data' y crear un csv
    df = pd.DataFrame(trabajos_data)
    df.to_csv('CSV/trabajos_yanacocha.csv', index=False)

    print("Archivo 'trabajos_yanacocha.csv' creado satisfactoriamente.")

YanacochaScrap()