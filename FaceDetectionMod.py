import cv2
import mediapipe as mp
import time

from mediapipe.python.solutions.face_detection import FaceDetection

class FaceDetector():
    def __init__(self, detectionCon=0.5, model=0):
        self.detectionCon=detectionCon
        self.model=model


        self.myFace=mp.solutions.face_detection
        self.FaceDetection=self.myFace.FaceDetection(self.detectionCon, self.model)
        self.myDraw=mp.solutions.drawing_utils


    def findFace(self,img):
        imgRGB=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results=self.FaceDetection.process(imgRGB)
        if self.results.detections:
            for id, detection in enumerate(self.results.detections):
                
                bboxC=detection.location_data.relative_bounding_box
                ih, iw, ic =img.shape
                bbox = int(bboxC.xmin*iw), int(bboxC.ymin*ih), \
                    int(bboxC.width*iw), int(bboxC.height*ih)
                cv2.rectangle(img, bbox, (0,255,0), 2)
        
        return img


def main():

    cap=cv2.VideoCapture(r"C:\Users\Aashi\Downloads\t5.mp4")
    detector=FaceDetector(0.5)
    ptime=0
    ctime=0
    while True:
        success, img = cap.read()
        img=detector.findFace(img)

    
        ctime=time.time()
        fps=1/(ctime-ptime)
        ptime=time.time()
        cv2.putText(img, str(int(fps)),(10,100), cv2.FONT_HERSHEY_COMPLEX, 3, (0,255,0),3)

        cv2.imshow("Face Detector", img)
        cv2.waitKey(50)




if __name__ =="__main__":
    main()