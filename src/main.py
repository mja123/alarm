import cv2
import os
import numpy as np
from decouple import config

RTSP_URL = config('VIDEO_URL')

# initialize the HOG descriptor/person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
# cap = cv2.VideoCapture(RTSP_URL, cv2.CAP_FFMPEG)
cap = cv2.VideoCapture("./../XVR_ch4_main_20230519021800_20230519022524 (online-video-cutter.com).mp4")
# cap = cv2.VideoCapture("./../XVR_ch4_main_20230526184600_20230526184700.asf")
if not cap.isOpened():
    print('Cannot open RTSP stream')
    exit(-1)

count = 1
while True:
    ret, frame = cap.read()
    # cv2.imshow('RTSP stream', frame)
    # resizing for faster detection
    frame = cv2.resize(frame, (640, 500))
    # using a greyscale picture, also for faster detection
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    # detect people in the image
    # returns the bounding boxes for the detected objects
    boxes, weights = hog.detectMultiScale(frame, winStride=(12, 12), padding=(8, 8), scale=1.1)

    boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])

    if boxes.size > 0:
        print(count)
        count += 1
        os.system("./../runAlarm.sh")

    for (xA, yA, xB, yB) in boxes:
        # display the detected boxes in the colour picture
        cv2.rectangle(frame, (xA, yA), (xB, yB),
                      (0, 255, 0), 2)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

if __name__ == '__main__':
    print('PyCharm')
