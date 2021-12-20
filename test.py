import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

for i in range(1, 51):

    url = 'https://books.toscrape.com/catalogue/page-{i}.html'
    page = (f'https://books.toscrape.com/catalogue/page-{i}.html')
    print(page)

    cherche = BeautifulSoup(requests.get(page).content, 'html.parser')

    liste = cherche.find_all('h3')

    for title in liste:
        print(title.text)

        livre = title.find('a')
        lien_livre = livre['href']
        p = lien_livre
        test = 'https://books.toscrape.com/catalogue/'
        url_livre = (test + p)
        donc = requests.get(url_livre)
        book = {}

        if donc.ok:

            soup = BeautifulSoup(donc.content, 'html.parser')

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

            stock = soup.find('th', text='Availability')
            for d in stock:
                stocke = d.find_next('td').text.strip()
                book['stock'] = stocke

            vues = soup.find('th', text='Number of reviews')
            for e in vues:
                vue = e.find_next('td').text.strip()
                book['vues'] = vue

            try:
                description = soup.find('h2', text='Product Description')
                for f in description:
                    texte = f.find_next('p').text.strip()
                    book['description'] = texte
            except:
                print('Pas de description')

            print(book)
            print("")

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
        print("")
