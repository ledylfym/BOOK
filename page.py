import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

url = 'https://books.toscrape.com/catalogue/page-1.html'
liste_url = []
liste_url.append(url)

page_en_cours = url
page_en_cours_parse = BeautifulSoup(requests.get(page_en_cours).content, 'html.parser')

while page_en_cours_parse.find('li', class_='next'):
    for i in page_en_cours_parse.find_all('li', class_='next'):
        page_suivante = i.find('a')
        url_page_suivante = urljoin(page_en_cours, page_suivante['href'])

liste_url.append(url_page_suivante)
page_en_cours = url_page_suivante
page_en_cours_parse = BeautifulSoup(requests.get(page_en_cours).content, 'html.parser')

print(liste_url)