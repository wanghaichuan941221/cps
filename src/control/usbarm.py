from time import sleep
import operator
import atexit

# Define the exit handler
def exithandler():
    if usb_arm == None:
        raise Exception("Robotic arm not connected")
    # Stop the movement after waiting a specified duration
    usb_arm.ctrl_transfer(0x40, 6, 0x100, 0, [0, 0, 0], 1000)
    print("Stopping motors now, goodbye")

atexit.register(exithandler)

# Define a procedure to connect to the arm via USB
def connect():
    '''
    Connect to the USB arm.
    '''
    global usb_arm
    # Attempt to import the USB and time libraries into Python
    #try:
    #    from time import sleep
    #except:
    #    raise Exception("Time library not found")
    try:
        import usb.core, usb.util
    except:
        raise Exception("USB library not found")
    usb_arm = usb.core.find(idVendor=0x1267, idProduct=0x001)
    # Check if the arm is detected and warn if not
    if usb_arm == None:
        raise Exception("Robotic arm not found")
    else:
        return True

# Define commands to control arm
rotate_ccw = [0,2,0] # Rotate base counter-clockwise
rotate_cw = [0,1,0] # Rotate base clockwise
shoulder_up = [128,0,0] # Shoulder up
shoulder_down = [64,0,0] # Shoulder down
elbow_up = [16,0,0] # Elbow up
elbow_down = [32,0,0] # Elbow down
wrist_up = [8,0,0] # Wrist up
wrist_down = [4,0,0] # Wrist down
grip_open = [2,0,0] # Open grip
grip_close = [1,0,0] # Close grip
light_on = [0,0,1] # Light on
off = [0,0,0] # something is turned off

# Define safety angles in radians
# save_angles = [rotate_upper, rotate_lower, shoulder_upper, shoulder_lower, elbow_upper, elbow_lower, wrist_upper, wrist_lower]
save_angles= [2.094, -2.094, 1.571, - 1.396, 2.793, -2.793, 0.960, -0.960]

def safe_setpoints(setpoints):
    for x in range(0, len(setpoints)):
        if setpoints[x]>=save_angles[2*x]:
            setpoints[x]=save_angles[2*x]
        elif setpoints[x]<=save_angles[(2*x)+1]:
            setpoints[x]=save_angles[(2*x)+1]
        #else:
            #print("no unsafe setpoint found", x, setpoints[x])

    return setpoints

# Define what the direction is for the rotate joint
def rotate(clock_counterclock):
    if clock_counterclock == 0:
        rotate_ = off
    elif clock_counterclock == 1:
        rotate_ = rotate_cw
    elif clock_counterclock == 2:
        rotate_ = rotate_ccw
    else:
        print("error rotate can not be lower than 0 or higher then 2 now set to 0")
        rotate_ = 0
    return rotate_

# Define what the direction is for the shoulder joint
def shoulder(clock_counterclock):
    if clock_counterclock == 0:
        shoulder_ = off
    elif clock_counterclock == 1:
        shoulder_ = shoulder_up
    elif clock_counterclock == 2:
        shoulder_ = shoulder_down
    else:
        print("error rotate can not be lower than 0 or higher then 2 now set to 0")
        shoulder_ = 0
    return shoulder_

# Define what the direction is for the elbow joint
def elbow(clock_counterclock):
    if clock_counterclock == 0:
        elbow_ = off
    elif clock_counterclock == 1:
        elbow_ = elbow_up
    elif clock_counterclock == 2:
        elbow_ = elbow_down
    else:
        print("error rotate can not be lower than 0 or higher then 2 now set to 0")
        elbow_ = 0
    return elbow_

# Define what the direction is for the wrist joint
def wrist(clock_counterclock):
    if clock_counterclock == 0:
        wrist_ = off
    elif clock_counterclock == 1:
        wrist_ = wrist_up
    elif clock_counterclock == 2:
        wrist_ = wrist_down
    else:
        print("error rotate can not be lower than 0 or higher then 2 now set to 0")
        wrist_ = 0
    return wrist_

