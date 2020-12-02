
import cv2
import numpy as np
import math
import serial
import time
import codecs
import os
import Telcontrol
import io

import zwoasi as asi

telescope=Telcontrol.Telcontrol()
time.sleep(2)
print("connected")
#telescope.setAzimut(7)
#telescope.setAltitude(10)
#telescope.imidiateStop()
#time.sleep(10)


command= chr(80)+ chr(2)+ chr(16)+ chr(36)+ chr(3)+ chr(142)+ chr(56)+ chr(0)   #go left slow speed

command1=chr(80)+ chr(2)+ chr(16)+ chr(36)+ chr(6)+ chr(142)+ chr(56)+ chr(0)  #going right at speed of 4
command2=chr(80)+ chr(2)+ chr(16)+ chr(36)+ chr(0)+ chr(0)+ chr(0)+ chr(0)  #Stop

command3=chr(80)+ chr(2)+ chr(16)+ chr(37)+ chr(7)+ chr(142)+ chr(56)+ chr(0)  #left (reset)
command4=chr(80)+ chr(2)+ chr(17)+ chr(36)+ chr(6) + chr(142)+ chr(56)+ chr(0) #up
command5=chr(80)+ chr(2)+ chr(17)+ chr(37)+ chr(6)+ chr(142)+ chr(56)+ chr(0) #down

command6=chr(80)+ chr(2)+ chr(17)+ chr(37)+ chr(0)+ chr(0)+ chr(0)+ chr(0) #stop


#telescope.ser.write(command6.encode())
#time.sleep(5)

#line=telescope.ser.read(18)
#print(line)


#telescope.ser.write(command2.encode())
#time.sleep(3)
#sio = io.TextIOWrapper(io.BufferedRWPair(telescope.ser, telescope.ser))
#sio.write(command3)
#time.sleep(10)
#sio.flush() # it is buffering. required to get the data out *now*
#line = sio.readline()
#telescope.ser.write(command8.encode())
#print("Reset to 0 ")
#time.sleep(5)
#telescope.ser.write(command6.encode())
#time.sleep(5)
#line=telescope.ser.read(18)
#print(line)
#telescope.ser.flush()
#line = telescope.ser.readline()

#telescope.ser.write(command.encode())
#print("Hello begin to go right at very slow speed ")
#telescope.ser.write(command.encode())
#time.sleep(10)

print("now go right at normal speed ")
telescope.ser.write(command1.encode())
time.sleep(10)

print("STOP")
telescope.ser.write(command2.encode())
time.sleep(3)

print("going left fast speed ")
telescope.ser.write(command3.encode())
time.sleep(5)

print("STOP")
telescope.ser.write(command2.encode())
time.sleep(3)

print("going up slow speed")
telescope.ser.write(command4.encode())
time.sleep(10)

print("going down normal speed")
telescope.ser.write(command5.encode())
time.sleep(2)

print("STOP")
telescope.ser.write(command6.encode())

print("done")




#telescope.setAzimut(5)
#telescope.stopTelescope()

