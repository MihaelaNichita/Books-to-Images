from tkinter import *
import tkinter.messagebox as messagebox
import nltk
from nltk.tokenize import sent_tokenize
from tkinter import font
#from PyDictionary import PyDictionary
from googletrans import Translator
translator = Translator()
#import getParagraphs

#dictionary=PyDictionary()

content = []
par_no = 0
book_opened = False
list_buttons_pos = []; list_buttons_comb = []; list_buttons_check = []
list_buttons_content = []
list_buttons_chosen = []
list_in_words = []
nouns = []; verbs = []; adj = []
all_comb = []
under_frame_y = 400

books = [('the-little-prince','The Little Prince','Antoine de Saint Exupery'),
    ('to-kill-a-mocking-bird','To Kill a Mocking Bird','Harper Lee'),
    ('breakfast-at-tiffany',"Breakfast at Tiffany's",'Truman Capote')]


def shiftLeftButtons(list_buttons,index):
    if index is len(list_buttons)-1:
        return

    n = len(list_buttons_chosen)
    print('n=',n)
    for b in list_buttons_chosen[index+1:n]:
        i = list_buttons_chosen.index(b)
        newX = list_buttons_chosen[i-1].winfo_x()
        newY = list_buttons_chosen[i-1].winfo_y()
        b.place(x=newX,y=newY)
        print('b = ',b['text'])


def deleteButton(event):
    answer = messagebox.askyesno("Question","Are you sure you want to delete the word from the list?")
    print(answer)
    if answer is False:
        return
    caller = event.widget
    index = list_buttons_chosen.index(caller)

    # First shift to the left all the buttons starting the one at index+1
    shiftLeftButtons(list_buttons_chosen,index)

    # Then remove the button from the list
    list_buttons_chosen.remove(caller)
    caller.destroy()


def createChosenList(caller):
    global list_buttons_chosen
    new_button = Button (window,text=caller['text'],borderwidth=1,relief='solid')
    new_button.bind("<Button-3>",deleteButton)
    print(len(list_buttons_chosen))
    if len(list_buttons_chosen)==0:
        new_button.place(x=610,y=under_frame_y,height=25,width=95)
    else:
        new_button.place(x=610+(len(list_buttons_chosen)%4)*100,y=under_frame_y+int(len(list_buttons_chosen)/4)*30,height=25,width=95)
    list_buttons_chosen.append(new_button)


def itsaKeyWord(event):
    caller = event.widget
    caller.configure(bg='#A9A9A9',borderwidth=2)
    createChosenList(caller)


def justaWord(event):
    global list_in_words
    caller = event.widget
    caller.configure(bg='#A9A9A9',borderwidth=2)
    createChosenList(caller)
    list_in_words.append(caller['text'])
    print(list_in_words)


def translate(event):
    caller = event.widget
    toTrans = caller['text']
    r = translator.translate(toTrans,dest='ro')
    translate_frame = Text(window,height=10, width=30, borderwidth=2,relief='groove')
    translate_frame.place(x = 760, y = 60)
    translate_frame.configure(bg="#f1f1f1")
    translate_frame.insert(END,' '+toTrans+' = ')
    translate_frame.insert(END,r.text)


def insert_text(par):
    lastx,lasty = 0,0
    tok_text = nltk.word_tokenize(par)
    for w in tok_text:
        #while w in """.,'?"!:."""
        if lastx + len(w)*10 > 550:
            lastx,lasty = 0,lasty+30

        #times11 = font.Font(font='Times',size=11)
        #ss = font.Font(font='Sans-Serif', size=3)
        new_button = Button(content_frame, text = w,borderwidth=0,fg='#0F1626') # '''font=times14'''
        
        new_button.place(x=lastx, y=lasty, height=25)
        list_buttons_content.append(new_button)
        #new_button.bind("<Leave>", on_leave)
        #new_button.bind("<Enter>", on_enter)
        new_button.bind("<Button-1>", justaWord)
        new_button.bind("<Button-3>", translate)

        if w in nouns+verbs+adj:
            new_button.bind("<Button-1>", itsaKeyWord)
            new_button.configure(bg='#bdbdbd')
            #new_button.configure(borderwidth=1,relief='solid')

        content_frame.update_idletasks() 
        lastx += new_button.winfo_width()
        if w in ".:!?,":lastx += 10


