MALI
====


Machine Assisted Literary Interpretation

By Raza Dawood

A program that tokenizes texts and visualizes the output.

Built using Python and D3.


Folders and Files:

MALI

	src

		-->	__init__.py
				Initializes the programs directory to allow
				imports. It is intentionally blank and should
				not be edited.

		--> stopwords.txt 
				A stock list of stop words compiled for use
				in the program. Using it is entirely optional
				and the user can replace the file with his/her
				own, so long as it is named 'stopwords.txt'.

		--> tokenizer.py
				Functions used to read a text, tokenize it,
				and create a frequency distribution of word 
				use.

		--> visualizer.py
				Contains numerous helper functions for compiling
				the javascript necessary to render the programs
				graphical outputs. Also, it rewrites data from 
				list and tuple structures to a string resembling
				JSON. Ultimately, it writes and calls the 
				container.html file that contains the visualization.
				The program runs in a loop to allow the user to render
				multiple visualizations.

		--> [container.html]
				This file only appears after the program is run and
				a visualization is rendered. If the graph is not 
				scaling properly (such as if lines are written on
				top of each other), maximize your screen and 
				refresh the page (usually the F5 key). The graphs
				are rendered for full-screen use. 
				
				To save a certain graph for use later, copy the
				container.html file to a different directory. 
				It is a self-contained script that has its data
				hard coded into it. 

	Texts

		AUthor's Last Name

			--> .txt files with author's work.
					The program comes with six sample texts from
					six separate authors. 
					
					To add your own text, create a new folder
					under 'Texts', name it, and place the files
					containing the text to be read within the 
					folder that you created. The program will 
					only select text files one level down from 
					'Texts', so the structure
					
					Texts -- Shakespeare -- Tragedies --> R&J.txt
					will not work.

					Plaint text file formats are preferred, but 
					the program will be able to read text
					from HTML, and could successfully read its
					own code in the visualizer.py file. 

	--> LICENSE
			This software is provided under an MIT license, and
			as such can be freely used so long as the license 
			and copyright are included. Please refer to LICENSE
			for more information. 

	--> README.md
			This file.

	--> MALI.py
			Source code for the main function of the program.
			This program utilizes all or some of the programs/
			files contained in 'src' and 'Texts'.


	*If you plan on moving the program to a different folder, move
	all folders and files in the order that they are currently in.
	
	**This software is provided 'as is' and does not come with a
	warranty. Please refer to the LICENSE for more details. 