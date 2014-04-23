#!/usr/bin/python

def readFile(filePath):
	""" str -> str	
	""" 
	fileInput = open(filePath, 'r')
	readThis = fileInput.read()
	return readThis

def parseFileIntoWords(readThis):    
	""" str -> list
	"""
	
	import re

	wordList = []

	regCompiled = re.compile(r"""
							(
								[']*[a-z]+([-][a-z]+)+(['][a-z]+)+[']*| 
								[']*[a-z]+(['][a-z]+)+([-][a-z]+)+[']*|
								['][a-z]+[']+[a-z]+|
								['][a-z]+['][a-z]+[']|
								['][a-z]+[']\s+|
								[a-z]+['][a-z]+|
								['][a-z]+|
								[a-z]+[']|
								[a-z]+([-][a-z]+)+|
								[a-z]+['][a-z]+|
								[a-z]+|
								[0-9]+([:][0-9]+)+(\.*[0-9]*)*|
								[0-9]+([-][0-9]+)+|
								[0-9]+([,][0-9]+)+(\.*[0-9]*)*|
								[0-9]+
							)
							""", re.VERBOSE)

	matchObj = re.findall(regCompiled, readThis.lower())

	for tup in matchObj:
		wordList.append(str(tup[0]))

	return wordList

def aposStrip(word):
	if len(word) > 0:
		if word[-1] == "'":
			word = word[0:-1]		
		if word[0] == "'":
			word = word[1:]
	
	return word	

def frequencyDistribution(words, type, stopWordsList):
	"""	 """ 
	from collections import Counter
	import csv

	if type == "word":
		wordCounter = Counter()
		wordList = []

		if stopWordsList != False:
			for word in words:
				if word.lower() not in stopWordsList and word.lower() != '':
					wordList.append(word.lower())
			wordCounter = wordCounter + Counter(wordList)
			return wordCounter
		else:
			for word in words:
				if word.lower() != '':
					wordList.append(word.lower())
			wordCounter = wordCounter + Counter(wordList)
			return wordCounter

	if type == "length":
		wordLengthCounter = Counter()
		wordLengthList = []

		for value in words:
			word = words[value]
			word = wordStrip(word, quoteDelim, stripApos)
			if word != '':
				wordLengthList.append(len(word))
		wordLengthCounter = wordLengthCounter + Counter(wordLengthList)
		return wordLengthCounter