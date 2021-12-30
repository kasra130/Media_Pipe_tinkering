import cv2 as cv
import mediapipe as mp
import time




class FaceMeshDetector():
    def __init__(self, staticMode=False, maxFaces=2, refine_landmarks=False, minDetectionConfidence=0.5, minTracking=0.5):
        self.mode = staticMode  # create an object with its own varibale
        self.maxfaces = maxFaces
        self.rf=refine_landmarks
        self.detection_confidence = minDetectionConfidence
        self.tracking_confidence = minTracking
        
        self.mpDraw = mp.solutions.drawing_utils
        self.mpFaceMesh = mp.solutions.face_mesh
        self.faceMesh = self.mpFaceMesh.FaceMesh(self.mode, self.maxfaces, self.rf, self.detection_confidence, self.tracking_confidence)
        self.drawSpec = self.mpDraw.DrawingSpec(thickness=1, circle_radius=2)


    def findFace(self, img, draw=True):
        self.imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)  # to RGB
        self.results = self.faceMesh.process(self.imgRGB)  # process
    #print(results.multi_hand_landmarks)
        faces = []
        self.detect = self.results.multi_face_landmarks
        if self.detect:
            
            for face_landmark in self.detect:
                if draw:
                    self.mpDraw.draw_landmarks(img, face_landmark, self.mpFaceMesh.FACEMESH_CONTOURS, self.drawSpec, self.drawSpec)  # CONtour
                face=[]
                for id, face_landmarks in enumerate(face_landmark.landmark):
                    
                    h, w, c = img.shape
                    cx, cy = int(face_landmarks.x*w), int(face_landmarks.y*h)
                    cv.putText(img, str(id), (cx, cy), cv.FONT_HERSHEY_PLAIN, 0.5, (255,0,0),1)
                    if id ==  (10) :  
                       cv.circle(img, (cx, cy), 10, (0, 0, 255), cv.FILLED) #forhead 10 , eye 24

                    #print(id, cx, cy)
                    face.append([cx,cy])
                faces.append(face)
        
        return img, faces

 


def main():
    pTime = 0
    cTime = 0
    cap = cv.VideoCapture('dragon.mp4')
    detector = FaceMeshDetector()

    while True:
        success, img = cap.read()
        img, faces= detector.findFace(img)
        if len(faces)!=0:
            #time.sleep(0.1)
            print(len(faces)) #number of faces
   
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv.putText(img, str(int(fps)), (10, 78),
                   cv.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 3)

        cv.imshow("Image", img)
        cv.waitKey(10)


if __name__ == "__main__":
    main()
