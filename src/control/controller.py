from time import sleep
import operator
import usbarm
import math
import statemachine
import forwardkinematics

setpoints_ = [0*math.pi, 0*math.pi, 0*math.pi, 0*math.pi]
angles_ = [0*math.pi, 0*math.pi, 0*math.pi, 0*math.pi]
endeffector_to_box_ = 2
endeffector_to_droppoint_ = 2


def control(time, setpoints, angles, endeffector_to_box, endeffector_to_droppoint, top_points):
    print("start control")



    state = statemachine.state0  # initial state
    while state: state = state(angles, setpoints, endeffector_to_box, endeffector_to_droppoint)  # launch state machine
    print("Done with states")

    sleep(time)
    stopmotors = usbarm.stop_motors()

while True:

    print("Enter the duration:",)
    duration = float(input())  # Fetch the input from the terminal#
    print("duration =", duration)

    control(duration, setpoints_, angles_, endeffector_to_box_, endeffector_to_droppoint_, top_points_)



