from time import sleep
import operator
import usbarm
import math
import statemachine
import pixaltoangle

setpoints_ = [0*math.pi, 0*math.pi, 0*math.pi, 0*math.pi]
angles_ = [0*math.pi, 0*math.pi, 0*math.pi, 0*math.pi]
#pixalcordinates = [0,300,450,450,600,300,450,450]
#pixalcordinates = [150,150,450,300,450,450,300,600]

pixalcordinates = [0,300,450,300,600,300,300,600]
#pixalcordinates = [150,450,300,0,450,150,300,600]

endeffector_to_box_ = 2
endeffector_to_droppoint_ = 2


def control(time, setpoints, angles, endeffector_to_box, endeffector_to_droppoint):
    print("start control")

    theta1= pixaltoangle.get_theta1_setpoint1(pixalcordinates)
    print("theta1 and setpoint1", theta1)
    state = statemachine.state0  # initial state
    #while state: state = state(angles, setpoints, endeffector_to_box, endeffector_to_droppoint)  # launch state machine
    print("Done with states")

    sleep(time)
    stopmotors = usbarm.stop_motors()

while True:

    print("Enter the duration:",)
    duration = float(input())  # Fetch the input from the terminal#
    print("duration =", duration)

    control(duration, setpoints_, angles_, endeffector_to_box_, endeffector_to_droppoint_)



