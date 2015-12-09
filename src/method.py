#system import
import sys
BUFFER_LINES = []
#Definitions and methods
def printxy(y, x, text):
	sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (x, y, text))
	sys.stdout.flush()
def bufferxy(x, y, text):
	temp=BUFFER_LINES[y]
	counter=0
	i=0
	while c<x:
		if temp[i]=="&":
			c-=3

		c+=1
		i+=1
	BUFFER_LINES[y]=temp[:i] + text + temp[i+len(text):]
def printBuffer():
	for i in range(0,len(BUFFER_LINES)):
		method.printxy(0,i+1,BUFFER_LINES[i])
def getMobsInZone(zone): #returns 1 if zone==5, else returns 10
	return 9*((zone%5+4)/5)+1
def dispBigNum(num): #returns num as a string
	num=str(num)
	if int(num) >= 100000:
		num = num[:1] + "." + num[1:3] + str(int(round(float(num[3:5])/10.0))) + "e" + str(len(num)-1)
	return num
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

f=open("../resources/gui/gui.txt")
for line in f:
	BUFFER_LINES.append(color(line))
