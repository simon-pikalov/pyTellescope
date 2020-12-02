import serial
#from threading import *
import threading as tr
import time
import math



class Telcontrol(tr.Thread):

    def __init__(self,port="COM14", baudrate="9600", maxdx=200, maxdy=200,threshx=0,threshy=0):
        tr.Thread.__init__(self);
        self.ser = serial.Serial(port, baudrate)  # need to check the com
        # x = ser.is_open
        self.initProtocol()
        self.maxdx=maxdx
        self.maxdy=maxdy
        self.isReady=True
        self.threshx=threshx
        self.threshy=threshy
        self.whileLock = tr.Semaphore(value=0)
        self.readyLock = tr.Lock()
        #self.lock.acquire()
        self.dx = 0
        self.dy = 0
        self.start()

    def connect(self):
        if not self.ser.is_open:
            self.ser.open()

    def disconnect(self):
        if not self.ser.closed:
            self.ser.close()

    def initProtocol(self):
        # self.goRight_9 = (b':K1\r=\r:f1\r=103\r:f1\r=103\r:G130\r=\r:I1200000\r=\r:J1\r=\r')
        # self.goLeft_9 = (b':K1\r=\r:f1\r=303\r:f1\r=303\r:G131\r=\r:I1200000\r=\r:J1\r=\r')
        # self.goUp = (b':K2\r=\r:f2\r=103\r:f2\r=103\r:G230\r=\r:I2200000\r=\r:J2\r=\r')
        # self.goDown = (b':K2\r=\r:f2\r=303\r:f2\r=303\r:G231\r=\r:I2200000\r=\r:J2\r=\r')

        self.goRight_9 = (b':K1\r=\r:f1\r=103\r:f1\r=103\r:G130\r=\r:I1200000\r=\r:J1\r=\r')
        self.goLeft_9 = (b':K1\r=\r:f1\r=303\r:f1\r=303\r:G131\r=\r:I1200000\r=\r:J1\r=\r')
        self.goUp = (b':K2\r=\r:f2\r=103\r:f2\r=103\r:G230\r=\r:I2200000\r=\r:J2\r=\r')
        self.goDown = (b':K2\r=\r:f2\r=303\r:f2\r=303\r:G231\r=\r:I2200000\r=\r:J2\r=\r')


        #self.goRight_9 = (b':K1\r=\r:f1\r=103\r:f1\r=103\r:G130\r=\r:I10C0000\r=\r:J1\r=\r')
        #self.goLeft_9 = (b':K1\r=\r:f1\r=303\r:f1\r=303\r:G131\r=\r:I10C0000\r=\r:J1\r=\r')
        #self.goDown = (b':K2\r=\r:f2\r=303\r:f2\r=303\r:G231\r=\r:I1190000\r=\r:J2\r=\r')
        #self.goUp =(b':K2\r=\r:f2\r=103\r:f2\r=103\r:G230\r=\r:I1320000\r=\r:J2\r=\r')        #self.goUp = (b':K2\r=\r:f2\r=103\r:f2\r=103\r:G230\r=\r:I2200000\r=\r:J2\r=\r')
        #self.goDown = (b':K2\r=\r:f2\r=303\r:f2\r=303\r:G231\r=\r:I2200000\r=\r:J2\r=\r')
        self.StopX = (b':K1\r=\r')
        self.StopY = (b':K2\r=\r')

    def getIsReady(self):
        self.readyLock.acquire()
        ans = self.isReady
        self.readyLock.release()
        return ans

    def setReady(self ,isReady):
        self.readyLock.acquire()
        self.isReady=isReady
        self.readyLock.release()

    def setCorrection(self,dx=0,dy=0):
        if self.getIsReady():
            self.dx=dx;self.dy=dy
            self.setReady(False)
            self.whileLock.release()

    def correct(self):
        print(self.dx / self.maxdx)
        if (self.dx > self.threshx):
            self.ser.write(self.goRight_9)
        elif (self.dx < -self.threshx):
            self.ser.write(self.goLeft_9)
        #time.sleep(math.abs(self.dx / self.maxdx))
        time.sleep(0.2)
        self.ser.write(self.StopX)
        if (self.dy > self.threshy):
            self.ser.write(self.goDown)
        elif (self.dy < -self.threshy):
            self.ser.write(self.goUp)
        #time.sleep(self.dy / self.maxdy)
        time.sleep(0.2)
        #time.sleep(math.abs(self.dy / self.maxdy))
        self.ser.write(self.StopY)
        print("up down")


    # move up
    def run(self):
        while True:
            self.whileLock.acquire()
            self.correct()
            self.setReady(True)

    def stopTelescope(self):
        self.ser.write(self.StopX)
        self.ser.write(self.StopY)
        self.disconnect()
        print("Telescope stopped")

    def manualRight(self):
        self.ser.write(self.goRight_9)
        time.sleep(0.2)
        self.ser.write(self.StopX)
    def manualLeft(self):
        self.ser.write(self.goLeft_9)
        time.sleep(0.2)
        self.ser.write(self.StopX)
    def manualUp(self):
        self.ser.write(self.goUp)
        time.sleep(0.2)
        self.ser.write(self.StopX)
    def manualDown(self):
        self.ser.write(self.goDown)
        time.sleep(0.2)
        self.ser.write(self.StopX)