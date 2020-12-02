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
#set serial parameters
# x = ser.is_open
telescope=Telcontrol.Telcontrol()
time.sleep(2)
print("connected")
#set frame parameters
angToPix_x=57.14
angToPix_y=42.85
telROIsize=0.63*angToPix_x

frameCounter=0

# cap = cv2.VideoCapture('greyRSmall.mp4')
#cap = cv2.VideoCapture('whiteBallon1.mp4')
#cap = cv2.VideoCapture("satellite0.mp4")
#cap = cv2.VideoCapture(0)

#home
#cap = cv2.VideoCapture('http://10.0.0.17:8080/video') #home
#router
cap=cv2.VideoCapture('http://192.168.8.144:8080/video')

#KCG
#cap = cv2.VideoCapture('http://192.168.8.215:8080/video')

#cap = cv2.VideoCapture('http://192.168.100.115:8080/video')
w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5)
#detector = cv2.SimpleBlobDetector_create()

bx = -1
by = -1

myAz=0
myElv=0

def setAz(az):
    global myAz
    if az<0:
        myAz=az+360
    if az>360:
        myAz=az-360
    else:
        myAz=az

def setElv(elv):
    global myElv
    if elv < 0:
        myElv = 0
    if elv > 360:
        myElv = elv - 360
    else:
        myElv = elv

#print(str(asi.list_cameras()))
#out = cv2.VideoWriter('output1.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10, (200, 200))
out = cv2.VideoWriter('output1'+str(time.time())+'.avi', fourcc, 20.0, (w, h))
ok, image=cap.read()
#width = len(image[0])
#length = len(image)
height, width = image.shape[:2]
cy= int(height/2)
cx=int(width/2)
hx=600
hy=300
image = image[cy - hy:cy + hy, cx - hx:cx + hx]
n_height, n_width = image.shape[:2]
n_cy= int(n_height/2)
n_cx=int(n_width/2)

if not ok:
    print('Failed to read video')
    exit()
bbox = cv2.selectROI("tracking", image)
#tracker = cv2.TrackerMIL_create()
#tracker = cv2.TrackerBoosting_create()
tracker = cv2.TrackerCSRT_create()

init_once = False

#cx = int(width / 2)
#cy = int(length / 2)
dx=0
dy=0
telROIsize=(int)(telROIsize)
cv2.rectangle(image, (n_cy - telROIsize, n_cy - telROIsize), (n_cy + telROIsize, n_cy + telROIsize), (0, 0, 0), 5)
def dist(new, old):
    res = new - old
    return res

while cap.isOpened():
    ok, image=cap.read()
    image = image[cy - hy:cy + hy, cx - hx:cx + hx]
    #image = image[40:length - 130, 130:width - 130]
    if not ok:
        print('Failed to read video')
        exit()

    if not ok:
        print('no image to read')
        break

    if not init_once:
        ok = tracker.init(image, bbox)
        #image = image[cy - hy:cy + hy, cx - hx:cx + hx]
        init_once = True
    #image = image[40:length - 130, 130:width - 130]
    ok, newbox = tracker.update(image)
    #print(ok, newbox)

    if ok:
        p1 = (int(newbox[0]), int(newbox[1]))
        p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
        sat_center_x= int((p1[0] + p2[0]) / 2)
        sat_center_y = int((p1[1] + p2[1]) / 2)
        cv2.rectangle(image, p1, p2, (200, 0, 0))
        cv2.rectangle(image, (n_cx - 2, n_cy - 2), (n_cx + 2, n_cy + 2), (0, 0, 0),5)
        cv2.circle(image, (int(n_cx), int(n_cy)), 3, (0, 200, 0))

        #if (sat_center_x > 100 and sat_center_x < width - 100 and sat_center_y > 100 and sat_center_y < length - 100):
        bx = sat_center_x
        by = sat_center_y
        dx=bx-cx
        dy=cy-by
        #dx = dist(bx, cx)
        #dy = dist(by, cy)
        #distance from center
        d = math.sqrt(dx ** 2 + dy ** 2)
        # if d < 50:
        #     bx = int(bx * 0.9 + centerx * 0.1)
        #     by = int(by * 0.9 + centery * 0.1)



        cv2.line(image, (int(n_cx),int(n_cy)),(int(bx),int(by)) ,(0, 200, 0),3 )

    #print(width, length)
    #image_size = (int(cut_factor * width),int( cut_factor * length))
    # image_size = (int(width), int( length))
    # print(image_size)
    #
    # cutPixX=int(cut_factor*image_size[0])
    # cutPixY=int(cut_factor*image_size[1])
    #
    # frame = cv2.resize(frame, image_size)
    #
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #
    # corners = cv2.goodFeaturesToTrack(gray, 1, 0.7, 1)
    # try:
    #     corners = np.int0(corners)
    # except TypeError:
    #     continue




    # Display the resulting frame
#    print("with","length", width,length)
    # cv2.circle(frame, (bx, by), 3, (255, 0, 0), -1)
    # cv2.circle(frame, (cx, cy), 3, (255, 255, 0), -1)
    # cv2.putText(frame, "move x :" + str(dist(x, oldx)), (30, 30), 2, cv2.FONT_HERSHEY_PLAIN, (255, 0, 255), 1)
    # cv2.putText(frame, "move y :" + str(dist(y, oldy)), (30, 50), 2, cv2.FONT_HERSHEY_PLAIN, (255, 0, 255), 1)
    # cv2.imshow('frame', frame)
    #cv2.circle(image, (int(bx), int(by)), 3, (255, 0, 0), -1)
    #diffx=(dist(sat_center_x, oldx))
    #diffy=(dist(sat_center_y, oldy))

    #refactor by camera angle /pixel ratip
    diffx=(dx/angToPix_x)/10000
    diffy=(dy/angToPix_y)/10000
    #telescope.setCorrection(diffx, diffy)

    cv2.putText(image, "move x :" + str(diffx), (30, 30), 2, cv2.FONT_HERSHEY_PLAIN, (255, 0, 255), 1)
    cv2.putText(image, "move y :" + str(diffy), (30, 50), 2, cv2.FONT_HERSHEY_PLAIN, (255, 0, 255), 1)
    #0.6 is the telescope fov- so i set the bound to 0.5
    frameCounter=frameCounter+1
    #diff=0.05
    if(frameCounter%60==0 ):
        print("diffx", diffx, "diffy", diffy)
        if(diffy>0.5):
            telescope.setAltitude((myElv+diffy))
            #myElv=myElv+diffy
            setElv(myElv+diffy)
            print("move up ",myElv)
        if(diffy< -0.5):
            telescope.setAltitude((myElv - diffy))
            #myElv = myElv - diffy
            setElv(myElv - diffy)
            print("move down ", myElv)
        #time.sleep(1)
    if (frameCounter%61 ==0 ):
        if(diffx>0.5):
            telescope.setAzimut(myAz -diffx)
            #myAz =myAz - diffx/50
            setAz(myAz - diffx)
            print("move left ", myAz)
        if (diffx <0.5):
            telescope.setAzimut(myAz+ diffx)
            #myAz = myAz + diffx/50
            setAz(myAz + diffx )
            print("move right ", myAz)
        print(frameCounter, "frameCounter")
        #frameCounter=0

    diffy=0
    diffx=0
    # time.sleep(0.2)
    #cv2.imshow('frame', image)
    #cv2.imshow('gray', image)

    cv2.imshow("tracking", image)
    #out.write(image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        telescope.stopTelescope()
        telescope.disconnect()
        break
cv2.destroyAllWindows()
out.release()
cap.release()

















