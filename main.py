import os
import requests
from bs4 import BeautifulSoup # to parse HTML

BASE_URL = 'https://agot.theangels.eu'
SAVE_FOLDER = 'imagenes'

def main():
    if not os.path.exists(SAVE_FOLDER):
        os.mkdir(SAVE_FOLDER)
    n_categorias = int(input('Cuantas categorias? '))
    n_imagenes = int(input('Cuantas imagenes descargaras? '))
    createBinders(dowloand_categories(), n_categorias)
    imagesUrlList = getImagesUrl(getImagesPageUrl(n_imagenes))
    print('Lista de url de la imagen obtenidas')
    print(imagesUrlList)
    download_images(imagesUrlList)

def dowloand_categories():
    print('Iniciando creacion de carpetas para imagenes')
    with open("page.html") as fp:
        soup = BeautifulSoup(fp, 'html.parser')
        results = soup.findAll('span', {'class': 'resultSpacer_title'})
        category_list = []
        for re in results:
            category_list.append(re.text)
    print(f'Numero de categorias encontradas {len(category_list)}')
    return category_list

def createBinders(categories_list, n_categorias):
    numeroCarpetas = 0
    for category in categories_list:
        category = category.strip()
        category = category.replace(" ", "")
        if numeroCarpetas < n_categorias:
            if not os.path.exists(SAVE_FOLDER +'/'+ category):
                os.mkdir(SAVE_FOLDER +'/'+ category)
        else:
            break
        numeroCarpetas += 1
    print(f'Se crearon {numeroCarpetas} carpetas')
        
def getImagesPageUrl(n_imagenes):
    print('Iniciando obtencion de url de la pagina donde esta la imagen')
    with open("page.html") as fp:
        soup = BeautifulSoup(fp, 'html.parser')
        results = soup.findAll('div', {'class': 'cardLine'}, limit=n_imagenes)
        img_url_list = []
        for re in results:
            img_url_list.append(re.a['href'])
    return img_url_list

def getImagesUrl(imgpage_url_list):
    print('Se ingresa a la pagina de la imagen para obtener su url')
    img_url = []
    for search_url in imgpage_url_list:
        response = requests.get(search_url)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        results = soup.findAll('img',{'id':'cardImg1'})
        for re in results:
            img_url.append(BASE_URL + re['src'])
    return img_url

def download_images(img_url_list):
    print('Start dowloand images...')
    contador = 1
    for url in img_url_list:
         response = requests.get(url)
         imagename = SAVE_FOLDER + '/core' + str(contador) + '.jpg'
         with open(imagename, 'wb') as file:
             file.write(response.content)
         contador += 1
    print('Finaliza la descraga')


if __name__ == '__main__':
    main()