import cv2
import sys
import logging as log
import datetime as dt
import time
from time import sleep
import serial

cascPath = "haarcascade_frontalface_default.xml" #'haarcascade_frontalface_alt.xml'
faceCascade = cv2.CascadeClassifier(cascPath)
log.basicConfig(filename='webcam.log',level=log.INFO)
ser = serial.Serial('/dev/ttyACM0', 9600) # change for different serial ports
video_capture = cv2.VideoCapture(0) # change for different webcams?
anterior = 0

size = (640,480)
centerX, centerY = size[0]/2, size[1]/2
unitX, unitY = centerX/10, centerY/10
moveX, moveY = None, None

minFaceSize = 30
maxFaceSize = min(size)
faceUnit = (maxFaceSize-minFaceSize)/10

prevprinted = time.time()
delay = 0.05

cv2.namedWindow('Video', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Video', size[0], size[1])

while True:
	if not video_capture.isOpened():
		print('Unable to load camera.')
		sleep(5)
		pass
	
	# Capture frame-by-frame
	ret, frame = video_capture.read()

	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	faces = faceCascade.detectMultiScale(
		gray,
		scaleFactor=1.2,
		minNeighbors=5,
		minSize=(minFaceSize, minFaceSize)
	)

	if len(faces) > 0:
		(x,y,w,h) = faces[0]
		cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
		cx, cy = x+w/2, y+h/2 #center coordinates of face

		moveX = str(int(abs(cx-centerX)//unitX))
		if int(moveX) >= 10:
			moveX = '9'

		moveY = str(int(abs(cy-centerY)//unitY))
		if int(moveY) >= 10:
			moveY = '9'
		
		faceSize = str(int((w-minFaceSize)//faceUnit))
		if int(faceSize) >= 10:
			faceSize = '9'
		
		#sends information in format "x direction, y direction, x movement amount, y movement amount, face size"
		if prevprinted+delay <= time.time():
			if cx > centerX and cy > centerY:
				print("--"+moveX+moveY+faceSize)
				ser.write(bytes("--"+moveX+moveY+faceSize+"\n",'utf-8'))
			elif cx < centerX and cy > centerY:
				print("+-"+moveX+moveY+faceSize)
				ser.write(bytes("+-"+moveX+moveY+faceSize+"\n",'utf-8'))
			elif cx > centerX and cy < centerY:
				print("-+"+moveX+moveY+faceSize)
				ser.write(bytes("-+"+moveX+moveY+faceSize+"\n",'utf-8'))
			elif cx < centerX and cy < centerY:
				print("++"+moveX+moveY+faceSize)
				ser.write(bytes("++"+moveX+moveY+faceSize+"\n",'utf-8'))
			prevprinted = time.time()
	
		if moveX == '0' and moveY == '0':
			#print(cx,cy)
			cv2.putText(frame,'Target Acquired!',(10,30),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255))
	
	if anterior != len(faces):
		anterior = len(faces)
		log.info("faces: "+str(len(faces))+" at "+str(dt.datetime.now()))

	# Display the resulting frame
	cv2.imshow('Video', frame)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

'''
# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
'''
