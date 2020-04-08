import sys
import math
import random
import time

#
# Polar Plotting - Matt Ganis
#
#
# The OLED screen ranges from (0,0) to (127,63)
# The center of the screen is (63,31)
#
#
#

if len(sys.argv) > 1:
    ESP = 0
else:
    ESP  = 1 


if ESP:

 from machine import I2C, Pin
 import ssd1306


 rst = Pin(16, Pin.OUT)
 rst.value(1)
 scl = Pin(15, Pin.OUT, Pin.PULL_UP)
 sda = Pin(4, Pin.OUT, Pin.PULL_UP)
 i2c = I2C(scl=scl, sda=sda, freq=450000)
 oled = ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3c)

 oled.fill(0)

 def plot(x,y):
   oled.pixel(x+63,31-y,1)

t = int( time.time() * 1000.0 )     # Seeds the random number gen.
random.seed( ((t & 0xff000000) >> 24) +
             ((t & 0x00ff0000) >>  8) +
             ((t & 0x0000ff00) <<  8) +
             ((t & 0x000000ff) << 24)   )

for _ in range(0,20):  # do 20 polar plots with random leaves

 leaves = random.randint(2,20)
 for i in range(360):
   theta = 3.1415 * i/180
   r =   2 - 30 * math.cos(leaves * theta)

   x = r * math.cos(theta)  # convert polar to x,y
   x = round(x)
   y = r * math.sin(theta)
   y = round(y)

   if ESP:
      plot(x,y)
      oled.show()
   else:
       print ( "(",x,",",y,")" )

 time.sleep(1)
 if ESP:
    oled.fill(0)
 else:
    print ("-------------------")
