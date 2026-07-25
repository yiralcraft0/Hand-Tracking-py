import cv2 as cv
import numpy as np
import math
import time
import pyautogui as gui
import autopy
from HandTrakingModule import HandDetection

# Disable PyAutoGUI fail-safe pause for smoother motion
gui.PAUSE = 0

# Initialise Camera and Screen Size
capture = cv.VideoCapture(0)
wCam, hCam = 640, 480
capture.set(cv.CAP_PROP_FRAME_WIDTH, wCam)
capture.set(cv.CAP_PROP_FRAME_HEIGHT, hCam)

wS, hS = gui.size()
frameR = 100  # Frame reduction margin

clocX, clocY = 0, 0
plocX, pLocY = 0, 0
smooth = 5
dragging = False

# Click cooldown parameters for Right Click / Quick Clicks
last_click_time = 0
click_cooldown = 0.3  # seconds

# Initialise Hand Detection
handD = HandDetection(
    maxHands=1,
    modelComplexity=0,
    detectConfidence=0.6,
    trackConfidence=0.6
)

cTime, pTime = 0, 0

while True:
    isTrue, frame = capture.read()
    if not isTrue:
        break

    frame = cv.flip(frame, 1)

    # Initialise Hand Tracking
    handD.findHands(frame)
    lmList = handD.findHandPos(frame)
    finger = handD.fingersUp()

    # Draw active screen bounds box
    cv.rectangle(frame, (frameR, frameR), (wCam - frameR, hCam - frameR), (0, 0, 255), 2)

    # Make sure hand landmark list exists and is non-empty
    if lmList and len(finger) >= 3:
        indexFinTip = lmList[8]
        x, y = indexFinTip[1], indexFinTip[2]

        thumbTip = lmList[4]
        xT, yT = thumbTip[1], thumbTip[2]

        middleFinTip = lmList[12]
        xM, yM = middleFinTip[1], middleFinTip[2]

        # 1. Map & Clamp coordinates
        xS = np.interp(x, [frameR, wCam - frameR], [0, wS])
        yS = np.interp(y, [frameR, hCam - frameR], [0, hS])
        xS = int(np.clip(xS, 0, wS - 1))
        yS = int(np.clip(yS, 0, hS - 1))

        # Exponential moving average for smoothing
        clocX = plocX + (xS - plocX) / smooth
        clocY = pLocY + (yS - pLocY) / smooth

        curr_time = time.time()

        # MODE 1: Cursor Movement (Index UP, Middle DOWN)
        if finger[1] == 1 and finger[2] == 0:
            # If we were dragging, release the mouse button now
            if dragging:
                gui.mouseUp()
                dragging = False

            cv.circle(frame, (x, y), 10, (0, 255, 0), -1)
            autopy.mouse.move(clocX, clocY)
            plocX, pLocY = clocX, clocY

        # MODE 2: Left Click Hold & Drag (Index UP, Middle UP)
        elif finger[1] == 1 and finger[2] == 1:
            lenOfIndexTipAndMiddelTip = math.hypot(x - xM, y - yM)

            # Pinch detected: Hold down and move
            if lenOfIndexTipAndMiddelTip <= 35:
                cv.circle(frame, (x, y), 12, (0, 0, 255), -1)  # Red = Holding

                if not dragging:
                    gui.mouseDown()
                    dragging = True

                # Move cursor while maintaining the held click
                autopy.mouse.move(clocX, clocY)
                plocX, pLocY = clocX, clocY

            # Fingers opened up: Release the hold
            else:
                if dragging:
                    gui.mouseUp()
                    dragging = False

        # MODE 3: Right Click (Thumb & Middle finger pinch)
        lenOfThumbAndMiddleTip = math.hypot(xT - xM, yT - yM)
        if lenOfThumbAndMiddleTip <= 35:
            cv.circle(frame, (xT, yT), 10, (255, 0, 0), -1)
            if curr_time - last_click_time > click_cooldown:
                gui.rightClick()
                last_click_time = curr_time

    # FPS Calculation
    cTime = time.time()
    fps = int(1 / (cTime - pTime)) if (cTime - pTime) > 0 else 0
    pTime = cTime
    cv.putText(frame, f"FPS: {fps}", (10, 40), cv.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)

    cv.imshow("Virtual Mouse Control", frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        # Safety check: release mouse if program exits while dragging
        if dragging:
            gui.mouseUp()
        break

capture.release()
cv.destroyAllWindows()