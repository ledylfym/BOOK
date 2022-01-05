import csv
import requests
from bs4 import BeautifulSoup

for i in range(1, 51):

    url = 'https://books.toscrape.com/catalogue/page-{i}.html'
    page = (f'https://books.toscrape.com/catalogue/page-{i}.html')
    print(page)

    soup_page = BeautifulSoup(requests.get(page).content, 'html.parser')

    list_book = soup_page.find_all('h3')

    for title in list_book:
        print(title.text)

        title_book = title.find('a')
        link_book = title_book['href']
        p = link_book
        test = 'https://books.toscrape.com/catalogue/'
        url_book = (test + p)
        print(url_book)

        donc = requests.get(url_book)
        book = {}

        if donc.ok:

            soup = BeautifulSoup(donc.content, 'html.parser')

            title_books = soup.find('h1').text.strip()
            book['titre'] = title_books
            
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

            try:
                description = soup.find('h2', text='Product Description')
                for f in description:
                    texte = f.find_next('p').text.strip()
                    book['description'] = texte
            except:
                print('Pas de description')

            title_book_csv = soup.find('h1').text.strip()
                
            if ":" in title_book_csv:
                title_book_csv = title_book_csv.replace(":", "_")
        
            if "?" in title_book_csv:
                title_book_csv = title_book_csv.replace("?", "")
        
            if "**" in title_book_csv:
                title_book_csv = title_book_csv.replace("**", "")

            if "*" in title_book_csv:
                title_book_csv = title_book_csv.replace("*", "")

            if "/" in title_book_csv:
                title_book_csv = title_book_csv.replace("/", "_")
            
            if "\"" in title_book_csv:
                title_book_csv = title_book_csv.replace("\"", "_")
            
            with open(title_book_csv + '.csv', 'w', newline='', encoding='utf-8') as csv_file:
                spamwriter = csv.writer(csv_file, dialect='excel')
                spamwriter.writerows([[title_book_csv], [upcs], [prix], [prixe], [stocke], [vue], [texte]])

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

        if ":" in name:
            name = name.replace(":", "_")
        
        if "?" in name:
            name = name.replace("?", "")
        
        if "**" in name:
            name = name.replace("**", "")

        if "*" in name:
            name = name.replace("*", "")

        if "/" in name:
            name = name.replace("/", "_")

        if '"' in name:
            name = name.replace('"', '_')

        if "..." in name:
            name = name.replace("...", "")
    
        with open(name + '.jpg','wb') as f:
            response = requests.get(image_link)
            f.write(response.content)
            f.close()
        print(f'image de {name} récuperer')
        print("")
