"""  if len(landmarklist) != 0:
       #print(landmarklist[4], landmarklist[8])
        x1, y1 = landmarklist[4][1], landmarklist[4][2]  # id, x/y
        x2, y2 = landmarklist[8][1], landmarklist[8][2]
        cv.circle(img, (x1, y1), 15, (255, 0, 255), cv.FILLED)  # circle
        cv.circle(img, (x2, y2), 15, (255, 0, 255), cv.FILLED)
        # line , ifmg, points, color, thickness
        cv.line(img, (x1, y1), (x2, y2), (255, 0, 255), 2)

        cx, cy = (x1+x2)//2, (y1+y2)//2
        cv.circle(img, (cx, cy), 15, (255, 0, 255), cv.FILLED)
        #tx, ty = x2-x1, y2-y1
        #length = math.sqrt((tx**2) + (ty**2))
        length = math.hypot(x2-x1, y2-y1)

        if length < 40:    # min dist between finger for clock
            cv.circle(img, (cx, cy), 15, (255, 0, 0), cv.FILLED)
        if length > 240:  # max
            cv.circle(img, (cx, cy), 15, (0, 0, 255), cv.FILLED)

        #my hand range is betwen 40 - 250
        # volume range is -65 to 0
        vol = np.interp(length, [50, 250], [
                        minvolume, maxvolume])  # needs tuning
        vol_bar = np.interp(length, [50, 250], [
            400, 150])  # volume for bar
        vol_per = np.interp(length, [50, 250], [
            0, 100])  # needs tuning

        print(vol)
        volume.SetMasterVolumeLevel(vol, None)

    cv.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
    cv.rectangle(img, (50, int(vol_bar)), (85, 400), (0, 255, 0),
                 cv.FILLED)  # img, width, height,
    cv.putText(img, f'{str(int(vol_per))}%', (100, 150),
               cv.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 3) """

import pose_module as pose
import cv2 as cv
import mediapipe as mp
import time
import math
import numpy as np


pTime = 0
cTime = 0
cap = cv.VideoCapture(0)
detector = pose.poseDetector(detection_confidence=0.6)

while True:
    success, img = cap.read()
    img=detector.findpose(img)
    landmarklist=detector.getPosition(img, False)
    if len(landmarklist) != 0:
        detector.getAngle(img,12,14,16) #right arm 
        angle=detector.getAngle(img, 11,13,15)#left

        per=np.interp(angle,(210,310),(0,100))
        print(angle, per)

   
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv.putText(img, str(int(fps)), (10, 78),
               cv.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 3)
    cv.imshow("Image", img)
    cv.waitKey(1)
