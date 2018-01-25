import math
from threading import Thread, Condition

import control.statemachine as statemachine
import control.pixaltoangle as pixaltoangle
from control import usbarm

setpoints_ = [0*math.pi, 0*math.pi, 0*math.pi, 0*math.pi]
angles_ = [0*math.pi, 0*math.pi, 0*math.pi, 0*math.pi]
#  pixalcordinates = [0,300,450,450,600,300,450,450]
#  pixalcordinates = [150,150,450,300,450,450,300,600]

pixalcordinates = [0,300,450,450,600,300,450,150]
#  pixalcordinates = [150,450,300,0,450,150,300,600]

endeffector_to_object_ = 2
endeffector_to_droppoint_ = 2

calibration_distance_in_cm = 40
height_object_in_cm = 5


class Controller(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.new_data = Condition()
        self.top_view_data = []
        self.side_view_data = []
        self.running = True

    def run(self):
        while self.running:
            self.new_data.acquire()
            self.new_data.wait()
            tv_data = self.top_view_data.copy()
            sv_data = self.side_view_data.copy()
            self.new_data.release()

            self.control(tv_data, sv_data)

    def update_data(self, top_vew_data, side_view_data):
        self.new_data.acquire()

        self.top_view_data = top_vew_data
        self.side_view_data = side_view_data

        self.new_data.notify()
        self.new_data.release()

    def control(self, pixel_coords_top, pixel_coords_side):
        print("CONTROLLER start control with ", str(pixel_coords_top))

        theta1, setpoint1 = pixaltoangle.get_theta1_setpoint1(pixel_coords_top)
        # theta2, theta3, theta4 = pixaltoangle.get_theta234(pixel_coords_side)
        # endeffector_to_object = pixaltoangle.get_distance_to_object(pixel_coords_top, pixel_coords_side, calibration_distance_in_cm,
        #                                    height_object_in_cm)
        print("CONTROLLER theta1 and setpoint1", theta1, setpoint1)
        state = statemachine.state0  # initial state

        only_first_angle = [theta1, 0, 0, 0]
        only_first_setpoint = [setpoint1, 0, 0, 0]
        while state: state = state(only_first_angle, only_first_setpoint, endeffector_to_object_,
                                   endeffector_to_droppoint_)  # launch state machine
        print("Done with states")
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



