import numpy as np
import cv2
import matplotlib as plt
import math

centerx=0
centery=0

Cwidth= 0
Clength=0

velocity=0
xold=0
yold=0

cutFrame =200

def run_main():
    msgE = str(99)
    print(msgE)
    #To save the video later
    fourcc = cv2.VideoWriter_fourcc('H', '2', '6', '4')
    #out = cv2.VideoWriter('output1.mp4', -1, 20.0, (1280, 480))

    cap = cv2.VideoCapture('drone3.h264')
    #cap = cv2.VideoCapture('greaySmall.mp4')
    #cap = cv2.VideoCapture(1)


    # Read the first frame of the video
    ret, frame = cap.read()
    height, width, channels = frame.shape
    print(height, width, channels)
    out = cv2.VideoWriter('output1.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10, (width, height))

    centerx = int(width/2)
    centery = int(height/2)

    Cwidth = width-100
    Clength = height-100

    #feature detection

    def detection(frame):

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #gray=frame
        corners = cv2.goodFeaturesToTrack(gray,1, 0.9, 1)
        corners = np.int0(corners)
        return corners

    def hughDetection(frame):
        #frame = cv2.medianBlur(frame, 5)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1,1,
                                   param1=200, param2=256, minRadius=0, maxRadius=0)
        circles = np.int0(np.around(circles))
        return circles

    def distanceFromCenterX(x):
        distx =x-centerx
        return distx
    def distanceFromCenterY(y):
        disty =y-centery
        return disty
    corners=detection(frame)
    x, y = corners[0].ravel()
    c, r, w, h = x, y, 30, 30
    xold=x
    yold=y
    lower_grey = np.array([200, 255, 255])
    upper_grey = np.array([256, 255, 255])
    i=0
    #while True:
    while (cap.isOpened()):
        i=i+1
        if i>7000:
            break
        ret, frame = cap.read()
        frame_sub=frame
        #frame_sub = frame[cutFrame:height-cutFrame, cutFrame: width-cutFrame]  # left

        #if harris:
        corners=detection(frame_sub)
        np.int0(corners)
        x, y = corners[0].ravel()
        w=30
        h=30

        print("corners" ,corners)
        colorDistx=70
        colorDisty =70
        if(math.fabs(distanceFromCenterX(x))-Cwidth>0):
            print(distanceFromCenterX(x))
            colorDistx=200
            msgE="move left "+str(distanceFromCenterX(x)-Cwidth)
        if (math.fabs(distanceFromCenterY(y)) - Clength>0):
            colorDisty = 200
            msgE = msgE+"move up " + str(distanceFromCenterY(y) - Clength)

        velocity=math.sqrt(math.pow(x-xold,2)+math.pow(y-yold,2))

        if(velocity>10  and velocity<150) :
            cv2.circle(frame, (x, y), int((w + h) / 2), 255, 2)
            cv2.putText(frame, msgE, (100, 130), cv2.FONT_HERSHEY_SIMPLEX,1,40)
            cv2.putText(frame,"distance x: "+str(distanceFromCenterX(x)),(100,100) ,cv2.FONT_HERSHEY_SIMPLEX,1,colorDistx)
            cv2.putText(frame, "distance y: "+str(distanceFromCenterY( y)), (100, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, colorDisty)
            cv2.putText(frame, "velocity: " + str(velocity), (100, 20), cv2.FONT_HERSHEY_SIMPLEX, 1,colorDisty)
        cv2.rectangle(frame,(centerx-int(Cwidth), centery-int(Clength)),(centerx+int(Cwidth), centery+int(Clength)),200 )
        cv2.circle(frame, (centerx, centery), 3, 50, 2)
        cv2.putText(frame, str(centerx) + " " + str(centery), (centerx, centery), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 50)
        xold=x
        yold=y
        msgE=""
        #if hugh:
        # circles= hughDetection(frame)
        # for i in circles[0, :]:
        #     # draw the outer circle
        #     cv2.circle(frame, (i[0], i[1]), i[2], (0, 255, 0), 2)
        #     # draw the center of the circle
        #     cv2.circle(frame, (i[0], i[1]), 2, (0, 0, 255), 3)



        out.write(frame)
        #cv2.namedWindow("KCG Ballon tracker", cv2.WINDOW_NORMAL)
        imS = cv2.resize(frame, (1500, 600))
        cv2.imshow("KCG Ballon tracker", frame)

        if cv2.waitKey(15) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    run_main()
