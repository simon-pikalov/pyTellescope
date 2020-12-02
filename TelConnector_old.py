import serial
import time
import codecs
import os
#ser = serial.Serial('/dev/ttyUSB0')  # open serial port
       # check which port was really used

ser = serial.Serial('COM3', 9600)
print(ser.name)
s = ser.read(100)
goRightCommand= ":K1\r=\r:f1\r=103\r:f1\r=103\r:G130\r=\r:I1200000\r=\r:J1\r=\r"
goRightCommand_hex=goRightCommand.encode().hex()
goRightCommand_hex_b=bytes.fromhex(goRightCommand_hex)
goRightCommand_hex_b=bytes(goRightCommand_hex.encode())


#bRight=bytes(goRightCommand_hex)
print (len(goRightCommand))
stopRightCommand= ":K1\r=\r"
stopRightCommand_hex=stopRightCommand.encode().hex()
stopRightCommand_hex_b=bytes.fromhex(stopRightCommand_hex)
stopRightCommand_hex_b=bytes(stopRightCommand_hex.encode())

print(goRightCommand_hex_b)
print(stopRightCommand_hex_b)
print(len(goRightCommand_hex_b))
print(len(stopRightCommand_hex_b))
#bStop= bytes(goRightCommand_hex)
print()
#print(stopRightCommand_hex_b[0])
#start command:
byte= bytes(0x30)
print(byte)


ser.write(goRightCommand_hex_b)     # write a string


time.sleep(4)
#stop command:
ser.write(stopRightCommand_hex_b)

ser.close()