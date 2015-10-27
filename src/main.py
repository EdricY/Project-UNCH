import sys
for x in range (0,25):
	for y in range(0,25):
		print '.',
	print
print "Setup complete, please wait..."
def printxy(x, y, text):
     sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (x, y, text))
     sys.stdout.flush()
printxy(10,10,"Hello!")