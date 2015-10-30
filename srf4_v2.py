'''
expeyes-junior with HY-SRF05 ultrasound sensor module
Nikiforakis Manos (nikiforakis.m@gmail.com)
[connections] 
* gnd to gnd, 
* echo to in1(3), 
* trig to sqr1(8) and 
* od1(10) to vcc of srf5'''

import expeyes.eyesj, time, sys
p=expeyes.eyesj.open()
if p == None: sys.exit()

f1 = open('srf.dat','w')
f2 = open('srfv.dat','w')

vs = 0.0340 #sound velocity 340m/s = (340/10-2)*10-6=340*10-4=0.0340cm/usec
p.set_state(10,1) #give 5 V to VCC
p.enable_set_high(10)
#p.set_voltage(5)
time.sleep(0.1)
strt = time.time()
ta = []
da = []
et =0
#set trigger with f=40Hz as the maximum echo time is 25ms (see srf05 datasheet)
#p.set_pulsewidth(10)
p.set_sqr1(40)	
while et < 3: # get data for 3 seconds
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
	f1.write('%1.4f,%3.1f\n'%(et,s))
	et = time.time() - strt
#p.set_state(10,0) #0V to VCC

#-------------PROCCESSING DATA--------------
import matplotlib.pyplot as plt
import numpy as np

plt.subplot(2,1,1)
plt.xlabel('time t(sec)')
plt.ylabel('position x(cm)')
plt.plot(ta,da,'-k') # - for solid, k for black
#plt.show()

#calculate velocity over time
tb = []
vb = []
for i in range(len(da)-1):
	tb_v = ta[i]+(ta[i+1] - ta[i])/2
	vb_v = (da[i+1] - da[i])/(ta[i+1] - ta[i])	
	tb.append(tb_v)
	vb.append(vb_v)
	f2.write('%1.4f,%3.2f\n'%(tb_v,vb_v))
plt.subplot(2,1,2)
plt.xlabel('time t(sec)')
plt.ylabel('velocity v(cm/sec)')
plt.plot(tb,vb,'bo') # b for blue, o for filled circles

# calc the trendline (it is simply a linear fitting)
z = np.polyfit(tb, vb, 1)
p = np.poly1d(z)
plt.plot(tb,p(tb),'r-', label='v=%3.1ft+(%3.1f)'%(z[0]/100,z[1]/100))
plt.legend(loc='upper right')
plt.show()
