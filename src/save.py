l1 = []
l1.append("test string")
l1.append(15)
l1.append("test string 2")
lsub = []
lsub.append("test")
lsub.append("test")
l1.append(lsub)
lsub1 = []
lsub1.append("test1")
lsub1.append("test2")
lsub2 = []
lsub2.append("test3")
lsub2.append("test4")
lsu = []
lsu.append(lsub1)
lsu.append(lsub2)
l1.append(lsu)

def save(ls):
	f = open("../save1.sav","w")
	for index in ls:
		if type(index).__name__ == "int":
			f.write("int:" + str(index) + "\n")
		elif type(index).__name__ == "str":
			f.write("str:" + index + "\n")
		elif type(index).__name__ == "list":
			if(isinstance(index[0],list)):
				f.write("2st:" + "\n")
				for list1 in index:
					for element in list2:
						f.write(element + "	")
					f.write("\n")
				f.write("end\n")
			else:
				f.write("1st:" + "\n")
				for element in index:
					f.write(element + "	")
				f.write("\n")
		else:
			f.write("not a real type\n")
	f.close()
		
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
	f.close()
	

save(l1)