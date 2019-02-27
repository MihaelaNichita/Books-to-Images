from tkinter import *
import tkinter.messagebox as messagebox
import nltk
from nltk.tokenize import sent_tokenize


content = []
par_no = 0
book_opened = False
list_buttons_pos = []; list_buttons_comb = []; list_buttons_check = []
nouns = []; verbs = []; adj = []
all_comb = []


def open_book(event):
	global content
	global book_opened
	book_opened = True

	text.delete(1.0, END)
	f = open("paragraphs/breakfast-at-tiffany-paragraphs.txt",'r')
	content = f.readlines()
	text.insert(INSERT,content[0])
	getPOS(content[0])


def removeButtons(list_buttons):
	for e in list_buttons:
		e.destroy()
	list_buttons = []


def change_par():
	if book_opened == False:
		messagebox.showwarning("Warning","Please open a book first!")
		return

	global par_no, content,all_comb
	all_comb = []
	text.delete(1.0, END)
	
	text.insert(END,content[par_no])
	# Remove previous buttons
	removeButtons(list_buttons_pos)
	removeButtons(list_buttons_comb)
	removeButtons(list_buttons_check)

	getPOS(content[par_no])


def prev_par(event):
	global par_no
	par_no = par_no - 1
	change_par()


def next_par(event):
	global par_no
	par_no = par_no + 1
	change_par()


def getPOS(par):	
	print("Original Paragraph: ",par);print()
	# Remove Punctuation
	par = re.sub(r'[^\w\s]',' ',par)
	par = par.lower() # won't be able to identify NNPs
	
	## Word tokenization
	tok_text = nltk.word_tokenize(par)
	print("Tokenized Paragraph: ",tok_text);print()

	# Removing Stopwords
	from nltk.corpus import stopwords
	stop_words=set(stopwords.words("english"))
	filtered_par=[]
	for w in tok_text:
		if w not in stop_words and w not in filtered_par:
			filtered_par.append(w)
	print("Filterd Paragraph:",filtered_par);print()

	# POS tagging
	parts_of_speech = nltk.pos_tag(filtered_par)
	print(parts_of_speech);print()

	global nouns,verbs,adj
	# Get Nouns
	nouns = [e[0] for e in parts_of_speech if 'NN' in e[1]]
	createButtons(nouns,700,60,True)
	print("Nouns: ",nouns);print()

	# Get Actions
	verbs = [e[0] for e in parts_of_speech if 'VB' in e[1] or 'RB' in e[1]]
	createButtons(verbs,800,60,True)
	print("Actions: ",verbs);print()

	# Get Adjectives
	adj = [e[0] for e in parts_of_speech if 'JJ' in e[1]]
	createButtons(adj,900,60,True)
	print("Adjectives: ",adj);print()


def createButtons(list,xi,yi,col):
	global list_buttons_pos, list_buttons_comb
	i=0
	for item in list:
		new_button = Button(window, text = item)
		if col:
			new_button.place(x=xi, y=yi+i*30,width = 95, height=25)
			list_buttons_pos.append(new_button)
		else:
			new_button.place(x=xi+i*100, y=yi,width = 95, height=25)
			list_buttons_comb.append(new_button)
		i=i+1


def check_comb(event,index):
	print("index = ", index)


def getRand(n):
	import random
	return random.randint(0,n-1)


def genComb(event):
	global nouns,verbs,adj,all_comb,list_buttons_check
	nn = len(nouns)
	nv = len(verbs)
	na = len(adj)

	print(f"Limit = {nn*nv*na}. When hitting Hint Button, len = ",len(all_comb))

	n = 10
	left = nn*nv*na-len(all_comb)
	print("left : ", left)
	if  11 >= left:
		n = left
		messagebox.showwarning("Warning","These are the last combinations left!")

	for e in range(1,n+1):
		new_button = Button(window, text = str(e+len(all_comb)))
		new_button.place(x=140, y=220+(e-1)*30,width = 35, height=25)
		list_buttons_check.append(new_button)
		index = list_buttons_check.index(new_button)
		new_button.bind("<Button-1>", check_comb(event,index))

	for i in range(n):
		r = [ getRand(nn),getRand(nv),getRand(na)]
		while r in all_comb:
			print("Duplicat: ",r)
			r = [ getRand(nn),getRand(nv),getRand(na)]
			
		all_comb.append(r)
		print("After Appending r, len = ",len(all_comb))
		createButtons([nouns[r[0]],verbs[r[1]],adj[r[2]]],200,220+i*30,False)
		

def resetColors(event):
	pass


window = Tk()
window.geometry("1100x700")

label_paragraph = Label(window, text = "Paragraph:")
label_paragraph.place(x = 30, y = 60, width=100, height=25)

button_open_book = Button(window, text = "Open Book")
button_open_book.place(x = 30, y = 30, width=100, height=25)
button_open_book.bind("<Button-1>", open_book)

text = Text(window,height=9, width=60)
text.place(x = 140, y = 60)

button_prev_par = Button(window, text = "Previous Paragraph")
button_prev_par.place(x = 140, y = 30, width=95, height=25)
button_prev_par.bind("<Button-1>", prev_par)

button_next_par = Button(window, text = "Next Paragraph")
button_next_par.place(x = 240, y = 30, width=95, height=25)
button_next_par.bind("<Button-1>", next_par)

label_nouns = Label(window, text = "Nouns:")
label_nouns.place(x = 700, y = 30, width=100, height=25)

label_actions = Label(window, text = "Actions:")
label_actions.place(x = 800, y = 30, width=100, height=25)

label_adjectives = Label(window, text = "Adjectives:")
label_adjectives.place(x = 900, y = 30, width=100, height=25)

button_hint=Button(window, text="Hint")
button_hint.place(x=30, y=220, width=100, height=25)
button_hint.bind("<Button-1>", genComb)

button_reset=Button(window, text="Reset")
button_reset.place(x=30, y=250, width=100, height=25)
button_reset.bind("<Button-1>", resetColors)

label_chosen = Label(window, text = "Chosen:")
label_chosen.place(x = 30, y = 520, width=100, height=25)

window.mainloop()