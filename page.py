import requests
from bs4 import BeautifulSoup
import os

url = 'https://books.toscrape.com/catalogue/page-1.html'
reponse = requests.get(url)
soup = BeautifulSoup(reponse.content, 'html.parser')

images = soup.find_all('img')

for image in images:
    name = image['alt']
    x = image
    new_name = x['src'][3:]
    image_link = f'https://books.toscrape.com/{new_name}'
    print(f'recupération image livre {name}')
    print(image_link)
    with open(name + '.jpg','wb') as f:
        response = requests.get(image_link)
        f.write(response.content)
        f.close()
        print(f'image de {name} récuperer')
