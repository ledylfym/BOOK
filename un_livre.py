import requests
from bs4 import BeautifulSoup

url = 'https://books.toscrape.com/catalogue/soumission_998/index.html'

reponse = requests.get(url)
book = {}

if reponse.ok:
    soup = BeautifulSoup(reponse.content, 'html.parser')

    title = soup.find('h1').text.strip()
    book['titre'] = title
            
    upc = soup.find('th', text='UPC')
    for a in upc:
        upcs = a.find_next('td').text.strip()
        book['upc'] = upcs

    price_tax = soup.find('th', text='Price (incl. tax)')
    for b in price_tax:
        prix = b.find_next('td').text.strip()
        book['prix_tax'] = prix

    price_no_tax = soup.find('th', text='Price (excl. tax)')
    for c in price_no_tax:
        prixe = c.find_next('td').text.strip()
        book['prix_sans_tax'] = prixe

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

    print(book)