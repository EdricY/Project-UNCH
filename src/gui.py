#System imports
import sys

#Module imports
import method

#load GUI file.
f=open("../resources/gui/gui.txt")
GUI_LINES = []
for line in f:
	GUI_LINES.append(line)

#Definitions and methods
def drawgui():
	for i in range(0,len(GUI_LINES)):
		method.printxy(0,i+1,GUI_LINES[i])