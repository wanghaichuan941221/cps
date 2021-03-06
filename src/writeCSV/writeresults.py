import csv
import time

need_to_write = True
time_at_start = time.time()

def write_to_csv_intial_motor1():
    if need_to_write:
        myFile = open('motor1.csv', 'w+')
        with myFile:
            myFields = ['time', 'setpoint1', 'theta1']
            writer = csv.DictWriter(myFile, fieldnames=myFields)
            writer.writeheader()
        myFile.close()

def write_to_csv_intial_motor234():
    if need_to_write:
        myFile = open('motor234.csv', 'w+')
        with myFile:
            myFields = ['time', 'setpoint2', 'setpoint3', 'setpoint4', 'theta2', 'theta3', 'theta4']
            writer = csv.DictWriter(myFile, fieldnames=myFields)
            writer.writeheader()
        myFile.close()


def write_to_csv_motor1(setpoint1, theta1):
    if need_to_write:
        myFile = open('motor1.csv', 'a')
        with myFile:
            myFields = ['time', 'setpoint_1', 'theta_1']
            writer = csv.DictWriter(myFile, fieldnames=myFields)
            cur_time = time.time()-time_at_start
            writer.writerow({'time': cur_time, 'setpoint_1': setpoint1, 'theta_1': theta1} )
        myFile.close()

def write_to_csv_motor234(setpoint234, theta234):
    if need_to_write:
        myFile = open('motor234.csv', 'a')
        with myFile:
            myFields = ['time', 'setpoint_2', 'setpoint_3', 'setpoint_4', 'theta_2', 'theta_3', 'theta_4']
            writer = csv.DictWriter(myFile, fieldnames=myFields)
            cur_time = time.time()-time_at_start
            writer.writerow({'time': cur_time, 'setpoint_2': setpoint234[0], 'setpoint_3': setpoint234[1], 'setpoint_4': setpoint234[2], 'theta_2': theta234[0], 'theta_3': theta234[1], 'theta_4': theta234[2]} )
        myFile.close()

write_to_csv_intial_motor1()
write_to_csv_intial_motor234()