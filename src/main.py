#System imports
import math
import sys
import time
import os
import glob
import signal
import getch
import threading

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
FRAMES_PER_SECOND = 20
GAME_RUNNING = True
MOB_FILES = glob.glob("../resources/mobs/*.txt")
COUNT_FILES=0
MOBS=[]

#Private variables
hitDmg=1
dps=0
mobHP=10
mobMaxHP=10

#Mob loading
for i in MOB_FILES:
	MOBS.append([])
	f=open(i)
	for line in f:
		MOBS[COUNT_FILES].append(line)
	COUNT_FILES+=1
	f.close()
	
#Draw Title
gui.drawtitle()

#Definitions and methods
def writesave():
	todo="write"

def readsave():
	todo="read"

def update():
	todo="everything"
	#test
	
def hit():
	mobHP -= hitDmg
	if mobHP < 0
		mobHP = 0 #maybe change to "rekt" later

def draw():
	gui.drawgui()
	for i in range(0,len(MOBS[0])):
		method.printxy(33,6+i,MOBS[0][i])
	method.printxy(37,17,mobHP)
		
#Wait for SPACE before moving on.
g = getch.getch()
while g != ' ':
	g = getch.getch()


#Main loop
hitter = threading.Thread(name='hitter', target=method.inputhandler)
while GAME_RUNNING:
	startTime=time.time()
	update()
	draw()
	endTime=time.time()
	timeElapsed=endTime-startTime
	sleepTime=1/FRAMES_PER_SECOND-timeElapsed
	time.sleep(sleepTime)
	hitDmg = hitDmg + 1
