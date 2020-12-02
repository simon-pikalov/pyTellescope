import cv2
#home

#stream = cv2.VideoCapture('http://10.2.0.248:8080/video')
#router
#stream = cv2.VideoCapture('http://192.168.8.144:8080/video')

#KCG
stream = cv2.VideoCapture('http://192.168.100.109:8080/video')

# Use the next line if your camera has a username and password
# stream = cv2.VideoCapture('protocol://username:password@IP:port/1')
hx=600
hy=300

# the final resolution is 1200-x on 600-y
while True:


    r, f = stream.read()
    height, width = f.shape[:2]
    cy= int(height/2)
    cx=int(width/2)
    cv2.rectangle(f, (cx - 10, cy - 10), (cx + 10, cy + 10), (256, 256, 0), 5)
    #f = cv2.resize(f, fx=0.5, fy=0.5, interpolation=cv2.INTER_LINEAR)
    f = f[ cy-hy:cy+hy,cx-hx:cx+hx]
    print(cx,cy, height,width)

    #cv2.circle(f,(cx,cy),5, (30,40,50))
    cv2.imshow('IP Camera stream',f)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()