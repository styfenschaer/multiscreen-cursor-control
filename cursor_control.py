import cv2
import pyautogui
import time


""" Settings """
center_screen1 = (3440/2, 1440+1440/2)  # Center of screen 2
center_screen2 = (2560/2, 1440/2)  # Center of screen 1 
#print(pyautogui.position())  # check current position of cursor 

face_height = 185  # height of face
dist_init = 0.65  # distance at which height of face equals face_height
dist_lim = 0.55  # distance at which cursor switches from screen 1 to screen 2

show = True  # show webcam recording
sleep = 0.0  # time asleep after each iteration

""" Init webcam and face detection """
cv = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_profileface.xml')


""" Run script and release all resources and close windows when script gets aborted """
try:
	dist = dist_lim
	position = 0
	while True:
		_, frame = cv.read()

		# Set colorspace and detect face
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		face = face_cascade.detectMultiScale(gray, 1.1, 5)
		
		# Find face
		try:
			# Calculate distance to webcam
			x, y, w, h = face[0]
			dist = face_height / h * dist_init

			# Show webcam image if show == True
			if show:
				cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 129), 2)
				label = 'Distance: {:.2f}'.format(dist)
				cv2.putText(frame, label,
						(frame.shape[1]-200, frame.shape[0]-20), 
						cv2.FONT_ITALIC, 0.8, (255, 255, 255), 2)
				cv2.imshow('frame', frame)
		except:
			pass

		# Switch to screen 1 if distance is > dist_lim and coursor is on screen 2
		if dist > dist_lim and position != 0:
			pyautogui.moveTo(x=center_screen1[0], y=center_screen1[1], duration=0)
			position = 0
		# Switch to screen 2 if distance is < dist_lim and coursor is on screen 1
		elif dist < dist_lim and position != 1:
			pyautogui.moveTo(x=center_screen2[0], y=center_screen2[1], duration=0)
			position = 1
		
		# Exit with ESC
		if cv2.waitKey(20) == 27: 
			break

		# Pause
		time.sleep(sleep)

finally:
	# Release all software and hardware and close all windows
	cv.release()
	cv2.destroyAllWindows()


