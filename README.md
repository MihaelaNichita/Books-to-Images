# Books-to-Images

## Step 1: Books-to-Paragraphs
Python script receives .txt files as input and creates .txt files with the input text separated into paragraphs

* Books need to be given as txt files inside books directory
* The script will generate a txt file inside paragraphs directory for each txt file representing a book in books directory
	* The names of the files being created will have the following format: "'name-of-the-file-representing-the-book'-paragraphs". If a file with this name already exists in the paragraphs directory, then the script will append text to that file. Therefore, for creating new files with that name, you need to remove the existing one.

## Step 2: GUI to collect data for the neural network
For each paragraph, POS tag the words and extract Nouns, Verbs and Adjectives (plus Adverbs).
The user will submit combinations of noun+verb+adj/adv.

