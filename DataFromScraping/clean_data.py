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
	init_content = all_content
	new_content1 = []
	for l in init_content:
		if '\t' not in l:
			print('line with no tab')
			continue
		new_content1.append(l)

	# prev=""
	# for l in new_content1:
	# 	if prev != "" and areIdentical(prev,l[:len(prev)]):
	# 		new_content.append(l[len(prev):])
	# 		prev = l[:l.index('\t')]
	# 		continue
	# 	if prev == "":
	# 		prev = l[:l.index('\t')]
	# 	else:
	# 		prev = ""
	# 	new_content.append(l)

	for l in new_content1:
		if "sex" in l:
			print('Removed line with sex')
			continue
		if l == '' or '\n\n' in l or l == '\t\n' or l=='\n\t':
			print('not a good line')
			continue
		new_content.append(l)


def filterLine(line):
	if line == None or '\t' not in line:
		return ''

	pair = line.split('\t')

	if len(pair)<2:
		return ''

	if len(pair[0])<2 or len(pair[0]) == len(pair[1]) or pair[1]=='\n':
		return ''

	if pair[0][0] == ' ':
		pair[0] = pair[0][1:]

	if pair[0][-1] == ' ':
		# print('TS')
		pair[0] = pair[0][:-1]

	text = "Europe East Asia years ago"
	if text in pair[0]:
		pair[0] = pair[0][pair[0].index(text):]

	if pair[0][0] == ' ':
		print('PROBLEM')
		pair[0] = pair[0][1:]

	line = pair[0] + '\t' + pair[1]
	print('1. ',pair[0])
	print('2. ',pair[1])


	return line


def isOK(line):
	if line == '':
		return False
	return True


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
	files=glob.glob("*.txt")

	for file in files:
		print(file)
		getContent(file)
		
		for l in init_content:

			l = filterLine(l)
			if isOK(l):
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
	




getAllFilesContent()
print(len(all_content))

