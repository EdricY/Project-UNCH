#system import
import sys

import main

#Definitions and methods
def printxy(y, x, text):
	sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (x, y, text))
	sys.stdout.flush()
	
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
def inputhandler():
	while main.GAME_RUNNING:
		g = getch.getch()
		while g != '.' and g != '>':
			g = getch.getch()
		main.hit()
		g = getch.getch()
		while g != ',' and g != '<':
			g = getch.getch()
		main.hit()
