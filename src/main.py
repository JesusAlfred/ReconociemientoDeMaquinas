from traceback import print_tb
from google_images_search import GoogleImagesSearch
import os
import shutil
import pickle

def my_progressbar(url, progress):
    print(url[:10] + ' ' + str(progress) + '%')

dir = './../img/'
try:
  os.mkdir(dir)
except Exception as e:
  print(e)
  shutil.rmtree(dir)
  os.mkdir(dir)

#gis = GoogleImagesSearch('AIzaSyA0pSMDVGYmag6rpSNNRE1f4jjDjiF4qMU', '52431cda185b04ae5', progressbar_fn=my_progressbar)
gis = GoogleImagesSearch('AIzaSyA2uvjsmG_XSG-5NmneCvZ7IRnh5Ke4tXA', '52ed765d7c57849b7', progressbar_fn=my_progressbar)

listaDeBusquedas = [
  'weight training bench',
  'excercise cable machine'
]


for search in listaDeBusquedas:
  _search_params = {
      'q': search,
      'num': 100,
      'fileType': 'jpg|gif|png',
  }

  # this will search, download and resize:
  
  gis.search(search_params=_search_params)

  data = gis.results()
  file = open('./datos'+search+'.pc', 'wb')
  pickle.dump(data, file)
  file.close()


  file = open('./datos'+search+'.pc', 'rb')
  data = pickle.load(file)
  file.close()

  for image in data:
    print(image)
    image.url  # image direct url
    image.referrer_url  # image referrer url (source) 
    
    image.download(dir+search+'/')  # download image
    image.resize(500, 500)  # resize downloaded image

    image.path  # downloaded local file path
