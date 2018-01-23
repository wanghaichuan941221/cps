import math
import control.statemachine as statemachine
import control.pixaltoangle as pixaltoangle
from control import usbarm

setpoints_ = [0*math.pi, 0*math.pi, 0*math.pi, 0*math.pi]
angles_ = [0*math.pi, 0*math.pi, 0*math.pi, 0*math.pi]
#  pixalcordinates = [0,300,450,450,600,300,450,450]
#  pixalcordinates = [150,150,450,300,450,450,300,600]

pixalcordinates = [0,300,450,450,600,300,450,150]
#  pixalcordinates = [150,450,300,0,450,150,300,600]

endeffector_to_object_ = 10
endeffector_to_droppoint_ = 10


class Controller:

    def control(self, pixel_coords_top):
        print("start control with ", str(pixel_coords_top))
        #
        # theta1, setpoint1 = pixaltoangle.get_theta1_setpoint1(pixel_coords_top)
        # print("theta1 and setpoint1", theta1, setpoint1)
        # state = statemachine.state0  # initial state
        #
        # only_first_angle = [theta1, 0, 0, 0]
        # only_first_setpoint = [setpoint1, 0, 0, 0]
        # while state: state = state(only_first_angle, only_first_setpoint, endeffector_to_object_, endeffector_to_droppoint_)  # launch state machine
        # print("Done with states")
        #
        # sleep(time)
        # stopmotors = usbarm.stop_motors()

    def connect_usb_arm(self):
        usbarm.connect_usb_arm()

    def stop_motors(self):
        usbarm.stop_motors()


# controller = Controller()
# while True:
#
#     print("Enter the duration:",)
#     duration = float(input())  # Fetch the input from the terminal#
#     print("duration =", duration)
#
#     controller.control(duration, setpoints_, angles_, endeffector_to_object_, endeffector_to_droppoint_)



