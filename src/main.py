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
HIGHEST_ZONE=1
CURRENT_ZONE=1
ZONE_MOBS_KILLED=0
MOB_DEAD=False
quitMenuOpen=False
#Mob loading
for i in MOB_FILES:
	MOBS.append([])
	f=open(i)
	MOBS[COUNT_FILES].append(method.color("&RK"+i[16+i.find("/resources/mobs/"):len(i)-4].capitalize()+"&XX"))
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
		MOB_HP = 0
def createMob():
	global MOB_MAX_HP, MOB_HP, CURRENT_MOB, MOB_DEAD
	MOB_DEAD=False
	MOB_MAX_HP = 10
	MOB_HP = MOB_MAX_HP
	CURRENT_MOB=random.randint(0,COUNT_FILES-1)
def killMob():
	global ZONE_MOBS_KILLED, HIGHEST_ZONE, MOB_DEAD
	MOB_DEAD=True
	if CURRENT_ZONE % 5 != 0:
		ZONE_MOBS_KILLED = min(ZONE_MOBS_KILLED + 1, 10)
		if ZONE_MOBS_KILLED==10:
			HIGHEST_ZONE=max(HIGHEST_ZONE,CURRENT_ZONE+)
	else:
		ZONE_MOBS_KILLED = 1
		HIGHEST_ZONE=HIGHEST_ZONE+1
def update():
	global MOB_HP, HIGHEST_ZONE, CURRENT_ZONE, ZONE_MOBS_KILLED
	if MOB_HP <= 0 and not MOB_DEAD:
		killMob()
def draw():
	global DEATH_FRAME, ZONE_MOBS_KILLED
	gui.drawgui()
	method.printxy(34,4,MOBS[CURRENT_MOB][0]) #mob name
	if CURRENT_ZONE-1>0:
		method.printxy(36,2,str(CURRENT_ZONE-1)) #zone num -
	if CURRENT_ZONE != HIGHEST_ZONE:
		method.printxy(45,2,str(CURRENT_ZONE+1)) #zone num + 
	method.printxy(42,2,str(CURRENT_ZONE)) #zone num
	if CURRENT_ZONE % 5 == 0: #zone mob nums
		method.printxy(45,4,"(0/1)")
	else:
		if ZONE_MOBS_KILLED == 10:
			method.printxy(45,4,"(10/10)")
		else:
			method.printxy(46,4,"("+str(ZONE_MOBS_KILLED)+"/10)")
	if MOB_HP <= 0: #mob death animation
		method.printxy(37,17,"rekt")
		if DEATH_FRAME == 20:
			DEATH_FRAME = 0
			createMob()
		else:
			for i in range(1,len(MOBS[CURRENT_MOB]) - (DEATH_FRAME/2)):
				method.printxy(33,(5 + (DEATH_FRAME/2)) +i,MOBS[CURRENT_MOB][i])
			DEATH_FRAME+=1
	else:
		for i in range(1,len(MOBS[CURRENT_MOB])): #mob drawing
			method.printxy(33,5+i,MOBS[CURRENT_MOB][i])
			method.printxy(37,17,MOB_HP)
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
			GAME_RUNNING=False
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
		elif (ch=='=' or ch=='+') and CURRENT_ZONE<HIGHEST_ZONE:
			CURRENT_ZONE=CURRENT_ZONE+1
			if CURRENT_ZONE == HIGHEST_ZONE:
				ZONE_MOBS_KILLED=0
			createMob()
		elif (ch=='-' or ch=='_') and CURRENT_ZONE-1>0:
			CURRENT_ZONE=CURRENT_ZONE-1c
			ZONE_MOBS_KILLED=method.getMobsInZone(CURRENT_ZONE)
			createMob()
