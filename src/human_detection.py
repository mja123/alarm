from _datetime import datetime

import cv2
import os
from imutils.object_detection import non_max_suppression
from imutils import resize
from time import time
from numpy import array as np_array
from pyautogui import screenshot
from decouple import config


class HumanDetection:
    alarm_integration: bool

    def __init__(self, video, options=None, alarm_integration=False):
        self.hog = cv2.HOGDescriptor()
        self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
        if options is not None:
            self.cap = cv2.VideoCapture(video, options)
        else:
            self.cap = cv2.VideoCapture(video)
        self.duration = self._calculate_duration()
        self.alarm_integration = alarm_integration

    def detection(self, winStride=(7, 8), padding=(4, 4), scale=1.035):
        count = 0
        start = time()
        root_dir = os.path.dirname(os.path.abspath(__package__))

        while True:
            ret, frame = self.cap.read()
            if frame is None:
                break
            width = min(300, frame.shape[1])
            height = min(300, frame.shape[0])
            frame = resize(frame, width, height)
            boxes, weights = self.hog.detectMultiScale(frame, winStride=winStride, padding=padding, scale=scale)
            boxes = np_array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])

            if boxes.size > 0:
                image = screenshot(region=(0, 0, int(width * 1.5), int(height * 1.5)))
                image_name = str(datetime.now()).replace(" ", "-")
                image = cv2.cvtColor(np_array(image),
                                     cv2.COLOR_RGB2BGR)
                print(root_dir)
                cv2.imwrite(f"{root_dir}/resources/matches/{image_name}-{count}.png", image)
                count += 1
                if self.alarm_integration:
                    os.system(f"{root_dir}scripts/runAlarm.sh")

            pick = non_max_suppression(boxes, probs=None, overlapThresh=0.65)
            for (xA, yA, xB, yB) in pick:
                cv2.rectangle(frame, (xA, yA), (xB, yB),
                              (0, 255, 0), 2)

            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()

        return count, time() - start

    def _calculate_duration(self):
        frames = self.cap.get(cv2.CAP_PROP_FRAME_COUNT)
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        seconds = round(frames / fps)
        print(f"Duration {seconds}")
        return seconds


if __name__ == '__main__':
    HumanDetection(config('VIDEO_URL'), cv2.CAP_FFMPEG).detection()
