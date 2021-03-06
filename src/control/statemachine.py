import time
from threading import Timer
import control.usbarm as usbarm
import math
import writeCSV.writeresults as writeresults
# Each of the state functions below performs some action and then implements
# logic to choose next state.  Each state function returns the next state.
from control.inverseKinematics import inverse_kinematics

setpoints_initial = [0,0,(1/2)*math.pi,0]
setpoints_droppoint = [-(1/2)*math.pi,(1/4)*math.pi,(1/2)*math.pi,-(1/4)*math.pi]
buffer = 0.04*math.pi
buffer_rot = 0.02*math.pi
state_counter = 0
setpoints_inv_kin = [0]*4
need_inv_kin = True
open_gripper = True
reached_object = False
rot_alarm_time = 0.1

def state0(angles, setpoints, tx, ty, con):
    print("state0 start")
    # delay and decision path to simulate some application logic
    if state_counter == 0:
        return state1
    elif state_counter == 1:
        return state5
    elif state_counter == 2:
        return state11
    elif state_counter == 3:
        return state13
    elif state_counter == 4:
        return state19
    else:
        return None



# ___________________________________________________________branch 1_______________________________________________________________

def state1(angles, setpoints, tx, ty, con):
    global reached_object
    print("state1 determine angle motor1 for initial setpoint")
    # delay and decision path to simulate some application logic

    error = usbarm.get_error(setpoints_initial, angles)
    if abs(error[0])>=buffer_rot:
        return state2
    if abs(error[0])<buffer_rot:
        reached_object = True
        return state3

def state2(angles, setpoints, tx, ty, con):
    print("state2 control motor1 for initial setpoint")
    usb_direction =  usbarm.get_usb_direction(setpoints_initial, angles)

    usbarm.ctrl(usb_direction[0])
    writeresults.write_to_csv_motor1(setpoints_initial[0],angles[0])

    if reached_object:
        Timer(rot_alarm_time,usbarm.stop_motors).start()
    return None

def state3(angles, setpoints, tx, ty, con):
    print("state3 motor1 is fine control angle motor1234")
    # delay and decision path to simulate some application logic
    error = usbarm.get_error(setpoints_initial, angles)


    if abs(error[1])<buffer and abs(error[2])< buffer and abs(error[3])< buffer:
        return state4
    else:
        usb_direction = usbarm.get_usb_direction(setpoints_initial, angles)
        total_movement = usbarm.get_total_movement([0,0,0], usb_direction[1], usb_direction[2], usb_direction[3])
        usbarm.ctrl(total_movement)
        writeresults.write_to_csv_motor234(setpoints_initial[1:4], angles[1:4])
        return None

def state4(angles, setpoints, tx, ty, con):
    global state_counter
    global open_gripper
    global reached_object
    print("state4 motor1234 are fine open and close gripper and set state counter to 1")
    usbarm.stop_motors()
    reached_object = False
    if open_gripper == True:
        usbarm.open_close_gripper(1)
        open_gripper = False
    state_counter = 1
    return state0

# ___________________________________________________________branch 2_______________________________________________________________



def state5(angles, setpoints, tx, ty, con):
    global reached_object
    print("state5 determine rotational setpoint for box")
    error = usbarm.get_error(setpoints, angles)
    if abs(error[0])>=buffer_rot:
        return state6
    if abs(error[0])<buffer_rot:
        reached_object = True
        return state7

def state6(angles, setpoints, tx, ty, con):
    print("state6 control motor1 for setpoint")
    global need_inv_kin
    usb_direction =  usbarm.get_usb_direction(setpoints, angles)
    usbarm.ctrl(usb_direction[0])
    writeresults.write_to_csv_motor1(setpoints[0],angles[0])

    need_inv_kin = True

    if reached_object:
        Timer(rot_alarm_time,usbarm.stop_motors).start()
    return None

def state7(angles, setpoints, tx, ty, con):
    print("state7 motor1 fine control angle motor234 for the box")
    global setpoints_inv_kin
    global need_inv_kin
    # delay and decision path to simulate some application logic
    start_time = time.time()

    setpoints_inv_kin[0] = setpoints[0]
    if need_inv_kin:
        usbarm.stop_motors()
        setpoints_inv_kin[1], setpoints_inv_kin[2], setpoints_inv_kin[3] = inverse_kinematics(angles[1], angles[2], angles[3], tx, ty)
        need_inv_kin = False

    print("CONTROLLER setpoints: ", setpoints_inv_kin[1], setpoints_inv_kin[2], setpoints_inv_kin[3])
    print("CONTROLLER INVERSE KIN TOOK ", (time.time() - start_time), "seconds")

    error = usbarm.get_error(setpoints_inv_kin, angles)

    if abs(error[1])<buffer and abs(error[2])< buffer and abs(error[3])< buffer :
        need_inv_kin = True
        return state8
    else:
        usb_direction = usbarm.get_usb_direction(setpoints_inv_kin, angles)
        total_movement = usbarm.get_total_movement([0,0,0], usb_direction[1], usb_direction[2], usb_direction[3])
        usbarm.ctrl(total_movement)
        writeresults.write_to_csv_motor234(setpoints_inv_kin[1:4], angles[1:4])

        return None


