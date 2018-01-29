import csv

myFile = open('countries.csv', 'w')
with myFile:
    myFields = ['country', 'capital']
    writer = csv.DictWriter(myFile, fieldnames=myFields)
    writer.writeheader()
    writer.writerow({'country' : 'France', 'capital': 'Paris'})
    writer.writerow({'country' : 'Italy', 'capital': 'Rome'})
    writer.writerow({'country' : 'Spain', 'capital': 'Madrid'})
    writer.writerow({'country' : 'Russia', 'capital': 'Moscow'})


with open('countries.csv') as myFile:
    reader = csv.DictReader(myFile)
    for row in reader:
        print(row['country'])