def open_book(event):
    global content, book_opened, list_in_words, list_buttons_content
    book_opened = True
    #text.delete(1.0, END)
    list_buttons_content=removeButtons(list_buttons_content)
    caller = event.widget
    bookNames = [e[1] for e in books]
    bookName = books[bookNames.index(caller['text'])][0]
    f = open("paragraphs/" + bookName + "-paragraphs.txt",'r')

    content = f.readlines()
    getPOS(content[0])
    insert_text(content[par_no])
    list_in_words = nouns + verbs + adj
    print(f"list_in_words = {list_in_words}")
    


def removeButtons(list_buttons):
    for e in list_buttons:  
        e.destroy()
    list_buttons = []
    return list_buttons


def change_par():
    if book_opened == False:
        messagebox.showwarning("Warning","Please open a book first!")
        return

    global par_no, content,all_comb, list_in_words, list_buttons_chosen
    global list_buttons_check, list_buttons_comb, list_buttons_content
    all_comb = []

    # Remove previous buttons
    # removeButtons(list_buttons_pos)
    list_buttons_check=removeButtons(list_buttons_check)
    list_buttons_comb=removeButtons(list_buttons_comb)
    list_buttons_content=removeButtons(list_buttons_content)
    list_buttons_chosen=removeButtons(list_buttons_chosen)
    print('list_buttons_chosen = ',list_buttons_chosen)

    getPOS(content[par_no])
    insert_text(content[par_no])
    list_in_words = nouns + verbs + adj


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
    #createButtons(nouns,700,60,True)
    print("Nouns: ",nouns);print()

    # Get Actions
    verbs = [e[0] for e in parts_of_speech if 'VB' in e[1] or 'RB' in e[1]]
    #createButtons(verbs,800,60,True)
    print("Actions: ",verbs);print()

    # Get Adjectives
    adj = [e[0] for e in parts_of_speech if 'JJ' in e[1]]
    #createButtons(adj,900,60,True)
    print("Adjectives: ",adj);print()




def createButtons(list,xi,yi,col):
    
    global list_buttons_pos, list_buttons_comb
    i=0
    for item in list:
        new_button = Button(window, text = item,borderwidth=1,relief='groove')
        if col:
            new_button.place(x=xi, y=yi+i*30,width = 95, height=25)
            list_buttons_pos.append(new_button)
        else:
            new_button.place(x=xi+i*100, y=yi,width = 95, height=25)
            list_buttons_comb.append(new_button)
        i=i+1


def check_comb(event):
    caller = event.widget
    index = caller['text']
    print("index = ", index)
    index = int(index)*3
    for i in [index-3,index-2,index-1]:
        createChosenList(list_buttons_comb[i])




def getRand(n):
    import random
    return random.randint(0,n-1)


def genComb(event):
    if book_opened == False:
        messagebox.showwarning("Warning","Please open a book first!")
        return

    global nouns,verbs,adj,all_comb,list_buttons_check
    nn = len(nouns)
    nv = len(verbs)
    na = len(adj)

    #print(f"Limit = {nn*nv*na}. When hitting Hint Button, len = ",len(all_comb))

    n = 5 ##### 10
    left = nn*nv*na-len(all_comb)
    print("left : ", left)
    if  6 >= left:
        n = left
        messagebox.showwarning("Warning","These are the last combinations left!")

    for e in range(1,n+1):
        new_button = Button(window, text = str(e+len(all_comb)),borderwidth=1,relief='groove')
        new_button.place(x=140, y=under_frame_y+e*30,width = 35, height=25)
        new_button.bind("<Button-1>", check_comb)
        list_buttons_check.append(new_button)


    for i in range(n):
        r = [ getRand(nn),getRand(nv),getRand(na)]
        while r in all_comb:
            print("Duplicat: ",r)
            r = [ getRand(nn),getRand(nv),getRand(na)]
            
        all_comb.append(r)
        #print("After Appending r, len = ",len(all_comb))
        createButtons([nouns[r[0]],verbs[r[1]],adj[r[2]]],185,under_frame_y+(i+1)*30,False)


