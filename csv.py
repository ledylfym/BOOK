from os import write
from os import close
import requests
from bs4 import BeautifulSoup
import csv

with open('faux.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(("Dylan", "Fabienne", "Fortune", "Natha"))
    writer.writerows("24", "45", "65", "30")
    csv_file.close()