def state8(angles, setpoints, tx, ty, con):
    global state_counter
    global reached_object
    reached_object = False
    print("state8 control gripper to grab object and set state counter to 2")
    usbarm.stop_motors()
    state_counter = 2
    usbarm.open_close_gripper(2)
    return state0



# ___________________________________________________________branch 3_______________________________________________________________



def state11(angles, setpoints, tx, ty, con):
    print("state11 motor1 fine control angle motor234 for setpoints initial")
    # delay and decision path to simulate some application logic
    new_setpoints = [0]*4
    new_setpoints[0] = setpoints[0]
    new_setpoints[1] = setpoints_initial[1]
    new_setpoints[2] = setpoints_initial[2]
    new_setpoints[3] = setpoints_initial[3]

    print("check", new_setpoints)
    error = usbarm.get_error(new_setpoints, angles)


    if abs(error[1])<buffer and abs(error[2])< buffer and abs(error[3])< buffer:
        return state12
    else:
        usb_direction = usbarm.get_usb_direction(new_setpoints, angles)
        total_movement = usbarm.get_total_movement([0,0,0], usb_direction[1], usb_direction[2], usb_direction[3])
        usbarm.ctrl(total_movement)
        writeresults.write_to_csv_motor234(new_setpoints[1:4], angles[1:4])

        return None

def state12(angles, setpoints, tx, ty, con):
    global state_counter
    print("state12 go to droppoint and set state counter to 3")
    usbarm.stop_motors()
    state_counter = 3
    return state0



# ___________________________________________________________branch 4_______________________________________________________________


def state13(angles, setpoints, tx, ty, con):
    print("state13 determine rotational setpoint for droppoint")
    global reached_object
    error = usbarm.get_error(setpoints_droppoint, angles)
    if abs(error[0])>=buffer_rot:
        return state14
    if abs(error[0])<buffer_rot:
        reached_object = True
        return state15

def state14(angles, setpoints, tx, ty, con):
    print("state14 control motor1 for droppoint")
    usb_direction =  usbarm.get_usb_direction(setpoints_droppoint, angles)
    usbarm.ctrl(usb_direction[0])
    writeresults.write_to_csv_motor1(setpoints_droppoint[0],angles[0])


    if reached_object:
        Timer(rot_alarm_time,usbarm.stop_motors).start()

    return None

def state15(angles, setpoints, tx, ty, con):
    print("state15 motor1 fine control angle motor234 for droppoint")
    # delay and decision path to simulate some application logic
    error = usbarm.get_error(setpoints_droppoint, angles)

    if abs(error[1])<buffer and abs(error[2])< buffer and abs(error[3])< buffer:
        return state16
    else:
        usb_direction = usbarm.get_usb_direction(setpoints_droppoint, angles)
        total_movement = usbarm.get_total_movement([0,0,0], usb_direction[1], usb_direction[2], usb_direction[3])
        usbarm.ctrl(total_movement)
        writeresults.write_to_csv_motor234(setpoints_droppoint[1:4], angles[1:4])

        return None

def state16(angles, setpoints, tx, ty, con):
    global state_counter
    global reached_object
    print("state16 open gripper and set state counter to 4")
    reached_object = False
    usbarm.stop_motors()
    usbarm.open_close_gripper(1)
    state_counter = 4
    con.request_new_object()
    return None





# ___________________________________________________________branch 5_______________________________________________________________

def state19(angles, setpoints, tx, ty, con):
    print("state19")
    # delay and decision path to simulate some application logic
    new_setpoints = [0]*4
    new_setpoints[0] = setpoints_droppoint[0]
    new_setpoints[1] = setpoints_initial[1]
    new_setpoints[2] = setpoints_initial[2]
    new_setpoints[3] = setpoints_initial[3]

    print("check", new_setpoints)
    error = usbarm.get_error(new_setpoints, angles)


    if abs(error[1])<buffer and abs(error[2])< buffer and abs(error[3])< buffer:
        return state20
    else:
        usb_direction = usbarm.get_usb_direction(new_setpoints, angles)
        total_movement = usbarm.get_total_movement([0,0,0], usb_direction[1], usb_direction[2], usb_direction[3])
        usbarm.ctrl(total_movement)
        writeresults.write_to_csv_motor234(new_setpoints[1:4], angles[1:4])

        return None

def state20(angles, setpoints, tx, ty, con):
    global state_counter
    print("state20")
    usbarm.stop_motors()
    state_counter = 0
    return state0







