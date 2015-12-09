import method

for i in MOB_FILES:
	MOBS.append([])
	f=open(i)
	MOBS[COUNT_FILES].append("&RK"+i[16+i.find("/resources/mobs/"):len(i)-4].capitalize()+"&XX")
	for line in f:
		MOBS[COUNT_FILES].append(line)
	COUNT_FILES+=1
	f.close()
for i in range(1,len(MOBS[CURRENT_MOB])): #mob drawing
        method.bufferxy(32,4+i,MOBS[CURRENT_MOB][i])
MOB_MAX_HP=10
MOB_HP=MOB_MAX_HP
Y=int((float(MOB_HP)/float(MOB_MAX_HP))*22.0)
X=55
for i in range(22-Y, 22):
        method.bufferxy(X,i+1,("&GG" if Y > 0.5*22.0 else ("&YY" if Y > 0.25*22.0 else "&RR")) + "XX" + "&XX") #hashtag healthbar
method.printBuffer()
