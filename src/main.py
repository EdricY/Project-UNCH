#System imports
import math
import sys
import time
import os
import glob
import signal

#Module imports
import gui
import method

#Platform code
os.system("clear")
os.system("stty -echo")
os.system("setterm -cursor off")
def signalhandler(signal, frame):
	os.system("stty echo")
	os.system('clear')
	os.system("setterm -cursor on")
	print "Project UNCH has quit."
	sys.exit(0)
signal.signal(signal.SIGINT, signalhandler)

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
def writesave():
	todo="write"

def readsave():
	todo="read"

def update():
	todo="everything"

def draw():
	gui.drawgui()

#Main loop
while GAME_RUNNING:
	startTime=time.time()
	update()
	draw()
	endTime=time.time()
	timeElapsed=endTime-startTime
	sleepTime=1/FRAMES_PER_SECOND-timeElapsed
	time.sleep(sleepTime)
