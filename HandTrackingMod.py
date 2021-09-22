import cv2
import mediapipe as mp
import time

class HandDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode=mode
        self.maxHands=maxHands
        self.detectionCon=detectionCon
        self.trackCon=trackCon

        self.mpHands=mp.solutions.hands
        self.hands=self.mpHands.Hands(self.mode, self.maxHands, self.detectionCon, self.trackCon)
        self.mpdraw=mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results=self.hands.process(imgRGB)

        
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw == True:
                    self.mpdraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)

        return img
    
    def findPosition(self, img, draw=True, handNo=0):
        
        self.lmList=[]
        if self.results.multi_hand_landmarks:
            myHand=self.results.multi_hand_landmarks[handNo]
            
            for id,lm in enumerate(myHand.landmark):
                h,w,c=img.shape
                cx, cy= int(lm.x*w), int(lm.y*h)
                self.lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 15, (255,0,0), cv2.FILLED)
        return self.lmList

    def fingersUP(self):
        fingers=[]
        
        #Left Hand Thumb
        if self.lmList[1][1]<self.lmList[0][1]:
            if self.lmList[4][1]<self.lmList[5][1]:
                fingers.append(1)
            else:
                fingers.append(0)
        #Right Hand Thumb
        else:
            if self.lmList[4][1]>self.lmList[5][1]:
                fingers.append(1)
            else:
                fingers.append(0)

        #Other 4 Fingers
        for i in range(2,6):
            if self.lmList[4*i][2]<self.lmList[4*i-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        
        return fingers

def main():

    cap=cv2.VideoCapture(0)
    detector=HandDetector()
    cTime=0
    pTime=0

    while True:
        success, img=cap.read()

        img = detector.findHands(img)
        lmList=detector.findPosition(img, False)
        if(len(lmList)!=0):
            print(lmList[0])

        cTime=time.time()
        fps=1/(cTime-pTime)
        pTime=cTime

        cv2.putText(img, str(int(fps)),(10,100), cv2.FONT_HERSHEY_COMPLEX, 3, (255,0,0),3)
        cv2.imshow("Image", img)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()