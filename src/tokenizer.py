#!/usr/bin/python

def readFile(filePath):
	""" str -> str	
	""" 
	fileInput = open(filePath, 'r')
	readThis = fileInput.read()
	return readThis

def parseFileIntoWords(readThis):    
	""" str -> list

		This function does the main work of the entire program by taking in 
		one long piece of text as input, such as the entirety of Moby Dick, 
		and outputs a list of tokens from it. Coming up with this function 
		would seem to be a simple thing to do: human readers are well aware 
		of what a word is, where it begins and ends, and what punctuation 
		is necessary to a word and what isn't. To a machine, however, these 
		distinctions are not as obvious. Code is executed without context, 
		and every algorithm, regardless of how sophisticated, will likely 
		boil down to a handful of simple instructions repeated over and over 
		again. 
		
		Over the various iterations of this program (a total of 11 distinct 
		versions were written, before this one), the parseFilesIntoWords 
		function was the one that was touched the most often. If we look
		at the first two sentences of Shakespeare's Coriolanus, which is 
		included as a sample text in this package, we can see how various 
		approaches to tokenization can produce quite varied results. 

		'Before we proceed any further, hear me speak. Speak, speak.'

		Tokenizing this in the conventional, simplest, and least accurate 
		means, would be to split the text on white space.

			1.a: 
			Before
			we
			proceed
			any
			further,
			hear
			me
			speak.
			Speak,
			speak.

			If this was run into a counter, the results would be:

			1.b:
			Before      1
			we          1
			proceed     1
			any         1
			further,    1
			hear        1
			me          1
			speak.      2
			Speak       1

		Does the word speak occur three times or does [speak.] occur twice while 
		[Speak] occurs once? Which count would be considered distinct? The better 
		questions may be, which count is accurate? One way to address this issue 
		would be, and was one of the tokenizer versions for this program, to run 
		the tokenized output into a function that would strip off punctuation marks, 
		such as periods, commas, and quotation marks. The function was flawed 
		however, and couldn't understand the need to tokenize [by-the-way] as one 
		token rather than [by] [the] and [way]. This distinction, however, is
		debateable. Others, such as understanding the difference between an apostrophe 
		at the beginng of a word to indicate dialect, such as ['bout] and an inline quote 
		such as ["'bout] is something that a simple algorithm could not address. 

		An early version of the parseFileIntoWords function was written as:

		def parseFileIntoWords(readThis):
			wordDictionary = {}
			split = readThis.split()
			i = 0
			for each in split:
				wordDictionary[i] = each
				i += 1

			return wordDictionary

		def wordStrip(word):
			word = word.strip('.')
			word = word.strip(',')
			word = word.strip('?')
			word = word.strip('!')
			word = word.strip('"')
			word = word.strip(':')
			word = word.strip(';')
			word = word.strip('/')
			word = word.strip('\\')

			return word

		The first function splits the text into a set of tokens based on 
		white space. The output of this is heavily affected by punctuation, as
		discussed above with the first two sentences of Coriolanus. Once the 
		tokenized words were input into a dictionary, which, prior to the use
		of python's enumerate function to derive array indices, was MALI's way
		of assigning each 'word' in a text to a numeric position in that text, a 
		function called wordStrip was run. This relied on python's internal
		strip() function to remove a list of stop characters from the word.

		However, stripping a word without context led to tokens being dropped
		and others being picked up that introduced a lot of noise into the dataset.

		The next iteration of the wordStrip functionality became:

		def wordStrip(word):
			import re
			word = word.strip('./,?:;!\\"')
			word = word.strip('--')
			word = word.strip(',--')
			word = word.strip(",'")
			word = word.strip("--'")
			word = word.strip(':')

			searchCriteria = "[A-Z]'s$|[a-z]'s$"

			matchObj = re.findall(searchCriteria, word)

			if matchObj:
				word = word.strip("'s")

			return word		

		This attempted a more robust set of stripping rules that included tags which 
		often occurred in digital copies of texts, such as the double dash [--] for 
		the long dash. 

		Likewise, the word stripper attempted to flatten occurrences of tokens such
		as [Samuel] and [Samuel's] into an occurrence of [Samuel]. 

		What is to be included and what is removed by the program is highly 
		subjective,	where one can argue that [Rome] and [Rome's] are two instances 
		of the word [Rome],	or one of [Rome] and one of [Rome's]. Is the possessive 
		a separate token or a specialized form of a derivable word? 
		My experience in writing this program was to keep the first pass at a text, 
		which this function is (the first attempt at tokenizing a text, before one 
		undertakes several further passes to produce meaningful data) as a 
		function that casts as wide a net as possible. MALI's first pass separates [Rome] 
		and [Rome's] and likewise commits its frequency distribution on these words 
		being distinct. A second, more targeted pass can root out [Rome] from
		[Rome's] if the user's data requirements necessitate that the distinction
		be smoothed out. Data smoothing should be done with care and context;
		something this program should not be trusted with doing automatically. 

		For version 5, I had hoped that this algorithm would give me the words 
		I needed:

			wordStr = ""

			for letter in word:
				if letter.isalpha() or letter == "'":
					wordStr += letter

			return wordStr


		This checked each letter in a word to see if it was an alpha character or 
		apostrophe and concatenated them into a new word. This was extremely flawed
		as [by-the-way] wouldn't become [by] [the] [way] (and it is highly debatable
		to say whether or not it should be considered three tokens), but became
		[bytheway], which is a unique but completely unpredictable treatment 
		of the text. 

		Version 6 of the tokenizer contained this stripping function:

		def wordStrip(word):

			import re
			wordStr = ""

			stopChar = [",", ".", "!", "?", ":", ";", "<", ">", "/", "\\", "[", 
			"]", "{", "}", "(", ")", "*", "&"]

			for letter in word:
				if letter not in stopChar:
					wordStr += letter

			if len(wordStr) > 0:
				if wordStr[-1] == "'":
					wordStr = wordStr[0:-1]
			if len(wordStr) > 0:		
				if wordStr[0] == "'":
					wordStr = wordStr[1:]

			return wordStr

		This attempted to read each letter of a word and concatenate it into 
		a new word as long as it did not appear in a stop character list. This 
		was ultimately a more sophisticated way of incorrectly tokenizing the 
		same output as version 5 above. I was more specific about which 
		characters I would restrict, but ultimately rendered the same types 
		of flawed tokens. This version also assumed that beginning and ending
		apostrophes should be removed from a token, but considering words such
		as [bout] as a confrontation and ['bout] as a shortening of the word 
		[about], this function would incorrectly count [bout] twice. 

		Version 7 had kept the same base algorithm but allowed the user the 
		ability to choose whether or not to remove beginning and ending 
		apostrophes from words. The main focus of versions 7 and 8 were in
		fleshing out the ability of the program to render complex visualizations
		with the output from the tokenizer, to refine the internal functions for
		better performance and cleaner code, and to split the entire program 
		into numerous files. Ultimately, however, the main issue remained 
		unresolved.	Of what use is an attractive visualization of word usage 
		in a text if the underlying data was unreliable?

		Ultimately, and ninth version into the software's life, I settled on a more 
		complex solution. It relies on regular expressions and basic 'or' logic 
		to run through the text and match patterns. 

		The patterns are as follows:
							Pattern  									Matches
            __________________________________________|_____________________________
		1.  [']*[a-z]+([-][a-z]+)+(['][a-z]+)+[']*|   |	    [']matter-of-fact's['] 
		2.  [']*[a-z]+(['][a-z]+)+([-][a-z]+)+[']*|   |	    [']what's-his-name['] 
		3.  ['][a-z]+[']+[a-z]+|                      |	    'what's
		4.  ['][a-z]+['][a-z]+[']|                    |	    'what's'
		5.  ['][a-z]+[']\s+|                          |	    'what'
		6.  [a-z]+['][a-z]+|                          |      what's
		7.  ['][a-z]+|                                |	    'bout
		8.  [a-z]+[']|                                |	    james'
		9.  [a-z]+([-][a-z]+)+|                       |	    by-the-way
	    10. [a-z]+|                                   |	    his 
	    11. [0-9]+([:][0-9]+)+(\.*[0-9]*)*|           |	    9:09 
	    12. [0-9]+([-][0-9]+)+|                       |	    718-339-4456
	    13. [0-9]+([,][0-9]+)+(\.*[0-9]*)*|           |	    6,0756.023
	    14. [0-9]+                                    |	    200
		
		You can see how some of these patterns are more theoretical, such as the first, 
		and when looking at the patterns 1-10, they are in descending order from rare to 
		common. This order ensures that the tokenizer doesn't gloss over a rare token just 
		because it matches a more common pattern, where [by] [the] [way] would take 
		precedence over [by-the-way]. 

		Because of the nature of this implementation of pattern recognition, the results 
		for any given complex token, such as what's-his-name, would be a tuple. In that tuple 
		are all	of the results of the pattern matching, beginning with [what's-his-name], followed 
		by [what's], [his], [name]. In the end, this tokenizer seeks to cast the widest 
		possible net without repetition, so the zeroth entry in each tuple is written to the 
		final wordlist. Although the memory where the tuples are stored is lost once we 
		exit the function call, it wouldn't be difficult to make use of these tuples to 
		parse complex words like [what's-his-name] into the roots that make it up.

		Again, this is an example of a second pass at a text to further smooth, or even
		make more complex, the data derived from it. 
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
	"""
		str -> str
	If the user specifies apostrophes as the quote delimiter of the text that they are 
	working on, or if they specify that beginning and ending apostrophes should be removed, 
	this function is executed. It checks if the zeroth or last character of a token is 
	an apostrophe and rewrites that token as the token minus one character from the beginning 
	or from the end. Noise is possible in this implementation, as [''bout'], a quote where 
	the first letter of the token is an apostrophe, would retain its apostrophe and become 
	['bout], but an instance of ['bout] outside of quotes would be stripped down to [bout].
	Since use of this is user specified, and it is a 'second pass' function, the user 
	is able to judge whether or not the results will be statistically material. 
	"""
	if len(word) > 0:
		if word[-1] == "'":
			word = word[0:-1]		
		if word[0] == "'":
			word = word[1:]
	
	return word	

def frequencyDistribution(words, type, stopWordsList):
	"""	 
		str -> [tuple]
	This function does all of the counting for the tokenizer. As important as the tokenizer 
	function is, in that the input it provides will be the basis for the counts, the 
	frequencyDistribution function provides the data that the user interacts with. The 
	function is flexible in that it can count how often a word occurs, or it can count
	how often a word length occurs.

	For example, a text may have 1,000 instances of the token [the] and 6,000 instances of 
	three letter words.

	For the sake of the tokenizer's main output, which visualizes word occurrences and 
	counts, the interface is hard coded to pass a type of 'word' to this function. 

	Also built into this function is flag of whether or not to run the tokenized output 
	against a list of stop words. 
	""" 
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