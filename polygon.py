import cv2
import numpy as np
import matplotlib.pyplot as plt
import imutils
# from collection import deque

# green_lower = np.array([50,140,128])
# green_upper = np.array([110,230,250])

#red color
green_lower = np.array([122,144,21])
green_upper = np.array([200,230,120])


counter = 0
(dx,dy) =(0,0)
direction =""

camera = cv2.VideoCapture(1)
while(1):
    (grabbed,frame) = camera.read()
    frame = imutils.resize(frame,width=600)
    blurred = cv2.GaussianBlur(frame,(11,11),0)
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv,green_lower,green_upper)
    mask = cv2.erode(mask,None,iterations=2)
    mask = cv2.dilate(mask,None,iterations=2)
    cnt = cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None
    if len(cnt)>0:
        c = max(cnt,key=cv2.contourArea)
        ((x,y),r) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"]/M["m00"]),int(M["m01"]/M["m00"]))
        if r>20:
            cv2.circle(frame,(int(x),int(y)),int(r),(0,255,255),2)
            # cv2.circle(frame,c,5,(0,0,255),-1)
            # pts.appendleft(c)
            print (x,y,r)
    cv2.imshow("mask",mask)
    if cv2.waitKey(1) & 0xFF == ord('q'):
            break
camera.release()
cv2.destroyAllWindows()
