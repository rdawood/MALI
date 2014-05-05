#!/usr/bin/python

"""
	M.A.L.I. (Machine Assisted Literary Interpretation)
	version 1.0
	This software is provided under the MIT License. 
	Please refer to the license documentation included 
	with this package.

		This software package is an experiment in the design 
		and implementation of a tokenizer for use in the context 
		of literary study. 

		It tokenizes texts, generates word frequencies for the 
		text, and provides the user with two dynamic visualization
		options for viewing the tokenizer output. 

		The program can run with any plain text file.

		This version (branch 1.0) and versions with any future
		updates can	be retrieved from:

		https://github.com/rdawood/MALI
"""

from src.visualizer import *
from src.tokenizer import *
import os
import sys
from multiprocessing import Pool
import time

def main():
	
	padding = "---------------------------------------------"

	"""
>>>>-----------------------------------------Start--Traversal
	"""

	currentDirectory = os.path.dirname(os.path.realpath(__file__)) + "/Texts/"
	#Find the program's current directory

	listOfFolders, listOfFiles = [], []

	for root, dirs, files in os.walk(currentDirectory):
		for dir in dirs:
			listOfFolders.append(dir)

	dictOfFolders = {}

	for each in range(len(listOfFolders)):
		dictOfFolders[each] = listOfFolders[each]
	#Write a dictionary of folders for the user to choose from.

	print "Which directory would you like to search?\n"

	for each in dictOfFolders:
		print str(each+1) + ": " + dictOfFolders[each]

	folderPicked = raw_input(">>")
	folderPicked = dictOfFolders[int(folderPicked)-1]

	traverseDirectory = currentDirectory + '/' + folderPicked + '/'
	#traverse the directory chosen and compile a dictionary of files.

	for root, dirs, files in os.walk(traverseDirectory):
			for file in files:
				listOfFiles.append(file)

	dictOfFiles = {}

	for each in range(len(listOfFiles)):
		dictOfFiles[each] = listOfFiles[each]

	print """Which file would you like to read into the program?
		""" + padding

	for each in dictOfFiles:
		print str(each+1) + ": " + dictOfFiles[each]

	filePicked = raw_input(">>")
	filePicked = dictOfFiles[int(filePicked)-1]

	fileToBeParsed = traverseDirectory + filePicked

	"""
>>>>------------------------------------------Start--Options
	"""

	quoteDelim = raw_input("""
	What is the quote delimiter for this text?

	\" or \' 

	>>""")

	stripApos = raw_input("""
	Strip beginning and trailing apostrophes from words? 
	
	Y or N

	>>""")

	if stripApos.lower() != 'y' and stripApos.lower() != 'n':
		print "Defaulting to Y"

	stopWords = raw_input("""
	Run the file against a list to remove common words? 

	(If you choose yes the program will use a stock stop words list 
	in the 'src' folder. 

	You can replace this file with your own.) 

	Y or N

	>>""")

	if stopWords.lower() == 'y': 
		stopWordsFile = open('src/stopwords.txt', 'r')
		stopWordsList = stopWordsFile.read().split()
	else:
		stopWordsList = False
	
	"""
>>>>----------------------------------Begin--Tokenizing

	"""

	words = parseFileIntoWords(readFile(fileToBeParsed))

	t2 = time.time()

	if quoteDelim == "'" or stripApos.lower() == 'y':
		pool = Pool()
		#initiate a pool of workers for parallel 
		#processing
		words = pool.map(aposStrip, words)
		#rewrite each word to remove beginning and ending 
		#apostrophes

	wordCounter = frequencyDistribution(words, "word", stopWordsList)

	print "\n\n" + padding + "Completed in " + str(round((time.time() - t2),2)) + " sec" + padding
	
	"""
>>>>-----------------------------------------Write--Tokenizer--Output
	"""

	print "\n\nPrinting tokenizer output to tokenizer_output_" + filePicked[0:-4] + ".txt in\n\n" + os.path.dirname(os.path.realpath(__file__)) + "\n\n"

	fileWrite = open("tokenizer_output_" + filePicked[0:-4] + ".txt", "w")
	for tup in sorted(wordCounter.most_common(), key = lambda word: word[0]):
		fileWrite.write(str(tup[0]) + ", " + str(tup[1]) +"\n")
	fileWrite.close()
	#Writes the tokenizers data to a text file in a comma separated format
	#sorted by word

	print "\n"
	input = raw_input("""
	Show the top _____ number of words in the text:

	Enter value here

	>>""")

	print "Generating top " + input + " words in " + filePicked

	print padding
	for tup in wordCounter.most_common(int(input)):
		print "\nWord: " + tup[0] + ", Count: " + str(tup[1])
	print padding

	"""
>>>>----------------------------------Call--Visualizer
	"""

	print """
	Visualize the tokenizer's output using the options below:

	1: Frequency Plot - display the frequency with which a word 
	appears over the life of the text.

	You may want to select one of the words in the top """ + input + """
	displayed above. 

	Type '1' to select this option.

	2. Histogram - chart the most often used words in the text 
	in a standard bar chart. 

	Type '2' to select this option.

	Type 'Q' to exit."""
	

	visualizationType = raw_input("""

	>>""")

	while visualizationType.lower() != 'q':
		if visualizationType == '1':
			wordToTest = raw_input("""
	Which word(s) would you like to plot? 

	Enter a list of up to five words separated by spaces:

	>>"""
			)
			wordToTest = wordToTest.split()
			frequencyPlot(wordToTest, words, filePicked)
		elif visualizationType == '2':
			histogram(filePicked, wordCounter.most_common(25), len(words))
		else:
			print """
	Visualize the tokenizer's output using the options below:

	1: Frequency Plot - display the frequency with which a word 
	appears over the life of the text.

	You may want to select one of the words in the top """ + input + """
	displayed above. 

	Type '1' to select this option.

	2. Histogram - chart the most often used words in the text 
	in a standard bar chart. 

	Type '2' to select this option.

	Type 'Q' to exit.
			"""
	

		visualizationType = raw_input("""

	>>"""
		)

	sys.exit()

if __name__ == '__main__':
	main()
