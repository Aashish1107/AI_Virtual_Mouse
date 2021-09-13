import cv2
import mediapipe as mp
import time

from mediapipe.python.solutions.drawing_styles import _THICKNESS_CONTOURS

cap=cv2.VideoCapture(r"C:\Users\Aashi\Downloads\t6.mp4")
ptime=0
ctime=0

mpDraw=mp.solutions.drawing_utils
mpFaceMesh=mp.solutions.face_mesh
faceMesh=mpFaceMesh.FaceMesh()

#DrawingSpec provides specifications while drawing landmarks
#DrawingSpec(color, thickness, circle_radius)
drawspecs=mpDraw.DrawingSpec((0,255,0),1,1)

while True:
    success, img = cap.read()
    imgRGB=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results=faceMesh.process(imgRGB)
    if results.multi_face_landmarks:
        for facelms in results.multi_face_landmarks:
            mpDraw.draw_landmarks(img, facelms ,mpFaceMesh.FACEMESH_CONTOURS,drawspecs,drawspecs)
    
    ctime=time.time()
    fps=1/(ctime-ptime)
    ptime=time.time()

    cv2.putText(img,"FPS:"+str(int(fps)),(20,70),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),1)

    cv2.imshow("FaceMesh",img)
    cv2,cv2.waitKey(1)