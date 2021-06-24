# ESP32 Graphing examples

Included are three examples of pixel based graphics for the ESP32 and OLED display (specifically I'm using 
the ESP32 from HELTEC - which has a built in OLED display).

Once the ESP32 is flashed with Micropython, you will need to upload the SSD1306.py library onto the board (note
this is a deprecated version of the library that I found on Adafruit)

## Game of Life
This is the classic cellular automata game of life by Conway.  

The universe of the Game of Life is an infinite, two-dimensional orthogonal grid of square cells, each of which 
is in one of # two possible states: alive or dead, (or populated and unpopulated). Every cell interacts with its eight 
neighbors, which are the cells that are horizontally, vertically, or diagonally adjacent. At each step in time, t
he following transitions occur:

   -  Any live cell with fewer than two live neighbours dies, as if by underpopulation.
   -  Any live cell with two or three live neighbours lives on to the next generation.
   -  Any live cell with more than three live neighbours dies, as if by overpopulation.
   -  Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
   
For this implementation, each graphic cell is made of up of a 3x3 pixel image - as a result the "universe" 
is 31 x 16 (or 496 cells)

To run life, you will need to upload the file `world.txt` which an ascii representation of the inital state
of the Universe.

To run the code, I use ampy `ampy --port /dev/tty.SLAB_USBtoUART run life.py`.  The code is configured to run just 20 
generations (feel free to modify it)

## Swirl

This is an implementation of a graphics program I saw years ago (does anybody remember the KIM-1 and MTU's 
Visible Memory board ?)

This generates 20 random swirl patterns.  Lines are randomly used between successive points for some interesting 
effects

to run it, again use ampy with: `ampy --port /dev/tty.SLAB_USBtoUART run sw.py`
(note the port is for my Mac - if you're using Windows or Linux it will be different)

## Polar

This plots 20 random polar equations based on:

`r =   2 - 30 * math.cos( *leaves* * theta)` where *theta* goes from 0 - 360 degrees and *leaves* is random 
between 2 and 20

o run it, again use ampy with: `ampy --port /dev/tty.SLAB_USBtoUART run polar.py`

## note4

ok, ok - it's not quite "music" but I had some fun with this one.  This play's "Ode to Joy" (Beethoven) but displays the score on the ESP's display.  Requires a piezo speaker attached to pin 13 


## Note:

All of the code is written so you it can be run on both the ESP32 and a laptop running python3.  If you run the 
code and specify any parameter the output will be dumped to a screen (versus no parameters which indicates
the code should be run on an ESP32 device) I called this *host mode* - note in *_host mode_* the graphics obviously don't work 

