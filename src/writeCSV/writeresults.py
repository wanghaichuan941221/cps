import csv
import time

setpoints = ['1', '2', '3', '4']
angles = ['5', '6', '7', '8']



def write_to_csv(setpoint, angle):
    myFile = open('results.csv', 'w')
    with myFile:
        myFields = ['time', 'setpoints', 'angles']
        writer = csv.DictWriter(myFile, fieldnames=myFields)
        writer.writeheader()
        cur_time = time.time()
        writer.writerow({'time': cur_time, 'setpoints': setpoint, 'angles': angle} )

def read_results():
    with open('results.csv') as myFile:
        reader = csv.DictReader(myFile)
        for row in reader:
            print(row['setpoint'])
            print(row['angle'])
            print(row['time'])

for i in range(0, len(setpoints)):
    write_to_csv(setpoints[i], angles[i])

read_results()