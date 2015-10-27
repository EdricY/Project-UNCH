import sys
import time
import math
def printxy(x, y, text):
     sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (x, y, text))
     sys.stdout.flush()
def refresh():
	raw_input()
	print(chr(27) + "[2J")
def clear():
	print(chr(27) + "[2J")
	
for d in range(0,360):
	d = math.radians(d)
	printxy(math.floor(11 + (10 * math.cos(d))),math.floor(21 - ((10 * math.sin(d))* 2)),"X")
	printxy(math.floor(11,21,"0")
	clear()
	time.sleep(0.1)