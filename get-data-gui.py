import os
from tkinter import *
import tkinter.messagebox as messagebox
import nltk
from nltk.tokenize import sent_tokenize
from tkinter import font
from googletrans import Translator
from bs4 import BeautifulSoup
import requests
from lxml import html
import glob
import getParagraphs


translator = Translator()
content = []
par_no = 0
book_opened = False
list_buttons_pos = []
list_buttons_comb = []
list_buttons_check = []
list_buttons_content = []
list_buttons_chosen = []
list_in_words = []
all_comb = []
under_frame_y = 400
page_link = ''
parFont = ('times', 12)
fonts = [9,10,11,12,13,14]
items_to_destroy = []
filtered_par = []
books=[]


def updateListOfBooks():
	global books
	try:
		files=glob.glob("paragraphs/*.txt")

		for file in files:
			filename = file[file.index('\\')+1:file.index('.')]
			i = filename.find('paragraphs')-1
			filename = filename[:i]

			f = open("Data\\books.txt","r+")
			content = f.readlines()

			list = []
			for line in content:
				line = re.sub(r"\n",r'',line)
				if line != '':
					if ',' in line:
						list.append(line[:line.index(',')])

			if filename not in list:
				# print(filename,' not in content')
				title = re.sub(r"-", r" ", filename)
				f.write(filename+','+title+'\tAuthor\n')
	except:
		catchError("Something went wrong when trying to update the list of books! \nPlease contact Mihaela Nichita.")
		return


def loadBooks():
	global books
	try:
		updateListOfBooks()
		f = open("Data\\books.txt","r")
		content = f.readlines()
		for line in content:
			line = re.sub(r"\n",r'',line)
			if line != '':
				book = (line[:line.index(',')],line[line.index(',')+1:line.index('\t')],line[line.index('\t')+1:])
				# print('book = ', book)
				books.append(book)
	except:
		catchError("Something went wrong when trying to load books! \nPlease contact Mihaela Nichita.")
		return

loadBooks()



def catchError(text):
	messagebox.showwarning("Warning",text)
	f = open("Data\\error_log.txt","a")
	f.write(text+"\n")
	f.close()

def shiftLeftButtons(list_buttons, index):
	if index is len(list_buttons) - 1:
		return

	n = len(list_buttons_chosen)
	for b in list_buttons_chosen[index + 1:n]:
		i = list_buttons_chosen.index(b)
		newX = list_buttons_chosen[i - 1].winfo_x()
		newY = list_buttons_chosen[i - 1].winfo_y()
		b.place(x=newX, y=newY)


def deleteButtonWhenClicked(event):
	global items_to_destroy
	removeButtons(items_to_destroy)
	caller = event.widget
	index = list_buttons_chosen.index(caller)

	# First shift to the left all the buttons starting the one at index+1
	shiftLeftButtons(list_buttons_chosen, index)

	# Then remove the button from the list
	list_buttons_chosen.remove(caller)
	caller.destroy()


def deleteButton(caller):
	global list_buttons_chosen
	index = list_buttons_chosen.index(caller)

	# First shift to the left all the buttons starting the one at index+1
	shiftLeftButtons(list_buttons_chosen, index)

	# Then remove the button from the list
	list_buttons_chosen.remove(caller)
	caller.destroy()


def showMessage(text,x,y):
	global window
	msg = Message(window, text=text, width=200)
	msg.config(bg='lightgreen', font=('times', 9))
	msg.place(x=x, y=y)

	items_to_destroy.append(msg)

def createChosenList(caller):
	global list_buttons_chosen,list_in_words, window

	if len(list_buttons_chosen) == 9:
		messagebox.showwarning("Warning","Only 9 words allowed!")
		return

	# if len(caller['text'])<2 and caller['text'] not in range(10):
	#     return

	if caller['text'] in [b['text'] for b in list_buttons_chosen]:
		showMessage('Word already in the list',x=500,y=32)
		return

	new_button = Button(window, text=caller['text'], borderwidth=1, relief='solid')
	new_button.bind("<Button-3>", deleteButtonWhenClicked)
	new_button.bind("<Button-1>", linkWords)

	if len(list_buttons_chosen) == 0:
		new_button.place(x=610, y=under_frame_y, height=25, width=95)
	else:
		new_button.place(x=610 + (len(list_buttons_chosen) % 4) * 100,
						 y=under_frame_y + int(len(list_buttons_chosen) / 4) * 30, height=25, width=95)
	list_buttons_chosen.append(new_button)
	list_in_words.append(caller['text'])


