import cv2 as cv
import mediapipe as mp
import time

cap = cv.VideoCapture(0)

mpHands= mp.solutions.hands
hands= mpHands.Hands()
mpDraw=mp.solutions.drawing_utils

pTime= 0
cTime= 0

while True:
    success, img = cap.read()
    imgRGB= cv.cvtColor(img, cv.COLOR_BGR2RGB)  #to RGB
    results=hands.process(imgRGB)   #process
    #print(results.multi_hand_landmarks)
    hand_detect=results.multi_hand_landmarks
    if hand_detect:
        for each_hand in hand_detect:
            for id, landmarks in enumerate(each_hand.landmark):
                #print(id, landmarks)
                #gettin pixel val
                h, w, c= img.shape
                cx, cy=int(landmarks.x*w), int(landmarks.y*h)
                print(id, cx, cy)
                if id==4:
                    cv.circle(img, (cx, cy), 15, (0, 0, 0), cv.FILLED)
                #for id in range(21):
                    #cv.circle(img, (cx, cy), 15, (100+id, 10+id, 2+id), cv.FILLED)




            #mpDraw.draw_landmarks(img, each_hand) #without hand connections 
            mpDraw.draw_landmarks(img, each_hand, mpHands.HAND_CONNECTIONS) #WITH connections
    cTime =time.time()
    fps=1/(cTime-pTime)
    pTime= cTime
    cv.putText(img, str(int(fps)), (18,78), cv.FONT_HERSHEY_PLAIN,3, (0,0,0), 3)
    
    cv.imshow("Image", img)
    cv.waitKey(1)
    
