'''
expeyes-junior with hy-srf05 ultrasound sensor module
Nikiforakis Manos (nikiforakis.m@gmail.com)
[connections] 
* gnd to gnd, 
* echo to in1(3), 
* trig to sqr1(8) and 
* od1(10) to vcc of srf5'''

import expeyes.eyesj, time, sys
p=expeyes.eyesj.open()
if p == None: sys.exit()
#f = open('srf.dat','w')
vs = 0.0340 #sound velocity 340m/s = (340/10-2)*10-6=340*10-4=0.0340cm/usec
p.set_state(10,1) #give 5 V to VCC
p.enable_set_high(10)
time.sleep(0.1)
strt = time.time()
ta = []
da = []
et =0
#set trigger with f=40Hz as the maximum echo time is 25ms (see srf05 datasheet)
#p.set_pulsewidth(10)
p.set_sqr1(40)	
while et < 90: # get data for 3 seconds
	#wait trigger to go high	
	p.enable_wait_high(6)
	#wait echo to go high	
	p.enable_wait_high(3)
	#measure the time between high and low of sensors' echo (in1(3))
	t=p.r2ftime(3,3) #in usec
	#calculate the distance	
	s = t*vs/2 #in cm
	#print t
	print 'Reflector at %3.1f cm'%s
	ta.append(et)
	da.append(s)
	#f.write('%s,%3.2f\n'%(et,s))
	et = time.time() - strt
#from pylab import *
#plot(ta,da)
#show()
p.set_state(10,0) #0V to VCC

