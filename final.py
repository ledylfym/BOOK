import time
import requests
from bs4 import BeautifulSoup

url = 'https://books.toscrape.com/catalogue/page-1.html'
reponse = requests.get(url)
book = {}

soup = BeautifulSoup(reponse.text, 'html.parser')

liste_categorie = soup.find('ul', {'class': 'nav nav-list'}).findAll('a')
for categorie in liste_categorie:
    link_category = 'https://books.toscrape.com/catalogue/' + categorie['href']
    new_link = requests.get(link_category)
    
    if new_link.ok:
        soupe = BeautifulSoup(new_link.content, 'html.parser')

        title_category = soupe.find('h1').text.strip()
        print(f'récupération des livres de {title_category}')
        print("")
        time.sleep(2)
        print(title_category)

        books = soupe.find_all('h3')            
        for link in books:
            title_book = link.find('a')
            link_book = title_book['href']
            new_book = link_book[6:]
            if "../" in new_book:
                try:
                    new_book = link_book[9:]
                except:
                    print('erreur url')    
            new_link_books = f'https://books.toscrape.com/catalogue/{new_book}'
            
            donc = requests.get(new_link_books)
            if donc.ok:
                soup_book = BeautifulSoup(donc.content, 'html.parser')

                titre = soup_book.find('h1').text.strip()
                book['titre'] = titre

                upc = soup_book.find('th', text='UPC')
                for a in upc:
                    upcs = a.find_next('td').text.strip()
                    book['upc'] = upcs

                prix_tax = soup_book.find('th', text='Price (incl. tax)')
                for b in prix_tax:
                    prix = b.find_next('td').text.strip()
                    book['prix_tax'] = prix

                prix_sans_tax = soup_book.find('th', text='Price (excl. tax)')
                for c in prix_sans_tax:
                    prixe = c.find_next('td').text.strip()
                    book['prix_sans_tax'] = prixe

                stock = soup_book.find('th', text='Availability')
                for d in stock:
                    stocke = d.find_next('td').text.strip()
                    book['stock'] = stocke

                vues = soup_book.find('th', text='Number of reviews')
                for e in vues:
                    vue = e.find_next('td').text.strip()
                    book['vues'] = vue

                try:
                    description = soup_book.find('h2', text='Product Description')
                    for f in description:
                        texte = f.find_next('p').text.strip()
                        book['description'] = texte
                except:
                    print('Pas de description')
                
                print(book)
                print("")
    time.sleep(2)
    print(f'tous les livres de la catégorie {title_category} ont été récupéré')
    print("")

    images = soup_book.find_all('img')
    for image in images:
        name = image['alt']
        x = image
        new_name = x['src'][3:]
        image_link = f'https://books.toscrape.com/{new_name}'
        print(f'recupération image livre {name}')
        print(image_link)

        if ":" in name:
            name = name.replace(":", "_")
        
        if "?" in name:
            name = name.replace("?", "")
        
        if "**" in name:
            name = name.replace("**", "")
    
        with open(name + '.jpg','wb') as f:
            response = requests.get(image_link)
            f.write(response.content)
            f.close()
        print(f'image de {name} récuperer')
        print("")