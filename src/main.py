import math
import sys
import time
import subprocess
def printxy(y, x, text):
	sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (x, y, text))
	sys.stdout.flush()
def wipe():
	for y in range(1,26):
		printxy(1,y,"                                                            ")
def refresh():
	raw_input()
	wipe()
def writesave():
	x=1
def readsave():
	x=1
def update():
	x=1
def draw():
	x=1
#game loop
FRAMES_PER_SECOND = 1
game_running = True
while game_running:
	startTime=time.time()
	update()
	draw()
	endTime=time.time()
	timeElapsed=endTime-startTime
	sleepTime=1/FRAMES_PER_SECOND-timeElapsed
	time.sleep(sleepTime)
