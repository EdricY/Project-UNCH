import math
import sys
import time
def printxy(y, x, text):
	sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (x, y, text))
	sys.stdout.flush()
def wipe():
	for y in range(1,26):
		printxy(1,y,"                                                            ")
def refresh():
	raw_input()
	wipe()
def clear():
	wipe()

for d in range(0,360):
	d = math.radians(d)
	printxy(21,11,math.cos(d))
	printxy(21,12,math.sin(d))
	printxy(math.floor(21 + 2*(10 * math.cos(d))),math.floor(11 -(10 * math.sin(d))),"X")
	time.sleep(0.05)
	clear()