def resetColors():
    next_par('<Button-1>')
    prev_par('<Button-1>')
    """
    for b in list_buttons_content:
        if b['text'] in list_in_words:
            b.configure(bg='#2F4F4F',fg='white')
        if b['text'] not in nouns+verbs+adj:
            b.configure(bg='#f1f1f1',fg='black')
    """

def reset(event):
    global list_buttons_chosen
    list_buttons_chosen=removeButtons(list_buttons_chosen)
    list_in_words = nouns + verbs + adj
    print(list_in_words)
    resetColors()
    

def sendComb(event):
    global list_in_words, list_buttons_chosen
    list_out_words = []

    for b in list_buttons_chosen:
        list_out_words.append(b['text'])

    f = open("Data/Data.txt",'a')
    for w in list_in_words:
        f.write(w + " ")
    f.write('\t')

    for w in list_out_words:
        f.write(w + " ")
    f.write('\n')
    


def getInfo():
    how_to = Toplevel(window)
    how_to.title('GUIDELINE')
    how_to.geometry("500x600")

    guideline = Frame(how_to,height=500, width=400, borderwidth=2,relief='groove',bg='lightgreen')
    guideline.place(x=30,y=30)

    m0 = 'GUIDELINE'
    m1 = 'TARGET: Enjoy reading Books or Articles you like & help in developing a tool for you to REMEMBER everything you read easier.'
    m2 = 'STEPS:'
    m3 = '1. Select the BOOK or ARTICLE you want to read. Menu -> "Open"'
    m4 = '2. Read the paragraph and left-click the words you consider RELEVANT and MEMORABLE. (3 to 10 per paragraph)'
    m5 = 'Right-click the words in order to get its TRANSLATION to Romanian.'
    m6 = '3. Press the "Hint" button in the bottom-left to get random combinations of words.'
    m7 = 'If you like any of those combinations, left-click its coresponding number in order to send them to the chosen RELEVANT words.'
    m8 = '4. Right-click a word in "Chosen" words in order to remove it from the ones that are to be sent as the BEST choice of RELEVANT combination of words'
    m9 = '5. Press "Send" button when you feel that the list of words labeled as "Chosen" looks simply UNFORGETABLE.'
    m10 = '6. Navigate through paragraphs using "<<" and ">>" buttons.'

    msg1 = Message(how_to, text = m1, width = 380)
    msg1.config(bg='lightgreen', font=('times', 9))
    msg1.place(x=35,y=40)

    msg2 = Message(how_to, text = m2, width = 380)
    msg2.config(bg='lightgreen',font=('times', 9,'bold'))
    msg2.place(x=35,y=80)

    msg3 = Message(how_to, text = m3, width = 380)
    msg3.config(bg='lightgreen',font=('times', 9))
    msg3.place(x=40,y=100)

    msg4 = Message(how_to, text = m4, width = 380)
    msg4.config(bg='lightgreen',font=('times', 9))
    msg4.place(x=40,y=122)


    msg5 = Message(how_to, text = m5, width = 380)
    msg5.config(bg='lightgreen',font=('times', 9))
    msg5.place(x=50,y=155)


    msg6 = Message(how_to, text = m6, width = 380)
    msg6.config(bg='lightgreen',font=('times', 9))
    msg6.place(x=40,y=185)


    msg7 = Message(how_to, text = m7, width = 380)
    msg7.config(bg='lightgreen',font=('times', 9))
    msg7.place(x=50,y=220)


    msg8 = Message(how_to, text = m8, width = 380)
    msg8.config(bg='lightgreen',font=('times', 9))
    msg8.place(x=40,y=260)


    msg9 = Message(how_to, text = m9, width = 380)
    msg9.config(bg='lightgreen',font=('times', 9))
    msg9.place(x=40,y=300)

    msg10 = Message(how_to, text = m10, width = 380)
    msg10.config(bg='lightgreen',font=('times', 9))
    msg10.place(x=40,y=340)


