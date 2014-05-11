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

	folderPicked = ''

	while (not folderPicked.isdigit()) or (int(folderPicked) > len(dictOfFolders) or (int(folderPicked) == 0)):
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

	filePicked = ''

	while (not filePicked.isdigit()) or (int(filePicked) > len(dictOfFolders) or (int(filePicked) == 0)):

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

	quoteDelim = 0

	while quoteDelim == 0:
		quoteDelim = raw_input("""
		What is the quote delimiter for this text?

		1: \" 
		2: \' 

		>>""")

		if not quoteDelim.isdigit():
			print "Please select 1 or 2"
			quoteDelim = 0
		elif int(quoteDelim) == 1:
			quoteDelim = '"'
		elif int(quoteDelim) == 2:
			quoteDelim = "'"
		else:
			print "Please select 1 or 2"
			quoteDelim = 0

	stripApos = ''

	while stripApos.lower() != 'y' and stripApos.lower() != 'n':
		stripApos = raw_input("""
		Strip beginning and trailing apostrophes from words? 
		
		Y or N

		>>""")



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

	print "\n\n" + padding + "\n" + "Completed in " +  str(round((time.time() - t2),2)) + " sec" + "\n" + padding
	
	"""
>>>>-----------------------------------------Write--Tokenizer--Output
	"""

	sortOutput = 0
	tokenCount = len(words)

	while sortOutput == 0:
		sortOutput = raw_input("""
			Sort the tokenizer output by word or by frequency?
	
			1: Sort by word: A ---> Z
			2: Sort by frequency: 9 ---> 0

			>>""")

		if not sortOutput.isdigit():
			print "Please enter 1 or 2"
			sortOutput = 0
		elif int(sortOutput) == 1:
			print "\n\nPrinting tokenizer output to tokenizer_output_" + filePicked[0:-4] + ".txt in\n\n" + os.path.dirname(os.path.realpath(__file__)) + "\n\n"
			try:
				fileWrite = open("tokenizer_output_" + filePicked[0:-4] + ".txt", "w")
				fileWrite.write("WORD, COUNT, RELATIVE_FREQUENCY")
				for tup in sorted(wordCounter.most_common(), key = lambda word: word[0]):
					fileWrite.write(str(tup[0]) + ", " + str(tup[1]) + "," + str(float(tup[1])/float(tokenCount)) +"\n")
				fileWrite.close()
			except IOError:
				print "File is currently open. Please close it and try again."
		elif int(sortOutput) == 2:
			print "\n\nPrinting tokenizer output to tokenizer_output_" + filePicked[0:-4] + ".txt in\n\n" + os.path.dirname(os.path.realpath(__file__)) + "\n\n"
			try:
				fileWrite = open("tokenizer_output_" + filePicked[0:-4] + ".txt", "w")
				fileWrite.write("WORD, COUNT, RELATIVE_FREQUENCY")
				for tup in wordCounter.most_common():
					fileWrite.write(str(tup[0]) + ", " + str(tup[1]) + "," + str(float(tup[1])/float(tokenCount)) +"\n")
				fileWrite.close()
			except IOError:
				print "File is currently open. Please close it and try again."
		else:
			print "Please enter 1 or 2"
			sortOutput = 0			



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


	visualizationType = ""

	while visualizationType.lower() != 'q':
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

	>>""")
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

	sys.exit()

if __name__ == '__main__':
	main()
