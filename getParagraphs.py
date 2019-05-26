

def writeParagraph(par,nr,filename):
	# Write one paragraph a line (enter between paragraphs)
	f = open("paragraphs/"+ filename +"-paragraphs.txt",'a')
	try:
		f.write(nr + ". " + par + '\n')
	except UnicodeEncodeError:
		pass

def goodParagraph(par,no_spaces,min_lim,max_lim):
	if par=="" or no_spaces<min_lim or no_spaces>max_lim:
		return False
	return True

def getNoSpaces(string):
	return len([e for e in string if e==' '])

def separatePar(par,no_spaces,min_lim,max_lim,i,filename):
	# Separate into paragraphs than contain min 40 and max 80 spaces & no double '\n's

	## Estimate no of subparagraphs & no of spaces per subparagraph
	count = 1
	while no_spaces>max_lim:
		no_spaces = int(no_spaces/2)
		count = count * 2

	# create vector containing all positions of '.', respectively ' ' in paragraph
	dotPos = [pos for pos, char in enumerate(par) if char == '.']
	spacePos = [pos for pos, char in enumerate(par) if char == ' ']

	startIndex=0 # start index for current paragraph
	indexSpacePos = 0 # current index in spacePos list

	sumdiff = 0 # accumulates the carry-over of spaces per paragraphs

	while indexSpacePos+no_spaces<len(spacePos) and count>1:

		posSpace = spacePos[indexSpacePos+no_spaces]
		posDot = next((e for e in dotPos if e>=posSpace), None)

		writeParagraph(par[startIndex:posDot+1],str(i),filename)
		i=i+1

		currNoSpaces = getNoSpaces(par[startIndex:posDot+1])
		diff = no_spaces - currNoSpaces
		sumdiff = sumdiff + diff;

		# If carry-over accumulates the number of spaces per subparagraph, 
		# then the number of subparagraphs decreases
		if sumdiff >= no_spaces:
			count = count-1
			sumdiff = 0

		startIndex = posDot+1
		posSpace = next((e for e in spacePos if e>=startIndex), None)
		if posSpace != None:
			indexSpacePos = spacePos.index(posSpace)
		else:
			break
		count = count - 1

	if startIndex<len(par)-2:
		writeParagraph(par[startIndex:],str(i),filename)
		i=i+1

	return i


def extract_paragraphs(content):

	flag = 0; max_len = 0; par = ""
	no_spaces=0; i=1
	max_lim = 80; min_lim = 40 # unit = spaces
	for x in content:
		if x == ' ':
			no_spaces=no_spaces+1	
		if x == '\n':
			if flag == 1:
				flag = 0
				if no_spaces > max_len:
					max_len = no_spaces
				
				if '\n' in par or '\r' in par:
					par.replace('\n',' ')
					par.replace('\r',' ')
				if goodParagraph(par,no_spaces,min_lim,max_lim)==True:
					writeParagraph(par,str(i),filename)
					i=i+1
					no_spaces = 0
					par = ""
				else:
					if no_spaces>max_lim:
						if par[len(par)-1]!='.':
							par = par + '.'
						i=separatePar(par,no_spaces,min_lim,max_lim,i,filename)
						no_spaces = 0
						par = ""
					else:
						if (no_spaces != 0):
							par = par + ' '
							pass
						else:
							par = ""
						
			else:
				flag=flag+1
		else:
			flag = 0
			par = par + str(x)

	# print("Number of paragraphs = i-1 = "+ str(i-1))

import glob
import os
files=glob.glob("books/*.txt")
print(files)
for file in files:
	f = open(file, "r",encoding='UTF-8') 
	content = f.read()
	filename = file[file.index('\\')+1:file.index('.')]

	exists = os.path.isfile("paragraphs/"+ filename +"-paragraphs.txt")
	if exists:
		print(filename +"-paragraphs.txt already exists")
	else:
		print(filename)
		extract_paragraphs(content)

	f.close()
