import math
from threading import Thread, Condition, Timer

import time

import control.statemachine as statemachine
import control.pixaltoangle as pixaltoangle
from control import usbarm
from control.inverseKinematics import inverse_kinematics

# setpoints_ = [0*math.pi, 0*math.pi, 0*math.pi, 0*math.pi]
# angles_ = [0*math.pi, 0*math.pi, 0*math.pi, 0*math.pi]
#  pixalcordinates = [0,300,450,450,600,300,450,450]
#  pixalcordinates = [150,150,450,300,450,450,300,600]

#  pixalcordinates = [0,300,450,450,600,300,450,150]
#  pixalcordinates = [150,450,300,0,450,150,300,600]

endeffector_to_object_ = 2
endeffector_to_droppoint_ = 2

calibration_distance_in_cm = 60
height_object_in_cm = 2


class Controller(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.new_data = Condition()
        self.top_view_data = []
        self.left_view_data = []
        self.right_view_data = []
        self.timer = Timer(0.2, self.kill_switch)
        self.running = True

    def run(self):
        while self.running:
            self.timer = Timer(0.5, self.kill_switch)
            self.timer.start()

            self.new_data.acquire()
            self.new_data.wait()
            tv_data = self.top_view_data.copy()
            lv_data = self.left_view_data.copy()
            rv_data = self.right_view_data.copy()
            self.new_data.release()

            self.timer.cancel()

            self.timer = Timer(0.2, self.kill_switch)
            self.timer.start()

            self.control(tv_data, lv_data, rv_data)

            self.timer.cancel()


    def update_data(self, top_vew_data, left_view_data, right_view_data):
        self.new_data.acquire()

        self.top_view_data = top_vew_data
        self.left_view_data = left_view_data
        self.right_view_data = right_view_data

        self.new_data.notify()
        self.new_data.release()

    def control(self, pixel_coords_top, pixel_coords_side, pixel_coords_right):
        print("CONTROLLER start control with ", str(pixel_coords_top))

        theta1, setpoint1 = pixaltoangle.get_theta1_setpoint1(pixel_coords_top)

        theta2, theta3, theta4 = pixaltoangle.get_coords_side_or_right(theta1, pixel_coords_side, pixel_coords_right)
        endeffector_to_object, tx, ty = pixaltoangle.get_distance_to_object(pixel_coords_top, pixel_coords_side, calibration_distance_in_cm,
                                           height_object_in_cm)
        print("CONTROLLER theta1 and setpoint1 = ", theta1, setpoint1)
        print("CONTROLLER theta2, theta3, theta4 = ", theta2, theta3, theta4)
        print("CONTROLLER tx ty = ", tx, ty)


        state = statemachine.state0  # initial state

        measured_angels = [theta1, theta2, theta3, theta4]
        setpoints = [setpoint1, 0, 0, 0]
        while state: state = state(measured_angels, setpoints, tx, ty)  # launch state machine
        print("Done with states")
        #
        # sleep(time)
        # stopmotors = usbarm.stop_motors()

    def connect_usb_arm(self):
        usbarm.connect_usb_arm()

    def stop_motors(self):
        usbarm.stop_motors()

    def kill_switch(self):
        self.stop_motors()
        print('HIT KILL SWITCH')

