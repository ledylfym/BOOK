from os import write
import requests
from bs4 import BeautifulSoup
import csv

with open('faux.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['Dylan'])

    with open('faux.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for line in csv_reader:
            print(line)

