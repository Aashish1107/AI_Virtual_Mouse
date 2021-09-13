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
        bboxs=[]
        if self.results.detections:
            for id, detection in enumerate(self.results.detections):
                
                bboxC=detection.location_data.relative_bounding_box
                ih, iw, ic =img.shape
                bbox = int(bboxC.xmin*iw), int(bboxC.ymin*ih), \
                    int(bboxC.width*iw), int(bboxC.height*ih)
                bboxs.append([id, bbox, detection.score])
                
                img=self.TargetFace(img,bbox)
        
        return img, bboxs

    def TargetFace(self, img, bbox, l=25, t=5, rt=1):
        x,y,w,h=bbox
        x1,y1=x+w,y+h

        cv2.rectangle(img, bbox, (0,255,0), 1)

        #TOP LEFT (x,y)
        cv2.line(img, (x,y),(x+l,y),(0,255,0),t)
        cv2.line(img,(x,y),(x,y+l),(0,255,0),t)

        #TOP RIGHT (x1,y)
        cv2.line(img, (x1,y),(x1-l,y),(0,255,0),t)
        cv2.line(img,(x1,y),(x1,y+l),(0,255,0),t)

        #BOTTOM LEFT (x,y1)
        cv2.line(img, (x,y1),(x+l,y1),(0,255,0),t)
        cv2.line(img,(x,y1),(x,y1-l),(0,255,0),t)

        #BOTTOM RIGHT (x1,y1)
        cv2.line(img, (x1,y1),(x1-l,y1),(0,255,0),t)
        cv2.line(img,(x1,y1),(x1,y1-l),(0,255,0),t)

        return img

def main():

    cap=cv2.VideoCapture(r"C:\Users\Aashi\Downloads\t5.mp4")
    detector=FaceDetector(0.25)
    ptime=0
    ctime=0
    while True:
        success, img = cap.read()
        img, bboxs=detector.findFace(img)
        print(bboxs)
    
        ctime=time.time()
        fps=1/(ctime-ptime)
        ptime=time.time()
        cv2.putText(img, "FPS:"+str(int(fps)),(10,70), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,255),1)

        cv2.imshow("Face Detector", img)
        cv2.waitKey(50)




if __name__ =="__main__":
    main()