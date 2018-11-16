import numpy as np
import cv2
from pyzbar.pyzbar import decode

cap = cv2.VideoCapture(0)
code = []

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    code = decode(gray)
    if len(code) != 0:
        print("code = ", code)
    # Display the resulting frame
    cv2.imshow('frame',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()