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
os.system("stty -icanon time 0 min 0")

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
MONEY_BUFFER=0
HIT_DMG=1
DPS=0
DPS_BUFFER=0.0
MOB_HP=10
MOB_MAX_HP=10
CURRENT_MOB=0
HIGHEST_ZONE=1
CURRENT_ZONE=1
MONEY_POS=0
ZONE_MOBS_KILLED=0
BOSS_TIMER=0.0
MOB_DEAD=False
quitMenuOpen=False
loadMenuOpen=False
newMenuOpen=False
purchaseComplete=0

HEROES=[] # hero names 9 chars max
HEROES.append(["Red", 0, 0, 25]) # name, level, dps, cost
HEROES.append(["Yu", 0, 0, 125])
HEROES.append(["Thebleegel", 0, 0, 500])
HEROES.append(["Brickster", 0, 0, 2500])
HEROES.append(["Edge", 0, 0, 12500])
#HEROES.append(["Samurai", 0, 0, 62500])
#HEROES.append(["Leon", 0, 0, 5000000])
#HEROES.append(["Seer", 0, 0, 25000000])
HERO_SCREEN=0 #for now this is 0 or 1
                   
HERO_DESC=[]     #"                                                   "
HERO_DESC.append(["Known to be inquisitive. \"What's this button do?\"", "Every 5 levels, Red increases your hit damage."])#Red
HERO_DESC.append(["Loves to spam OP abilities.", "Unlocks &MXFireball&XX which cools faster every 5 levels."])#Yu
HERO_DESC.append(["Sometimes uncontrollably enters a state of rage.", "Unlocks &MXRage&XX which strengthens every 5 levels."])#Bleegel
HERO_DESC.append(["Enjoys long walks on short bridges.", "\"The best thing since Betty White.\""])#Brickster
HERO_DESC.append(["The Dev", "'sup"])#Edge
#HERO_DESC.append(["Blah Blah Blah", "And6 More Blah"])#Samurai
#HERO_DESC.append(["Blah Blah7 Blah", "And More Blah"])#Leon
#HERO_DESC.append(["Blah Blah Blah", "An8d More Blah"])#Seer

HELP_DISP_NUM=0 #display info for # hero/skill

SKILLS=[]
SKILLS.append(["Big Hits  ",0,0]) # name, cd (seconds) (if 0, its a passive skill), cd timer (time used last)
SKILLS.append(["Fireball",30,time.time()])
SKILLS.append(["Rage",30,time.time()])
SKILLS.append(["Money Bag",3600,time.time()])
SKILLS.append(["Firestorm",0,0])
#SKILLS.append(["Fireball",30,0.0])
#SKILLS.append(["Fireball",30,0.0])
#SKILLS.append(["Fireball",30,0.0])

SKILL_DESC=[]     #"                                                   "
SKILL_DESC.append(["Increases Hit Damage.", "Every 5 leves, &MXRed&XX complains about the hit damage."])
SKILL_DESC.append(["Shoots a Fireball to deal a lot of damage.", "(R)&MXYu&XX likes to spam this."])
SKILL_DESC.append(["&MXThebleegel&XX enters a state of rage, making hits", "do double damage."])
SKILL_DESC.append(["Through the power of creativity, &MXthe Brickster&XX", "doubles your &GXmoney&XX."])
SKILL_DESC.append(["The dev doesn't now what to do.", "So he buffs &MXYu&XX's attack."])
#SKILL_DESC.append(["Blah Blah Blah", "And6 More Blah"])
#SKILL_DESC.append(["Blah Blah7 Blah", "And More Blah"])
#SKILL_DESC.append(["Blah Blah Blah", "An8d More Blah"])

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
	MOB_MAX_HP = CURRENT_ZONE*CURRENT_ZONE+random.randint(9,CURRENT_ZONE+9)
	if CURRENT_ZONE % 5 == 0:
		MOB_MAX_HP = 10*CURRENT_ZONE+5*CURRENT_ZONE
		BOSS_TIMER = time.time()
	MOB_HP = MOB_MAX_HP
	CURRENT_MOB=random.randint(0,COUNT_FILES-1)

def killMob():
	global ZONE_MOBS_KILLED, HIGHEST_ZONE, MOB_DEAD, MONEY, MONEY_BUFFER, MONEY_POS
	MOB_DEAD=True
	MONEY_BUFFER = CURRENT_ZONE + random.randint(1,5)*(1+CURRENT_ZONE/10)
	MONEY+=MONEY_BUFFER
	MONEY_POS=random.randint(0,17-len(str(MONEY_BUFFER)))
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
	global MOB_HP, HIGHEST_ZONE, CURRENT_ZONE, ZONE_MOBS_KILLED, DPS_BUFFER
        MOB_HP -= int(math.floor(DPS_BUFFER))
        DPS_BUFFER -= math.floor(DPS_BUFFER)
        DPS_BUFFER = float(DPS)/20.0 + DPS_BUFFER
	if MOB_HP <= 0 and not MOB_DEAD:
		killMob()
	if CURRENT_ZONE % 5 == 0 and 30.0-time.time()+BOSS_TIMER<=0:
		createMob()


