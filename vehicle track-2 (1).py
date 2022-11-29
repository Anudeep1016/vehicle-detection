import cv2 #to read the image
import dlib#to track the objects
import time# it allows work in  time 
import threading# it will do multipe task
import math# to calculate te speed 
import urllib.request# to get request from website
import numpy as np #to calculate the pixel
import requests # user give request to server
import time# it allows work in  time 
import os#interaction between user and operatin system 
import glob# used to return all file path 
import smtplib# used to send the mail 
import base64
##from email.mime.image import MIMEImage
##from email.mime.multipart import MIMEMultipart
##from email.mime.text import MIMEText
import sys
import pandas as pd# data analysis te data
from colorthief import ColorThief  # used to get te color information

carCascade = cv2.CascadeClassifier('myhaar.xml')#read the cascade file 
video = cv2.VideoCapture('input.mp4')#read the input file 
WIDTH = 1280
HEIGHT = 720
#Reading csv file with pandas and giving names to each column
index=["color","color_name","hex","R","G","B"]#color comparsion
csv = pd.read_csv('colors.csv', names=index, header=None)#read the color file

def getColorName(R,G,B):#apply color detection
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R- int(csv.loc[i,"R"])) + abs(G- int(csv.loc[i,"G"]))+ abs(B- int(csv.loc[i,"B"]))
        if(d<=minimum):
            minimum = d
            cname = csv.loc[i,"color_name"]
    return cname

def getrgb():#output color file come
        
                color_thief = ColorThief('out.png')
                dominant_color = color_thief.get_color(quality=1)
                
                
        

def estimateSpeed(location1, location2):#speed detetion 
	d_pixels = math.sqrt(math.pow(location2[0] - location1[0], 2) + math.pow(location2[1] - location1[1], 2))
	# ppm = location2[2] / carWidht
	ppm = 8.8
	d_meters = d_pixels / ppm
	#print("d_pixels=" + str(d_pixels), "d_meters=" + str(d_meters))
	fps = 18
	speed = d_meters * fps * 3.6
	return speed
	

def trackMultipleObjects():# veichle counting code
	rectangleColor = (0, 255, 0)
	frameCounter = 0
	currentCarID = 0
	fps = 0
	
	carTracker = {}
	carNumbers = {}
	carLocation1 = {}
	carLocation2 = {}
	speed = [None] * 1000
	
	# Write output to video file
	out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (WIDTH,HEIGHT))

        
	while True:
		start_time = time.time()
##		imgResp = urllib.request.urlopen(url)
##		imgNp = np.array(bytearray(imgResp.read()),dtype=np.uint8)
##		image = cv2.imdecode(imgNp,-1)
##		
		rc, image = video.read()
		
		
		if type(image) == type(None):
			break
		
		image = cv2.resize(image, (WIDTH, HEIGHT))
		resultImage = image.copy()
		
		frameCounter = frameCounter + 1
		
		#carIDtoDelete = []
		

		for carID in carTracker.keys():
			trackingQuality = carTracker[carID].update(image)
			
			
			
				
				
