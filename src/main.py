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

hitDmg=1
dps=0
mobHP=10
mobMaxHP=10
ch=' '
lastch=' '
quitMenuOpen=False

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

#Saving
def writesave():
	todo="write"

def readsave():
	todo="read"

#Methods
def hit():
	global hitDmg
	global mobHP
	mobHP -= hitDmg
	if mobHP < 0:
		mobHP = 0 #maybe change to "rekt" later

def update():
	global mobHP
	todo="everything"
	#test
def draw():
	gui.drawgui()
	for i in range(0,len(MOBS[0])):
		method.printxy(33,6+i,MOBS[0][i])
	method.printxy(37,17,mobHP)
	if quitMenuOpen:
		gui.drawquitmenu()

#Wait for SPACE before moving on.
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
