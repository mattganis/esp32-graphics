import sys
import math
import time
import random
#

# The OLED screen ranges from (0,0) to (127,63)
# The center of the screen is (63,31)
#
#
#

if len(sys.argv) > 1:  # pass any paramter to run this on a host
    ESP = 0            #  vs running on the ESP32
else:
    ESP  = 1


if ESP:   # stuff specific to ESP32

 from machine import I2C, Pin
 import ssd1306


 rst = Pin(16, Pin.OUT)
 rst.value(1)
 scl = Pin(15, Pin.OUT, Pin.PULL_UP)
 sda = Pin(4, Pin.OUT, Pin.PULL_UP)
 i2c = I2C(scl=scl, sda=sda, freq=450000)
 oled = ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3c)

 oled.fill(0)

 
 def plot2(a,b):
  x = int(a)
  y = int(b)
  
  y2 = 63-y

  oled.pixel(x,y2,1)


 def line(x1,y1,x2,y2):
#
# Implementation of Bresenham's line algorithm 
#  (see: https://rosettacode.org/wiki/Bitmap/Bresenham%27s_line_algorithm)
#
# 
   deltax = abs(x2-x1)
   signx = -1
   if x1< x2:
      signx = 1

   deltay = abs(y2-y1)
   signy = -1
   if y1< y2:
       signy = 1

   er = 0-deltay 

   if deltax > deltay:
      er = deltax

   er = int(er/2)

   for _ in range(1000):   # plot up to 1000 points 
    plot2(x1,y1)           # just an easy way to loop

    if ((x1 == x2) & (y1 == y2)):
       return

    e2 = er

    if (e2 > (0-deltax)):
       er = er -  deltay
       x1 = x1 + signx
    
    if e2 < deltay:
       er = er + deltax
       y1 = y1 + signy 


#
# Main Swirl code.
#   Ported form the MTU Visible Memory Graphics Software Packege (K-1008)
#    see: http://mikenaberezny.com/wp-content/uploads/2018/03/mtu-k1008-grapics-software-package.pdf)
#
#

t = int( time.time() * 1000.0 )     # Seeds the random number gen.
random.seed( ((t & 0xff000000) >> 24) +
             ((t & 0x00ff0000) >>  8) +
             ((t & 0x0000ff00) <<  8) +
             ((t & 0x000000ff) << 24)   )

for _ in range(20):   # Just do 20 swirls

 sin = 0
 cos = .999
 maxX = 127
 maxY = 63
 x1 = 0 
 y1 = 0 


 freq = random.uniform(.9,.99999)
 damp = random.uniform(.9,.99999)
 lines = random.randint(0,50)


 for i in range(500):  # do a max of 500 points / swirl

  x2 = maxX/2 * sin + maxX/2
  y2 = maxY/2 * cos + maxY/2

  sin = (sin*damp)+cos*freq
  cos = cos - freq*sin

  if ESP:
   plot2(int(x2),int(y2))
   oled.show()
  
  if (abs(sin) <= .001 ):
    break


  deltax = abs(x1-x2)
  deltay = abs(y1-y2)
 

  if i>1:
    if ESP:
      if lines <= 25:
         line(int(x1),int(y1),int(x2),int(y2))
         oled.show()
    else:
      print ("(",int(x1),"),",int(y1),") -> (",int(x2),",",int(y2),")")
    
  x1 = x2
  y1 = y2 

 if ESP:
    oled.show()
    time.sleep(2)
    oled.fill(0)

