import cv2
import numpy as np
import time
import HandTrackingMod as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


cap=cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

ptime=0

handDetector=htm.HandDetector(False, 1,0.88)


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()

#VolRange= -96 - 0 after testing
volRange=volume.GetVolumeRange()

minVol=volRange[0]
maxVol=volRange[1]

while True:
    success, img=cap.read()
    img=handDetector.findHands(img)
    lmList=handDetector.findPosition(img, draw=False)
    if len(lmList)!=0:
        #print(lmList[4],lmList[8])

        x1,y1=lmList[4][1],lmList[4][2]
        x2,y2=lmList[8][1],lmList[8][2]

        cv2.circle(img, (x1,y1), 7,(0,255,0) ,cv2.FILLED)
        cv2.circle(img, (x2,y2), 7,(0,255,0) ,cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(0,0,255),1)

        cx,cy=(x1+x2)//2,(y1+y2)//2
        cv2.circle(img, (cx,cy), 7,(0,255,0) ,cv2.FILLED)
        length=math.hypot(x2-x1, y2-y1)
        print(length)

        if length<10:
            length=10
            cv2.circle(img, (cx,cy), 7,(0,0,255) ,cv2.FILLED)

        #Length range 10-120
        perc=np.interp(length,[10,120],[0,100])
        vol=np.interp(length,[10,120],[minVol,maxVol])
        volume.SetMasterVolumeLevel(vol, None)
        bar=np.interp(vol,[minVol,maxVol],[400,150])
        

        cv2.rectangle(img,(50,150),(80,400),(0,0,255),2)
        cv2.rectangle(img,(50,int(bar)),(80,400),(0,0,255),cv2.FILLED)
        cv2.putText(img, f'{int(perc)}%',(40,140),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),1)

        

    ctime=time.time()
    fps=1/(ctime-ptime)
    ptime=ctime


    cv2.putText(img, f'FPS:{int(fps)}',(20,70),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),2)
    cv2.imshow("Image", img)
    cv2.waitKey(1)