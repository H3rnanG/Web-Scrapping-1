from bs4 import BeautifulSoup 
import requests

def getContenedor(url, etiqueta, clase=None, ide=None):
    """
    Esta funcion retorna el contenedor de un elemento HTML en una pagina web.

    Args:
        url (string): url
        etiqueta (string): etiqueta html
        clase (string o array, opcional): clase de un elemento html
        ide (string o array, opcional): id de un elemento html

    Returns:
        contenedor: elemento html filtrado por clase y id
    """

    pedido_obtenido = requests.get(url)
    html_obtenido = pedido_obtenido.text

    soup = BeautifulSoup(html_obtenido, "html5lib")
    
    contenedor = soup.find(etiqueta, class_=clase, id=ide)

    return contenedor

def getTituloEnlace(row,url,claseTitulo=None,idTitulo=None):
    """
    Esta funcion retorna el titulo y el enlace de un elemento html

    Args:
        row (elemento): elemento de un array
        url (string): url
        claseTitulo (string o array, opcional): clase de un elemento html
        idTitulo (string o array, opcional): id de un elemento html
    """
    titulo_elemento = row.find('a', class_=claseTitulo, id=idTitulo)

    titulo = titulo_elemento.text.strip() if titulo_elemento else None

    enlace = url + titulo_elemento['href'] if titulo_elemento else None

    return titulo,enlace