def openBooksList():
    global books_list
    books_list = Toplevel(window)
    books_list.title('Books List')
    books_list.geometry("400x600")

    label_books = Label(books_list, text='Books:', font = ('times',9,'bold'))
    label_books.place(x=50,y=30)

    label_authors = Label(books_list, text='Authors:', font = ('times',9,'bold'))
    label_authors.place(x=250,y=30)

    for book in books:
        b = Button(books_list,text = book[1],command=books_list.destroy, font = ('times',9))
        b.place(x=30,y=60+20*books.index(book))
        b.configure(borderwidth=0)
        b.bind("<Button-1>", open_book) 

        a = Button(books_list,text = book[2], font = ('times',9))
        a.place(x=225,y=60+20*books.index(book))
        a.configure(borderwidth=0)
       

def getArticle(event):
    pass

def openArticlesList():
    art_list = Toplevel(window)
    art_list.title('Articles List')
    art_list.geometry("800x100")

    l = Label(art_list,text='Link:')
    l.place(x=30,y=30)
    l.configure(bg='black', fg='white')

    v = StringVar()
    e = Entry(art_list, textvariable=v,width=100)
    e.place(x=120,y=30)

    v.set("Enter page link of the article here...")
    s = v.get()

    b = Button(art_list,text='OK',borderwidth=2,relief=GROOVE)
    b.place(x=730,y=30)
    b.bind('<Button-1>',getArticle)




window = Tk()
window.geometry("1100x700")
window.title('Reading Assistant')

menubar = Menu(window)

# create a pulldown menu, and add it to the menu bar
filemenu1 = Menu(menubar, tearoff=0)
filemenu1.add_command(label="Book", command=openBooksList) # call open_book
filemenu1.add_command(label="Article", command=openArticlesList)
filemenu1.add_separator()
filemenu1.add_command(label="Exit", command=window.quit)

menubar.add_cascade(label="Open", menu=filemenu1)
menubar.add_cascade(label="How to", command=getInfo) # call getInfo

window.config(menu=menubar)



label_paragraph = Label(window, text = "Paragraph:")
label_paragraph.place(x = 140, y = 32, width=100, height=22)
label_paragraph.configure(bg='black', fg='white')

content_frame = Frame(window,height=300, width=600, borderwidth=2, relief="groove") #, fg = '#003333'
content_frame.place(x = 140, y = 60)

button_prev_par = Button(window, text = "<<",borderwidth=2,relief='groove')
button_prev_par.place(x = 243, y = 32, width=22, height=22)
button_prev_par.bind("<Button-1>", prev_par)
#button_prev_par.configure(bg='black',fg='white')

button_next_par = Button(window, text = ">>",borderwidth=2,relief='groove')
button_next_par.place(x = 267, y = 32, width=22, height=22)
button_next_par.bind("<Button-1>", next_par)
#button_next_par.configure(bg='black',fg='white')

label_nouns2 = Label(window, text = "Nouns:")
label_nouns2.place(x = 185, y = under_frame_y, width=95, height=25)
label_nouns2.configure(bg='black',fg='white')

label_actions2 = Label(window, text = "Actions:")
label_actions2.place(x = 285, y = under_frame_y, width=95, height=25)
label_actions2.configure(bg='black',fg='white')

label_adjectives2 = Label(window, text = "Adjectives:")
label_adjectives2.place(x = 385, y = under_frame_y, width=95, height=25)
label_adjectives2.configure(bg='black',fg='white')

button_hint=Button(window, text="Hint",borderwidth=2,relief='groove')
button_hint.place(x=90, y=under_frame_y, width=40, height=25)
button_hint.bind("<Button-1>", genComb)

label_check = Label(window, text='No:')
label_check.place(x=140, y=under_frame_y,width = 40, height=25)
label_check.configure(bg='black', fg='white')

button_reset=Button(window, text="Reset",borderwidth=2,relief='groove')
button_reset.place(x=505, y=under_frame_y+30, width=100, height=25)
button_reset.bind("<Button-1>", reset)

label_chosen = Label(window, text = "Chosen:")
label_chosen.place(x = 505, y = under_frame_y, width=100, height=25)
label_chosen.configure(bg='black', fg='white')

button_send = Button(window, text="Send",borderwidth=2,relief='groove')
button_send.place(x=505, y=under_frame_y+60, width=100, height=25)
button_send.bind("<Button-1>", sendComb)


window.mainloop()