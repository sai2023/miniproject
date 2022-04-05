import cv2

def center_handle(x,y,w,h):
    x1=int(w/2)
    y1=int(h/2)
    cx=x+x1
    cy=y+y1
    return cx,cy

path="cars.xml"
detect=[]
count=0
cameraNo=0
objectName = 'car'
frameWidth=300
frameHeight=400
color=(255,0,255)
videopath="Car Detection_video.avi"
videopath1="video.mp4"
cap=cv2.VideoCapture(videopath1)
cap.set(3,frameWidth)
cap.set(4,frameHeight)
min_width_react=80
min_height_react=80
count_line_position=400
counter=0
offset=6

def empty(a):
    pass

cv2.namedWindow("Result")
cv2.resizeWindow("Result",frameWidth,frameHeight+100)
cv2.createTrackbar("Scale","Result",400,1000,empty)
cv2.createTrackbar("Neig","Result",8,20,empty)
cv2.createTrackbar("Min Area","Result",100,2000,empty)
cv2.createTrackbar("Brightness","Result",180,255,empty)

cascade=cv2.CascadeClassifier(path)

while True:
    cameraBrightness = cv2.getTrackbarPos("Brightness","Result")
    cap.set(10,cameraBrightness)
    success,img=cap.read()
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    cv2.line(img, (350, count_line_position), (900, count_line_position), (255, 127, 0), 3)
    scaleval =1+(cv2.getTrackbarPos("Scale","Result")/500)
    neig=cv2.getTrackbarPos("Neig","Result")
    objects=cascade.detectMultiScale(gray,scaleval,1)

    for(x,y,w,h) in objects:
        area=w*h
        minArea=cv2.getTrackbarPos("Min Area","Result")
        if area>minArea:
            cv2.rectangle(img,(x,y),(x+w,y+h),color,3)
            center=center_handle(x,y,w,h)
            detect.append(center)
            cv2.circle(img, center, 4, (0, 0, 255), -1)
            cv2.putText(img,objectName,(x,y-5),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,color,2)
           # cv2.putText(img,count,(x,y-5),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,color,2)
            roi_color = img[y:y+h,x:x+w]
            cv2.circle(img,center,4,(255,0,0),-1)
            count=count+1
            for (x, y) in detect:
                if y < (count_line_position + offset) and y > (count_line_position - offset):
                    counter += 1
                    cv2.line(img, (350, count_line_position), (900, count_line_position), (0, 127, 255), 3)
                    detect.remove((x, y))
                    print("VEHICLE COUNTER:" + str(counter))
            cv2.putText(img, "VEHICLE COUNTER :" + str(counter), (450, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255),
                        5)

    cv2.imshow("Result",img)
    if cv2.waitKey(1) & 0xFF ==ord('q'):
        break
    print(count)