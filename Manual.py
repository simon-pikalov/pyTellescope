import Telcontrol
import sys
#telescope=Telcontrol.Telcontrol()
import cv2
cap = cv2.VideoCapture(1)
telescope=Telcontrol.Telcontrol()
#img = cv2.imread('sof.jpg') # load a dummy image
while(1):
    ret, frame = cap.read()
    cv2.imshow('frame', frame)
    #cv2.imshow('img',img)
    k = cv2.waitKey(1)
    if k==27:    # Esc key to stop
        print('esc')
        telescope.stopTelescope()
        break
    if k == ord('w'):  # Esc key to stop
        telescope.manualUp()
        print('up')
    if k == ord('s'):  # Esc key to stop
        print('down')
        telescope.manualDown()
    if k == ord('a'):  # Esc key to stop
        print('right')
        telescope.manualLeft()
    if k == ord('d'):  # Esc key to stop
        print('left')
        telescope.manualRight()
    if k == ord('p'):  # Esc key to stop
        print('p')
        telescope.manualUp()
    elif k==-1:  # normally -1 returned,so don't print it
        continue
    else:
        print( k) # else print its value
cap.release()
cv2.destroyAllWindows()
