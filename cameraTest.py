import Telcontrol
import sys
import urllib
#telescope=Telcontrol.Telcontrol()
import cv2
#cam = "mms://194.90.203.111/cam2"
#cam = 'http://192.168.8.215:8080/video'
cam = 0 # Use  local webcam.

cap = cv2.VideoCapture(cam)
#cap = cv2.VideoCapture(0)
#cap2 = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'DIVX')

w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5)
cap.set(3, w)
cap.set(4, h)
out = cv2.VideoWriter('outputy9.avi', fourcc, 10, (w, h))
w1=int(w/2)-260
h1=int(h/2)-260


while(1):
    ret, frame = cap.read()
    height, width = frame.shape[:2]
    cy = int(height / 2)
    cx = int(width / 2)
    hx = 600
    hy = 300
    image = frame[cy - hy:cy + hy, cx - hx:cx + hx]
    n_height, n_width = image.shape[:2]
    n_cy = int(n_height / 2)
    n_cx = int(n_width / 2)
    #frame=frame[130:h-130 , 130:w-130]
#    ret2, frame2 = cap2.read()
    cv2.rectangle(frame, (n_cx- 20, n_cy - 20), (n_cx+ 20, n_cy + 20), (0, 250, 0), 5)
    out.write(frame )
    cv2.imshow('frame', frame)
#    cv2.imshow('frame2', frame2)
    #cv2.imshow('img',img)
    k = cv2.waitKey(1)
    if k==27:    # Esc key to stop
        print('esc')
        break
out.release()
cap.release()
#cap2.release()
cv2.destroyAllWindows()