import cv2 as cv
import mediapipe as mp
import time


class HandDetection:
    def __init__(self,
                mode: bool = False,
                maxHands: int = 2,
                detectConfidence: float = 0.5,
                trackConfidence: float = 0.5):

        self.mode = mode
        self.maxHands = maxHands
        self.detectConfidence = detectConfidence
        self.trackConfidence = trackConfidence

        self.mpHands = mp.solutions.hands
        
        # Note: In newer mediapipe versions, named arguments are preferred
        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode, 
            max_num_hands=self.maxHands, 
            min_detection_confidence=self.detectConfidence, 
            min_tracking_confidence=self.trackConfidence
        )
        
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, frame, isDraw=True):
        frameRGB = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        results = self.hands.process(frameRGB)

        if results.multi_hand_landmarks and isDraw:
            for handLms in results.multi_hand_landmarks:
                self.mpDraw.draw_landmarks(
                    frame,
                    handLms,
                    self.mpHands.HAND_CONNECTIONS  # Fixed typo: mpHand -> mpHands
                )
                
        return frame


def main():
    cTime = 0
    pTime = 0  # Fixed typo: ptime -> pTime

    capture = cv.VideoCapture(0)
    handtraking = HandDetection()

    while True:
        loaded, frame = capture.read()
        if not loaded:
            break

        # Fixed call: using instance `handtraking` instead of class `HandDetection`
        frame = handtraking.findHands(frame)

        cTime = time.time()
        fps = f"FPS : {round(1 / (cTime - pTime))}" if (cTime - pTime) > 0 else "FPS : 0"
        pTime = cTime 
        
        cv.putText(frame, str(fps), (20, 50), cv.FONT_HERSHEY_PLAIN, 2, (60, 112, 206), 4)
        cv.imshow("Hand Tracking", frame)
        
        if cv.waitKey(20) & 0xFF == ord('q'):
            break

    capture.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    main()