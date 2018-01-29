import csv
import time

myFile = open('countries.csv', 'w')
setpoints = ['France', 'Italy', 'Spain, Russia']
angles = ['Paris', 'Rome', 'Madrid', 'Moscow']

with myFile:
    myFields = ['setpoint', 'angle', 'time']
    writer = csv.DictWriter(myFile, fieldnames=myFields)
    writer.writeheader()

    for i in range(0,len(setpoints)):
        cur_time = time.time()

        writer.writerow({'setpoint': setpoints[i], 'angle': angles[i], 'time': cur_time} )


with open('countries.csv') as myFile:
    reader = csv.DictReader(myFile)
    for row in reader:
        print(row['setpoint'])
        print(row['angle'])
        print(row['time'])