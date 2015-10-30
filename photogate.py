'''
expeyes-junior with photogate (ir emitter - detector)
Nikiforakis Manos (nikiforakis.m@gmail.com)

[connections] 
* od1 to VCC, 
* Collector of photodetector to in1(3) for single photogate, in2(4) for second photogate, 
* Ground to grd'''

import expeyes.eyesj, time, sys, os

from expeyes.press_any_key import *
from expeyes.console_colors import *

p=expeyes.eyesj.open()
if p == None: sys.exit()


'''The main loop for the program'''
while True:
	os.system('clear')
	print '''Photogate menu options:
	1. Time through each photogate (1 or 2 photogates)
	2. Picket fence mode (8 measures)
	3. Use 2 photogates to calculate the passing through time
	4. Pendulum mode (period calculation)
	5. Exit'''
	
	try:
		a= int(raw_input('Select 1-5:')) 
		if a in range(1,6):
			p.set_state(10,1) #give 5 V to VCC
			p.enable_set_high(10)
			os.system('clear')
			if a==1:
				print "***************************\n** Simple photogate mode **\n***************************"
				num =raw_input("How many photogates do you want to use [1/2]? ")
				while num<>'1' and num<>'2':
					num=raw_input("Only 1 or 2 are accepted as answers. Try again: ")
				key = PressAnyKey()
				if key==1:
					t=p.r2ftime(3,3) #in usec	
					txt= 'PHOTOGATE #1: The IR beam was interupted for: %f sec\n'%(t*10**(-6))
 					printout(txt, colour=YELLOW)
					if num=='2':
						t=p.r2ftime(4,4) #in usec	
						txt= 'PHOTOGATE #2: The IR beam was interupted for: %f sec\n'%(t*10**(-6))
 						printout(txt, colour=YELLOW)
			elif a==2:
				print "***************************\n**   Picket Fence mode   **\n***************************"
				key = PressAnyKey()
				if key==1:
					dat=['TIME(sec),VELOCITY(m/sec)\n']
					#strt = time.time()
					printout("TIME(sec)\tVELOCITY(m/sec)\n", colour=RED)
					#the following is needed to know when we are about to start measuring time 
					stop=False 
					while stop==False: 
						if p.get_state(3)==1: #first black strip
							stop=True						
					strt = time.time() 
					for k in range (8):
						t=p.r2ftime(3,3) #in usec
						et = time.time() -  strt
						txt= '%f\t%f\n'%(et-t*10**(-6)/2,0.026/(t*10**(-6)))
						printout(txt, colour=YELLOW)
						dat.append(txt.replace("\t",","))
					genpl = raw_input("Do you want to generate a v-t plot and calculate the trendline [yes/no]? ")
					while genpl<>'yes' and genpl<>'no' :
						genpl = raw_input( "only yes/no are accepted answers. Try again: ")	
					if genpl == 'yes':
						ta=[] #time values
						va=[] #velocity values
						for i in range (1, len(dat)):
							sd = dat[i].strip("\n").split(',')
							ta.append(float(sd[0]))
							va.append(float(sd[1]))	
						import matplotlib.pyplot as plt
						import numpy as np
						plt.xlabel('time t(sec)')
						plt.ylabel('velocity v(m/sec)')
						plt.plot(ta,va,'bo') # b for blue, o for filled circles
						# calc the trendline (it is simply a linear fitting)
						z = np.polyfit(ta, va, 1)
						pp = np.poly1d(z)
						plt.plot(ta,pp(ta),'r-', label='v=%3.2ft+%3.2f'%(z[0],z[1]))
						plt.legend(loc='upper right')
						plt.show()
					fs = raw_input("Do you want to save the data to a csv file [yes/no]? ")
					while fs<>'yes' and fs<>'no' :
						fs = raw_input( "only yes/no are accepted answers. Try again: ")	
					if fs=='yes':
						fname = raw_input("Give a filename or press enter for default [pfence.csv]:")
						if fname=="":
							fname = "pfence.csv"
						with open(fname, 'w') as f:
							for val in dat:
								f.write(val)
						print 'Data written in %s'%fname
			elif a==3:
				print "************************************************************\n** Use 2 photogates to calculate the passing through time **\n************************************************************"
				key = PressAnyKey()
				if key==1:
					t=p.r2rtime(3,4)
					txt =  'The passing through time was: %f sec\n'%(t*10**(-6))
					printout(txt, colour=YELLOW)
			elif a==4:
				print "****************************************\n** Pendulum mode (period calculation) **\n****************************************"
				key = PressAnyKey()
				if key==1:
					t=p.multi_r2rtime(3,1)
					txt =  'The period is: %f sec\n'%(t*10**(-6))
					printout(txt, colour=YELLOW)
			elif a==5:
				#break
				sys.exit()
			time.sleep(.5)			
			if key==1:
				raw_input("Press <enter> to return to main menu...")
		else:
			print 'This is not a valid input. Try again.'
			time.sleep(1)
	except ValueError:
			print 'This is not a valid input. Try again.'
			time.sleep(1)
	finally:
			p.set_state(10,0) #power off 
			p.enable_set_low(10)
sys.exit()

