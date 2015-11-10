#System imports
import math
import sys
import time
import os
import glob

#Module imports
import gui

#Platform code
os.system('clear')

#Global variables
FRAMES_PER_SECOND = 1
GAME_RUNNING = True
MOB_FILES = glob.glob("../resources/mobs/*.txt")
COUNT_FILES=0
MOBS=[]

#Mob loading
for i in MOB_FILES:
	MOBS.append([])
	f=open(i)
	for line in f:
		MOBS[COUNT_FILES].append(line)
	COUNT_FILES+=1
	f.close()

#Definitions and methods
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
#	for i in range(0,10):
#		printxy(0,i+1,MOBS[currentMob][i])

#Main loop
while GAME_RUNNING:
	startTime=time.time()
	update()
	draw()
	endTime=time.time()
	timeElapsed=endTime-startTime
	sleepTime=1/FRAMES_PER_SECOND-timeElapsed
	time.sleep(sleepTime)
