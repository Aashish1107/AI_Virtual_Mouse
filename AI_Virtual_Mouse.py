import cv2
import HandTrackingMod as htm
import numpy as np
import time
import pyautogui

#Variables
##############
wCam, hCam= 1280,720
wScr, hScr= pyautogui.size()
wRange,hRange=120,200
smoothener=4

##############
cap=cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)


detector=htm.HandDetector(0.85)
ptime=0
plocX,plocY,clocX,clocY=0,0,0,0
thumbPrev=1

while True:
    success, img = cap.read()
    img=cv2.flip(img,1)
    #Find hand Landmarks
    img=detector.findHands(img)
    lmList, bbox=detector.findPosition(img)

    if len(lmList)!=0:
        #Get the positions of the tips of the index finger and the middle finger
        x1,y1=lmList[8][1:]
        x2,y2=lmList[12][1:]

        #Check fingers up
        fingers=detector.fingersUP()
        
        #Moving Mode
        cv2.rectangle(img,(wRange,hRange),(wCam-wRange,hCam-hRange),(0,255,0),1)
        if fingers==[0,1,0,0,0] or fingers==[1,1,0,0,0]:

            #Convet Coordinates
            x3=np.interp(x1,(wRange,wCam-wRange),(0, wScr))
            y3=np.interp(y1,(hRange,hCam-hRange),(0, hScr))
        
            #Smoothen
            clocX=plocX + (x3-plocX)/smoothener
            clocY=plocY + (y3-plocY)/smoothener
            plocX,plocY=clocX,clocY
            #Move Mouse
            pyautogui.moveTo(clocX,clocY)
        #Select Mode
        if fingers[1:]==[1,1,0,0]:
            length , img, posinfo = detector.findDistance(8,12,img)
            if fingers[0]==0:
                pyautogui.leftClick()
                cv2.circle(img,(lmList[4][1],lmList[4][2]),7,(255,0,0),cv2.FILLED)
            if length<45:
                pyautogui.rightClick()
                cv2.circle(img,(posinfo[-2],posinfo[-1]),7,(255,0,0),cv2.FILLED)

    #FPS
    ctime=time.time()
    fps=1/(ctime-ptime)
    ptime=ctime

    #Show
    cv2.putText(img, f'{int(fps)}',(20,100),cv2.FONT_HERSHEY_PLAIN,1,(255,0,255),2)
    cv2.imshow("Img", img)
    cv2.waitKey(1)