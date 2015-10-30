'''
expeyes-junior with loadcell live data module
Nikiforakis Manos (nikiforakis.m@gmail.com)
[connections] 
* gnd to gnd, 
* 10th pin of IC to in1(3), 
* od1(10) to vcc'''

import numpy as np
import expeyes.eyesj, time, sys
time.sleep(0.1)
loop = True
p=expeyes.eyesj.open()
if p == None: sys.exit()

p.set_state(10,1) #give 5 V to VCC
p.enable_set_high(10)
print "wait while resetting zero value..."
t1,reset = p.capture(3,500,20)
zeroval = np.mean(reset)
p.set_state(10,0) #give 0 V to VCC
p.enable_set_low(10)
time.sleep(2)
print "weighing scale is zeroed!"
while loop:
	try:	
		print "-"*40
		a=raw_input("Press: \n* ENTER to weight a load \n* A number for multiple measurements\n* Ctrl+C to exit.\n Your choise: ")
		print "-"*40		
		if a.isdigit():
			repeat = int(a)
		else:
			repeat = 1
		for i in range(0, repeat):		
			p.set_state(10,1) #give 5 V to VCC
			p.enable_set_high(10)
			t2,data = p.capture(3,500,20)
			analogValue = np.mean(data)
			differ = 0.92-zeroval 
			load = (analogValue - zeroval) * (1892+differ-0) / (1.68-0.92) + 0
			print "%i gr" %load
			p.set_state(10,0) #give 0 V to VCC
			p.enable_set_low(10)
			time.sleep(1)
	except KeyboardInterrupt:		
		print '\nexiting...'
		break
	finally:
		p.set_state(10,0) #give 0 V to VCC
		p.enable_set_low(10)

