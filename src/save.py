def save(list):
	f = open("../save1.sav","w")
	for index in list:
		if type(i).__name__ == "int":
			f.write("int:" + index + "\n")
		elif type(i).__name__ == "str":
			f.write("str:" + index + "\n")
		elif type(i).__name__ == "list":
			f.write("lst:" + "\n")
		else:
			f.write("not a real type\n")
	close(f)
		
def load():
	f = open("../save1.sav","r")
	returnList = []
	for line in f:
		if line[0:4] == "int:":
			returnList.append(int(line[4:]))
		elif line[0:4] == "str:":
			returnList.append(str(line[4:]))
		elif line[0:4] == "list:":
			returnList.append("oh noe")
		else:
			returnList.append("not a real type")
	return returnList
	close(f)
	