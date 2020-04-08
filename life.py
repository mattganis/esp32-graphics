import sys


#
# Conway's Game of Life implemented on a HELTEC ESP32 with OLED display
#
#  04/03/20 - Initial Release - Matt Ganis (mganis@pace.edu)
#
#

if len(sys.argv) > 1:
    ESP = 0
else:
    ESP  = 1 


if ESP:

 from machine import I2C, Pin
 import ssd1306
 import time


 rst = Pin(16, Pin.OUT)
 rst.value(1)
 scl = Pin(15, Pin.OUT, Pin.PULL_UP)
 sda = Pin(4, Pin.OUT, Pin.PULL_UP)
 i2c = I2C(scl=scl, sda=sda, freq=450000)
 oled = ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3c)

 oled.fill(0)


 def trans(x,y,draw=1,type=1):
  #
  # draw: 1 means turnon pixels, 0 is off (erase)
  # type: 1 will draw a square any other number produces a diamond
  #
  x2 = (x*4)+1
  y2 = (y*4)+1

  oled.pixel(x2,y2-1,draw)

  if type == 1:
   oled.pixel(x2-1,y2-1,draw)
   oled.pixel(x2+1,y2-1,draw)

  oled.pixel(x2,y2+1,draw)

  if type == 1:
   oled.pixel(x2-1,y2+1,draw)
   oled.pixel(x2+1,y2+1,draw)

  oled.pixel(x2-1,y2,draw)
  oled.pixel(x2+1,y2,draw)




 def display_world(version):

  global maxX,maxY

  if version == 1:
   for i in range(maxY):
    for j in range(maxX):
      # screen2[i][j]=0
      if screen[j][i] == 1:
        trans(j,i,1)
        # oled.pixel(j,i,1);
      else:
        trans(j,i,0)
        # oled.pixel(j,i,0)

  oled.show()

#
# end of the ESP-only micropython code
#

import time
class Matrix(object):
    def __init__(self, rows, columns, default=0):
        self.m = []
        for i in range(rows):
            self.m.append([default for j in range(columns)])

    def __getitem__(self, index):
        return self.m[index]

maxX = 31  # ranges from 0 to 30 
maxY = 16  # ranges from 0 to 15

screen  = Matrix(maxX,maxY)
screen2 = Matrix(maxX,maxY)

f = open("world.txt")
f.readline().rstrip()    # throw away first line

for i in range(maxY):
 line = f.readline().rstrip()
 if line == '':
        for j in range(maxY):
         screen[j][i] = 0
        #  outline = outline+ "0"
        # print outline
        # print str(i)+("(0):blank")
 else:
    x = 0 
    for char in line:
      if char == "*":
        screen[x][i] = 1
      else:
        screen[x][i] = 0
      x=x+1

    for _ in range(maxX-len(line)):
      screen[x][i] = 0
      x = x+1

#########################################
#
#
# Neighbor() will count the number of neighbors a cell has 
#            

def neighbor(x,y):

 global maxX, maxY
 edgex = maxX - 1
 edgey = maxY - 1
 count = 0

 #check left #1

 tempx = x-1
 tempy = y

 if tempx < 0:
   tempx = edgex

 count = count + screen[tempx][tempy]

 # check right #2 

 tempx = x+1
 tempy = y

 if tempx>edgex:
   tempx = 0

 count = count + screen[tempx][tempy]

 # check up  #3 

 tempx = x
 tempy = y - 1

 if tempy < 0:
  tempy = edgey

 count = count + screen[tempx][tempy]

 # check upper-left #4

 tempx = x - 1
 tempy = y - 1

 if tempx < 0:
  tempx = edgex

 if tempy < 0:
  tempy = edgey

 count = count + screen[tempx][tempy]

 # check upper right #5 

 tempx = x + 1
 tempy = y - 1

 if tempx > edgex:
   tempx = 0

 if tempy < 0:
   tempy = edgey

 count = count + screen[tempx][tempy]

 # lower left #6

 tempx = x - 1
 tempy = y + 1

 if tempx < 0:
   tempx = edgex

 if tempy > edgey:
   tempy = 0

 count = count + screen[tempx][tempy]

 # underneath #7

 tempx = x
 tempy = y + 1

 if tempy > edgey:
   tempy = 0

 count = count + screen[tempx][tempy]

 # lower right #8

 tempx = x + 1
 tempy = y + 1

 if tempx > edgex:
   tempx = 0

 if tempy > edgey:
   tempy = 0

 count = count + screen[tempx][tempy]

 return(count) 


#
# printworld - is not used on the ESP version - this is for debugging 
#              on a host system
#
#

def printworld(which):
 if which==1:
  for i in range(maxY):
    line = ""
    for j in range(maxX):
       if screen[j][i] == 1:
         line = line+"x"
       else:
         line = line + " "
    print (line)
 else:
  for i in range(maxY):
    line = ""
    for j in range(maxX):
       if screen2[j][i] == 1:
         line = line+"1"
       else:
         line = line + "0"
    print (line)




def iteration():
 global screen
 global screen2
 global maxY,MaxX

 for i in range(maxY):
  for j in range(maxX):
    x = neighbor(j,i)
    if ((screen[j][i] == 0) & (x == 3)):
       screen2[j][i] = 1
    elif ( (screen[j][i] == 1) & ((x <= 1) | (x>=4)) ):
         screen2[j][i] = 0
    elif ((screen[j][i]==1) & ((x == 2) | (x == 3))):
         screen2[j][i] = 1

def copy():
  for i in range(maxY):
   for j in range(maxX):
    screen[j][i] = screen2[j][i]
    screen2[j][i] = 0


if ESP:

 for looper in range(30):     # run 30 iterations on esp
  display_world(1)
  iteration() # creates screen2[][]
  copy()
else:
   for looper in range(30):   # run 30 iterations on a host (non-esp)
      printworld(1) 
      iteration()
      copy()
      print ("--------------------------")
