import math
import sys
import time
def printxy(y, x, text):
        sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (x, y, text))
        sys.stdout.flush()
def wipe():
        for y in range(1,26):
                printxy(1,y,"                                                            ")
def refresh():
        raw_input()
        wipe()
#game loop
FRAMES_PER_SECOND = 1
game_running = True
c=0
while game_running:
        startTime=time.time()
        for a in range(0,30):
                wipe()
                t = math.radians(a+30*c)
                printxy(21,11,math.cos(t))
                printxy(21,12,math.sin(t))
                printxy(math.floor(21.5 + 2*(10 * math.cos(t))),math.floor(11.5 -(10 * math.sin(t))),"X")
                time.sleep(.01)
        c = c+1
        endTime=time.time()
        timeElapsed=endTime-startTime
        sleepTime=1/FRAMES_PER_SECOND-timeElapsed
        time.sleep(sleepTime)
