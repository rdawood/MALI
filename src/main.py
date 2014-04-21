#!/usr/bin/python

from src.visualizer import *
from src.tokenizer import *
import os
import sys

def main():
	"""version .7 beta
	main() searches the directory of the script to find folders contained within it. Folders should contian text files. It prompts the users to select a folder and a text file. It then prompts for various inputs to provide the tokenized data to the user."""
	currentDirectory = os.path.dirname(os.path.realpath(__file__)) + "\\Texts\\"

	listOfFolders, listOfFiles = [], []
	
	for root, dirs, files in os.walk(currentDirectory):
		for dir in dirs:
			listOfFolders.append(dir)

	dictOfFolders = {}

	for each in range(len(listOfFolders)):
		dictOfFolders[each] = listOfFolders[each]

	print "Which directory would you like to search?\n"

	for each in dictOfFolders:
		print str(each) + ": " + dictOfFolders[each]

	folderPicked = raw_input("")
	folderPicked = dictOfFolders[int(folderPicked)]

	traverseDirectory = currentDirectory + '/' + folderPicked + '/'

	for root, dirs, files in os.walk(traverseDirectory):
			for file in files:
				listOfFiles.append(file)

	dictOfFiles = {}

	for each in range(len(listOfFiles)):
		dictOfFiles[each] = listOfFiles[each]

	print "Which file would you like to read into the program? \n"

	for each in dictOfFiles:
		print str(each) + ": " + dictOfFiles[each]

	filePicked = raw_input("")
	filePicked = dictOfFiles[int(filePicked)]

	fileToBeParsed = traverseDirectory + filePicked

	quoteDelim = raw_input("What is the quote delimiter for this text: (Choose \" or \') ")

	stripApos = raw_input("Strip beginning and trailing apostrophes from words? (Y or N)")

	if stripApos.lower() != 'y' and stripApos.lower() != 'n':
		print "Defaulting to Y"

	text = readFile(fileToBeParsed)
	words = parseFileIntoWords(text)
	wordCounter = frequencyDistribution(words, "word", quoteDelim, stripApos)
	wordLengthCounter = frequencyDistribution(words, "length", quoteDelim, stripApos)

	"""================================================="""

	print "\n"
	input = raw_input("Show the top _____ number of words in the text:\n\nEnter value here: ")

	print "Generating top " + input + " words in " + filePicked

	for tup in wordCounter.most_common(int(input)):
		print "\nWord: " + tup[0] + ", Count: " + str(tup[1])

	print "\nVisualize the tokenizer's output using the options below:\n"
	print "1: Frequency Plot - display the frequency with which a word apears over the life of the text. You may want to select one of the words in the top " + input + " displayed above. Type '1' to select this option.\n"
	print "2. Histogram - chart the most often used words in the text in a standard bar chart. Type '2' to select this option.\n"
	print "Type 'Q' to exit.\n"

	visualizationType = raw_input(">>")

	while visualizationType.lower() != 'q':
		if visualizationType == '1':
			wordToTest = raw_input("\nWhich word(s) would you like to plot? Enter a list of up to five words seperated by spaces:\n\n>>")
			wordToTest = wordToTest.split()
			frequencyPlot(wordToTest, words, quoteDelim, stripApos)
		elif visualizationType == '2':
			histogram(filePicked, wordCounter.most_common(25))
		else:
			print "1: Frequency Plot - display the frequency with which a word apears over the life of the text. You may want to select one of the words in the top " + input + " displayed above. Type '1' to select this option.\n"
			print "2. Histogram - chart the most often used words in the text in a standard bar chart. Type '2' to select this option.\n"
			print "Type 'Q' to exit."
		# sys.stdout = sys.__stdout__
		# sys.stderr = sys.__stderr__
		visualizationType = raw_input(">>")

	sys.exit()

if __name__ == '__main__':
	main()