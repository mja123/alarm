import cv2
import os
from imutils.object_detection import non_max_suppression
from imutils import resize
import time
import numpy as np
import pyautogui
from decouple import config


class HumanDetection:
    alarm_integration: bool

    def __init__(self, video, options='', alarm_integration=False):
        self.hog = cv2.HOGDescriptor()
        self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
        if options != '':
            self.cap = cv2.VideoCapture(video, options)
        else:
            self.cap = cv2.VideoCapture(video)
        self.duration = self._calculate_duration()
        self.alarm_integration = alarm_integration

    def detection(self, winStride=(7, 8), padding=(4, 4), scale=1.035):
        count = 0
        start = time.time()
        while True:
            ret, frame = self.cap.read()
            if frame is None:
                break
            frame = resize(frame, width=min(300, frame.shape[1]))
            boxes, weights = self.hog.detectMultiScale(frame, winStride=winStride, padding=padding, scale=scale)
            boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])

            if boxes.size > 0:
                image = pyautogui.screenshot()
                image = cv2.cvtColor(np.array(image),
                                     cv2.COLOR_RGB2BGR)
                cv2.imwrite(f"image{count}.png", image)
                print(count)
                count += 1
                if self.alarm_integration:
                    os.system("./../scripts/runAlarm.sh")

            pick = non_max_suppression(boxes, probs=None, overlapThresh=0.65)
            for (xA, yA, xB, yB) in pick:
                cv2.rectangle(frame, (xA, yA), (xB, yB),
                              (0, 255, 0), 2)

            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()

        return count, time.time() - start

    def _calculate_duration(self):
        frames = self.cap.get(cv2.CAP_PROP_FRAME_COUNT)
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        seconds = round(frames / fps)
        print(f"Duration {seconds}")
        return seconds


if __name__ == '__main__':
    HumanDetection(config('VIDEO_URL'), cv2.CAP_FFMPEG).detection()
