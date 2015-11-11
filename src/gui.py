#System imports
import sys

#Module imports
import method

#Definitions and methods
def drawgui():
	for i in range(0,len(GUI_LINES)):
		method.printxy(0,i+1,GUI_LINES[i])
		
def getintfromletter(string):
	if string == "K":
		return 0
	if string == "R":
		return 1
	if string == "G":
		return 2
	if string == "Y":
		return 3
	if string == "B":
		return 4
	if string == "M":
		return 5
	if string == "C":
		return 6
	if string == "W":
		return 7
	if string == "X":
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
	
#load GUI file.
f=open("../resources/gui/gui.txt")
GUI_LINES = []
for line in f:
	GUI_LINES.append(color(line))