#l1 = []
#l1.append("test string")
#l1.append(15)
#l1.append("test string 2")
#lsub = []
#lsub.append("test")
#lsub.append("test1")
#lsub.append("test2")
#lsub.append("test3")
#l1.append(lsub)
#lsub1 = []
#lsub1.append("test1")
#lsub1.append("test2")
#lsub2 = []
#lsub2.append("test3")
#lsub2.append("test4")
#lsu = []
#lsu.append(lsub1)
#lsu.append(lsub2)
#l1.append(lsu)

def save(ls):
	f = open("../saves/data.save","w")
	for index in ls:
		if type(index).__name__ == "int":
			f.write("int:" + str(index) + "\n")
		elif type(index).__name__ == "str":
			f.write("str:" + index + "\n")
		elif type(index).__name__ == "list":
			if(isinstance(index[0],list)):
				f.write("2dl:" + "\n")
				for list1 in index:
					for element in list1:
						if type(element).__name__ == "int":
							f.write("int:" + str(element) + "	")
						elif type(element).__name__ == "str":
							f.write("str:" + element + "	")
					f.write("\n")
				f.write("end\n")
			else:
				f.write("1dl:")
				for element in index:
					if type(element).__name__ == "int":
						f.write("int:" + str(element) + "	")
					elif type(element).__name__ == "str":
						f.write("str:" + element + "	")
				f.write("\n")
		else:
			f.write("not a real type\n")
	f.close()
		
def load():
	if os.stat("../saves/data.save").st_size <= 2:
		return "NEW"
	f = open("../saves/data.save","r")
	returnList = []
	isLoading2D = False
	firstDim = []
	for line in f:
		line = line.rstrip()
		if isLoading2D:
			if line == "end":
				isLoading2D = False
				returnList.append(firstDim)
				continue
			secondDim = line.split("	")
			index = 0
			while index < len(secondDim):
				if secondDim[index][0:4] == "int:":
					secondDim[index] = int(secondDim[index][4:])
				else:
					secondDim[index] = secondDim[index][4:]
				index += 1
			firstDim.append(secondDim)
		else:
			if line[0:4] == "int:":
				returnList.append(int(line[4:]))
			elif line[0:4] == "str:":
				returnList.append(str(line[4:]))
			elif line[0:4] == "2dl:":
				isLoading2D = True
				firstDim = []
			elif line[0:4] == "1dl:":
				newList = line[4:].split("	")
				index = 0
				while index < len(newList):
					if newList[index][0:4] == "int:":
						newList[index] = int(newList[index][4:])
					else:
						newList[index] = newList[index][4:]
					index += 1
				returnList.append(newList)
			else:
				returnList.append("not a real type")
	return returnList
	f.close()
	

#save(l1)
#print(load())