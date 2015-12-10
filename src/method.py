#system import
import sys

#Global variables
BUFFER_LINES = []
GUI_LINES = []

#Import code
f=open("../resources/gui/gui.txt")
for line in f:
	BUFFER_LINES.append(line)
	GUI_LINES.append(line)
f.close()

#Definitions and methods
#@depricated
#prints text directly to the running frame.
def printxy(x, y, text):
	sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (y, x, text))
	sys.stdout.flush()

#param x and y where 0,0 is top left and text to write.
def bufferxy(x, y, text):
	temp=BUFFER_LINES[y]
	
	#phase 1: get the actual index we need to start at
	putIndex=0
	for int in range(0,len(temp)):
		if(putIndex==x):
			putIndex = int
			break
		if(temp[int:int+1]=="&"):
			putIndex-=3
		putIndex+=1
	
	#phase 2: get the actual length of the things we will be replacing
	charsInText=len(text) - text.count("&")*3
	rangeToRemove=0
	for int in range(putIndex,len(temp)):
		if(rangeToRemove==charsInText):
			rangeToRemove = int - putIndex
			break
		if(temp[int:int+1]=="&"):
			rangeToRemove-=3
		rangeToRemove+=1	
	
	#phase 3: tack it all together
	BUFFER_LINES[y]=temp[:putIndex] + text + temp[putIndex+rangeToRemove:]
	
	'''
	ampsUpToX=temp[:x].count("&")
	charsInBuff=len(temp) - temp[:x].count("&")*3
	charsInText=len(text) - text.count("&")*3
	BUFFER_LINES[y]=temp[:
	i = 1 + x + 3*ampsInBuff
	end=i
	for index in range(i, i+charsInText):
		if temp[end]=="&":
			end+=3
	BUFFER_LINES[y]=temp[:i] + text + temp[end:]
	'''
	
	'''
	i=0
	c=0
	if temp[i]=="&": #check if it starts with &
		c-=2
		i+=1
	while c<x:
		if i<len(temp) and temp[i]=="&":
			c-=3
		c+=1
		i+=1
	if i<len(temp) and temp[i]=="&": #check if it ends on &
		i+=3
	BUFFER_LINES[y]=temp[:i] + text + temp[i+len(text) - 3*text.count("&"):]
	'''

#param the current zone
#returns 1 if zone==5, else returns 10
def getMobsInZone(zone):
	return 9*((zone%5+4)/5)+1

#param a number
#returns num as a string
def dispBigNum(num):
	num=str(num)
	if int(num) >= 100000:
		num = num[:1] + "." + num[1:3] + str(int(round(float(num[3:5])/10.0))) + "e" + str(len(num)-1)
	return num
	
#param a string with a single letter K,R,G,Y,B,M,C,W (or X to clear).
#returns a number representing the inputed letter
def getintfromletter(string):
	if string == "K": #Black
		return 0
	if string == "R": #Red
		return 1
	if string == "G": #Green
		return 2
	if string == "Y": #Yellow
		return 3
	if string == "B": #Blue
		return 4
	if string == "M": #Magenta
		return 5
	if string == "C": #Cyan
		return 6
	if string == "W": #White
		return 7
	if string == "X": #Clear
		return 9
	return 9

#param a string with a character code in the format of &XX
#returns a string with escape characters.
def color(string):
	location = 0
	location = string.find("&", location)
	while location < len(string):
		location = string.find("&", location)
		if location != -1:
			location += 1
			escape = "\x1b[3%d;4%dm" % (getintfromletter(string[location:location+1]),getintfromletter(string[location+1:location+2]))
			string = string[0:location - 1] + escape + string[location+2:len(string)]
		else:
			location = len(string)
	return string
	
#Resets buffer with the GUI file.
def refreshBuffer():
	for i in range(0,len(GUI_LINES)):
		BUFFER_LINES[i] = ""
		BUFFER_LINES[i] = GUI_LINES[i]

#Completely output the framebuffer to the frame.
def printBuffer():
	for i in range(0,len(BUFFER_LINES)):
		printxy(0,i+1,color(BUFFER_LINES[i]))
