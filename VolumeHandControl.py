import cv2 as cv
import time
import math
import numpy as np
import mediapipe as mp
from HandTrakingModule import HandDetection
from pycaw.pycaw import AudioUtilities

def set_windows_volume_scalar(scalar_value: float) -> None:
    try:
        device = AudioUtilities.GetSpeakers()
        volume = device.EndpointVolume

        # Clamp between 0.0 (0%) and 1.0 (100%)
        target_scalar = max(0.0, min(1.0, float(scalar_value)))

        # Set scalar volume directly matching Windows UI
        volume.SetMasterVolumeLevelScalar(target_scalar, None)

    except Exception as error:
        print(f"Failed to change volume: {error}")


wCam, hCam = 640, 480

capture = cv.VideoCapture(1)
capture.set(cv.CAP_PROP_FRAME_WIDTH, wCam)
capture.set(cv.CAP_PROP_FRAME_HEIGHT, hCam)

pTime = 0
handD = HandDetection(modelComplexity=0, detectConfidence=0.7, trackConfidence=0.7, maxHands=1)

while True:
    success, frame = capture.read()
    if not success:
        break

    flipedFrame = cv.flip(frame, 1)

    findHand = handD.findHands(flipedFrame)
    lmList = handD.findHandPos(flipedFrame)

    if lmList is not None and len(lmList) > 0:
        thumbTip = lmList[4]
        thumbX, thumbY = thumbTip[1], thumbTip[2]
        
        indexFingTip = lmList[8]
        indexX, indexY = indexFingTip[1], indexFingTip[2]

        cv.line(flipedFrame, (thumbX, thumbY), (indexX, indexY), (145, 188, 75), 5)

        cv.circle(flipedFrame, (thumbX, thumbY), 10, (65, 203, 203), -1)
        cv.circle(flipedFrame, (indexX, indexY), 10, (65, 203, 203), -1)
        
        xCoord, yCoord = int((thumbX + indexX) / 2), int((thumbY + indexY) / 2)
        cv.circle(flipedFrame, (xCoord, yCoord), 10, (65, 203, 203), -1)

        # Calculate distance between thumb and index finger
        lineLength = math.hypot(thumbX - indexX, thumbY - indexY)

        # 1. Map distance (20px to 200px) -> Percent (0 to 100) for display
        volPercent = int(np.interp(lineLength, [20, 200], [0, 100]))
        
        # 2. Map distance (20px to 200px) -> Scalar (0.0 to 1.0) for PyCAW
        volScalar = np.interp(lineLength, [20, 200], [0.0, 1.0])

        # Set Windows master volume
        set_windows_volume_scalar(volScalar)

        # Display percentage on screen
        cv.putText(flipedFrame, f"Volume : {volPercent} %", (400, 40), 
                    cv.FONT_HERSHEY_COMPLEX, 0.8, (65, 203, 203), 2)

        if volPercent < 15:
            cv.circle(flipedFrame, (xCoord, yCoord), 10, (0, 0, 255), -1)

    # FPS Calculation
    cTime = time.time()
    fps = int(1 / (cTime - pTime)) if (cTime - pTime) > 0 else 0
    pTime = cTime

    cv.putText(flipedFrame, f"FPS : {fps}", (10, 40), 
                cv.FONT_HERSHEY_COMPLEX, 1, (65, 203, 203), 2)
    
    cv.imshow("Volume Control", flipedFrame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv.destroyAllWindows()