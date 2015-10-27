import sys
import time
def printxy(x, y, text):
     sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (x, y, text))
     sys.stdout.flush()
def refresh():
	raw_input()
	print(chr(27) + "[2J")
	
for d in range(0,360)
	printxy(math.floor(10 + (11 * math.cos(d))),math.floor(10 - (11 * math.sin(d))),"X")
	refresh()
	time.sleep(0.1)