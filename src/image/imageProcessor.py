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

# top view
red_top_lower = np.array([154, 98, 185])
red_top_upper = np.array([179, 228, 255])
# yellow_top_lower = np.array([24, 137, 98])
# yellow_top_upper = np.array([40, 199, 207])
orange_top_lower = np.array([10, 163, 129])
orange_top_upper = np.array([19, 219, 195])

# side view
red_side_lower = np.array([149, 134, 100])
red_side_upper = np.array([169, 217, 176])
green_side_lower = np.array([38, 199, 41])
green_side_upper = np.array([70, 255, 150])
blue_side_lower = np.array([109, 111, 32])
blue_side_upper = np.array([126, 253, 98])
# Niet lokaal
# blue_side_lower = np.array([102, 158, 39])
# blue_side_upper = np.array([116, 237, 125])
yellow_side_lower = np.array([21, 221, 110])
yellow_side_upper = np.array([33, 255, 180])
# old yellow
# yellow_side_lower = np.array([28, 167, 98])
# yellow_side_upper = np.array([38, 255, 195])


imgWidth = 640
imgHeight = 480

kernel = np.ones((5, 5), np.uint8)


class ImageProcessor(Thread):

    def __init__(self, nwh: 'NetworkHandlerUDP', log: 'Logger', is_top_view: 'bool'):
        super().__init__()

        self.nwh = nwh
        self.log = log
        self.is_top_view = is_top_view

        self.running = True
        self.write_img = False

        self.log.log('ImageProcessor', 'Opening camera...')
        self.camera = PiCamera()
        self.camera.rotation = 180
        self.camera.resolution = (imgWidth, imgHeight)
        self.camera.framerate = 32
        self.rawCapture = PiRGBArray(self.camera, size=(imgWidth, imgHeight))

        time.sleep(0.5)  # give the camera some time to setup
        self.log.log('ImageProcessor', 'Camera opened')

    def run(self):
        imgNr = 0
        if self.is_top_view:
            while self.running:
                img = self.capture_image()
                hsv = self.convert_to_hsv(img)
                mask_red = self.filter_hsv_image(hsv, red_top_lower, red_top_upper)
                mask_yellow_obj = self.filter_hsv_image(hsv, orange_top_lower, orange_top_upper)
                circles = self.find_circles(mask_red)
                circles_object = self.find_one_circle(mask_yellow_obj)

                if self.write_img:
                    imgNr += 1
                    if imgNr == 10:
                        self.write_img = False
                        self.log.print('Done writing images')
                    for cir in circles:
                        cv2.circle(img, cir, 10, (255, 0, 0), 3)
                    if circles_object is not None:
                        cv2.circle(img, (circles_object[0], circles_object[1]), 10, (0, 255, 0), 3)
                    cv2.imwrite('/home/pi/Desktop/Images/img' + str(imgNr) + '.png', img)
                    cv2.imwrite('/home/pi/Desktop/Images/mask_red' + str(imgNr) + '.png', mask_red)
                    cv2.imwrite('/home/pi/Desktop/Images/mask_yellow_obj' + str(imgNr) + '.png', mask_yellow_obj)

                if len(circles) == 3:
                    circles.sort()
                    if circles_object is not None:
                        points = self.unzip_list(circles) + circles_object
                    else:
                        points = self.unzip_list(circles) + [imgWidth, imgHeight]
                    # try:
                    self.nwh.multisend(self.nwh.protocol.wrap_top_view(points))
                    # except ValueError:
                    #     print("WEIRD ERROR ================================================")
                    #     print("WEIRD ERROR ================================================")
                    #     print("WEIRD ERROR circles =", circles)
                    #     print("WEIRD ERROR points =", points)
                    #     print("WEIRD ERROR circles_object =", circles_object)
                    #     print("WEIRD ERROR ================================================")
                    #     print("WEIRD ERROR ================================================")
                else:
                    self.log.log('ImageProcessor', '3 data points are required, found: ' + str(circles))
        else:
            while self.running:
                start_time = time.time()
                img = self.capture_image()
                end_time = time.time()
                print("CAP IMG TOOK", end_time - start_time, "s")
                start_time = time.time()
                hsv = self.convert_to_hsv(img)
                mask_red = self.filter_hsv_image(hsv, red_side_lower, red_side_upper)
                mask_yellow = self.filter_hsv_image(hsv, yellow_side_lower, yellow_side_upper)
                mask_green = self.filter_hsv_image(hsv, green_side_lower, green_side_upper)
                mask_blue = self.filter_hsv_image(hsv, blue_side_lower, blue_side_upper)
                cal_points = self.find_circles(mask_red)
                cal_points.sort()

                if len(cal_points) > 2:
                    cal_points = [cal_points[0], cal_points[len(cal_points) - 1]]

                p2 = self.find_one_circle(mask_yellow)
                p3 = self.find_one_circle(mask_green)
                p4 = self.find_one_circle(mask_blue)
                arm_points = [p2, p3, p4]

                if self.write_img:
                    imgNr += 1
                    if imgNr == 10:
                        self.write_img = False
                        self.log.print('Done writing images')
                    for point in cal_points:
                        cv2.circle(img, point, 10, (0, 0, 255), 3)
                    for point in arm_points:
                        if point is not None:
                            cv2.circle(img, (point[0], point[1]), 10, (255, 0, 0), 3)
                    cv2.imwrite('/home/pi/Desktop/Images/img' + str(imgNr) + '.png', img)
                    cv2.imwrite('/home/pi/Desktop/Images/mask_red' + str(imgNr) + '.png', mask_red)
                    cv2.imwrite('/home/pi/Desktop/Images/mask_yellow' + str(imgNr) + '.png', mask_yellow)
                    cv2.imwrite('/home/pi/Desktop/Images/mask_green' + str(imgNr) + '.png', mask_green)
                    cv2.imwrite('/home/pi/Desktop/Images/mask_blue' + str(imgNr) + '.png', mask_blue)

                if len(cal_points) == 2 and None not in arm_points:
                    points = [cal_points[0][0], cal_points[0][1]]
                    for point in arm_points:
                        points = points + point
                    points = points + [cal_points[1][0], cal_points[1][1]]
                    end_time = time.time()
                    print("PRO IMG TOOK: ", end_time - start_time, "s")
                    start_time = time.time()
                    self.nwh.multisend(self.nwh.protocol.wrap_side_view(points))
                    end_time = time.time()
                    print("SEN IMG TOOK: ", end_time - start_time, "s")
                else:
                    self.log.log('ImageProcessor', '5 data points are required, found: cal=' + str(cal_points) + ' and arm=' + str(arm_points))


    def capture_image(self):
        self.rawCapture.truncate(0)
        self.camera.capture(self.rawCapture, format="bgr", use_video_port=True)
        return self.rawCapture.array  # TODO maybe do blur

    def convert_to_hsv(self, frame):
        return cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    def filter_hsv_image(self, img, lower_bounds, upper_bounds):
        mask = cv2.inRange(img, lower_bounds, upper_bounds)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        return mask

    def find_one_circle(self, mask):
        contours = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        if len(contours) > 0:
            biggest_contour = max(contours, key=cv2.contourArea)
            (x, y), r = cv2.minEnclosingCircle(biggest_contour)
            return [int(x), int(y)]
        else:
            return None

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

    def write_images(self):
        if not self.write_img:
            self.write_img = True


