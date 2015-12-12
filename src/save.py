def save(list):
	f = open("../save1.sav","w")
	for index in list:
		if type(i).__name__ == "int":
			f.write("int:" + index + "\n")
		elif type(i).__name__ == "str":
			f.write("str:" + index + "\n")
		elif type(i).__name__ == "list":
			if(isinstance(b in a in index, list)):
				f.write("2st:" + "\n")
				for list1 in index:
					for list2 in list1:
						for element in list2:
							f.write(element + "	")
						f.write("\n")
					f.write("\n")
				f.write("end")
			else:
				f.write("1st:" + "\n")
				for list1 in index:
					for element in list1:
						f.write(element + "	")
					f.write("\n")
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
		elif line[0:4] == "2st:":
			returnList.append("oh noe 2 deee")
		elif line[0:4] == "1st:":
			returnList.append("oh noe 1 deee")
		else:
			returnList.append("not a real type")
	return returnList
	close(f)
	