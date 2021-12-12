import requests
from bs4 import BeautifulSoup

for i in range(1, 51):

    url = 'https://books.toscrape.com/catalogue/page-{i}.html'
    page = (f'https://books.toscrape.com/catalogue/page-{i}.html')
    print(page)
    soup = BeautifulSoup(requests.get(page).content, 'html.parser')

    liste_categorie = soup.find('ul', {'class': 'nav nav-list'}).findAll('a')
    for k in liste_categorie:
        print(k.text.lstrip())
        print("")

        liste = soup.findAll('h3')
        print(liste)
        print("")
