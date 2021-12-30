import handtrackingModule as htm
import cv2 as cv
import mediapipe as mp
import time


pTime = 0
cTime = 0
cap = cv.VideoCapture(0)
detector = htm.handDetector()

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    landmarklist = detector.findPosition(img, draw=False)
    if len(landmarklist) != 0:
        print(landmarklist[4])
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv.putText(img, str(int(fps)), (10, 78),
               cv.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 3)
    cv.imshow("Image", img)
    cv.waitKey(1)