def itsaKeyWord(event):
	caller = event.widget
	caller.configure(bg='lightpink', borderwidth=2)
	createChosenList(caller)


def justaWord(event):
	global list_in_words
	caller = event.widget
	if caller['text'] in [',','.','!','?']:
		return
	caller.configure(bg='lightpink', borderwidth=2)
	createChosenList(caller)


def translate(event):
	try:
		global items_to_destroy, window
		removeButtons(items_to_destroy)
		caller = event.widget
		toTrans = caller['text']
		r = translator.translate(toTrans, dest='ro')
		translate_frame = Text(window, height=10, width=30, borderwidth=2, relief='groove')
		translate_frame.place(x=760, y=60)
		translate_frame.configure(bg="#f1f1f1")
		translate_frame.insert(END, ' ' + toTrans + ' = ')
		translate_frame.insert(END, r.text)
	except:
		catchError("Something went wrong when trying to translate this word! \nCheck your connection to the internet.")
		return


def insert_text(par):
	try:
		global parFont, content_frame
		lastx, lasty = 0, 0
		#tok_text = nltk.word_tokenize(par)
		par = re.sub(r"([.!?,:])", r" \1 ", par)
		tok_text = []
		for w in par.split(' '):
			if w not in ['',' ','\n']:
				tok_text.append(w)
		
		tok_text1 = []
		for w in tok_text:
			w.strip()
			if w != '':
				tok_text1.append(w)

		for w in tok_text1:
			if lastx + len(w) * 10 > 550:
				lastx, lasty = 0, lasty + 30

			new_button = Button(content_frame, text=w, borderwidth=0, fg='#0F1626',font=parFont)
			new_button.place(x=lastx, y=lasty, height=25)
			list_buttons_content.append(new_button)
			new_button.bind("<Button-1>", justaWord)
			new_button.bind("<Button-3>", translate)

			if w in filtered_par:
				new_button.bind("<Button-1>", itsaKeyWord)
				new_button.configure(bg='#bdbdbd')

			content_frame.update_idletasks()
			lastx += new_button.winfo_width()
			if w in ".:!?,": lastx += 10
	except:
		catchError("Something went wrong when trying to insert text! \nPlease contact Mihaela Nichita.")
		return


def appendParToContent(paragraphs):
	global content
	for p in paragraphs:
		if p.text is not '' and ' ' in p.text:
			par = re.sub(r'YOU ARE READING', ' ', p.text)
			content.append(par)


