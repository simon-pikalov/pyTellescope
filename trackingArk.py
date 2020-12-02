import cv2
import math
import time
import Telcontrol

#---------------------------
# get telescope controll

telescopeEnabled = True

if (telescopeEnabled):
    telescope = Telcontrol.Telcontrol()
    time.sleep(2)
    print("telescope connected")


CAMERA_ID = 0
OUTPUT_FOLDER = '~/Development/telescope_output'
OUTPUT_FILE = 'test1.avi'

print("init start")
frameCounter=0

#init input stream
cap = cv2.VideoCapture(CAMERA_ID)

#init output stream
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5)
target_center_x = int(frame_width/2)
target_center_y = int(frame_height/2)
print("image size: "+str(frame_width)+","+str(frame_height))

fourcc = cv2.VideoWriter_fourcc(*'DIVX')
out = cv2.VideoWriter(OUTPUT_FOLDER+OUTPUT_FILE, fourcc, 10, (frame_width, frame_height))

print("init end")

print("select tracking object start")

# get image, and select an object to track on it


#skip a few frames
for i in range (20):
    cap.read()

ok, image=cap.read()
if not ok:
    print('Failed to read video')
    exit()

bbox = cv2.selectROI("tracking", image)
#tracker = cv2.TrackerMIL_create()
#tracker = cv2.TrackerBoosting_create()
tracker = cv2.TrackerCSRT_create()
ok = tracker.init(image, bbox)

def click(event, x, y, flags, param):
    global target_center_x,target_center_y
    if event == cv2.EVENT_LBUTTONDOWN:
        print(" center selected ", x, y)
        target_center_x = x
        target_center_y = y


cv2.namedWindow("frame")
cv2.setMouseCallback("frame", click)



while cap.isOpened():
    # show the image
    ok, frame=cap.read()

    # update traker
    tracker_ok, newbox = tracker.update(frame)
    if (tracker_ok):
        # obj bounding box
        p1 = (int(newbox[0]), int(newbox[1]))
        p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
        cv2.rectangle(frame, p1, p2, (200, 0, 0))
        # obj center
        obj_center_x= int((p1[0] + p2[0]) / 2)
        obj_center_y = int((p1[1] + p2[1]) / 2)
        cv2.circle(frame, (obj_center_x, obj_center_y), 10, (200, 0, 0), 3)

        # calc the dist from center frame point to your object
        # the goal is to match between them

        # TODO: maybe the order should be diferent, once you know the axis of the telescope, fix this
        dx = obj_center_x - target_center_x
        dy = obj_center_y - target_center_y

        #print ("dist to obj "+str(dx)+","+str(dy))
        #listX = [9, 8, 7]
        #listX = [8, 7, 6]
        #listX = [7, 6, 4]
        listX = [6, 5, 4]

        speedX = listX[0]
        if (abs(dx) < 100):
            speedX = listX[0]

        if (abs(dx) < 75):
            speedX = listX[1]

        if (abs(dx) < 50):
            speedX = listX[2]

        # if (abs(dx) < 25):
        #     speedX = 5

        speedY = listX[0];
        if (abs(dy) < 100):
            speedY = listX[0]

        if (abs(dy) < 75):
            speedY = listX[1]

        if (abs(dy) < 50):
            speedY = listX[2]

        # if (abs(dy) < 25):
        #     speedY = 5

        if (telescopeEnabled):
            #telescope.moveX(dx,speedX)
            #telescope.moveY(dy,speedY)

            telescope.moveY(dx, speedX)
            telescope.moveX(-dy, speedY)

    cv2.circle(frame, (target_center_x, target_center_y), 10, (0, 200, 0),8)
    cv2.imshow('frame', frame)

    # keep frame count
    frameCounter = frameCounter+1
    # print("frame counter"+str(frameCounter))

    # let the drawing thread to work,by waiting for a key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        out.release()
        cap.release()
        cv2.destroyAllWindows()
        if (telescopeEnabled):
            telescope.stop()
            telescope.disconnect()
        exit()


#---------------------------
