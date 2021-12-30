
import handtrackingModule as htm
import cv2 as cv
import mediapipe as mp
import time
import os
import numpy as np
#to do
# import image
#find hand landmarks
#check which finger are up (ideally one finger draw and two selects)
xp, yp=0, 0
imgcanv= np.zeros((480, 640, 3), np.uint8)



pTime = 0
cTime = 0

detector = htm.handDetector(detection_confidence=0.86)
Identification = [4, 8, 12, 16, 20]  # tops of the finger from thumb to pinky

folderpath = "folder"
imageList = os.listdir(folderpath)

somegarbage=[]

for imagepath in imageList:
    image = cv.imread(f'{folderpath}/{imagepath}')
    somegarbage.append(image)
garbage=somegarbage[0]
cap = cv.VideoCapture(0)
h,w,c=image.shape



while True:
    success, img = cap.read()
    img=cv.flip(img, 1)
    img = detector.findHands(img)
    landmarklist = detector.findPosition(img, draw=False)

    img[0:h, 0:w] = image  # slicing
    if len(landmarklist) != 0:
        

        #tip of middle finger
        x1, y1 = landmarklist[8][1:]
        x2, y2= landmarklist[12][1:]
        x3, y3= landmarklist[20][1:]



        fingers=detector.fingersup()
        #if fingers[1] and fingers[2]:   #select
        #    drawingcolor = (0, 0, 0)
        #    cv.rectangle(img,(x1,y1-15),(x2,y2+15),(255,0,255),cv.FILLED)
        #    cv.rectangle(imgcanv, (xp, yp), (x1, y1), drawingcolor, 30)
        #    xp, yp = x1, y1
        #    print("selecting")
        if fingers[4]:    #erase
            drawingcolor = (0, 0, 0)
            cv.circle(img, (x1,y1),15,(255,0,255),cv.FILLED)
            cv.circle(img, (x3,y3),15,(255,0,255),cv.FILLED)
           

            cv.rectangle(imgcanv, (xp, yp), (x1, y1), drawingcolor, 40)
            xp, yp = x1, y1
            print("erasing")
            
        if fingers[1] and  not  (fingers[4] or fingers[2]):   #draw
            cv.circle(img, (x1,y1),15,(255,0,255),cv.FILLED)
            drawingcolor=(255,0,0)
            print("fking around")

            if xp ==0 and yp==0:
                xp,yp= x1,y1

            cv.line(imgcanv, (xp,yp), (x1,y1), drawingcolor,5)
            xp,yp=x1, y1
            

        
        #print(fingers)
        

      
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv.putText(img, f'{str(int(fps))} FPS', (10, 250),
               cv.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 3)
    img=cv.addWeighted(img, 0.5, imgcanv, 0.5,0)
    cv.imshow("Image", img)
    #cv.imshow("Imagecanv", imgcanv)
    cv.waitKey(1)
