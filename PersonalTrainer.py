import cv2
import time
import PoseTrackingMod as ptm
import math
import numpy as np

cap=cv2.VideoCapture(0)
ptime=0

detector=ptm.PoseDetector(detectionCon=0.75)
dir=0
count=0

while True:
    success, img=cap.read()
    img=cv2.resize(img, (720,480)) #instead of using the set function to set size, image is resized
    img=detector.findBody(img,draw=False)
    lmList=detector.findPosition(img,draw=False)
    if len(lmList)!=0:
        img,angle=detector.findAngle(img,12,14,16)
        
        per=np.interp(angle,[30,160],[0,100])
        
        #Check curls
        if per==100:
            if dir==0:
                count+=0.5
                dir=1
        if per==0:
            if dir==1:
                count+=0.5
                dir=0
        cv2.rectangle(img,(0,350),(100,480),(0,255,0),cv2.FILLED)
        cv2.putText(img,f'{int(count)}',(20,440),cv2.FONT_HERSHEY_PLAIN,5,(255,0,255),5)


    ctime=time.time()
    fps=1/(ctime-ptime)
    ptime=ctime

    
    cv2.putText(img, f'FPS:{int(fps)}',(20,40),cv2.FONT_HERSHEY_PLAIN,2,(255,0,0),1)
    
    cv2.imshow("Image",img)
    cv2.waitKey(1)