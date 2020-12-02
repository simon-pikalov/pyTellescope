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
fourcc = cv2.VideoWriter_fourcc(*'XVID')
#fourcc = cv2.VideoWriter_fourcc(*'MJPG')
#set serial parameters
# x = ser.is_open

#set frame parameters

size_factor = 1
cut_factor = 0.8
#image_size = (size_factor * 320, size_factor * 240)
oldx = 0
oldy = 0
frameEdgex=150
frameEdgey=150
# cap = cv2.VideoCapture('greyRSmall.mp4')
#cap = cv2.VideoCapture('whiteBallon1.mp4')
cap = cv2.VideoCapture(0)
w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5)
#detector = cv2.SimpleBlobDetector_create()

bx = -1
by = -1


def dist(new, old):
    res = new - old
    return res

telescope=Telcontrol.Telcontrol()
#print(str(asi.list_cameras()))
#out = cv2.VideoWriter('output1.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10, (200, 200))
out = cv2.VideoWriter('output1.avi', fourcc, 20.0, (w, h))

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    width = len(frame[0])
    length = len(frame)
    #print(width, length)
    #image_size = (int(cut_factor * width),int( cut_factor * length))
    image_size = (int(width), int( length))
    print(image_size)
    #frame = cv2.resize(frame, image_size)
    cutPixX=int(cut_factor*image_size[0])
    cutPixY=int(cut_factor*image_size[1])
    #frame=frame[width-image_size[0]:image_size[0],length-image_size[1]:image_size[1]]
    frame = cv2.resize(frame, image_size)
    #frame = frame[int(image_size[0] * cut_factor):int(image_size[0] * (1 - cut_factor)),   int(image_size[1] * cut_factor):int(image_size[1] * (1 - cut_factor))]
    # Our operations on the frame come here

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #gray_con = gray.copy()
    gray=gray[10:length-50,100:width-50 ]
    corners = cv2.goodFeaturesToTrack(gray, 1, 0.7, 1)
    try:
        corners = np.int0(corners)
    except TypeError:
        continue

    for i in corners:
        x, y = i.ravel()
        if bx == -1:
            bx = x
            by = y
        else:
            dx = dist(bx, oldx)
            dy = dist(by, oldy)
            d = math.sqrt(dx ** 2 + dy ** 2)
            if d < 20:
                bx = int(bx * 0.9 + x * 0.1)
                by = int(by * 0.9 + y * 0.1)
        oldx = bx
        oldy = by

    # Display the resulting frame
    cx=int(image_size[0]/2)
    cy=int(image_size[1]/2)
    print(cx,cy)
    # cv2.circle(frame, (bx, by), 3, (255, 0, 0), -1)
    # cv2.circle(frame, (cx, cy), 3, (255, 255, 0), -1)
    # cv2.putText(frame, "move x :" + str(dist(x, oldx)), (30, 30), 2, cv2.FONT_HERSHEY_PLAIN, (255, 0, 255), 1)
    # cv2.putText(frame, "move y :" + str(dist(y, oldy)), (30, 50), 2, cv2.FONT_HERSHEY_PLAIN, (255, 0, 255), 1)
    # cv2.imshow('frame', frame)
    cv2.circle(gray, (bx, by), 3, (255, 0, 0), -1)
    diffx=(dist(x, oldx))
    diffy=(dist(y, oldy))
    #telescope.setCorrection(diffx/70,diffy/70)
    print("diff", diffx/70, "diffy" ,diffy/70)
    cv2.putText(gray, "move x :" + str(dist(x, oldx)), (30, 30), 2, cv2.FONT_HERSHEY_PLAIN, (255, 0, 255), 1)
    cv2.putText(gray, "move y :" + str(dist(y, oldy)), (30, 50), 2, cv2.FONT_HERSHEY_PLAIN, (255, 0, 255), 1)
    cv2.imshow('frame', frame)
    cv2.imshow('gray', gray)
    out.write(gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        telescope.stopTelescope()
        telescope.disconnect()
        break
cv2.destroyAllWindows()
out.release()
cap.release()
#
















