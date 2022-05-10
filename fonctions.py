import time
from pathlib import Path
import csv
from slugify import slugify
from unicodedata import category
from webbrowser import get
import requests
from bs4 import BeautifulSoup

url_base = "https://books.toscrape.com/catalogue/page-1.html"

def get_links_urls_categories(url_base):
    """Return list of categories urls"""
    reponse = requests.get(url_base)
    soup = BeautifulSoup(reponse.text, 'html.parser')
    if not reponse.ok:
        print('Une erreur est survenue lors de la requête')
        return None

    liste_categorie = soup.find('ul', {'class': 'nav nav-list'}).findAll('a')
    categories_urls = []
    for categorie in liste_categorie:
        link_category = 'https://books.toscrape.com/catalogue/' + categorie['href']
        categories_urls.append(link_category)

    categories_urls.pop(0)

    return categories_urls
    
def get_name_categories(url):
    categorie_name = url[52:]    
    
    slash_position = categorie_name.index("_")
    categorie_name = categorie_name[:slash_position]
    print(f'Récupération des livres de {categorie_name}')
    print("")
    return categorie_name

def get_urls_books(url):
    reponse = requests.get(url)
    soup = BeautifulSoup(reponse.text, 'html.parser')
    if not reponse.ok:
        print('Une erreur est survenue lors de la récupération de lurl')

    book = soup.find_all('h3')
    book_urls = []            
    for link in book:
        title_book = link.find('a')
        link_book = title_book['href']
        new_book = link_book[6:]
        if "../" in new_book:
            try:
                new_book = link_book[9:]
            except:
                print('erreur url')    
            new_link_books = f'https://books.toscrape.com/catalogue/{new_book}'
            book_urls.append(new_link_books)

    return book_urls

def get_data_book(url):
    reponse = requests.get(url)
    soup = BeautifulSoup(reponse.text, 'html.parser')
    book = {}
    if not reponse.ok:
        print('Une erreur est survenue dans la récupération du livre')

    title = soup.find('h1').text.strip()
    book['title'] = title

    category_li = soup.find_all("li")[2]
    category = category_li.a.text
    book['categories'] = category

    upc = soup.find('th', text='UPC')
    for a in upc:
        upcs = a.find_next('td').text.strip()
        book['upc'] = upcs

    prix_tax = soup.find('th', text='Price (incl. tax)')
    for b in prix_tax:
        prix = b.find_next('td').text.strip()
        book['price_tax'] = prix[1:]

    prix_sans_tax = soup.find('th', text='Price (excl. tax)')
    for c in prix_sans_tax:
        prix = c.find_next('td').text.strip()
        book['price_no_tax'] = prix[1:]

    stock = soup.find('th', text='Availability')
    for d in stock:
        stocke = d.find_next('td').text.strip()
        book['stock'] = stocke[11:12]

    try:
        description = soup.find('h2', text='Product Description')
        for f in description:
            texte = f.find_next('p').text.strip()
            book['description'] = texte
    except:
        print('Pas de description')

    stars = soup.find_all("div", class_='col-sm-6 product_main')
    for e in stars:
        if e.find("p", class_='star-rating One'):
            star = "1"
        elif e.find("p", class_='star-rating Two'):
            star = "2"
        elif e.find("p", class_='star-rating Three'):
            star = "3"
        elif e.find("p", class_='star-rating Four'):
            star = "4"
        elif e.find("p", class_='star-rating Five'):
            star = "5"
        else:
            star = "Pas de notes"
        book['stars'] = star

    image_book = soup.find('img')
    for image in image_book:
        source = image['src']
        new_source = source[3:]
        if '../' in new_source:
            try:
                new_source = source[6:]
            except:
                print('erreur url image')
        link_image = f'https://books.toscrape.com/{new_source}'
        book['image_url'] = link_image
        book['image_file'] = "data/img/{slugify(book.get('title'))}.jpg"


    return book

def get_link_images(url):
    reponse = requests.get(url)
    soup = BeautifulSoup(reponse.text, 'html.parser')
    book_image = soup.find('div', class_='item active')
    for image in book_image:
        source = image['src']
        new_source = source[3:]
        if '../' in new_source:
            try:
                new_source = source[6:]
            except:
                print('erreur url image')
        link_image = f'https://books.toscrape.com/{new_source}'

    return link_image

def main():
    categories_urls = get_links_urls_categories(url_base)
    for category_url in categories_urls:
        # print(category_url)
        name_categories = get_name_categories(category_url)
        print(f"\nTraitement de la catégorie : {name_categories} en cours ...")
        books_urls = get_urls_books(category_url)
        # print(books_urls)
        books_data = []
        print(f"\nRécupération des livres de la catégorie : {name_categories} en cours ...")
        for book_url in books_urls:
            book_data = get_data_book(book_url)
            books_data.append(book_data)
        
        Path("data/csv").mkdir(parents=True, exist_ok=True)

        header = books_data[0].keys()

        print(f"\nSauvegarde des livres de la catégorie : {name_categories} en cours ...")

        with open(f"data/csv/{name_categories}.csv", "w", encoding="utf-8-sig", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=header, dialect="excel")
            writer.writeheader()
            writer.writerows(books_data)

        Path("data/img").mkdir(parents=True, exist_ok=True)

        print(f"\nRécupération des images de la catégorie : {name_categories} en cours ...")

        for book in books_data:
            with open(f"data/img/{slugify(book.get('title'))}.jpg", "wb") as f:
                image_url = book.get("image_url")
                reponse = requests.get(image_url)
                f.write(reponse.content)
        





if __name__ == "__main__":
    main()

""" PSEUDO CODE
Récupérer la liste des urls des catégories

Pour chaque url des catégories

    Récupérer la liste des urls des livres de la catégorie (Gérer le multi page)

    Pour chaque url des livres
        Récupérer les données du livre
    
    Sauvegarder le résultat (les données des livres) dans un fichier csv

    Sauvegarder les images des livres de la catégories(comprend la requete pour récupérer le contenu)

    Path("data/csv").mkdir(parents=True, exist_ok=True)

    from pathlib import Path

    title = "It's Only the Himalayas"
    print(f"titre avant slufigy : {title}")
    print(f"titre après :  {slugify(title)}")

    import csv

# Un exemple des données
books_data = [
    {"title": "Titre 1", "description": "Description 1", "price": 29},
    {"title": "Titre 2", "description": "Description 2", "price": 39},
    {"title": "Titre 3", "description": "Description 3", "price": 49},
]

# Récupération des clé pour les entetes du fichier csv
header = books_data[0].keys()

with open(f"data/exemple.csv", "w", encoding="utf-8-sig", newline="") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=header, dialect="excel")
    writer.writeheader()
    writer.writerows(books_data)

def get_categorie_name(url: str) -> str:
    ""Return the name of the categorie from the url""

    # Extract the last part of the url containing the category name
    categorie_name = url[51:]    
    
    # Find the position of the "_" char
    slash_position = categorie_name.index("_")
    categorie_name = categorie_name[:slash_position]
    return categorie_name

"""