import os

init_content = []
new_content = []

def getContent(path):
	global init_content
	if os.path.isfile(path) == False:
		print('No file at the specified path!')
		return
	f = open(path,"r")
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
	for l in new_content1[:20]:
		# print('\n\nline no ',new_content1.index(l))
		# print('prev = ',prev)
		# print('l = ',l)

		if prev != "" and areIdentical(prev,l[:len(prev)]):
			# print('repeating line')
			# print('line to append to new_content = ',l[len(prev):])
			new_content.append(l[len(prev):])
			prev = l[:l.index('\t')]
			continue
		if prev == "":
			# print('prev is empty')
			prev = l[:l.index('\t')]
		else:
			prev = ""
		new_content.append(l)


def writeNewContent():
	global new_content
	f = open("DataCollection\\words-keys-cleaned.txt","a")
	for l in new_content:
		#f.write(str(new_content.index(l))+'\n')
		f.write(l)
		#f.write('\n')


def checkText():
	global new_content
	for l in new_content[:20]:
		print('\n\n',l)


getContent("DataCollection\\words-keys.txt")
filterContent()
writeNewContent()
