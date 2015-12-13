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
import gamesave

#Platform code
os.system("clear")
os.system("stty -echo")
os.system("setterm -cursor off")
ROWS, COLUMNS = os.popen('stty size', 'r').read().split()
ROWS = int(ROWS)
COLUMNS = int(COLUMNS)
lastROWS=0
lastCOLS=0


#Global variables
FRAMES_PER_SECOND = 20
GAME_RUNNING = True
MOB_FILES = glob.glob("../resources/mobs/*.txt")
COUNT_FILES=0
MOBS=[]
DEATH_FRAME = 0
MONEY=0
HIT_DMG=1
DPS=0
MOB_HP=10
MOB_MAX_HP=10
CURRENT_MOB=0
HIGHEST_ZONE=1
CURRENT_ZONE=1
ZONE_MOBS_KILLED=0
BOSS_TIMER=0.0
MOB_DEAD=False
quitMenuOpen=False
loadMenuOpen=False
purchaseComplete=0

HEROES=[] # hero names 9 chars max
HEROES.append(["Treebeast", 0, 0, 25]) # name, level, dps, cost
HEROES.append(["Ivan", 0, 0, 125])
HEROES.append(["Brittany", 0, 0, 500])
HEROES.append(["Fish", 0, 0, 2500])
HEROES.append(["Betty", 0, 0, 12500])
HEROES.append(["Samurai", 0, 0, 62500])
HEROES.append(["Leon", 0, 0, 5000000])
HEROES.append(["Seer", 0, 0, 25000000])
HERO_SCREEN=0 #for now this is 0 or 1

HERO_DESC=[]
HERO_DESC.append(["Blah 1Blah Blah", "And More Blah"])#Treeb
HERO_DESC.append(["Blah Blah Bl2ah", "And More Blah"])#Ivan
HERO_DESC.append(["Blah Blah Blah", "And 3More Blah"])#Brittany
HERO_DESC.append(["Blah Blah B4lah", "And More Blah"])#Fish
HERO_DESC.append(["Blah Blah5 Blah", "And More Blah"])#Betty
HERO_DESC.append(["Blah Blah Blah", "And6 More Blah"])#Samurai
HERO_DESC.append(["Blah Blah7 Blah", "And More Blah"])#Leon
HERO_DESC.append(["Blah Blah Blah", "An8d More Blah"])#Seer
HERO_DISP_NUM=0 #display info for # hero

#Mob loading
for i in MOB_FILES:
	MOBS.append([])
	f=open(i)
	MOBS[COUNT_FILES].append("&RX"+i[16+i.find("/resources/mobs/"):len(i)-4].capitalize()+"&XX")
	for line in f:
		MOBS[COUNT_FILES].append(line)
	COUNT_FILES+=1
	f.close()
	
#Draw Title
gui.drawtitle(ROWS,COLUMNS)

#Definitions and methods
def hit():
	global HIT_DMG
	global MOB_HP
	MOB_HP -= HIT_DMG
	if MOB_HP < 0:
		MOB_HP = 0

def destroy():
	global MOB_HP
	MOB_HP -= 10000
	if MOB_HP < 0:
		MOB_HP = 0

def createMob():
	global MOB_MAX_HP, MOB_HP, CURRENT_MOB, MOB_DEAD, BOSS_TIMER
	MOB_DEAD=False
	MOB_MAX_HP = CURRENT_ZONE+random.randint(0,5)
	if CURRENT_ZONE % 5 == 0:
		MOB_MAX_HP = 10*CURRENT_ZONE+50
		BOSS_TIMER = time.time()
	MOB_HP = MOB_MAX_HP
	CURRENT_MOB=random.randint(0,COUNT_FILES-1)

def killMob():
	global ZONE_MOBS_KILLED, HIGHEST_ZONE, MOB_DEAD, MONEY
	MOB_DEAD=True
	MONEY += 1
	if CURRENT_ZONE==HIGHEST_ZONE:
		if CURRENT_ZONE % 5 != 0:
			ZONE_MOBS_KILLED = min(ZONE_MOBS_KILLED + 1, 10)
			if ZONE_MOBS_KILLED==10:
				ZONE_MOBS_KILLED=0
				HIGHEST_ZONE=max(HIGHEST_ZONE,CURRENT_ZONE+1)
		else:
			HIGHEST_ZONE=HIGHEST_ZONE+1
			ZONE_MOBS_KILLED=0

def update():
	global MOB_HP, HIGHEST_ZONE, CURRENT_ZONE, ZONE_MOBS_KILLED
	if MOB_HP <= 0 and not MOB_DEAD:
		killMob()
	if CURRENT_ZONE % 5 == 0 and 30.0-time.time()+BOSS_TIMER<=0:
		createMob()

