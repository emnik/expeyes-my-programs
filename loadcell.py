'''
expeyes-junior with loadcell live data module
Nikiforakis Manos (nikiforakis.m@gmail.com)
[connections] 
* gnd to gnd, 
* echo to in1(3), 
* trig to sqr1(8) and 
* od1(10) to vcc of srf5'''

import numpy as np
from collections import deque
import matplotlib.pyplot as plt 
import matplotlib.animation as animation
import expeyes.eyesj, time, sys

p=expeyes.eyesj.open()
if p == None: sys.exit()

p.set_state(10,1) #give 5 V to VCC
p.enable_set_high(10)

time.sleep(0.1)
strt = time.time()

pause = False

# plot class
class AnalogPlot:
  # constr
  def __init__(self, maxLen):
      # open serial port
      #self.ser = serial.Serial(strPort, 9600)
      self.ax = deque([0.0]*maxLen)
      self.ay = deque([0.0]*maxLen)
      self.maxLen = maxLen
 
  # add to buffer
  def addToBuf(self, buf, val):
      if len(buf) < self.maxLen:
          buf.append(val)
      else:
          buf.pop()
          buf.appendleft(val)
 
  # add data
  def add(self, data):
      assert(len(data) == 2)
      self.addToBuf(self.ax, data[0])
      self.addToBuf(self.ay, data[1])
 
  # update plot
  def update(self, frameNum, a0, a1):
      try:
	  analogValue = p.get_voltage(3)
          #print analogValue
          load = (analogValue - 0.92) * (1892-0) / (1.68-0.92) + 0
          #print load
          line = "%.3f %i"%(time.time() - strt, load)
          data = [float(val) for val in line.split()]
          if not pause:
              print data
          if(len(data) == 2):
              self.add(data)
              a0.set_data(range(self.maxLen), self.ax)
              if not pause:
                  a1.set_data(range(self.maxLen), self.ay)
      except KeyboardInterrupt:
          print('exiting')
	  
      return a0,


  # clean up
  def close(self):
      # close serial
      p.set_state(10,0) #give 0 V to VCC
      p.enable_set_low(10)


def onClick(event):
     global pause
     pause ^= True
     if pause==True:
	print "Pause"

# main() function
def main():
 
  print('reading from analog port...')
 
  # plot parameters
  analogPlot = AnalogPlot(100)
 
  print('plotting data...')
 
  # set up animation
  fig = plt.figure()
  ax = plt.axes(xlim=(0, 100), ylim=(0, 5000))
  a0, = ax.plot([], [])
  a1, = ax.plot([], [])
  fig.canvas.mpl_connect('button_press_event', onClick)
  anim = animation.FuncAnimation(fig, analogPlot.update, 
                                 fargs=(a0, a1), 
                                 blit=False, interval=50, repeat=False)

  # show plot
  plt.show()
  
  # clean up
  analogPlot.close()
  print('exiting.')
  
 
# call main
if __name__ == '__main__':
  main()

