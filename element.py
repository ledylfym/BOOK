import requests
from bs4 import BeautifulSoup

url = 'https://books.toscrape.com/catalogue/soumission_998/index.html'
urls = 'https://books.toscrape.com/catalogue/page-1.html'
reponse = requests.get(url)
reponse_test = requests.get(urls)
book = {}

def getbook(url):
    if reponse.ok:
        soup = BeautifulSoup(reponse.text, 'html.parser')

        titre = soup.find('h1').text.strip()
        book['titre'] = titre
            
        upc = soup.find('th', text='UPC')
        for a in upc:
            upcs = a.find_next('td').text.strip()
            book['upc'] = upcs

        prix_tax = soup.find('th', text='Price (incl. tax)')
        for b in prix_tax:
            prix = b.find_next('td').text.strip()
            book['prix_tax'] = prix

        prix_sans_tax = soup.find('th', text='Price (excl. tax)')
        for c in prix_sans_tax:
            prixe = c.find_next('td').text.strip()
            book['prix_sans_tax'] = prixe

        category = soup.find('th', text='Product Type')
        for c in category:
            genre = c.find_next('td').text.strip()
            book['category'] = genre

        stock = soup.find('th', text='Availability')
        for d in stock:
            stocke = d.find_next('td').text.strip()
            book['stock'] = stocke

        vues = soup.find('th', text='Number of reviews')
        for e in vues:
            vue = e.find_next('td').text.strip()
            book['vues'] = vue

        description = soup.find('h2', text='Product Description')
        for f in description:
            texte = f.find_next('p').text.strip()
            book['description'] = texte

        image = soup.find('link', {'rel': 'shortcut icon'}).findAll('href')
        book['image'] = image

        return book

def categorie(urls):
    if reponse_test.ok:
        soup = BeautifulSoup(reponse_test.text, 'html.parser')
        liste_categorie = soup.find('ul', {'class': 'nav nav-list'}).findAll('a')
        for i in liste_categorie:
            print(i.text.lstrip())
            print("")

        return liste_categorie

def listbook(urls):
    if reponse_test.ok:
        soup = BeautifulSoup(reponse.text, 'html.parser')
        liste = soup.findAll('h3')

    for title in liste:
        print(title.text)
    
    return liste
 


