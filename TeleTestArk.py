import cv2
import numpy as np
import math
import time
import codecs
import os
import Telcontrol

'''
in this class, I want to implement a filtering mechanism
from one side, i want to controll the telescope
from another side, I don't wont to send a command each frame,this may be have for the telescope controller.

so the idea is like so: save the last state of the telescope. f.ex. moving up, speed 5
if the new comand is the same, ignore it. if it's a new one, send it.


in the future, block the telescope, for not damaging itself (maybe this can be solved mechanicly)
'''



# get telescope controll
telescope = Telcontrol.Telcontrol()
time.sleep(2)
print("telescope connected")

# set frame parameters
angToPix_x = 57.14
angToPix_y = 42.85
telROIsize = 0.63 * angToPix_x

myAz = 0
myElv = 0

isContinue = True
while isContinue:
    k = input("Press Enter to continue...")
    print ("got from user: "+str(k))
    if (k == "q"): isContinue = False;

    if (k == "a"): telescope.manualLeft(7)
    if (k == "d"): telescope.manualRight(7)
    if (k == "f"): telescope.manualRightFast();
    if (k == "w"): telescope.manualUp(7)
    if (k == "s"): telescope.manualDown(7)
    if (k == "g"): telescope.getPosition()
    if (k == "z"): telescope.goToZero()



    if (k == "x"): telescope.stop()



    # if (frameCounter % 50 == 0):
    #     telescope.correct_x(rl=diffx, isStop=0)
    #
    # if frameCounter % 50 == 10:
    #     telescope.correct_y(ud=diffy, isStop=0)
    # if (frameCounter % 50 == 30):
    #     telescope.stop_x()
    # if (frameCounter % 50 == 40):
    #     telescope.stop_y()
    #     print("Stop")
    #
    # diffy = 0
    # diffx = 0
    # # time.sleep(0.2)
    # # cv2.imshow('frame', image)
    # # cv2.imshow('gray', image)
    #
    # cv2.imshow("tracking", image)
    # out.write(image)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     telescope.stopTelescope()
    #     telescope.disconnect()
    #     out.release()


telescope.stopTelescope()
telescope.disconnect()

time.sleep(2)
print("app done, exiting")
exit(0)


def setAz(az):
    global myAz
    if az < 0:
        myAz = az + 360
    if az > 360:
        myAz = az - 360
    else:
        myAz = az


def setElv(elv):
    global myElv
    if elv < 0:
        myElv = 0
    if elv > 360:
        myElv = elv - 360
    else:
        myElv = elv
