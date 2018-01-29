import csv
import time

myFile = open('countries.csv', 'w')
countries = [France, Italy, Spain, Russia]
capital = [Paris, Rome, Madrid, Moscow]

with myFile:
    myFields = ['country', 'capital']
    writer = csv.DictWriter(myFile, fieldnames=myFields)
    writer.writeheader()

    for i in range(0,len(countries)):
        writer.writerow({'country' : countries[i], 'capital': capital[i]})


with open('countries.csv') as myFile:
    reader = csv.DictReader(myFile)
    for row in reader:
        print(row['country'])
        print(row['capital'])