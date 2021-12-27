import csv

test = [1,2,3,4,5,6]
for i in test:

    with open('faux.csv', 'w', newline='') as csv_file:
        spamwriter = csv.writer(csv_file)
        spamwriter.writerow(i)
        