def draw():
	global DEATH_FRAME, ZONE_MOBS_KILLED, MOB_MAX_HP, HIGHEST_ZONE, CURRENT_ZONE, lastch
	#gui.drawgui()
	method.bufferxy(9,15,"Dn ]" if HERO_SCREEN==0 else "Up [") #scroll up/down
	method.bufferxy(22,15,"Dn ]" if HERO_SCREEN==0 else "Up [") #scroll up/down
	method.bufferxy(4,1,"&YX" + method.dispBigNum(MONEY) + "&YX") #money
	method.bufferxy(33,3,MOBS[CURRENT_MOB][0]) #mob name
	if CURRENT_ZONE-1>0:
		method.bufferxy(35,1,str(CURRENT_ZONE-1)) #zone num -
	if CURRENT_ZONE != HIGHEST_ZONE:
		method.bufferxy(49-len(str(CURRENT_ZONE)),1,str(CURRENT_ZONE+1)) #zone num + 
	method.bufferxy(42-len(str(CURRENT_ZONE))/2,1,str(CURRENT_ZONE)) #zone num
	if CURRENT_ZONE % 5 == 0: #zone mob nums
		method.bufferxy(36,15,"&RXTime: "+str(round(30.0-time.time()+BOSS_TIMER,1)) + "&XX") #boss timer
		if HIGHEST_ZONE > CURRENT_ZONE:
			method.bufferxy(46,3,"(1/1)")
		else:
			method.bufferxy(46,3,"(0/1)")
	else:
		if HIGHEST_ZONE > CURRENT_ZONE:
			method.bufferxy(44,3,"(10/10)")
		else:
			method.bufferxy(45,3,"("+str(ZONE_MOBS_KILLED)+"/10)")
	Y=int((float(MOB_HP)/float(MOB_MAX_HP))*22.0)
	for i in range(22-Y, 22):
		method.bufferxy(55,i+1,("&GG" if Y > 0.5*22.0 else ("&YY" if Y > 0.25*22.0 else "&RR")) + "XX" + "&XX") #hashtag healthbar
	if MOB_HP <= 0: #mob death animation
		method.bufferxy(36,16,"rekt&XX")
		if DEATH_FRAME == 20:
			DEATH_FRAME = 0
			createMob()
		else:
			for i in range(1,len(MOBS[CURRENT_MOB]) - (DEATH_FRAME/2)):
				method.bufferxy(32,(4 + (DEATH_FRAME/2)) +i,MOBS[CURRENT_MOB][i][:-1])
			DEATH_FRAME+=1
	else:
		for i in range(1,len(MOBS[CURRENT_MOB])): #mob drawing
			method.bufferxy(32,4+i,MOBS[CURRENT_MOB][i][:-1])
			method.bufferxy(36,16,method.dispBigNum(MOB_HP) + "&XX") #mob hp num
	#Heroes
	for i in range(4):
		method.bufferxy(1,4+3*i,HEROES[i+HERO_SCREEN*4][0]) # hero name
		method.bufferxy(15-len(str(HEROES[i+HERO_SCREEN*4][1])),4+3*i,str(HEROES[i+HERO_SCREEN*4][1])) # hero level
		method.bufferxy(1,5+3*i,"&CX" + str(1+i) + "&XX:")
		method.bufferxy(14-len(method.dispBigNum(HEROES[i+HERO_SCREEN*4][3])),5+3*i,"&GX$&YX" + method.dispBigNum(HEROES[i+HERO_SCREEN*4][3]) + "&XX") #hero cost
	if not quitMenuOpen:
		if lastch=='.' or lastch=='>': #characters at bottom
			method.bufferxy(49,22," &MX<&XX ")
		elif lastch=='h' or lastch=='H': # Information box
			method.bufferxy(49,22,"  &MX?&XX")
			method.bufferxy(1,18,"Press hero/skill key to find information about it.")
			method.bufferxy(1,19,"Press &CXQ&XX to Quit.")
			method.bufferxy(1,20,"Use &CX>&XX and &CX<&XX to attack (no need to press SHIFT)")
		elif HERO_DISP_NUM != 0:
			method.bufferxy(1, 18,HEROES[HERO_DISP_NUM-1+4*HERO_SCREEN][0] + "                                          ")
			for i in range(2):
				method.bufferxy(3, 19+i,HERO_DESC[HERO_DISP_NUM-1+4*HERO_SCREEN][i])
		else:
			method.bufferxy(49,22,"&MX>&XX  ")
	elif purchaseComplete!=0:
		if purchaseComplete==-1:
			method.bufferxy(1,18,"Not enough money!                                  ")
		else:
			method.bufferxy(1,18,HEROES[purchaseComplete-1][0] + " Gained a level!                          ")
	else:
		gui.drawquitmenu(ROWS,COLUMNS)
	if loadMenuOpen:
		gui.drawloadmenu(ROWS,COLUMNS)

#Wait for SPACE before moving on.
ch=' '
lastch=' '
ch = getch.getch()
while ch != ' ':
	ch = getch.getch()
#Create first mob	
createMob()