def draw():
	global DEATH_FRAME, ZONE_MOBS_KILLED, MOB_MAX_HP, HIGHEST_ZONE, CURRENT_ZONE, lastch
	#gui.drawgui()
	method.bufferxy(26,15,str(1+HERO_SCREEN)) #scroll up/down
	method.bufferxy(15,22,method.dispBigNum(HIT_DMG)) #Hit Dmg
	method.bufferxy(37,22,method.dispBigNum(DPS)) #DPS
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
			method.bufferxy(33+MONEY_POS,14-DEATH_FRAME/2,"+&YX"+str(MONEY_BUFFER)+"&XX") #money animation
			DEATH_FRAME+=1
	else:
		for i in range(1,len(MOBS[CURRENT_MOB])): #mob drawing
			method.bufferxy(32,4+i,MOBS[CURRENT_MOB][i][:-1])
			method.bufferxy(36,16,method.dispBigNum(MOB_HP) + "&XX") #mob hp num
	
	for i in range(4):
		if (i+HERO_SCREEN*4<len(HEROES)):
			#Heroes
			method.bufferxy(1,4+3*i,HEROES[i+HERO_SCREEN*4][0]) # hero name
			method.bufferxy(15-len(str(HEROES[i+HERO_SCREEN*4][1])),4+3*i,str(HEROES[i+HERO_SCREEN*4][1])) # hero level
			method.bufferxy(14-len(method.dispBigNum(HEROES[i+HERO_SCREEN*4][3])),5+3*i,"&GX$&YX" + method.dispBigNum(HEROES[i+HERO_SCREEN*4][3]) + "&XX") #hero cost
			#Skills
			method.bufferxy(19,4+3*i,SKILLS[i+HERO_SCREEN*4][0])
			if HEROES[i+HERO_SCREEN*4][1]>0
				if(SKILLS[i+HERO_SCREEN*4][1]==0):
					method.bufferxy(16,5+3*i,"(Passive)")
				
				elif round(SKILLS[i+HERO_SCREEN*4][1]-time.time()+SKILLS[i+HERO_SCREEN*4][2],1)<=0:
					method.bufferxy(16,5+3*i,"Ready")
				else:
					method.bufferxy(16,5+3*i,str(round(SKILLS[i+HERO_SCREEN*4][1]-time.time()+SKILLS[i+HERO_SCREEN*4][2],1)))
	if purchaseComplete!=0:
		if purchaseComplete==-1:
			method.bufferxy(1,18,"Not enough &GXmoney&XX!                                  ")
		else:
			method.bufferxy(1,18,HEROES[purchaseComplete-1][0] + " gained a level!                          ")
		method.bufferxy(1,20,"Press any key to continue...")
	if not quitMenuOpen:
		if lastch=='.' or lastch=='>': #characters at bottom
			method.bufferxy(49,22," &MX<&XX ")
		elif lastch=='h' or lastch=='H': # Information box
			method.bufferxy(49,22,"  &MX?&XX")
			method.bufferxy(1,18,"Press hero/skill key to find information about it.")
			method.bufferxy(1,19,"Press &CXQ&XX to Quit.")
			method.bufferxy(1,20,"Use &CX>&XX and &CX<&XX to attack (no need to press SHIFT)")
		elif HELP_DISP_NUM != 0:
			if HELP_DISP_NUM<5:
				method.bufferxy(1, 18,"                                                   ")
				method.bufferxy(1, 18,"&YX"+HEROES[HELP_DISP_NUM-1+4*HERO_SCREEN][0] + "&XX  (DPS: " + str(HEROES[HELP_DISP_NUM-1+4*HERO_SCREEN][2])+")")
				for i in range(2):
					method.bufferxy(1, 19+i,HERO_DESC[HELP_DISP_NUM-1+4*HERO_SCREEN][i])
			else: #Skill descriptions
				method.bufferxy(1, 18,"&YX"+SKILLS[HELP_DISP_NUM-5+4*HERO_SCREEN][0] + "&XX                                          ")
				for i in range(2):
					method.bufferxy(1, 19+i,SKILL_DESC[HELP_DISP_NUM-5+4*HERO_SCREEN][i])
		else:
			method.bufferxy(49,22,"&MX>&XX  ")
	else:
		gui.drawquitmenu(ROWS,COLUMNS)
	if loadMenuOpen:
		gui.drawloadmenu(ROWS,COLUMNS)
	if newMenuOpen:
		gui.drawnewmenu(ROWS,COLUMNS)

