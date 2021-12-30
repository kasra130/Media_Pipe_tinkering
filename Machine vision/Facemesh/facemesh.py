import cv2 as cv
import mediapipe as mp
import time


mpDraw= mp.solutions.drawing_utils
mpFaceMesh=mp.solutions.face_mesh
faceMesh=mpFaceMesh.FaceMesh(max_num_faces=2)  #static =flase, if true it will detect in every single image, detect and track-> garbage pc cant do
drawSpec=mpDraw.DrawingSpec(thickness=1, circle_radius=2)
cap =cv.VideoCapture(0)
pTime=0
cTime=0
while True:
    success, img= cap.read()
    imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)  # to RGB
    results = faceMesh.process(imgRGB)
    detect= results.multi_face_landmarks
    if detect:
        for face_landmark in detect:
            mpDraw.draw_landmarks(img, face_landmark, mpFaceMesh.FACEMESH_CONTOURS, drawSpec, drawSpec) #CONtour

            for id, face_landmarks in enumerate(face_landmark.landmark):
            
                h, w, c = img.shape
                cx, cy = int(face_landmarks.x*w), int(face_landmarks.y*h)
                print(id, cx, cy)
                
            
            


    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv.putText(img, str(int(fps)), (10, 80), cv.FONT_HERSHEY_PLAIN, 3, (0,0,0),3)
    cv.imshow("Image", img)
    cv.waitKey(1)
