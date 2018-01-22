import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
import matplotlib.pyplot as plt
import imutils
import math as m
# from collection import deque

green_lower = np.array([50,140,128])
green_upper = np.array([110,230,250])

#red color
# green_lower = np.array([122,144,21])
# green_upper = np.array([200,230,120])
red_lower = np.array([140,60,230])
red_upper = np.array([240,130,255])

#blue
blue_lower = np.array([80,120,200])
blue_upper = np.array([160,200,255])

counter = 0
(dx,dy) =(0,0)
direction =""
(x1,y1,w1,h1)=(0,0,0,0)
(x2,y2,w2,h2)=(1,0,0,0)
(x3,y3,w3,h3)=(1,0,0,0)

imgWidth = 640
imgHeight = 480

camera = PiCamera()
camera.rotation = 180
camera.resolution = (imgWidth, imgHeight)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(imgWidth, imgHeight))

while(1):
    camera.capture(rawCapture, format="bgr", use_video_port=True)
    frame = rawCapture.array
    
    blurred = cv2.GaussianBlur(frame,(11,11),0)
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    #green image
    mask_green = cv2.inRange(hsv,green_lower,green_upper)
    mask_green = cv2.erode(mask_green,None,iterations=2)
    mask_green = cv2.dilate(mask_green,None,iterations=2)
    cnt_green = cv2.findContours(mask_green.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
    # center = None
    if len(cnt_green)>0:
        c = max(cnt_green,key=cv2.contourArea)
        (x1,y1,w1,h1)=cv2.boundingRect(c)
        # print "green"
        # print (x1,y1,w1,h1)
        # ((x,y),r) = cv2.minEnclosingCircle(c)
        # M = cv2.moments(c)
        # center = (int(M["m10"]/M["m00"]),int(M["m01"]/M["m00"]))
        # if r>10:
        #     cv2.circle(frame,(int(x),int(y)),int(r),(0,255,255),2)
            # cv2.circle(frame,c,5,(0,0,255),-1)
            # pts.appendleft(c)
            # print (x,y,r)

    mask_red = cv2.inRange(hsv,red_lower,red_upper)
    mask_red = cv2.erode(mask_red,None,iterations=2)
    mask_red = cv2.dilate(mask_red,None,iterations=2)
    cnt_red = cv2.findContours(mask_red.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
    if len(cnt_red)>0:
        c2 = max(cnt_red,key=cv2.contourArea)
        (x2,y2,w2,h2)=cv2.boundingRect(c2)
        # print "red"
        # print (x2,y2,w2,h2)


    mask_blue = cv2.inRange(hsv,blue_lower,blue_upper)
    mask_blue = cv2.erode(mask_blue,None,iterations=2)
    mask_blue = cv2.dilate(mask_blue,None,iterations=2)
    cnt_blue = cv2.findContours(mask_blue.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
    if len(cnt_blue)>0:
        c3 = max(cnt_blue,key=cv2.contourArea)
        (x3,y3,w3,h3)=cv2.boundingRect(c3)
        # print "blue"
        # print (x3,y3,w3,h3)

    # l1 = m.sqrt(m.pow((x2-x3),2)+m.pow((y2-y3),2))
    # l2 = m.sqrt(m.pow((x1-x3),2)+m.pow((y1-y3),2))
    # l3 = m.sqrt(m.pow((x1-x2),2)+m.pow((y1-y2),2))
    # a = m.acos((m.pow(l2,2)+m.pow(l3,2)-m.pow(l1,2))/(2*l2*l3))
    # print a
    # cv2.imshow("frame",frame)
    # cv2.imshow("mask_green",mask_green)
    # cv2.imshow("mask_red",mask_red)
    # cv2.imshow("mask_blue",mask_blue)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #         break
    rawCapture.truncate(0)
camera.close()
# cv2.destroyAllWindows()
