from time import sleep
from random import random
import operator
import usbarm
import math

# Each of the state functions below performs some action and then implements
# logic to choose next state.  Each state function returns the next state.

go_to_initial_position = True
open_graper = True
setpoints_initial = [0,0,0,0]
buffer = 0.1*math.pi


def state0(time, angles, setpoint):
    print("state0_start")
    # delay and decision path to simulate some application logic
    if go_to_initial_position == True:
        return state1
    else:
        return None


def state1(time, angles, setpoint):
    print("state1_determine_angle_first_motor")
    # delay and decision path to simulate some application logic
    error = usbarm.get_error(setpoints_initial, angles)
    sleep(.5)
    if abs(error[0])>=buffer:
        return state2
    if abs(error[0])<buffer:
        return state3

def state2(time, angles, setpoint):
    print("state2_control_motor1")
    usb_direction =  usbarm.get_usb_direction(setpoints_initial, angles)

    usbarm.ctrl(usb_direction[0])
    return None

def state3(time, angles, setpoint):
    print("state3_motor1_fine_control_motor234")
    # delay and decision path to simulate some application logic
    error = usbarm.get_error(setpoints_initial, angles)
    usb_direction =  usbarm.get_usb_direction(setpoints_initial, angles)
    total_movement = usbarm.get_total_movement(usb_direction[0], usb_direction[1], usb_direction[2], usb_direction[3])

    usbarm.ctrl(total_movement)

    if abs(error[1])<buffer and abs(error[2])< buffer and abs(error[3])< buffer:
        return state4
    else:
        return None

def state4(time, angles, setpoint):
    global go_to_initial_position
    global open_graper
    open_graper = False
    usbarm.open_close_gripper(1)
    go_to_initial_position = False
    usbarm.open_close_gripper(2)
    return None



