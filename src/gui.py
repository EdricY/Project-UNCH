#System imports
import sys

#Module imports
import method

#Definitions and methods
def drawgui():
	for i in range(0,len(GUI_LINES)):
		method.printxy(0,i+1,GUI_LINES[i])
def drawtitle():
	for i in range(0,len(TITLE_LINES)):
		method.printxy(0,i+1,TITLE_LINES[i])
def drawquitmenu():
	for i in range(0,len(QUIT_LINES)):
		method.bufferxy(12,i+9,QUIT_LINES[i][:-1])
#load GUI file.
f=open("../resources/gui/gui.txt")
GUI_LINES = []
for line in f:
	GUI_LINES.append(method.color(line))
#load title file.
f=open("../resources/gui/title.txt")
TITLE_LINES = []
for line in f:
	TITLE_LINES.append(method.color(line))
#load quitmenu file.
	f=open("../resources/gui/quitmenu.txt")
QUIT_LINES = []
for line in f:
	QUIT_LINES.append(line)
