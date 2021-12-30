import time
import cv2 as cv
import mediapipe as mp


#cap = cv.VideoCapture("Face_detection/vid.mp4")
cap = cv.VideoCapture(0)
pTime = 0
cTime = 0

mpFaceDetection=mp.solutions.face_detection
mpDraw=mp.solutions.drawing_utils
faceDetection = mpFaceDetection.FaceDetection(0.70)  #certaunty val

while True:
    success, img= cap.read()
    imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    results = faceDetection.process(imgRGB)
    detect=results.detections
    if detect:
        for id, detection in enumerate(detect):

            #mpDraw.draw_detection(img, detection)   #quickdraw
            #print(id, detection)
            certainty = detection.score
            print(certainty)
            #print(detection.location_data.relative_bounding_box)   #rectabgle normalized
################################################################################################
            #own drawing
            target = detection.location_data.relative_bounding_box
            h, w, c = img.shape
            target= int(target.xmin * w), int(target.ymin *h), int(target.width * w), int(target.height *h)
            cv.rectangle(img, target, (255, 0, 0), 5)
            cv.putText(img, f'{(int(certainty[0]*100))}%', (target[0], target[1]-20),
                       cv.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 3)
            
            


    

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv.putText(img, str(int(fps)), (18, 78),
               cv.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 3)
               


    cv.imshow("Image", img)
    cv.waitKey(1)
