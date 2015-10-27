import sys
def printxy(x, y, text):
     sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (x, y, text))
     sys.stdout.flush()
def refresh():
	raw_input()
	print(chr(27) + "[2J")
	
for x in range (0,25):
	for y in range(0,50):
		sys.stdout.write('.')
	print
printxy(10,10,"Hello!")
refresh()
printxy(10,10,"......")
printxy(11,10,"Hello!")
refresh()
printxy(11,10,"......")
printxy(12,10,"Hello!")
refresh()
printxy(12,10,"......")
printxy(13,10,"Hello!")
refresh()