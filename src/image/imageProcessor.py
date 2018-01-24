from threading import Thread

import cv2
import numpy as np
import time
from picamera.array import PiRGBArray
from picamera import PiCamera
# from collection import deque

# green
from logger import Logger
from networking.networkHandlerUDP import NetworkHandlerUDP

# cam 2
green_lower = np.array([47, 104, 78])
green_upper = np.array([152, 255, 255])
red_lower = np.array([126, 64, 144])
red_upper = np.array([179, 191, 250])
yellow_lower = np.array([29, 163, 95])
yellow_upper = np.array([40, 252, 240])


# cam 7
# green_lower = np.array([47, 104, 78])
# green_upper = np.array([152, 255, 255])
# red_lower = np.array([159, 77, 146])
# red_upper = np.array([178, 255, 255])
# yellow_lower = np.array([27, 157, 76])
# yellow_upper = np.array([38, 254, 159])

imgWidth = 640
imgHeight = 480


class ImageProcessor(Thread):

    def __init__(self, nwh: 'NetworkHandlerUDP', log: 'Logger', is_top_view: 'bool'):
        super().__init__()

        self.nwh = nwh
        self.log = log
        self.is_top_view = is_top_view

        self.running = True

        self.log.log('ImageProcessor', 'Opening camera...')
        self.camera = PiCamera()
        self.camera.rotation = 180
        self.camera.resolution = (imgWidth, imgHeight)
        self.camera.framerate = 32
        self.rawCapture = PiRGBArray(self.camera, size=(imgWidth, imgHeight))

        time.sleep(0.5)  # give the camera some time to setup
        self.log.log('ImageProcessor', 'Camera opened')

    def run(self):
        if self.is_top_view:
            imgNr = 0
            while self.running:
                time.sleep(1)
                imgNr += 1
                img = self.capture_hsv_image()
                mask_red = self.filter_hsv_image(img, red_lower, red_upper)
                mask_yellow = self.filter_hsv_image(img, yellow_lower, yellow_upper)
                circles = self.find_circles(mask_red)
                circles_object = self.find_circles(mask_yellow)
                for cir in circles:
                    cv2.circle(img, cir, 10, (255,0,0), 3)
                cv2.imwrite('/home/pi/Desktop/Images/img' + str(imgNr) + '.png', img)
                cv2.imwrite('/home/pi/Desktop/Images/mask_red' + str(imgNr) + '.png', mask_red)
                cv2.imwrite('/home/pi/Desktop/Images/mask_yellow' + str(imgNr) + '.png', mask_yellow)
                if len(circles) == 3:
                    circles.sort()
                    if len(circles_object) > 0:
                        points = circles + [circles_object[0]]
                    else:
                        points = circles + [(imgWidth, img)]
                    self.nwh.multisend(self.nwh.protocol.wrap_top_view(self.unzip_list(points)))
                else:
                    self.log.log('ImageProcessor', '3 data points are required, found: ' + str(circles))
        else:
            while self.running:
                img = self.capture_hsv_image()
                mask_green = self.filter_hsv_image(img, green_lower, green_upper)
                circles = self.find_circles(mask_green)
                if len(circles) == 5:
                    self.nwh.multisend(self.nwh.protocol.wrap_side_view(self.unzip_list(circles)))
                else:
                    self.log.log('ImageProcessor', '5 data points are required, found: ' + str(circles))

    def capture_hsv_image(self):
        self.rawCapture.truncate(0)
        self.camera.capture(self.rawCapture, format="bgr", use_video_port=True)
        frame = self.rawCapture.array
        # blurred = cv2.GaussianBlur(frame, (11, 11), 0) TODO maybe do blur
        return cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    def filter_hsv_image(self, img, lower_bounds, upper_bounds):
        return cv2.inRange(img, lower_bounds, upper_bounds) # TODO maybe do open / close

    def find_circles(self, mask):
        res = []
        contours = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        for contour in contours:
            (x, y), r = cv2.minEnclosingCircle(contour)
            if r > 5:
                res.append((int(x), int(y)))
        return res

    def close_camera(self):
        self.camera.close()

    def unzip_list(self, list):
        res = []
        for (x, y) in list:
            res.append(x)
            res.append(y)
        return res