# Define what the direction is for the gripper
def grip(clock_counterclock):
    if clock_counterclock == 0:
        grip_ = off
    elif clock_counterclock == 1:
        grip_ = grip_open
    elif clock_counterclock == 2:
        grip_ = grip_close
    else:
        print("error rotate can not be lower than 0 or higher then 2 now off")
        grip_ = 0
    return grip_

# Define what the direction is for the light
def light(on_off):
    if on_off == 0:
        light_ = off
    elif on_off == 1:
        light_ = light_on
    elif on_off == 2:
        light_ = off
    else:
        print("error light can not be lower than 0 or higher then 1 now set to 0")
        light_ = off
    return light_
# Calculate the error
def get_error(setpoints_, angles_):
    error_ =[x1 - x2 for (x1, x2) in zip(setpoints_, angles_)]
    return error_

# Translate the error to direction
def get_direction(error):
    direction_ = [0] * len(error)
    for x in range(0, len(error)):
        #print "We're on time %d and error is %.2f" % (x,error[x])
        if error[x] == 0:
            direction_[x] = 0
        elif error[x] > 0:
            direction_[x] = 1
        elif error[x] < 0:
            direction_[x] = 2
    return direction_

# translate direction to motor control values
def get_motor_control_values(_direction):
    rotate1 = rotate(_direction[0])
    shoulder1 = shoulder(_direction[1])
    elbow1 = elbow(_direction[2])
    wrist1 = wrist(_direction[3])
    return rotate1, shoulder1, elbow1, wrist1

def get_usb_direction(setpoints, angles):
    setpoints_old = setpoints
    setpoints = safe_setpoints(setpoints)
    if setpoints_old != setpoints:
        print("new setpoints"), setpoints
    error = get_error(setpoints, angles)
    print("error    (1 2 3 4)", error)
    direction = get_direction(error)
    print("direction is ", direction)
    usb_direction =  get_motor_control_values(direction)
    #print("rotate, shoulder, elbow, wrist",usb_direction[0], usb_direction[1], usb_direction[2], usb_direction[3])
    return usb_direction

# Translate motor directions to one command for the arm
def get_total_movement(_rotate, _shoulder, _elbow, _wrist):
    total_movement_temp1 = [x1 + x2 for (x1, x2) in zip(_rotate, _shoulder)]
    total_movement_temp2 = [x1 + x2 for (x1, x2) in zip(total_movement_temp1, _elbow)]
    total_movement = [x1 + x2 for (x1, x2) in zip(total_movement_temp2, _wrist)]

    #print("total movement is",total_movement)
    return total_movement


# Define a procedure to transfer command via USB to the arm
def ctrl(command):
    if usb_arm == None:
        raise Exception("Robotic arm not connected")
    # Start the movement
    # usb_arm.ctrl_transfer(bmRequestType ,bmRequest ,wValue ,wIndex ,data ,timeout )
    # bmRequestType = The transfer direction = 0x40(write)/0xC(read)
    # bmRequest = bmRequestType/CTRL_LOOPBACK_READ
    # wValue
    # wIndex
    # data = len(msg)(read)/msg(write)
    # timeout
    usb_arm.ctrl_transfer(0x40,6,0x100,0,command,1000)
    return True

# Stop motors
def stop_motors():
    if usb_arm == None:
        raise Exception("Robotic arm not connected")
    # Stop the movement after waiting a specified duration
    usb_arm.ctrl_transfer(0x40, 6, 0x100, 0, [0, 0, 0], 1000)
    return True

def open_close_gripper(_grip):
    ctrl(grip(_grip))
    sleep(1)
    stop_motors()

    if _grip == 1:
        return True
    elif _grip == 0 or _grip == 2:
        return False

def connect_usb_arm():
    print("Connecting to USBarm")
    statusconnection = connect()
    print("Status Connection =", statusconnection)

if __name__ == "__main__":
    raise Exception("Cannot run standalone - use 'import usbarm' to utlise this module")
    exit()

