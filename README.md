# Books-to-Images
## Architecture
This section describes the developed prototype of the application. Text, model predictions, images and other specific services relating the user-machine interaction are all merged into the “Learning Assistant” application depicted in Fig. 10. The flow of interactions between various components of the application is started by the user requesting a book or a certain article on a web page to read. This request follows the purple path illustrated in Fig 10. If the user inserts the address of the desired web page, the request is carried on to the component that is specialized in extracting web content, i.e. the crawlers, for subsequently filtering it and dividing the whole text into paragraphs consisting of less than 50 words each. 
 

*Figure 10 - Illustration of the interaction between the user and the “Learning Assistant” application*

By choosing a book from the existing list, since online content is not required, the app retrieves the book content from the local library, which already includes the existing books divided into paragraphs. Whenever the application is started, the first thing it does is checking whether there are any new books, not divided into paragraphs yet, and completes the task, if so. The thread illustrated with purple in the diagram finally reaches its goal of delivering the desired content, divided into paragraphs, to the graphical user interface, so the user can visualize it.
The burgundy thread starts from the user as well and aims to collect two lists of words, convert them to specific format and send them to a local text file, where all the data from the user is gathered. The first sequence from one entry depicts a list of words from the current paragraph, that are not contained in a predefined list of stop-words, and the second sequence represents a memorable combination of words, summarizing the content of the paragraph, or the so called Visual Marker for the paragraph.
The RNN Encoder-Decoder is previously trained with a set of 90K pairs of sentences and related keywords, so that it can be used for keywords extraction in the application. The way it provides the desired result is emphasized with the yellow arrows and comments in Fig. 10. For the current paragraph, the list of source words, which are contained in the paragraph and not in the list of stop-words, are served as input to the model. It evaluates the input and returns a sequence of keywords which is further used for querying Google Images. The images provided by the online image library are then incorporated into the application, so the user can read and visualize relevant images, contributing to the efficiency of the learning process.


## Step 1: Books-to-Paragraphs
Python script getParagraphs.py receives .txt files as input and creates .txt files with the input text separated into paragraphs

* Books need to be given as .txt files inside books directory
* The script will generate a txt file inside paragraphs directory for each txt file representing a book in books directory
	* The names of the files being created will have the following format: "'name-of-the-file-representing-the-book'-paragraphs". If a file with this name already exists in the paragraphs directory, then the script will append text to that file. Therefore, for creating new files with that name, you need to remove the existing one.

## Step 2: GUI to collect data for the neural network
For each paragraph, POS tag the words and extract Nouns, Verbs and Adjectives (plus Adverbs).
The user will submit combinations of noun+verb+adj/adv.

