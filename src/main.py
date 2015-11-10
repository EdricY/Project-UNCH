import math
import sys
import time
import os
import glob

os.system('clear')
FRAMES_PER_SECOND = 1
game_running = True

mobfiles = glob.glob("../resources/mobs/*.txt")
ifile=0
mobs=[]
for i in mobfiles:
	mobs.append([])
	f=open(i)
	for line in f:
		mobs[ifile].append(line)
	ifile+=1
	
	f.close()
currentMob=0

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
	todo="write"
def readsave():
	todo="read"
def update():
	todo="everything"
def draw():
	wipe()
	for i in range(0,10):
		printxy(0,i+1,mobs[currentMob][i])
#game loop

while game_running:
	startTime=time.time()

	update()

	draw()
	currentMob=(currentMob+1)%ifile
	endTime=time.time()
	timeElapsed=endTime-startTime
	sleepTime=1/FRAMES_PER_SECOND-timeElapsed
	time.sleep(sleepTime)
