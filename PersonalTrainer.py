import cv2
import time
import PoseTrackingMod as ptm
import math
import numpy as np

print("input 12,14 and 16 for right hand or 11,13,15 for left hand")
#x,y,z are the 3 points to find the angle between xy and yz
x,y,z=int(input()), int(input()), int(input())
cap=cv2.VideoCapture(0)
ptime=0

detector=ptm.PoseDetector(detectionCon=0.75)
dir=0
count=0
color=(0,255,0)

while True:
    success, img=cap.read()
    img=cv2.resize(img, (720,480)) #instead of using the set function to set size, image is resized
    img=detector.findBody(img,draw=False)
    lmList=detector.findPosition(img,draw=False)
    if len(lmList)!=0:
        img,angle=detector.findAngle(img,x,y,z)
        if angle>180:
            angle=360-angle
        per=np.interp(angle,[30,160],[100,0])
        bar=np.interp(angle,[30,160],[300,450])
        
        #Check curls
        if per==100:
            color=(255,0,255)
            if dir==0:
                count+=0.5
                dir=1
        if per==0:
            color=(0,255,0)
            if dir==1:
                count+=0.5
                dir=0

        #Curl Progress Bar
        cv2.putText(img,str(int(per)),(650,250),cv2.FONT_HERSHEY_PLAIN,2,(255,0,0),2)
        cv2.rectangle(img, (650,300),(700,450),(0,255,0),2)
        cv2.rectangle(img,(700,450),(650,int(bar)),color,cv2.FILLED)  

        #Count Curls      
        cv2.rectangle(img,(0,350),(100,480),(0,255,0),cv2.FILLED)
        cv2.putText(img,f'{int(count)}',(20,440),cv2.FONT_HERSHEY_PLAIN,5,(255,0,255),5)


    ctime=time.time()
    fps=1/(ctime-ptime)
    ptime=ctime

    
    cv2.putText(img, f'FPS:{int(fps)}',(20,40),cv2.FONT_HERSHEY_PLAIN,2,(255,0,0),1)
    
    cv2.imshow("Image",img)
    cv2.waitKey(1)