def quit(forced):
	os.system("stty echo")
	os.system("setterm -cursor on")
	os.system('clear')
	os.system("stty icanon")

	if not forced:
		print "Project UNCH has quit."
		save()
	else:
		print "Keyboard Interrupt. Closing Project UNCH and destroying data."
	sys.exit(0)
		
#Wait for SPACE before moving on.
ch=' '
lastch=' '
try:
	ch = getch.getch()
except KeyboardInterrupt, EOFError:
	GAME_RUNNING=False
	quit(True)
while ch != ' ':
	try:
		ch = getch.getch()
	except KeyboardInterrupt, EOFError:
		GAME_RUNNING=False
		quit(True)

for y in range(1, ROWS+1): #refresh screen
	for x in range(1, COLUMNS+1):
		method.printxy(x,y," ")
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
	HEROES,
	int(os.popen('date +%s').read())]
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
	global loadMenuOpen, newMenuOpen
	#FOR NEW SAVEABLE VARIABLE, APPEND A VARIABLE TO THIS LIST
	global MONEY, HIT_DMG, DPS, HIGHEST_ZONE, CURRENT_ZONE, ZONE_MOBS_KILLED, HEROES
	try:
		LD = gamesave.load()
		if type(LD) == type("NEW"):
			if LD == "NEW":
				newMenuOpen = True
		else:
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
				for hero in HEROES:
					DPS += hero[2]
			else:
				loadMenuOpen = True
	except Exception:
		loadMenuOpen = True
	
#Handle Input
load()
mainthread = threading.Thread(name='main', target=mainloop)
mainthread.setDaemon(True)
mainthread.start()
while GAME_RUNNING:
	lastch=ch
	try:
		ch=os.popen("read ch; echo $ch").read()
	except KeyboardInterrupt, EOFError:
		GAME_RUNNING=False
		quit(True)
	ch=ch[:1]
	while ch.isspace():
		time.sleep(0.01)
		try:
			ch=os.popen("read ch; echo $ch").read()
		except KeyboardInterrupt, EOFError:
			GAME_RUNNING=False
			quit(True)
		ch=ch[:1]

	#cases
	if quitMenuOpen:
		if ch=='y' or ch=='Y':
			GAME_RUNNING=False
			quit(False)

		elif ch=='n' or ch=='N':
			quitMenuOpen = False
	elif HELP_DISP_NUM != 0 and ch != lastch:
		HELP_DISP_NUM = 0
		ch = "|"
		lastch = "|"
	elif purchaseComplete != 0 and ch != lastch:
		purchaseComplete = 0
		ch = "|"
		lastch = "|"
	elif loadMenuOpen and ch != lastch:
		loadMenuOpen = False
		ch = "|"
		lastch = "|"
	elif newMenuOpen and ch != lastch:
		newMenuOpen = False
		ch = "|"
		lastch = "|"
	elif lastch=='h':
		try:
			HELP_DISP_NUM = int(ch)
			if HELP_DISP_NUM > 8 or (HERO_SCREEN == 1 and HELP_DISP_NUM!= 1 and HELP_DISP_NUM!=5):
				HELP_DISP_NUM = 0
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
		elif (ch=='=' or ch=='+') and CURRENT_ZONE<HIGHEST_ZONE:
			CURRENT_ZONE=CURRENT_ZONE+1
			if MOB_DEAD==False:
				createMob()
		elif (ch=='-' or ch=='_') and CURRENT_ZONE-1>0:
			CURRENT_ZONE=CURRENT_ZONE-1
			if MOB_DEAD==False:
				createMob()
		elif ch=="[" or ch=="{":
			HERO_SCREEN=0
		elif ch=="]" or ch=="}":
			HERO_SCREEN=1
		else:
			for i in range(4):
				if ch==str(i+1) and i+4*HERO_SCREEN<len(HEROES):
					if MONEY>=HEROES[i+4*HERO_SCREEN][3]:
						MONEY-=HEROES[i+4*HERO_SCREEN][3]
						HEROES[i+4*HERO_SCREEN][1]+=1 #level
						HEROES[i+4*HERO_SCREEN][2]+=(1+i+4*HERO_SCREEN)*(1+i+4*HERO_SCREEN) #dps
						HEROES[i+4*HERO_SCREEN][3]+=(1+i+4*HERO_SCREEN)*HEROES[i+4*HERO_SCREEN][3]/25 *HEROES[i+4*HERO_SCREEN][3]/25 #cost
						DPS += (1+i+4*HERO_SCREEN)*(1+i+4*HERO_SCREEN)
						purchaseComplete=i+1+4*HERO_SCREEN
					else:
						purchaseComplete=-1
