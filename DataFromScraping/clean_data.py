import os
import glob
import re

init_content = []
new_content = []
all_content = []

def getContent(path):
	global init_content
	if os.path.isfile(path) == False:
		print('No file at the specified path!')
		return
	f = open(path,"r",encoding='utf-8')
	init_content = f.readlines()



def areIdentical(l1,l2):
	for i in range(len(l1)):
		if l1[i] != l2[i]:
			return False
	return True


def filterContent():
	global init_content, new_content

	new_content1 = []
	for l in init_content:
		if '\t' not in l:
			print('line with no tab')
			continue
		new_content1.append(l)

	prev=""
	for l in new_content1:
		if "sex" in l:
			print('Removed line with sex')
			continue
		if prev != "" and areIdentical(prev,l[:len(prev)]):
			new_content.append(l[len(prev):])
			prev = l[:l.index('\t')]
			continue
		if prev == "":
			prev = l[:l.index('\t')]
		else:
			prev = ""
		new_content.append(l)


def writeNewContent(content):
	f = open("keyword_data_new.txt","a",encoding='utf-8')
	for l in content:
		f.write(l)



def checkText():
	global new_content
	for l in new_content[:20]:
		print('\n\n',l)


def getAllFilesContent():
	global all_content,init_content
	files=glob.glob("DataCollection/*.txt")

	for file in files:
		print(file)
		getContent(file)
		print(init_content[0])
		for l in init_content:
			all_content.append(l)
		init_content = []


def removeAll_():
	global init_content,new_content
	for l in init_content:
		# l = re.sub(r'_',r' ',l)
		pair = l.split('\t')
		words1 = pair[0].split(' ')
		words2 = pair[1].split(' ')

		line = ""

		# give up numbers
		for w in words1[:-1]:
			if w!='' and w.isdigit() == False:
				line += w + ' '

		line += words1[-1] + '\t'

		for w in words2[:-1]:
			if w!='' and w.isdigit() == False:
				line += w + ' '		
		
		line += words1[-1] + '\n'

		new_content.append(line)
	




getContent("keyword_data.txt")
print(len(init_content))