##		for carID in carIDtoDelete:
##			#print ('Removing carID ' + str(carID) + ' from list of trackers.')
##			#print ('Removing carID ' + str(carID) + ' previous location.')
##			#print ('Removing carID ' + str(carID) + ' current location.')
##			carTracker.pop(carID, None)
##			carLocation1.pop(carID, None)
##			carLocation2.pop(carID, None)
			
		
		if not (frameCounter % 10):#frame count detection
			gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
			cars = carCascade.detectMultiScale(gray, 1.1, 13, 18, (24, 24))
			
			
			for (_x, _y, _w, _h) in cars:
				x = int(_x)
				y = int(_y)
				w = int(_w)
				h = int(_h)
			
				x_bar = x + 0.5 * w
				y_bar = y + 0.5 * h
				
				matchCarID = None
				
			        
			
				for carID in carTracker.keys():
					trackedPosition = carTracker[carID].get_position()
					
					t_x = int(trackedPosition.left())
					t_y = int(trackedPosition.top())
					t_w = int(trackedPosition.width())
					t_h = int(trackedPosition.height())
					
					t_x_bar = t_x + 0.5 * t_w
					t_y_bar = t_y + 0.5 * t_h
					
				
					if ((t_x <= x_bar <= (t_x + t_w)) and (t_y <= y_bar <= (t_y + t_h)) and (x <= t_x_bar <= (x + w)) and (y <= t_y_bar <= (y + h))):
						matchCarID = carID
						
				
				if matchCarID is None:
					#print ('Creating new tracker ' + str(currentCarID))
                                        
					tracker = dlib.correlation_tracker()
					tracker.start_track(image, dlib.rectangle(x, y, x + w, y + h))
					
					carTracker[currentCarID] = tracker
					carLocation1[currentCarID] = [x, y, w, h]

					currentCarID = currentCarID + 1
					#print('number of cars entered',currentCarID)
		
		#cv2.line(resultImage,(0,480),(1280,480),(255,0,0),5)


		for carID in carTracker.keys():
			trackedPosition = carTracker[carID].get_position()
					
			t_x = int(trackedPosition.left())
			t_y = int(trackedPosition.top())
			t_w = int(trackedPosition.width())
			t_h = int(trackedPosition.height())
			
			color=cv2.rectangle(resultImage, (t_x, t_y), (t_x + t_w, t_y + t_h), rectangleColor, 4)
			cv2.putText(resultImage, 'number of cars entered: '+str(currentCarID),
                                                            (20,20),cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,0,255), 2)
			out=color[t_y : t_y + t_h,t_x:t_x+t_w]
			
			
			cv2.imwrite('out.png',out)
			
			
                        
					
			# speed estimation
			carLocation2[carID] = [t_x, t_y, t_w, t_h]
		
		end_time = time.time()
		
		if not (end_time == start_time):
			fps = 1.0/(end_time - start_time)
		
		#cv2.putText(resultImage, 'FPS: ' + str(int(fps)), (620, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)


		for i in carLocation1.keys():	
			if frameCounter % 1 == 0:
				[x1, y1, w1, h1] = carLocation1[i]
				[x2, y2, w2, h2] = carLocation2[i]
		
				# print 'previous location: ' + str(carLocation1[i]) + ', current location: ' + str(carLocation2[i])
				carLocation1[i] = [x2, y2, w2, h2]
		
				# print 'new previous location: ' + str(carLocation1[i])
				if [x1, y1, w1, h1] != [x2, y2, w2, h2]:
					if (speed[i] == None or speed[i] == 0) and y1 >= 275 and y1 <= 285:
						speed[i] = estimateSpeed([x1, y1, w1, h1], [x2, y2, w2, h2])
						

					#if y1 > 275 and y1 < 285:
					if speed[i] != None and y1 >= 180:
						cv2.putText(resultImage, str(int(speed[i])) + " km/hr",
                                                            (int(x1 + w1/2), int(y1-5)),cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)
						cv2.putText(resultImage, str(currentCarID),
                                                            (int(x1 + w1/4), int(y1-15)),cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,255,0), 2)
						if y1>=30:
							print('high speed detected')#high speed detecting
							
					
					#print ('CarID ' + str(i) + ': speed is ' + str("%.2f" % round(speed[i], 0)) + ' km/h.\n')

					#else:
					#	cv2.putText(resultImage, "Far Object", (int(x1 + w1/2), int(y1)),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

						#print ('CarID ' + str(i) + ' Location1: ' + str(carLocation1[i]) + ' Location2: ' + str(carLocation2[i]) + ' speed is ' + str("%.2f" % round(speed[i], 0)) + ' km/h.\n')
		cv2.imshow('result', resultImage)#result output come
		color_thief = ColorThief('out.png')#color output come
		dominant_color = color_thief.get_color(quality=1)
		r,g,b=dominant_color
			
		text = getColorName(b,g,r) 
		print('detected color',text)#print detected color output
		# Write the frame into the file 'output.avi'
		#out.write(resultImage)


		if cv2.waitKey(33) == 27:
			break
	
	cv2.destroyAllWindows()#close the program 

if __name__ == '__main__':
	trackMultipleObjects()
