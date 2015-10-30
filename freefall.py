'''
expeyes-junior - free fall aparatus
arm and release of an electromagnet and time the fall duration.
The end of the fall is aquired by a speaker used as a microfon that is amplified via 
expeyes junior
Nikiforakis Manos (nikiforakis.m@gmail.com)

[connections] 
* ...TODO
* Ground to grd'''

import expeyes.eyesj, time, sys, os

from expeyes.press_any_key import *
from expeyes.console_colors import *

p=expeyes.eyesj.open()
if p == None: sys.exit()

threshold=1

a=raw_input("Press ENTER to power on the electromagnet...")
p.set_state(10,1) #give 5 V to VCC
p.enable_set_high(10)
print "The electromagnet should be ON. Please add the weight. "  
time.sleep(1)
txt="When ready, press ENTER to release"
printout(txt, colour=RED)
raw_input()
p.set_state(10,0) #power off electromagnet 
p.enable_set_low(10) # RELEASE 
strt = time.time() #Start timer
while True:
	mic = p.get_voltage(1)
	if mic>threshold:
		et = time.time() - strt
		break
duration = et
rtxt="The free fall's duration was %.3f sec.\n"%duration
printout(rtxt, colour=YELLOW)




