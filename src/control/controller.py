from time import sleep
import operator
import usbarm
import math
import statemachine

setpoints_ = [0*math.pi, 0*math.pi, 0*math.pi, 0*math.pi]
angles_ = [0*math.pi, 0*math.pi, 0*math.pi, 0*math.pi]
endeffector_to_box_ = 2
endeffector_to_droppoint_ = 2


def control(time, setpoints, angles, endeffector_to_box, endeffector_to_droppoint):
    print("start control")





    # usbarm.set_motors(rotate, shoulder, elbow, wrist, grip, light)
    # 0 = off, 1 = clockwise, 2 = counterclockwise for motors
    # 0 = off, 1 = on, 2 = off
    #print "total movement", total_movement



    state = statemachine.state0  # initial state
    while state: state = state(angles, setpoints, endeffector_to_box, endeffector_to_droppoint)  # launch state machine
    print("Done with states")

    sleep(time)
    stopmotors = usbarm.stop_motors()

while True:

    print("Enter the duration:",)
    duration = float(input())  # Fetch the input from the terminal#
    print("duration =", duration)

    control(duration, setpoints_, angles_, endeffector_to_box_, endeffector_to_droppoint_)



