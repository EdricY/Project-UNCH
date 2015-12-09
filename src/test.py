import method

MOB_MAX_HP=10
MOB_HP=MOB_MAX_HP
Y=int((float(MOB_HP)/float(MOB_MAX_HP))*22.0)
X=55
for i in range(22-Y, 22):
  method.bufferxy(X,i+1,  "XX")#("&GG" if Y > 0.5*22.0 else ("&YY" if Y > 0.25*22.0 else "&RR")) + "XX" + "&XX") #hashtag healthbar
method.printBuffer()
