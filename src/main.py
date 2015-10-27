import sys
def printxy(x, y, text):
     sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (x, y, text))
     sys.stdout.flush()
for x in range (0,25):
	for y in range(0,50):
		sys.stdout.write('.')
	print
printxy(10,10,"Hello!")
raw_input()
printxy(10,10,"......")
printxy(10,11,"Hello!")
raw_input()
printxy(10,11,"......")
printxy(10,12,"Hello!")
raw_input()
printxy(10,12,"......")
printxy(10,13,"Hello!")
raw_input()