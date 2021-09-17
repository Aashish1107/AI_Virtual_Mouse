import cv2
import time
import os
import HandTrackingMod as htm

cap=cv2.VideoCapture(0)
cap.set(3,720)
cap.set(4,480)

folderPath="Fingers"
myList=os.listdir(folderPath)
overlayList=[]

for imgPath in myList:
    image=cv2.imread(f'{folderPath}/{imgPath}')
    overlayList.append(image)


ptime=0
detector=htm.HandDetector(detectionCon=0.75)
while True:
    success, img=cap.read()
    img =detector.findHands(img)
    lmList=detector.findPosition(img, draw=False)

    if(len(lmList)!=0):
        fingers=[]
        
        #Left Hand Thumb
        if lmList[1][1]<lmList[0][1]:
            if lmList[4][1]<lmList[5][1]:
                fingers.append(1)
            else:
                fingers.append(0)
        #Right Hand Thumb
        else:
            if lmList[4][1]>lmList[5][1]:
                fingers.append(1)
            else:
                fingers.append(0)

        #Other 4 Fingers
        for i in range(2,6):
            if lmList[4*i][2]<lmList[4*i-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        
        h,w,c=overlayList[sum(fingers)].shape
        img[0:h, 0:w]=overlayList[sum(fingers)]

    ctime=time.time()
    fps=1/(ctime-ptime)
    ptime=ctime

    cv2.putText(img, f'FPS:{int(fps)}',(400,70),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),1)
    cv2.imshow("Image", img)
    cv2.waitKey(1)