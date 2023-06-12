import cv2
import os
import time
import numpy as np
from decouple import config


class HumanDetection:
    def __init__(self, video, options=''):
        self.hog = cv2.HOGDescriptor()
        self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
        if options != '':
            self.cap = cv2.VideoCapture(video, options)
        else:
            self.cap = cv2.VideoCapture(video)
        self.duration = self._calculate_duration()

    def detection(self, winStride=(12, 12), padding=(8, 8), scale=1.1):
        count = 0
        start = time.time()

        while True:
            ret, frame = self.cap.read()
            if frame is None:
                break
            frame = cv2.resize(frame, (640, 500))
            boxes, weights = self.hog.detectMultiScale(frame, winStride=winStride, padding=padding, scale=scale)
            boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])

            if boxes.size > 0:
                print(count)
                count += 1
                # os.system("./runAlarm.sh")

            for (xA, yA, xB, yB) in boxes:
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
        return seconds


if __name__ == '__main__':
    # HumanDetection(config('VIDEO_URL'), cv2.CAP_FFMPEG).detection()
    HumanDetection('./XVR_ch4_main_20230519021800_20230519022524 (online-video-cutter.com).mp4').detection()
