import cv2
import time



vs = cv2.VideoCapture(0)
img = vs.read()[1]
time.sleep(1)

img = vs.read()[1]
cv2.imwrite("slender2.png", img)


exit(0)
