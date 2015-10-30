'''
expeyes-junior -Tapping sensor
Nikiforakis Manos (nikiforakis.m@gmail.com)
'''

import expeyes.eyesj, time, sys, os

p=expeyes.eyesj.open()
if p == None: sys.exit()

threshold=0.03 #sensitivity (0.03 - 0.05 on a book)
sensorReading=0
counter=0

while True:
	sensorReading =  p.get_voltage(1) #for piezo + at A1
	#print sensorReading
	if abs(sensorReading)>=threshold:
		counter+=1
		print "Knock! %i"%(counter)
		#print sensorReading
	time.sleep(0.05)  
