#System imports
import math
import sys
import time
import os
import glob
import signal
import getch
import threading
import random

#Module imports
import gui
import method

#Platform code
os.system("clear")
os.system("stty -echo")
os.system("setterm -cursor off")
def quit():
	os.system("stty echo")
	os.system('clear')
	os.system("setterm -cursor on")
	print "Project UNCH has quit."
	sys.exit(0)

#Global variables
FRAMES_PER_SECOND = 20
GAME_RUNNING = True
MOB_FILES = glob.glob("../resources/mobs/*.txt")
COUNT_FILES=0
MOBS=[]
DEATH_FRAME = 0

HIT_DMG=1
DPS=0
MOB_HP=10
MOB_MAX_HP=10
CURRENT_MOB=0

quitMenuOpen=False
#Mob loading
for i in MOB_FILES:
	MOBS.append([])
	f=open(i)
	MOBS[COUNT_FILES].append(capitalize(i[16+i.find("/resources/mobs/"):len(i)-4]))
	for line in f:
		MOBS[COUNT_FILES].append(line)
	COUNT_FILES+=1
	f.close()
	
#Draw Title
gui.drawtitle()

#Definitions and methods

#Saving
def writesave():
	todo="write"

def readsave():
	todo="read"

#Methods
def hit():
	global HIT_DMG
	global MOB_HP
	MOB_HP -= HIT_DMG
	if MOB_HP < 0:
		MOB_HP = 0 #maybe change to "rekt" later
def createMob():
	global MOB_MAX_HP, MOB_HP, CURRENT_MOB
	MOB_MAX_HP = 10
	MOB_HP = MOB_MAX_HP
	CURRENT_MOB=random.randint(0,COUNT_FILES)

def update():
	global MOB_HP
	todo="everything"
	#test
def draw():
	gui.drawgui()
	if MOB_HP == 0:
	if DEATH_FRAME == 20:
            DEATH_FRAME = 0
            createMob()
	else:
            for i in range(1,len(MOBS[CURRENT_MOB]) - (DEATH_FRAME/2)):
                method.printxy(33,(6.0 + (DEATH_FRAME/2)) +i,MOBS[CURRENT_MOB][i])
            DEATH_FRAME+=1
	else:
		for i in range(1,len(MOBS[CURRENT_MOB])):
		method.printxy(33,6+i,MOBS[CURRENT_MOB][i])
		method.printxy(37,17,MOB_HP)
			method.printxy(33,4,MOBS[CURRENT_MOB][0])
		if quitMenuOpen:
			gui.drawquitmenu()

#Wait for SPACE before moving on.
ch=' '
lastch=' '

ch = getch.getch()
while ch != ' ':
	ch = getch.getch()


#Main loop
def mainloop():
	while GAME_RUNNING:
		startTime=time.time()
		update()
		draw()
		endTime=time.time()
		timeElapsed=endTime-startTime
		sleepTime=1.0/float(FRAMES_PER_SECOND)-float(timeElapsed)
		time.sleep(sleepTime)

mainthread = threading.Thread(name='main', target=mainloop)
mainthread.setDaemon(True)
mainthread.start()

#Handle Input
while GAME_RUNNING:
	lastch=ch
	ch = getch.getch()
	#cases
	
	if quitMenuOpen:
		if ch=='y' or ch=='Y':
			quit()
		elif ch=='n' or ch=='N':
			quitMenuOpen = False
	else:
		if ch=='.' and lastch!='.':
			hit()
		elif ch==',' and lastch=='.':
			hit()
		elif ch=='q':
			quitMenuOpen = True
