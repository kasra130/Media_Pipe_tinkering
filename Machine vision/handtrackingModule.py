import cv2 as cv
import mediapipe as mp
import time


class handDetector():
    def __init__(self, mode=False, maxHands=2, modelComplexcity=1, detection_confidence=0.5, tracking_confidence=0.5):
        self.mode=mode    #create an object with its own varibale
        self.maxHands=maxHands
        self.modelComplexcity=modelComplexcity
        self.detection_confidence=detection_confidence
        self.tracking_confidence=tracking_confidence
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelComplexcity, self.detection_confidence, self.tracking_confidence)
        self.mpDraw = mp.solutions.drawing_utils
        self.Identification = [4, 8, 12, 16, 20]

    def findHands(self, img, draw=True):
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)  # to RGB
        self.results = self.hands.process(imgRGB)  # process
    #print(results.multi_hand_landmarks)
        self.hand_detect = self.results.multi_hand_landmarks
        if self.hand_detect:
            for  each_hand in self.hand_detect:
                if draw:
                    self.mpDraw.draw_landmarks(img, each_hand, self.mpHands.HAND_CONNECTIONS)  # WITH connections
        return img
        

    def findPosition(self, img, handNo=0, draw=True):

        self.landmarklist=[]
        if self.hand_detect:
            myHand=self.hand_detect[handNo]
            for id, landmarks in enumerate(myHand.landmark):
                #print(id, landmarks)
                #gettin pixel val
                h, w, c = img.shape
                cx, cy = int(landmarks.x*w), int(landmarks.y*h)
                #print(id, cx, cy)
                self.landmarklist.append((id, cx, cy))
                #if id == 4:
                if draw:
                    cv.circle(img, (cx, cy), 15, (0, 0, 0), cv.FILLED)
            #for id in range(21):
                #cv.circle(img, (cx, cy), 15, (100+id, 10+id, 2+id), cv.FILLED)

        return self.landmarklist
        #mpDraw.draw_landmarks(img, each_hand) #without hand connections """


    def fingersup(self):
        # tops of the finger from thumb to pinky
        


        finger = []
        #right thumb # thumb is more complex, i have to make a logic
        if self.landmarklist[self.Identification[0]][1] < self.landmarklist[self.Identification[0]-1][1]:
           finger.append(1)
           #print(finger)
        else:
            finger.append(0)
        #print(finger)
# once the ifnger is identidfied, - x+x will let you specify finger
        for id in range(1, 5):
            # once the ifnger is identidfied, - x+x will let you specify finger
            if self.landmarklist[self.Identification[id]][2] < self.landmarklist[self.Identification[id]-2][2]:
                finger.append(1)
                #print(finger)
            else:
                finger.append(0)
                #print(finger)

        return finger
       






def main():
    pTime = 0
    cTime = 0
    cap = cv.VideoCapture(0)
    detector=handDetector()


    while True:
        success, img = cap.read()
        img=detector.findHands(img)
        landmarklist= detector.findPosition(img)
        #if len(landmarklist) !=0 :
            #print(landmarklist[4])
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv.putText(img, str(int(fps)), (10, 78),cv.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 3)

        cv.imshow("Image", img)
        cv.waitKey(1)





if __name__ == "__main__":
    main()




                
