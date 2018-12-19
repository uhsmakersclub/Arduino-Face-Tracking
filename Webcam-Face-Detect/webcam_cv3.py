import cv2
import sys
import logging as log
import datetime as dt
import time
from time import sleep
import serial

cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
log.basicConfig(filename='webcam.log',level=log.INFO)
ser = serial.Serial('/dev/ttyACM0', 9600) # change for different serial ports
video_capture = cv2.VideoCapture(0) # change for different webcams?
anterior = 0
size = (600,400)
centerX = size[0]/2
centerY = size[1]/2
unitX = centerX/10
unitY = centerY/10
prevprinted = time.time()

while True:
    if not video_capture.isOpened():
        print('Unable to load camera.')
        sleep(5)
        pass

    cv2.resizeWindow('Video', size[0], size[1])
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
	cx, cy = x+w/2, y+h/2
	moveX = str(abs(cx-centerX)//unitX)
	if moveX == '10':
		moveX = '9'
	moveY = str(abs(cy-centerY)//unitY)
	if moveY == '10':
		moveY = '9'
	
        # x y
	delay = 0.1
	if prevprinted+delay <= time.time():
		if cx > centerX and cy > centerY:
		    print("--"+moveX+moveY)
		    ser.write("--"+moveX+moveY+"\n")
		elif cx < centerX and cy > centerY:
		    print("+-"+moveX+moveY)
		    ser.write("+-"+moveX+moveY+"\n")
		elif cx > centerX and cy < centerY:
		    print("-+"+moveX+moveY)
		    ser.write("-+"+moveX+moveY+"\n")
		elif cx < centerX and cy < centerY:
		    print("++"+moveX+moveY)
		    ser.write("++"+moveX+moveY+"\n")
		prevprinted = time.time()
    	break

    if anterior != len(faces):
        anterior = len(faces)
        log.info("faces: "+str(len(faces))+" at "+str(dt.datetime.now()))


    # Display the resulting frame
    cv2.imshow('Video', frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
'''
    # Display the resulting frame
    cv2.imshow('Video', frame)
'''
# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
