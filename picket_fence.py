'''
expeyes-junior with photogate (ir emitter - detector)
Nikiforakis Manos (nikiforakis.m@gmail.com)
[connections] 
* od1 to VCC, 
* Collector of photodetector to in1(3), 
* Ground to grd'''

import expeyes.eyesj, time, sys
p=expeyes.eyesj.open()
if p == None: sys.exit()


p.set_state(10,1) #give 5 V to VCC
p.enable_set_high(10)
strt = time.time()

for k in range (9):
	#p.enable_wait_rising(3)
	t=p.r2ftime(3,3) #in usec
	et = time.time() - strt
	print '%f sec, %f m/sec'%(et-t*10**(-6)/2,0.025/t*10**(6))

p.set_state(10,0) #give 5 V to VCC
p.enable_set_low(10)

