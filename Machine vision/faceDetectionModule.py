import cv2 as cv
import mediapipe as mp
import time


class FaceDetector():
    def __init__(self, min_detection_confidence=0.7):
        self.min_detect= min_detection_confidence
        self.mpFaceDetection = mp.solutions.face_detection
        self.mpDraw = mp.solutions.drawing_utils
        self.faceDetection = self.mpFaceDetection.FaceDetection(self.min_detect)  # certaunty val
        
        #self.detect = self.mpFaceDetection.Pose(
         #   self.mode, self.modelComplexcity, self.smooth_segmentation, self.enable_segmentation, self.smooth_landm, self.detection_confidence, self.tracking_confidence)

    def findface(self, img, draw=True):
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)  # to RGB
        self.results = self.faceDetection.process(imgRGB)  # process
    # print(results.multi_hand_landmarks)
        detect= self.results.detections
        targets=[]
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
                target = int(target.xmin * w), int(target.ymin *
                                               h), int(target.width * w), int(target.height * h)
                targets.append([target, certainty])            
                #cv.rectangle(img, target, (255, 0, 0), 5)
                img = self.tryhard(img, target)
                cv.putText(img, f'{(int(certainty[0]*100))}%', (target[0], target[1]-20),
                       cv.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 3)

        return img, targets

    def tryhard(self, img, target, l=30, t=10, rt=1):
        X,y, W, h =target
        X1, y1 = X+W, y+h
        cv.rectangle(img, target, (255, 0, 0), rt)
        #Top left
        cv.line(img, (X,y),(X+ l, y), (255, 0, 0), t)
        cv.line(img, (X, y), (X, y+l), (255, 0, 0), t)
        #top right
        cv.line(img, (X1,y),(X1- l, y), (255, 0, 0), t)
        cv.line(img, (X1, y), (X1, y+l), (255, 0, 0), t)
        #Bottom left
        cv.line(img, (X, y1), (X + l, y1), (255, 0, 0), t)
        cv.line(img, (X, y1), (X, y1-l), (255, 0, 0), t)
        #Bottom right
        cv.line(img, (X1, y1), (X1 - l, y1), (255, 0, 0), t)
        cv.line(img, (X1, y1), (X1, y1 - l), (255, 0, 0), t)
        return img

   


def main():
    pTime = 0
    cTime = 0
    cap = cv.VideoCapture('dragon.mp4')
    detector = FaceDetector()

    while True:
        success, img = cap.read()
        img, targets = detector.findface(img)

        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv.putText(img, str(int(fps)), (10, 78), cv.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 3)

        cv.imshow("Image", img)
        cv.waitKey(10)


if __name__ == "__main__":
    main()
