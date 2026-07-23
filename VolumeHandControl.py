import cv2 as cv
import time
import mediapipe as mp
from HandTrakingModule import HandDetection
import math
from pycaw.pycaw import AudioUtilities
import numpy as np

def set_windows_volume_db(db_value: float) -> None:
    try:
        # Get the default Windows output device
        device = AudioUtilities.GetSpeakers()

        # Access its volume controller
        volume = device.EndpointVolume

        # Get supported decibel range
        min_db, max_db, step_db = volume.GetVolumeRange()

        # Keep the requested value inside the supported range
        target_db = max(min_db, min(max_db, float(db_value)))

        # Set the volume
        volume.SetMasterVolumeLevel(target_db, None)

        # print(f"Device: {device.FriendlyName}")
        # print(f"Volume range: {min_db:.2f} dB to {max_db:.2f} dB")
        # print(f"Master volume changed to: {target_db:.2f} dB")

    except Exception as error:
        print(f"Failed to change volume: {error}")


wCam, hCam = 640, 480

capture = cv.VideoCapture(1)

capture.set(cv.CAP_PROP_FRAME_WIDTH, 640)
capture.set(cv.CAP_PROP_FRAME_HEIGHT, 480)

pTime, cTime = 0, 0

handD = HandDetection(modelComplexity=0, detectConfidence= 0.7, trackConfidence=0.7, maxHands= 1)


while True:
    sucess , frame = capture.read()

    findHand = handD.findHands(frame)

    lmList = handD.findHandPos(frame)

    if lmList != None:
        thumbTip = lmList[4]
        thumbX, thumbY = thumbTip[1], thumbTip[2]
        indexFingTip = lmList[8]
        indexX, indexY = indexFingTip[1], indexFingTip[2]

        cv.line(frame, (thumbX, thumbY), (indexX, indexY), (145, 188, 75), 5)

        first = math.pow((thumbX - indexX), 2)
        second = math.pow((thumbY - indexY), 2)

        cv.circle(frame, (thumbX, thumbY), 10, (65, 203, 203), -1)
        cv.circle(frame, (indexX, indexY), 10, (65, 203, 203), -1)
        xCoord , yCoord = int((thumbX + indexX)/2) , int((thumbY + indexY)/2)
        cv.circle(frame, (xCoord, yCoord), 10, (65, 203, 203), -1 )

        length = int(math.sqrt(first + second))
        cv.putText(frame, str(f"Length : {length} pixel"), (400,40), cv.FONT_HERSHEY_COMPLEX, .8, (65, 203, 203), 2)

        volume = np.interp(length, [40, 150], [-96.0, 0.0])
        set_windows_volume_db(volume)
        if length < 40:
            cv.circle(frame, (xCoord, yCoord), 10, (0,255,0), -1 )


    cTime = time.time()
    fps = int(1/ (cTime - pTime))
    pTime = cTime

    cv.putText(frame, str(f"FPS : {fps}"), (10,40), cv.FONT_HERSHEY_COMPLEX, 1, (65, 203, 203), 2)
    cv.imshow("Volume Control", frame)

    if cv.waitKey(1) & 0xFF == ord('q') :
        break

capture.release()
cv.destroyAllWindows()