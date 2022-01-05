Hello people, welcome in my first project on Github
# BOOK
Is a project of OpenClassroom "Book to Scrape"

The language of my project is python and it works on Windows

# INSTALLATION
Open the file "Requierements" for all installations to the project

# USAGE
This project used to scrap informations on any sites. For this exemple, we use "https://books.toscrape.com/catalogue/page-1.html".

Before start the programm, we go create a virtual environnement. All installations of "Requierements" are in virtual environnement.

The first part, is collect some informations for one book, like "Title", "UPC", "Price", "Stock" and others.
The book I choice is "https://books.toscrape.com/catalogue/soumission_998/index.html". The programm of this exemple is "Un_livre"

The second part, is collect the same informations for all book of the site. I realize that in two parts :

- Firstly, the code "test" collect the link of all pages, then the links of every books on every pages and after that we applicate the same code of "Un_livre" to collect all informations to every book. We make a csv file with informations collected for any books. After that, we go collect links of every image to book. The problem of this code, is "Category of book" is not defined.

- Secondly, the code "final" is the solution. In that code, we go collect every links of every category and after every links of books in all categories. When we have this informations, we can use again the same code of "test".

# SUPPORT
I use Visual Studio Code.
