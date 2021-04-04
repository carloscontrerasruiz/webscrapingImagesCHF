import logging
import os
import requests
from bs4 import BeautifulSoup # to parse HTML

logging.basicConfig(level=logging.INFO,format='%(asctime)s:%(message)s')

BASE_URL = 'https://agot.theangels.eu'
SAVE_FOLDER = 'imagenes'

def main():
    if not os.path.exists(SAVE_FOLDER):
        os.mkdir(SAVE_FOLDER)
    n_categorias = int(input('Cuantas categorias? '))
    n_imagenes = int(input('Cuantas imagenes descargaras por categoria? '))
    imagesUrlList = getImagesUrl(getImagesPageUrl(n_categorias,n_imagenes))
    logging.info('Lista de url de la imagen obtenidas')
    download_images(imagesUrlList)

def createBinder(category):
    category = category.strip().replace(" ", "").replace("'", "")
    if not os.path.exists(SAVE_FOLDER +'/'+ category):
        os.mkdir(SAVE_FOLDER +'/'+ category)
    logging.info('Se creo la carpeta '+category)
    return category
        

def getImagesPageUrl(n_categorias = 5,n_imagenes=5):
    logging.info('Se inicia busqueda las categorias y la pagina del detalle de las imagenes')
    with open("page.html") as fp:
        soup = BeautifulSoup(fp, 'html.parser')
        results = soup.findAll('div', {'class': 'resultSpacer'}, limit=n_categorias)
        img_url_list = []
        for tag in results:
            contadorImagenes = 0
            categoryName = createBinder(tag.span.text)
            while True:
                tag = tag.nextSibling
                if(tag['class'][0] != 'resultSpacer' and contadorImagenes < n_imagenes):
                    img_url_list.append({
                        "imagePageUrl":tag.a['href'],
                        "category":categoryName
                    })
                    contadorImagenes += 1
                else:
                    break
    logging.info('Se obtienen %s paginas del detalle de la imagen',len(img_url_list))
    return img_url_list

def cleanRoute(imageName):
    return imageName.strip().replace(" ", "").replace("'", "")

def getImagesUrl(imgpage_url_list):
    logging.info('Se ingresa a la pagina del detalle de cada imagen para obtener su url')
    img_url = []
    for search_url in imgpage_url_list:
        logging.info('Peticion a la pagina %s',search_url["imagePageUrl"])
        response = requests.get(search_url["imagePageUrl"])
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        results = soup.find('div',{'class':'boxRight'})
        imageName = soup.find('div',{'id':'card_name'})
        img_url.append({
            "imageUrl":BASE_URL + results.img['src'],
            "category":search_url["category"],
            "imageName":cleanRoute(imageName.a.text)
        })
    return img_url

def download_images(img_url_list):
    logging.info('Inicia descarga de imagenes...')
    for url in img_url_list:
        logging.info('Descargando imagen %s',url['imageName'])
        response = requests.get(url['imageUrl'])
        imagename = SAVE_FOLDER + '/' + url['category'] + '/' + url['imageName'] + '.jpg'
        with open(imagename, 'wb') as file:
            file.write(response.content)
    logging.info('Finaliza la descraga')


if __name__ == '__main__':
    main()