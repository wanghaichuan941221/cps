from time import sleep
import operator
import usbarm
import math

setpoints_ = [-1*math.pi, -1*math.pi, 0*math.pi, 0*math.pi]
angles_ = [0*math.pi, 0*math.pi, 0*math.pi, 0*math.pi]
gripper = 0
light = 0


def control(time, setpoints, angles):
    print("start control")



    setpoints = usbarm.safe_setpoints(setpoints)
    print("new setpoints"), setpoints
    error = usbarm.get_error(setpoints, angles)
    print("error    (1 2 3 4)", error)
    direction = usbarm.get_direction(error)
    print("direction is ", direction)

    usbarm.open_close_gripper(1)
    usbarm.open_close_gripper(2)
    # usbarm.set_motors(rotate, shoulder, elbow, wrist, grip, light)
    # 0 = off, 1 = clockwise, 2 = counterclockwise for motors
    # 0 = off, 1 = on, 2 = off
    total_movement = usbarm.get_total_movement(direction[0],direction[1],direction[2],direction[3])
    #print "total movement", total_movement

    startmotors = usbarm.ctrl(total_movement)
    print("start motors ="), startmotors
    sleep(time)

    stopmotors = usbarm.stop_motors()
    print("Stopped motors =", stopmotors)





while True:

    print("Enter the duration:",)
    duration = float(input())  # Fetch the input from the terminal#
    print("duration =", duration)

    control(duration, setpoints_, angles_)



