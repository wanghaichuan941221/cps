import math
from threading import Thread, Condition, Timer, RLock

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
        self.new_data = Condition(RLock())
        self.top_view_data = []
        self.left_view_data = []
        self.right_view_data = []
        self.running = True

    def run(self):
        while self.running:
            self.control()

    def control(self):
        self.new_data.acquire()
        while True:
            if len(self.top_view_data) > 0:
                theta1, setpoint1 = pixaltoangle.get_theta1_setpoint1(self.top_view_data)
                use_left, inverse = pixaltoangle.get_coords_side_or_right(theta1)
                if use_left and len(self.left_view_data) > 0:
                    pixel_coords_top = self.top_view_data.copy()
                    pixel_coords_side = self.left_view_data.copy()
                    self.top_view_data = []
                    self.left_view_data = []
                    break
                elif not use_left and len(self.right_view_data) > 0:
                    pixel_coords_top = self.top_view_data.copy()
                    pixel_coords_side = self.right_view_data.copy()
                    self.top_view_data = []
                    self.right_view_data = []
                    break

            self.new_data.wait()

        self.new_data.release()

        theta1, setpoint1 = pixaltoangle.get_theta1_setpoint1(pixel_coords_top)
        theta2, theta3, theta4 = pixaltoangle.get_theta234(pixel_coords_side)
        if inverse:
            theta2, theta3, theta4 = pixaltoangle.invserse_angles(theta2, theta3, theta4)

        tx, ty = pixaltoangle.get_x_y_object(pixel_coords_top, calibration_distance_in_cm, height_object_in_cm)
        print("CONTROLLER theta1 and setpoint1 = ", theta1, setpoint1)
        print("CONTROLLER theta2, theta3, theta4 = ", theta2, theta3, theta4)
        print("CONTROLLER tx ty = ", tx, ty)


        state = statemachine.state0  # initial state

        measured_angels = [theta1, theta2, theta3, theta4]
        setpoints = [setpoint1, 0, 0, 0]
        while state: state = state(measured_angels, setpoints, tx, ty)  # launch state machine
        print("Done with states")

    def update_top_view_data(self, data):
        self.new_data.acquire()

        self.top_view_data = data

        self.new_data.notify()
        self.new_data.release()

    def update_left_view_data(self, data):
        self.new_data.acquire()

        self.left_view_data = data

        self.new_data.notify()
        self.new_data.release()

    def update_right_view_data(self, data):
        self.new_data.acquire()

        self.right_view_data = data

        self.new_data.notify()
        self.new_data.release()

    def connect_usb_arm(self):
        usbarm.connect_usb_arm()

    def stop_motors(self):
        usbarm.stop_motors()

    def kill_switch(self):
        self.stop_motors()
        print('HIT KILL SWITCH')