#Main loop
def mainloop():
	global ROWS, COLUMNS, lastROWS, lastCOLS
	while GAME_RUNNING:
		startTime=time.time()
		update()
		ROWS, COLUMNS = os.popen('stty size', 'r').read().split()
		ROWS = int(ROWS)
		COLUMNS = int(COLUMNS)
		if ROWS!=lastROWS or COLUMNS!=lastCOLS: #refresh screen
			for y in range(1, ROWS+1):
				for x in range(1, COLUMNS+1):
					method.printxy(x,y," ")
		lastROWS=ROWS
		lastCOLS=COLUMNS
		if ROWS<24 or COLUMNS<58:
			method.printxy(1,1,method.color("&RXYOUR SCREEN IS TOO SMALL!&XX"))
		else:
			method.refreshBuffer()
			draw()
			method.printBuffer(ROWS,COLUMNS)
		endTime=time.time()
		timeElapsed=endTime-startTime
		sleepTime=1.0/float(FRAMES_PER_SECOND)-float(timeElapsed)
		try:
			time.sleep(sleepTime)
		except Exception:
			pass

#Data to save
def updateVarsToSave():
	#FOR NEW SAVEABLE VARIABLE, APPEND A VARIABLE TO THIS LIST
	SD = [MONEY,
	HIT_DMG,
	DPS,
	HIGHEST_ZONE,
	CURRENT_ZONE,
	ZONE_MOBS_KILLED,
	HEROES]
	return SD
	
def checkTypes(list1, list2):
	if len(list1) != len(list2):
		return False
	index = 0
	for element in list1:
		if type(element) != type(list2[index]):
			return False
		if type(element) == type([]):
			if not checkTypes(element, list2[index]):
				return False
		index += 1
	return True

#Actually save
def save():
	SaveData = updateVarsToSave()
	gamesave.save(SaveData)

#Actually load
def load():
	global loadMenuOpen
	#FOR NEW SAVEABLE VARIABLE, APPEND A VARIABLE TO THIS LIST
	global MONEY, HIT_DMG, DPS, HIGHEST_ZONE, CURRENT_ZONE, ZONE_MOBS_KILLED, HEROES
	try:
		LD = gamesave.load()
		typesMatch  = checkTypes(updateVarsToSave(), LD)
		if typesMatch:
			#FOR NEW SAVEABLE VARIABLE, APPEND A VARIABLE TO THIS LIST
			MONEY = LD[0]
			HIT_DMG = LD[1]
			DPS = LD[2]
			HIGHEST_ZONE = LD[3]
			CURRENT_ZONE = LD[4]
			ZONE_MOBS_KILLED = LD[5]
			HEROES = LD[6]
		else:
			loadMenuOpen = True
	except Exception:
		loadMenuOpen = True

def quit():
	os.system("stty echo")
	os.system("setterm -cursor on")
	print "Project UNCH has quit."
	os.system('clear')
	save()
	sys.exit(0)
	
#Handle Input
load()
mainthread = threading.Thread(name='main', target=mainloop)
mainthread.setDaemon(True)
mainthread.start()
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
	elif HERO_DISP_NUM != 0 and ch != lastch:
		HERO_DISP_NUM = 0
		ch = " "
		lastch = " "
	elif purchaseComplete != 0 and ch != lastch:
		purchaseComplete = 0
		ch = " "
		lastch = " "
	elif loadMenuOpen and ch != lastch:
		loadMenuOpen = False
		ch = " "
		lastch = " "
	elif lastch=='h':
		try:
			HERO_DISP_NUM = int(ch)
			if HERO_DISP_NUM > 4:
				HERO_DISP_NUM = 0
		except ValueError:
			pass
	else:
		if (ch=='.' or ch=='>') and lastch!='.' and lastch!='>':
			hit()
		elif (ch==',' or ch=='<') and (lastch=='.' or lastch=='>'):
			hit()
		elif ch=='q':
			quitMenuOpen = True
		elif ch=='0': #THIS IS DEBUG CODE ONLY
			destroy()
		elif (ch=='=' or ch=='+') and CURRENT_ZONE<HIGHEST_ZONE and MOB_DEAD==False:
			CURRENT_ZONE=CURRENT_ZONE+1
			createMob()
		elif (ch=='-' or ch=='_') and CURRENT_ZONE-1>0 and MOB_DEAD==False:
			CURRENT_ZONE=CURRENT_ZONE-1
			createMob()
		elif ch=="[" or ch=="{":
			HERO_SCREEN=0
		elif ch=="]" or ch=="}":
			HERO_SCREEN=1
		else:
			for i in range(4):
				if ch==str(i+1):
					if MONEY>=HEROES[i+4*HERO_SCREEN][3]:
						MONEY-=HEROES[i+4*HERO_SCREEN][3]
						HEROES[i+4*HERO_SCREEN][1]+=1
						purchaseComplete=i+4*HERO_SCREEN
					else:
						purchaseComplete=-1
