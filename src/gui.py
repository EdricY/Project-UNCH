#System imports
import sys

#Module imports
import method

#Definitions and methods

#def drawgui():
#	for i in range(0,len(GUI_LINES)):
#		method.printxy(0,i+1,GUI_LINES[i])

def drawtitle(rows, columns):
	for i in range(0,len(TITLE_LINES)):
		method.printxy(columns/2 - 29, rows/2-11 + i,TITLE_LINES[i])
def drawquitmenu():
	for i in range(0,len(QUIT_LINES)):
		method.bufferxy(12, i+9,QUIT_LINES[i][:-1])
def drawloadmenu():
	for i in range(0,len(LOAD_LINES)):
		method.bufferxy(12, i+9,LOAD_LINES[i][:-1])
def drawnewmenu():
	for i in range(0,len(NEW_LINES)):
		method.bufferxy(11, i+9,NEW_LINES[i][:-1])
def drawreturnmenu(seconds, gold):
	for i in range(0,len(RETURN_LINES)):
		method.bufferxy(10, i+9,RETURN_LINES[i][:-1])
	m, s = divmod(seconds, 60)
	h, m = divmod(m, 60)
	method.bufferxy(14,11,"&MX" + str(h) + " hrs " + str(m) + " mins and " + str(s) + " secs&XX.&GX")
	method.bufferxy(34,13,"&YX" + method.dispBigNum(gold) + "&GX")

#load GUI file.
f=open("../resources/gui/gui.txt")
GUI_LINES = []
for line in f:
	GUI_LINES.append(method.color(line))
f.close()

#load title file.
f=open("../resources/gui/title.txt")
TITLE_LINES = []
for line in f:
	TITLE_LINES.append(method.color(line))
f.close()

#load quitmenu file.
f=open("../resources/gui/quitmenu.txt")
QUIT_LINES = []
for line in f:
	QUIT_LINES.append(line)
f.close()

#load loadmenu file.
f=open("../resources/gui/loadfaled.txt")
LOAD_LINES = []
for line in f:
	LOAD_LINES.append(line)
f.close()

#load newmenu file.
f=open("../resources/gui/welcome.txt")
NEW_LINES = []
for line in f:
	NEW_LINES.append(line)
f.close()

#load returnmenu file.
f=open("../resources/gui/welcomeback.txt")
RETURN_LINES = []
for line in f:
	RETURN_LINES.append(line)
f.close()
