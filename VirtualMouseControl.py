import cv2 as cv
import mediapipe as mp
import numpy
import math
from HandTrakingModule import HandDetection
import time
import pyautogui as gui

# Initialise Camere and Screen Size
capture = cv.VideoCapture(0)
    #My Screen -> (width=1366, height=768)
wCam, hCam = 800, 400
capture.set(cv.CAP_PROP_FRAME_WIDTH, wCam)
capture.set(cv.CAP_PROP_FRAME_HEIGHT, hCam)

# Initialise Hnad Detection
handD = HandDetection(maxHands = 1,
                        modelComplexity = 0,
                        detectConfidence = .6,
                        trackConfidence = .6)

cTime, pTime = 0,0
afterClick = 0
while True:
    isTrue, frame = capture.read()

    frame = cv.flip(frame, 1)

    # initialise Hand Traking
    handD.findHands(frame)
    lmList = handD.findHandPos(frame)

    if lmList != None:
        indexFinTip = lmList[8]
        x, y= indexFinTip[1], indexFinTip[2]

        # Curser Movement
        cv.circle(frame, (x,y), 10, (0, 255, 0), -1)
        gui.moveTo((x*2), (y*2))

        #Left Click
        thumbTip = lmList[4]
        xT, yT= thumbTip[1], thumbTip[2]
        middleFinTip = lmList[12]
        xM, yM= middleFinTip[1], middleFinTip[2]
        lenOfThumbAndMiddelTip = math.hypot(xT - xM, yT - yM)

        if lenOfThumbAndMiddelTip <= 15:
            gui.leftClick()

        # Right CLick
        Index_MCP = lmList[5]
        xMCP, yMCP = Index_MCP[1], Index_MCP[2]
        lenOfThumbAndMCP = math.hypot(xT- xMCP, yT-yMCP)

        if lenOfThumbAndMCP <= 20:
            gui.rightClick()
        



    # Calculate Frames Per second (FPS)
    cTime = time.time()
    fps = int(1/(cTime - pTime))
    pTime = cTime
    cv.putText(frame, f"FPS : {str(fps)}", (10,40), cv.FONT_HERSHEY_COMPLEX, 1, (0,0,0), 3)

    cv.imshow("Virtual Mouse Control", frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv.destroyAllWindows()