def getParFromWebPage():
	global e, content, window
	try:
		page_link = e.get()
		if 'wattpad' in page_link:
			paragraphs = ''
			while True:
				headers = {
					'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
				result = requests.get(page_link, headers=headers)
				page_content = BeautifulSoup(result.content.decode(), "lxml")
				paragraphs = page_content.find_all("p")
				appendParToContent(paragraphs)

				next_page_link = page_content.find('link', attrs={'rel': 'next'})
				if next_page_link is None:
					next_page_link = page_content.find('a', attrs={'class': 'on-navigate next-part-link'})

				if next_page_link is None:
					break

				page_link = next_page_link['href']

		else:
			page_response = requests.get(page_link, timeout=5)
			page_content = BeautifulSoup(page_response.content, "html.parser")
			paragraphs = page_content.find_all("p")
			appendParToContent(paragraphs)

		"* Add title of article *"
		title = page_content.find("title").text
		m_title = Message(window, text=title, width=700)
		m_title.config(font=('times', 12, 'bold'))
		m_title.place(x=345, y=5)
	except:
		catchError("Something went wrong when trying to access the article! \nCheck your connection to the internet.")
		return


def combineParagraphs():
	global content
	new_content = []
	carry = ''
	for p in content:
		# print('\n\np = ',p)
		if carry != '':
			p=carry+' '+p
			carry = ''
		# print('\n\np = ',p)

		tok_par = p.split(' ')
		# print('len(tok_par) = ',len(tok_par))
		if len(tok_par)<30:
			# print('short paragraph')
			carry = p
		if len(tok_par)>100:
			# print('long paragraph')
			# print('tok_par[100] = ',tok_par[100])
			i = p.find(tok_par[100],450)
			currentPar = p[:i]
			new_content.append(currentPar)
			carry = p[i:]

		if len(tok_par)>30 and len(tok_par)<100:
			new_content.append(p)

	while carry != '':
		# print('carry left: ',carry)
		tok_par = carry.split(' ')
		
		if len(tok_par)>100:
			# print('tok_par[100] = ',tok_par[100])
			i = carry.find(tok_par[100],450)
			currentPar = carry[:i]
			new_content.append(currentPar)
			carry = carry[i:]
		else:
			new_content.append(carry)
			break

	content = new_content


def open_book(event):
	global content, book_opened, list_in_words, list_buttons_content, window
	book_opened = True

	list_buttons_content = removeButtons(list_buttons_content)
	caller = event.widget

	if caller['text'] != 'OK':
		bookNames = [e[1] for e in books]
		bookName = books[bookNames.index(caller['text'])][0]
		f = open("paragraphs/" + bookName + "-paragraphs.txt", 'r')
		content = f.readlines()

		"* Add title of book *"
		m_title = Message(window, text=caller['text'], width=700)
		m_title.config(font=('times', 12, 'bold'))
		m_title.place(x=345, y=5)
	else:
		getParFromWebPage()

	combineParagraphs()
	getFilteredPar(content[0])
	insert_text(content[par_no])
	list_in_words = filtered_par


def removeButtons(list_buttons):
	for e in list_buttons:
		e.destroy()
	list_buttons = []
	return list_buttons


def change_par():
	if book_opened == False:
		catchError( "Please open a book first!")
		return

	try:

		global par_no, content, all_comb, list_in_words, list_buttons_chosen, items_to_destroy
		global list_buttons_check, list_buttons_comb, list_buttons_content, b_par_no
		all_comb = []

		# Remove previous buttons
		list_buttons_check = removeButtons(list_buttons_check)
		list_buttons_comb = removeButtons(list_buttons_comb)
		list_buttons_content = removeButtons(list_buttons_content)
		list_buttons_chosen = removeButtons(list_buttons_chosen)
		removeButtons(items_to_destroy)

		nr = par_no
		if nr < 0:
			nr += len(content)
		b_par_no['text'] = str(nr + 1)

		getFilteredPar(content[par_no])
		insert_text(content[par_no])
		list_in_words = filtered_par
	except:
		catchError("Something went wrong when trying to change the paragraph! \nPlease contact Mihaela Nichita.")
		return


def prev_par(event):
	global par_no
	par_no = par_no - 1
	if par_no < -len(content):
		par_no = 0
	change_par()


def next_par(event):
	global par_no
	par_no = par_no + 1
	if par_no > len(content) - 1:
		par_no = 0
	change_par()

# Get filtered_par which won't contain stop words -> no more POS tagging
def getFilteredPar(par):
	# try:
		# Remove Punctuation
		par = re.sub(r'[^\w\s]', ' ', par)
		# par = re.sub(r" \'\w", r"\'\w", par) # for not separating "don" from "\'t"
		par = par.lower() 

		## Word tokenization
		tok_text = []
		for w in par.split(' '):
			if w not in [' ','']:
				tok_text.append(w)

		for w in tok_text:
			w.strip()

		# Removing Stopwords
		from nltk.corpus import stopwords
		stop_words = set(stopwords.words("english"))
		
		global filtered_par
		for w in tok_text:
			if w not in stop_words and w not in filtered_par:
				filtered_par.append(w)
	# except:
	#     catchError("Something went wrong when trying to identify the parts of speech! \nPlease contact Mihaela Nichita.")
	#     return


def createButtons(list, xi, yi, col):
	try:
		global list_buttons_pos, list_buttons_comb, window
		i = 0
		for item in list:
			new_button = Button(window, text=item, borderwidth=1, relief='groove')
			if col:
				new_button.place(x=xi, y=yi + i * 30, width=95, height=25)
				list_buttons_pos.append(new_button)
			else:
				new_button.place(x=xi + i * 100, y=yi, width=95, height=25)
				list_buttons_comb.append(new_button)
			i = i + 1
	except:
		catchError("Something went wrong when trying to create buttons! \nPlease contact Mihaela Nichita.")
		return


def check_comb(event):
	try:
		global list_buttons_chosen
		if len(list_buttons_chosen)>6:
			messagebox.showwarning("Warning","Only 9 words allowed!")
			return
		caller = event.widget
		index = caller['text']
		index = int(index) * 3
		for i in [index - 3, index - 2, index - 1]:
			createChosenList(list_buttons_comb[i])
	except:
		catchError("Something went wrong when trying to send the combination to the list of chosen words! \nPlease contact Mihaela Nichita.")
		return

# not used
def getRand(n):
	import random
	return random.randint(0, n - 1)

# not used
def genComb(event):
	if book_opened == False:
		catchError( "Please open a book first!")
		return

	try:
		global filtered_par, all_comb, list_buttons_check, window

		# POS tagging
		parts_of_speech = nltk.pos_tag(filtered_par)

		# Get Nouns
		nouns = [e[0] for e in parts_of_speech if 'NN' in e[1]]

		# Get Actions
		verbs = [e[0] for e in parts_of_speech if 'VB' in e[1] or 'RB' in e[1]]

		# Get Adjectives
		adj = [e[0] for e in parts_of_speech if 'JJ' in e[1]]
		nn = len(nouns)
		nv = len(verbs)
		na = len(adj)

		n = 5
		left = nn * nv * na - len(all_comb)
		if 6 >= left:
			n = left
			catchError( "These are the last combinations left!")

		for e in range(1, n + 1):
			new_button = Button(window, text=str(e + len(all_comb)), borderwidth=1, relief='groove')
			new_button.place(x=140, y=under_frame_y + e * 30, width=35, height=25)
			new_button.bind("<Button-1>", check_comb)
			list_buttons_check.append(new_button)

		for i in range(n):
			r = [getRand(nn), getRand(nv), getRand(na)]
			while r in all_comb:
				# r is a Duplicate
				r = [getRand(nn), getRand(nv), getRand(na)]

			all_comb.append(r)
			createButtons([nouns[r[0]], verbs[r[1]], adj[r[2]]], 185, under_frame_y + (i + 1) * 30, False)
	except:
		catchError("Something went wrong when trying to generate combinations of words! \nPlease contact Mihaela Nichita.")
		return


def resetColors():
	next_par('<Button-1>')
	prev_par('<Button-1>')


def reset(event):
	try:
		global list_buttons_chosen, button_link_w,par_no,e2,b_par_no
		if event.widget['text'] == 'OK':
			if int(e2.get())>0 and int(e2.get())<=len(content):
				par_no = int(e2.get())-1
			else:
				catchError('The number is not within the specified range!')
				return
		removeButtons(items_to_destroy)
		list_buttons_chosen = removeButtons(list_buttons_chosen)
		list_in_words = filtered_par
		resetColors()
		button_link_w.configure(bg='#D3D3D3', fg='black',text = 'Link Words')
	except:
		catchError( "Something went wrong when resetting! \nPlease contact Mihaela Nichita.")
		return


def sendComb(event):
	global list_in_words, list_buttons_chosen
	list_out_words = []

	try:
		if len(list_buttons_chosen)<2:
			messagebox.showwarning("Warning",'Minimum 2 words needed')
			return
		for b in list_buttons_chosen:
			list_out_words.append(b['text'])

		f = open("Data/Data.txt", 'a')
		for w in list_in_words:
			f.write(w + " ")
		f.write('\t')

		for w in list_out_words:
			f.write(w + " ")
		f.write('\n')

		removeButtons(list_buttons_chosen)
		next_par('<Button-1>')
	except:
		catchError("Something went wrong when trying to send words to the file! \nPlease contact Mihaela Nichita.")
		return


def getInfo():
	try:
		global window
		how_to = Toplevel(window)
		how_to.title('GUIDELINE')
		how_to.geometry("500x600")

		guideline = Frame(how_to, height=500, width=400, borderwidth=2, relief='groove', bg='lightgreen')
		guideline.place(x=30, y=30)

		m0 = 'GUIDELINE'
		m1 = 'TARGET: Enjoy reading Books or Articles you like & help in developing a tool for you to REMEMBER everything you read easier.'
		m2 = 'STEPS:'
		m3 = '1. Select the BOOK or ARTICLE you want to read. Menu -> "Open"'
		m4 = '2. Read the paragraph and left-click the words you consider RELEVANT and MEMORABLE. (2 to 9 per paragraph)'
		m5 = 'Right-click the words in order to get its TRANSLATION to Romanian.'
		m6 = '3. Press the "Hint" button in the bottom-left to get random combinations of words.'
		m7 = 'If you like any of those combinations, left-click its coresponding number in order to send them to the chosen RELEVANT words.'
		m8 = '4. Right-click a word in "Chosen" words in order to remove it from the ones that are to be sent as the BEST choice of RELEVANT combination of words'
		m9 = '5. Press "Send" button when you feel that the list of words labeled as "Chosen" looks simply UNFORGETABLE.'
		m10 = '6. Navigate through paragraphs using "<<" and ">>" buttons.'

		msg1 = Message(how_to, text=m1, width=380)
		msg1.config(bg='lightgreen', font=('times', 9))
		msg1.place(x=35, y=40)

		msg2 = Message(how_to, text=m2, width=380)
		msg2.config(bg='lightgreen', font=('times', 9, 'bold'))
		msg2.place(x=35, y=80)

		msg3 = Message(how_to, text=m3, width=380)
		msg3.config(bg='lightgreen', font=('times', 9))
		msg3.place(x=40, y=100)

		msg4 = Message(how_to, text=m4, width=380)
		msg4.config(bg='lightgreen', font=('times', 9))
		msg4.place(x=40, y=122)

		msg5 = Message(how_to, text=m5, width=380)
		msg5.config(bg='lightgreen', font=('times', 9))
		msg5.place(x=50, y=155)

		msg6 = Message(how_to, text=m6, width=380)
		msg6.config(bg='lightgreen', font=('times', 9))
		msg6.place(x=40, y=185)

		msg7 = Message(how_to, text=m7, width=380)
		msg7.config(bg='lightgreen', font=('times', 9))
		msg7.place(x=50, y=220)

		msg8 = Message(how_to, text=m8, width=380)
		msg8.config(bg='lightgreen', font=('times', 9))
		msg8.place(x=40, y=260)

		msg9 = Message(how_to, text=m9, width=380)
		msg9.config(bg='lightgreen', font=('times', 9))
		msg9.place(x=40, y=300)

		msg10 = Message(how_to, text=m10, width=380)
		msg10.config(bg='lightgreen', font=('times', 9))
		msg10.place(x=40, y=340)
	except:
		catchError("Something went wrong when trying to open information window! \nPlease contact Mihaela Nichita.")
		return


def myfunction(event):
	global canvas
	canvas.configure(scrollregion=canvas.bbox("all"),width=300,height=400)


def data(frame):
	for i in range(len(books)):
		book = books[i]
		b = Button(frame, text=book[1], command=books_list.destroy, font=('times', 9))
		b.grid(row=i,column=1)
		b.configure(borderwidth=0)
		b.bind("<Button-1>", open_book)

		a = Button(frame, text=book[2], font=('times', 9))
		a.grid(row=i,column=2)
		a.configure(borderwidth=0)

		Label(frame,text=i).grid(row=i,column=0)


global canvas
def openBooksList():
	if book_opened is True:
		catchError( "Please EXIT first, then open the App again!")
		return
	try:
		global books_list, window, canvas
		books_list = Toplevel(window)
		books_list.title('Books List')
		books_list.geometry("500x600")

		label_books = Label(books_list, text='Books:', font=('times', 9, 'bold'))
		label_books.place(x=100, y=30)

		label_authors = Label(books_list, text='Authors:', font=('times', 9, 'bold'))
		label_authors.place(x=250, y=30)

		myframe=Frame(books_list,relief=GROOVE,width=400,height=300,bd=1)
		myframe.place(x=20,y=60)

		canvas=Canvas(myframe)
		frame=Frame(canvas)
		myscrollbar=Scrollbar(myframe,orient="vertical",command=canvas.yview)
		canvas.configure(yscrollcommand=myscrollbar.set)

		myscrollbar.pack(side="right",fill="y")
		canvas.pack(side="left")
		canvas.create_window((0,0),window=frame,anchor='nw')
		frame.bind("<Configure>",myfunction)
		data(frame)

		m = Message(books_list,text="If you've added new books to the library ->",width=250 )
		m.place(x=20,y=480)
		b = Button(books_list, text='UPDATE', font=('times', 10))
		b.place(x=260,y=480)
		b.configure(bg='lightpink')
		b.bind("<Button-1>",updateLibrary)

	except:
	    catchError("Something went wrong when trying to open the list of books! \nPlease contact Mihaela Nichita.")
	    return


def getParagraphsFromBooks():
	try:
		filename = ''
		content = ''
		files=glob.glob("books/*.txt")
		# print(files)
		for file in files:
			f = open(file, "r",encoding='UTF-8') 

			content = f.read()
			filename = file[file.index('\\')+1:file.index('.')]

			exists = os.path.isfile("paragraphs/"+ filename +"-paragraphs.txt")
			if exists:
				print(filename +"-paragraphs.txt already exists")
			else:
				# print(filename)
				getParagraphs.extract_paragraphs(content,filename)

			f.close()	
	except:
	    catchError("Something went wrong when trying to get paragraphs from books! \nPlease contact Mihaela Nichita.")
	    return


def updateLibrary(event):
	getParagraphsFromBooks()
	loadBooks()


def openWebSite(event):
	try:
		caller = event.widget
		import webbrowser
		webbrowser.open(caller['text'] + '.com', new=2)
	except:
		catchError("Something went wrong when trying to open the browser! \nPlease contact Mihaela Nichita.")
		return


global e
def openArticlesList():
	if book_opened is True:
		catchError( "Please EXIT first, then open the App again!")
		return

	global e,window
	try:
		art_list = Toplevel(window)
		art_list.title('Articles List')
		art_list.geometry("800x200")

		l = Label(art_list, text='Link:')
		l.place(x=30, y=30)
		l.configure(bg='black', fg='white')

		m_info = Message(art_list,
						 text='Copy and Paste below the full link of the article you\'d like to read. Also, make sure you are connected to internet.',
						 width=700)
		m_info.config(bg='lightgreen', font=('times', 9))
		m_info.place(x=120, y=5)

		r = Label(art_list, text='Recommendations:')
		r.place(x=30, y=60)
		r.configure(bg='black', fg='white')

		b1 = Button(art_list, text='Lifehacker', command=art_list.destroy, font=('times', 9))
		b1.place(x=160, y=60)
		b1.configure(borderwidth=0)
		b1.bind("<Button-1>", openWebSite)

		b2 = Button(art_list, text='Vice', command=art_list.destroy, font=('times', 9))
		b2.place(x=160, y=80)
		b2.configure(borderwidth=0)
		b2.bind("<Button-1>", openWebSite)

		b3 = Button(art_list, text='Wattpad', command=art_list.destroy, font=('times', 9))
		b3.place(x=160, y=100)
		b3.configure(borderwidth=0)
		b3.bind("<Button-1>", openWebSite)

		e = Entry(art_list, text='Enter page link of the article here...', width=100)
		e.place(x=120, y=30)

		b = Button(art_list, text='OK', borderwidth=2, relief=GROOVE, command=art_list.destroy)
		b.place(x=730, y=30)
		b.bind('<Button-1>', open_book)
	except:
		catchError("Something went wrong when trying to open the articles window! \nPlease contact Mihaela Nichita.")
		return


def setFont(fontWanted):
	global parFont,b_font

	b_font['text'] = fontWanted
	if parFont[1] != fontWanted and book_opened:
		parFont = ('times',fontWanted)
		changeFontCurrentParagraph()
	else:
		parFont = ('times',fontWanted)
   

def changeFontCurrentParagraph():
	resetColors()


def changeFont(event):
	caller = event.widget
	currentFont = caller['text']
	global fonts,window

	popup = Menu(window, tearoff=0)
	popup.add_command(label=9,command=lambda: setFont(9))
	popup.add_command(label=10,command=lambda: setFont(10))
	popup.add_command(label=11,command=lambda: setFont(11))
	popup.add_command(label=12,command=lambda: setFont(12))
	popup.add_command(label=13,command=lambda: setFont(13))
	popup.add_command(label=14,command=lambda: setFont(14))

	try:
		popup.tk_popup(event.x_root, event.y_root, 0)
	finally:
		# make sure to release the grab (Tk 8.0a1 only)
		popup.grab_release()


click1 = False
toBeLinked = []
def linkWords(event):
	global button_link_w
	if button_link_w['bg'] != 'black':
		return

	global list_buttons_chosen,toBeLinked
	if len(toBeLinked) == 2:
		messagebox.showwarning("Warning",'Not allowed to link more than 2 words at a time!')
	
	caller = event.widget
	# link 2 or 3 words
	toBeLinked.append(list_buttons_chosen.index(caller))
	caller['bg'] = 'lightpink'


def changeColor(event):
	global toBeLinked, list_buttons_chosen, button_link_w
	if button_link_w['bg'] != 'black':
		button_link_w.configure(bg='black', fg='white',text = 'OK')
	else:
		if len(toBeLinked)<2:
			messagebox.showwarning("Warning",'No words to link.')

		if len(toBeLinked)==2:
			list_buttons_chosen[toBeLinked[0]]['text'] += '_' + list_buttons_chosen[toBeLinked[1]]['text']
			deleteButton(list_buttons_chosen[toBeLinked[1]])
	
		toBeLinked = []
		button_link_w.configure(bg='#D3D3D3', fg='black',text = 'Link Words')
  
global e2
def goToParWindow(event):
	global b_par_no, window,par_no,e2

	if book_opened == False:
		catchError( "Please open a book first!")
		return
	try:
		go_to = Toplevel(window)
		go_to.title('Articles List')
		go_to.geometry("300x100")

		l = Label(go_to, text='Link:')
		l.place(x=30, y=30)
		l.configure(bg='black', fg='white')

		m_info = Message(go_to,text='Enter a number between 1 and '+str(len(content)),width=250)
		m_info.config(bg='lightgreen', font=('times', 9))
		m_info.place(x=30, y=5)

		e2 = Entry(go_to, width=10)
		e2.place(x=65, y=30)

		b = Button(go_to, text='OK', borderwidth=2, relief=GROOVE, command=go_to.destroy)
		b.place(x=130, y=30)
		b.bind('<Button-1>', reset)
	except:
		catchError("Something went wrong when trying to go to the desired paragraph! \nPlease contact Mihaela Nichita.")
		return 


def populateWindow():
	global window, b_par_no, button_link_w, b_font
	menubar = Menu(window)

	# create a pulldown menu, and add it to the menu bar
	filemenu1 = Menu(menubar, tearoff=0)
	filemenu1.add_command(label="Book", command=openBooksList)  # call open_book
	filemenu1.add_command(label="Article", command=openArticlesList)
	filemenu1.add_separator()
	filemenu1.add_command(label="Exit", command=window.quit)

	menubar.add_cascade(label="Open", menu=filemenu1)
	menubar.add_cascade(label="How to", command=getInfo)  # call getInfo

	window.config(menu=menubar)

	m_info1 = Message(window, text='In order to change the book/article, go Open -> Exit. Then start the app again.',
					 width=90)
	m_info1.config(bg='lightgreen', font=('times', 9))
	m_info1.place(x=25, y=60)

	m_info2 = Message(window, text='You can always skip paragraphs.',
					 width=90)
	m_info2.config(bg='lightpink', font=('times', 9))
	m_info2.place(x=25, y=150)

	m_info3 = Message(window, text="Do they trigger Images in your Mind's Eye?",width=300)
	m_info3.config(font=('verdana', 10))
	m_info3.place(x=610, y=under_frame_y-30)

	m_update = Message(window, text='UPDATEs: \n1. Now you can link words if they look better together. Press "Link Words", select 2 words and press OK.\n'+
		'\n2. For reading a specific paragraph, Press the button which indicates the paragraph number.',width=200)
	m_update.config(bg='lightblue', font=('calibre', 10))
	m_update.place(x=185, y=under_frame_y)

	# PARAGRAPH related: #
	label_paragraph = Label(window, text="Paragraph:")
	label_paragraph.place(x=140, y=32, width=100, height=22)
	label_paragraph.configure(bg='black', fg='white')

	button_prev_par = Button(window, text="<<", borderwidth=2, relief='groove')
	button_prev_par.place(x=243, y=32, width=22, height=22)
	button_prev_par.bind("<Button-1>", prev_par)

	button_next_par = Button(window, text=">>", borderwidth=2, relief='groove')
	button_next_par.place(x=303, y=32, width=22, height=22)
	button_next_par.bind("<Button-1>", next_par)

	b_par_no = Button(window, text='1', borderwidth=2, relief='groove')
	b_par_no.config(font=('times', 9, 'italic'))
	b_par_no.place(x=267, y=32, width=35, height=22)
	b_par_no.bind("<Button-1>",goToParWindow)

	# FONT related #
	label_font = Label(window, text="Font:")
	label_font.place(x=370, y=32, width=80, height=22)
	label_font.configure(bg='black', fg='white')

	b_font = Button(window, text='12', borderwidth=2, relief='groove')
	b_font.config(font=('times', 9, 'italic'))
	b_font.place(x=453, y=32, width=35, height=22)
	b_font.bind("<Button-1>", changeFont)

	button_reset = Button(window, text="Reset", borderwidth=2, relief='groove')
	button_reset.place(x=505, y=under_frame_y + 60, width=100, height=25)
	button_reset.bind("<Button-1>", reset)

	label_chosen = Label(window, text="Chosen:")
	label_chosen.place(x=505, y=under_frame_y, width=100, height=25)
	label_chosen.configure(bg='black', fg='white')

	button_link_w = Button(window, text="Link Words", borderwidth=2, relief='groove')
	button_link_w.place(x=505, y=under_frame_y + 30, width=100, height=25)
	button_link_w.bind("<Button-1>", changeColor)

	button_send = Button(window, text="Send", borderwidth=2, relief='groove')
	button_send.place(x=505, y=under_frame_y + 90, width=100, height=25)
	button_send.bind("<Button-1>", sendComb)

	# label_nouns2 = Label(window, text="Nouns:")
	# label_nouns2.place(x=185, y=under_frame_y, width=95, height=25)
	# label_nouns2.configure(bg='black', fg='white')
	# label_actions2 = Label(window, text="Actions:")
	# label_actions2.place(x=285, y=under_frame_y, width=95, height=25)
	# label_actions2.configure(bg='black', fg='white')      
	# label_adjectives2 = Label(window, text="Adjectives:")
	# label_adjectives2.place(x=385, y=under_frame_y, width=95, height=25)
	# label_adjectives2.configure(bg='black', fg='white')
	# button_hint = Button(window, text="Hint", borderwidth=2, relief='groove')
	# button_hint.place(x=90, y=under_frame_y, width=40, height=25)
	# button_hint.bind("<Button-1>", genComb)
	# label_check = Label(window, text='No:')
	# label_check.place(x=140, y=under_frame_y, width=40, height=25)
	# label_check.configure(bg='black', fg='white')

window = Tk()
window.geometry("1100x700")
window.title('Reading Assistant')
content_frame = Frame(window, height=300, width=600, borderwidth=2, relief="groove")  # , fg = '#003333'
content_frame.place(x=140, y=60)
populateWindow()
window.mainloop()