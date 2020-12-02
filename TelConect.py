import serial
import time
import codecs
import os

ser = serial.Serial('COM6',9600)# need to check the com
print(ser.name)
print(ser.is_open)
# x = ser.is_open
if not ser.is_open :
    ser.open()
print(ser.is_open)

goRight_9 = (b':K1\r=\r:f1\r=103\r:f1\r=103\r:G130\r=\r:I1200000\r=\r:J1\r=\r')
goLeft_9 = (b':K1\r=\r:f1\r=303\r:f1\r=303\r:G131\r=\r:I1200000\r=\r:J1\r=\r')
goUp =    (b':K2\r=\r:f2\r=103\r:f2\r=103\r:G230\r=\r:I2200000\r=\r:J2\r=\r')
goDown =  (b':K2\r=\r:f2\r=303\r:f2\r=303\r:G231\r=\r:I2200000\r=\r:J2\r=\r')

StopX =(b':K1\r=\r')

ser.write(goRight_9)
print("right")
time.sleep(1)
ser.write(StopX)
print("stop")
time.sleep(1)
ser.write(goLeft_9)
print("left")
time.sleep(4)
ser.write(StopX)
print("stop")

ser.close()
print(ser.is_open)

