import cv2
import mediapipe as mp
import time

class PoseDetector():
    def __init__(self, mode=False ,complex=1 ,smoothlms=True ,enableSeg=False ,smooth=True ,detectionCon=0.5 ,trackCon=0.5):
        
        self.mode=mode
        self.complx=complex
        self.smoothlms=smoothlms
        self.enableSeg=enableSeg
        self.smooth=smooth
        self.detectionCon=detectionCon
        self.trackCon=trackCon


        self.mpPose=mp.solutions.pose
        self.pose=self.mpPose.Pose(self.mode,self.complx,self.smoothlms,self.enableSeg,self.smooth,self.detectionCon,self.trackCon)
        self.mpdraw=mp.solutions.drawing_utils

    def findBody(self, img, draw=True):
        imgRGB=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results=self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            if draw == True:
                self.mpdraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)

        return img
    
    def findPosition(self, img, draw=True):
        
        lmList=[]
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c=img.shape
                cx, cy=int(lm.x*w), int(lm.y*h)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5,(255,0,0), cv2.FILLED)
        return lmList

def main():

    cap=cv2.VideoCapture(r"t1.mp4")
    detector=PoseDetector()
    cTime=0
    pTime=0

    while True:
        success, img=cap.read()

        img = detector.findBody(img)
        lmList=detector.findPosition(img)
        if(len(lmList)!=0):
            print(lmList)

        cTime=time.time()
        fps=1/(cTime-pTime)
        pTime=cTime

        cv2.putText(img, str(int(fps)),(10,100), cv2.FONT_HERSHEY_COMPLEX, 3, (255,0,0),3)
        cv2.imshow("Image", img)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()