import cv2
import time
import os
import numpy as np
import HandTrackingMod as htm

folderpath="Canva"
myList=os.listdir(folderpath)
overlayList=[]
for path in myList:
    image=cv2.imread(f'{folderpath}/{path}')
    overlayList.append(image)

header=overlayList[0]
colour=(0,0,255)
r=10

cap=cv2.VideoCapture(0)
ptime=0
detector=htm.HandDetector(detectionCon=0.75)
xp,yp=0,0
imgCanvas=np.zeros((480,720,3),np.uint8)


while True:
    #Image capture and setup
    success, img=cap.read()
    img=cv2.flip(img,1)
    img=cv2.resize(img,(720,480))
    
    
    #Find Hand Landmarks
    img=detector.findHands(img)
    lmList=detector.findPosition(img,False)
    

    if len(lmList)!=0:
        
        x1,y1=lmList[8][1:]
        x2,y2=lmList[12][1:]


        #Check Condition
        fingers=detector.fingersUP()
    

        #if Selection Mode
        if fingers[1] and fingers[2]:
            cv2.rectangle(img,(x1,y1-20),(x2,y2+20),(255,0,255),cv2.FILLED)

            if y1<110:
                if 140<x1<280:
                    header= overlayList[0]
                    colour=(0,0,255)
                    r=10
                elif 280<x1<420:
                    header= overlayList[1]
                    colour=(255,0,0)
                    r=10
                elif 420<x1<560:
                    header= overlayList[2]
                    colour=(0,255,0)
                    r=10
                elif 560<x1<720:
                    header= overlayList[3]
                    colour=(0,0,0)
                    r=25

        #if Drawing Mode
        if fingers[1] and fingers[2]==0:
            xp,yp=0,0
            cv2.circle(img,(x1,y1),r,colour,cv2.FILLED)
            if xp==0 and yp==0:
                xp,yp=x1,y1
            
            cv2.line(img,(xp,yp),(x1,y1),colour, r)
            cv2.line(imgCanvas,(xp,yp),(x1,y1),colour, r)

            xp,yp=x1,y1

    #FPS
    ctime=time.time()
    fps=1/(ctime-ptime)
    ptime=ctime

    cv2.putText(img,f'{int(fps)}',(20,120),cv2.FONT_HERSHEY_PLAIN,1,(255,0,0),1)
    
    #to remove the fade when using cv2.addthreshold()
    #we convert canvas to a gray image,
    #inverse it,so BG is white(max) (which ensures white wont be copied to img), and add it to img
    #bitwise or is used to add color from canvas to img

    imgGray=cv2.cvtColor(imgCanvas,cv2.COLOR_BGR2GRAY)
    _,imgInv=cv2.threshold(imgGray, 50,255,cv2.THRESH_BINARY_INV)
    imgInv=cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    img=cv2.bitwise_and(img, imgInv)
    img=cv2.bitwise_or(img, imgCanvas)
    
    img[0:110, 0:720]=header
    cv2.imshow("Img",img)
    cv2.waitKey(1)