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

    URL_BASE = url
    pedido_obtenido = requests.get(URL_BASE)
    html_obtenido = pedido_obtenido.text

    soup = BeautifulSoup(html_obtenido, "html5lib")
    
    if clase is not None and ide is not None:
        contenedor = soup.find(etiqueta, class_=clase, id=ide)
    elif clase is not None:
        contenedor = soup.find(etiqueta, class_=clase)
    elif ide is not None:
        contenedor = soup.find(etiqueta, id=ide)
    else:
        contenedor = soup.find(etiqueta)

    return contenedor