import requests
from bs4 import BeautifulSoup
import os

url = 'https://books.toscrape.com/catalogue/page-1.html'
reponse = requests.get(url)

soup = BeautifulSoup(reponse.text, 'html.parser')

images = soup.find_all('img')

for image in images:
    name = image['alt']
    link = image['src']
    with open(name + '.jpg', 'wb') as f:
        im = requests.get(link)
        f.write(im.content)
