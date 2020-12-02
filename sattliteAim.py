import cv2
import numpy as np
import math
import serial
import time
import codecs
import os
import Telcontrol

import zwoasi as asi

#ser = serial.Serial('COM3',9600)# need to check the com
#fourcc = cv2.VideoWriter_fourcc(*'XVID')
fourcc = cv2.VideoWriter_fourcc(*'MJPG')

time.sleep(2)
print("connected")

frameCounter=0

cap = cv2.VideoCapture(0)
w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5)
#detector = cv2.SimpleBlobDetector_create()



#print(str(asi.list_cameras()))
#out = cv2.VideoWriter('output1.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10, (200, 200))
out = cv2.VideoWriter('outSatt.avi', fourcc, 20.0, (w, h))
ok, image=cap.read()
if not ok:
    print('Failed to read video')
    exit()
bbox = cv2.selectROI("tracking", image)
tracker = cv2.TrackerMIL_create()
#tracker = cv2.TrackerKCF_create()
#tracker = cv2.TrackerBoosting_create()
init_once = False
width = len(image[0])
length = len(image)
cx = width / 2
cy = length / 2
dx=0
dy=0

def dist(new, old):
    res = new - old
    return res

while cap.isOpened():
    ok, image=cap.read()
    if not ok:
        print('Failed to read video')
        exit()

    if not ok:
        print('no image to read')
        break

    if not init_once:
        ok = tracker.init(image, bbox)
        init_once = True

    ok, newbox = tracker.update(image)
    print(ok, newbox)

    if ok:
        p1 = (int(newbox[0]), int(newbox[1]))
        p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
        sat_center_x= (p1[0] + p2[0]) / 2
        sat_center_y = (p1[1] + p2[1]) / 2
        #cv2.rectangle(image, p1, p2, (200, 0, 0))
        cv2.circle(image, (int(sat_center_x), int(sat_center_y)), 60, (250, 0, 0), 5)

        #if (sat_center_x > 100 and sat_center_x < width - 100 and sat_center_y > 100 and sat_center_y < length - 100):
        bx = sat_center_x
        by = sat_center_y
        dx=bx-cx
        dy=by-cy
        #dx = dist(bx, cx)
        #dy = dist(by, cy)  ;;                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          ,
        #distance from center
#        d = math.sqrt(dx ** 2 + dy ** 2)q
        # if d < 50:
        #     bx = int(bx * 0.9 + centerx * 0.1)
        #     by = int(by * 0.9 + centery * 0.1)



        #cv2.line(image, (int(cx),int(cy)),(int(bx),int(by)) ,(0, 200, 0),3 )

    cv2.imshow("tracking", image)
    out.write(image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()
out.release()
cap.release()

















