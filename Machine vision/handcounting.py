
import handtrackingModule as htm
import cv2 as cv
import mediapipe as mp
import time
import os

pTime = 0
cTime = 0
cap = cv.VideoCapture(0)
detector = htm.handDetector(detection_confidence=0.75)
Identification=[4, 8, 12, 16, 20]   #tops of the finger from thumb to pinky

folderpath="fingers"
imageList=os.listdir(folderpath)
fings=[]
#print(imageList)

for imagepath in imageList:
    image= cv.imread(f'{folderpath}/{imagepath}')
    #print((f'{folderpath}/{imagepath}'))
    fings.append(image)





while True:
    success, img = cap.read()
 #   fings[0].resize(200,200,3)
   
    img = detector.findHands(img)
    landmarklist = detector.findPosition(img, draw=False)
    if len(landmarklist) != 0:
        finger=[]
        #right thumb # thumb is more complex, i have to make a logic
        #if landmarklist[Identification[0]][1] > landmarklist[Identification[0]-1][1]:
         #   finger.append(1)
         #   print(finger)
        #else:
            #finger.append(0)
            #print(finger)
# once the ifnger is identidfied, - x+x will let you specify finger
        for id in range(0,5):
            if landmarklist[Identification[id]][2] < landmarklist[Identification[id]-2][2]:   #once the ifnger is identidfied, - x+x will let you specify finger
                finger.append(1)
                #print(finger)
            else:
                finger.append(0)
                #print(finger)
                
        totalfingers=finger.count(1)
        print(totalfingers)

        h, w, c = fings[totalfingers-2].shape
        img[0:h, 0:w] = fings[totalfingers-2]  # slicing



        #if landmarklist[8][2] < landmarklist[6][2]:   #if values  100 50 ->closed 
         #   print("inedex finger open")

        #else:
         #   print("not open§")
        
        #print(landmarklist[4])
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv.putText(img, f'{str(int(fps))} FPS', (10, 250),
               cv.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 3)
    cv.imshow("Image", img)
    cv.waitKey(1)
