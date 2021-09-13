import cv2
import mediapipe as mp
import time

class FaceMeshDetector():
    def __init__(self, mode=False, maxFaces=1,detectionCon=0.5, trackCon=0.5):
        self.mode=mode
        self.maxFaces=maxFaces
        self.detectionCon=detectionCon
        self.trackCon=trackCon


        self.mpDraw=mp.solutions.drawing_utils
        self.mpFaceMesh=mp.solutions.face_mesh
        self.faceMesh=self.mpFaceMesh.FaceMesh(self.mode, self.maxFaces, self.detectionCon, self.trackCon)

    def findFaceMesh(self, img):

        #DrawingSpec provides specifications while drawing landmarks
        #DrawingSpec(color, thickness, circle_radius)
        drawspecs=self.mpDraw.DrawingSpec((0,255,0),1,1)

        imgRGB=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results=self.faceMesh.process(imgRGB)
        lmList=[]
        if self.results.multi_face_landmarks:
            for fid,facelms in enumerate(self.results.multi_face_landmarks):
                self.mpDraw.draw_landmarks(img, facelms ,self.mpFaceMesh.FACEMESH_CONTOURS,drawspecs,drawspecs)
                face=[]
                for id, lm in enumerate(facelms.landmark):
                    ih, iw, ic = img.shape
                    x,y=int(lm.x * iw), int(lm.y * ih)
                    face.append([id,x,y])
                lmList.append([fid, face])
        return img,lmList
    


def main():
    cap=cv2.VideoCapture(0)
    ptime=0
    ctime=0
    detector=FaceMeshDetector()

    while True:
        success, img = cap.read()
        img, lmList =detector.findFaceMesh(img)
        print(lmList)
        
        ctime=time.time()
        fps=1/(ctime-ptime)
        ptime=time.time()

        cv2.putText(img,"FPS:"+str(int(fps)),(20,70),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),1)
        cv2.imshow("FaceMesh",img)
        cv2,cv2.waitKey(1)


if __name__ == "__main__":
    main()