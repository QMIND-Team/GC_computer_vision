import cv2
import numpy as np


cap = cv2.VideoCapture(0)

while(True):

	#returns retvalue (did it read a frame) and image
	ret, frame = cap.read()

	#ops on frame
	#gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	cv2.imshow('frame',frame)
	if cv2.waitKey(1) & 0xFF  == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()
