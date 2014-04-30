#!/usr/bin/python

from tokenizer import *

"""
	This part of the program is a series of functions that systematically
	build the output for an html file.

	Where tokenizer.py produces the data necessary to carry out statistical
	analyses of texts, visualizer.py produces the distillation of that data
	into a form that can be digested by the user. While the conventional 
	essay is the tool of choice for literary scholars who are doing close
	readings of a text, examining a text on a statistical level requires
	that the reader, here split into two entities: the machine, and the user,
	be able to see the 'forest for the trees', and paint a picture of the
	text as a whole. In this regard, I feel that data visualization is 
	the best tool for representing a text that is read through the lens
	of machine assistance. 

	While python has numerous libraries for data visualization, such as
	matplotlib, the D3 (data driven documents, http://d3js.org/) is a
	flexible and powerful web-based visualization library that uses 
	scalable vector graphics, which this program leverages for its
	visualization. 

	As such, there are actually two programming languages employed in this
	file. The python takes long form strings that contain javascript.

	To get python to write the javascript for me, I broke the visualization
	script into sections for the header, body, and style sheet, and then, 
	based on whether the user wants to view a bar chart or a frequency plot, 
	the visualizer reformats the tokenized data, collects the individual 
	pieces of the javascript, and writes the new program to an html file,
	which it executes using the user's default browser. The D3 is interpreted
	by the browser, so these two programs can live harmoniously but be executed
	separately. This also allows the user to save a visualization, as the 
	HTML file that MALI generates is a self-contained script, complete with
	the data necessary for the visualization to run. 

	In an example run, the user might select a frequency plot as the 
	visualization type that they would like to view. The program will write 
	separate variables for the header, body, and style portion of the HTML 
	file. The header is uniform for all of the visualization types. The body is
	completely unique to the visualization type, so each is a separate javascript
	program in itself. The style portions are similar but are also written 
	separately for each visualization type, as each has its own unique style,
	which informs its purpose. 

	Once the three variables are written, they are concatenated together into
	a long string that contains an HTML header, a body with javascript and 
	data, and a style sheet. The contents are written to a file called 
	container.html, and can be read and modified as if it were a separate 
	program written in HTML/javascript.

	Although most browsers work, I recommend firefox. When I write the user
	interface for the program, the visualization script will be interpreted
	by the QT-Browser within the program. 
"""

def writeHeader():
	return """
	<html>
	<head>
	<script src="d3.min.js"></script>
	<meta charset="utf-8">
	</head>
	"""

def writeStyle(visualization):
	if visualization == 'histogram':
		return """
		<style type="text/css">
		.toolTip {
			position: absolute;
			text-align: left;
			width: 200px;
			height: 125px;
			padding: 2px;
			font: 24px sans-serif;
			background: #DCE3AB;
			border: 0px;
			border-radius: 8px;
			pointer-events: none;
		}
		rect:hover {
			opacity:.825;
		}
		</style>
		</body>
		</html>
		"""
	elif visualization == 'frequencyPlot':
		return """
			<style type="text/css">
				.axis path, 
				.axis line,
				.axis text{
					fill: #7B7B97;
				}
				body {
					background-color: #474747;
				}
				#descriptor {
					color: white;
				}
			</style>
		</body>
		</html>
		"""

def writeBody(visualization, dataset, title="", textLength=0):
	if visualization == 'histogram':
		return """
		</body>
		<script>

			var title = """ + title + """
	
			var dataset = """ + dataset + """

			var textLength = """ + str(textLength) + """
			
			//These variables set up the canvas size and margins.

			var margins = {top: 20, bottom: 20, left: 50, right: 20};

			var w = 800;

			var h = 800;

			var padding = 4;

			//set min and max of word counts. Since output is sorted by the tokenizer.py file, the min and max are simply decided by their placement in the array.

			var max = dataset[0].count;

			var min = dataset[dataset.length-1].count;

			//set up scales for x, y and colors for the histogram.

			var xScale = d3.scale.linear()
							.domain([0, max])
							.range([0, w - margins.left - margins.right])
							.nice();

			var yScale = d3.scale.linear()
							.domain([0, dataset.length])
							.range([0, h - margins.bottom - margins.top]);

			var colorScale = d3.scale.linear()
							.domain([min, max])
							.range(["#A46CAC", "#96C53D"]);

			var axis = d3.svg.axis()
							.ticks(5)
							.scale(xScale);

			//append svg element to body

			var svg = d3.select("body")
							.append("svg")
								.attr("height", h)
								.attr("width", w);

			var toolTip = d3.select("body")
							.append("div")
							.attr("class", "toolTip")
							.style("opacity", 0);

			//create bars for dataset. Because scales were used, changing the number of words and counts returned (here, we have 25) to any other number should be fine, as all calculations for the scales account for the length of the array that is put in.

			var bars = svg.selectAll("rect")
							.data(dataset)
							.enter()
							.append("rect")
								.attr("width", 0)
			bars.transition()
					.duration(1000)
					.attr("width", function(d) {
						return xScale(d.count);
					})
					.attr("x", margins.left)
					.attr("height", (h/dataset.length)-padding)
					.attr("y", function(d, i) {
						return yScale(i);
					})
					.attr("fill", function(d) {
						return colorScale(d.count);
					});

			bars.on("mouseover", function(d) {
				toolTip.transition()
					.duration(600)
					.style("opacity", .9);
				toolTip.html("Word: " + d.word + "<br><br>" + "Count: " + d.count)
					.style("left", (d3.event.pageX) + "px")
					.style("top", (d3.event.pageY - 15) + "px")
			});

			bars.on("mouseleave", function(d) {
				toolTip.transition()
					.transition(500)
					.style("opacity", 0);
			})

			//append text elements to the svg, and have it display the word with each bar. 

			svg.selectAll("text")
				.data(dataset)
				.enter()
				.append("text")
					.attr("x", 0)
					.attr("y", function(d, i ){
						return yScale(i) + ((h/dataset.length)-padding)/2;
					})
					.attr("fill", "black")
					.attr("font-size", "10px")
					.text(function(d) {
						return d.word;
					});

			//append an axis to the svg element. Built on the same scale as the width of the bars, so axis should always be in sync with the data. 

			svg.append("g")
				.attr("transform", "translate(" + margins.left + ", " + (h - margins.bottom - margins.bottom) + ")")
				.call(axis);

			//append graph title to bottom of graph

			svg.append("text")
				.attr("transform", "translate(" + ((w/2) - 100) + ", " + (h-padding) + ")")
				.text(title + " Word Frequency Distribution")
				.attr("text-align", "center")
				.attr("font-weight", "bold")
				.attr("font-size", "1em");
		</script>	
		"""
	elif visualization == 'frequencyPlot':
		return """
		<body>
		<script>
				var title = """ + title + """
				var dataset = """ + dataset + """
				var textLength = """ + str(textLength) + """;
				var h = screen.height/1.5;
				var w = screen.width-100;

				var margins = {top: 20, bottom: 25, left: 200, right: 40};

				var duration = 150;

				if (textLength <= 20000) {
					var n = 5;
				} else if (textLength > 600000) {
					var n = 20;
				} else {
					var n = 12;
				}

				if(dataset.length == 1) {
					var ry = h/4;
				} else if (dataset.length == 2) {
					var ry = h/7;
				} else if (dataset.length == 3) {
					var ry = h/9;
				} else if (dataset.length == 4) {
					var ry = h/12;
				} else if (dataset.length == 5) {
					var ry = h/15;
				} else {
					var ry = h/2;
				}

				var xScale = d3.scale.linear()
									.domain([0, textLength])
									.range([margins.left, w-margins.right]);

				var yScale = d3.scale.linear()
									.domain([1, dataset.length])
									.range([((h/(h/200))*-1), (h/(h/200))]);

				var svg = d3.select("body")
							.append("svg")
								.attr('height', h)
								.attr('width', w);

				var words = svg.selectAll("text")
								.data(dataset)
								.enter()
									.append("text")
									.text(function (d, i) {
										console.log(i);
										return d.word;
									})
										.each(function (d, i) {
											d3.select(this).attr("transform", "translate(" + margins.left/2.5 + "," + ((h/2) + yScale(i+1)) + ")")
										})
										.attr("font-size", "1.5em")
										.attr("text-anchor", "middle")
										.attr("fill", "white")
										.attr("opacity", 0);

				words.transition()
					.duration(duration+1000)
						.attr("opacity", 1);			
			

				var axis = d3.svg.axis()
							.tickValues(xScale.domain())
							.scale(xScale);


				var markerScale = d3.scale.linear()
								.domain([20000, 1000000])
								.range([5, 1]);

				var container = svg.selectAll("g")
									.data(dataset)
									.enter()
										.append("g")
										.attr("class", "gee")
										.each(function (d, i) {
											d3.select(this).attr("transform", "translate(0," + yScale(i+1)+ ")")
										});

				var marker = container.selectAll("ellipse")
							.data(function (d, i) {
								return d.occurence;
							})
							.enter()
							.append("ellipse")
								.attr("rx", markerScale(textLength))
								.attr("ry", ry)
								.attr("cy", h/2)
								.attr("cx", w+50)
								.attr("opacity", 0)
								.attr("fill", "white");

				marker.transition().ease("cubic")
					.delay(function(d, i) {
						return i / (n) * duration;
					})
					.duration(duration)
						.attr("cx", function (d) {
							return xScale(d);
						})
						.attr("opacity", .5)
					.transition()
					.duration(duration*10)
							.attr("fill", "#FFF886");

				var colorScale = d3.scale.linear()
								.domain([0, dataset.length])
								.range(["white", "#CC9900"]);

				var axis = svg.append("g")
							.attr("transform", "translate(0" + ", " + (h - margins.bottom) + ")")
							.attr("class", "axis")
							.call(axis)
							.attr("opacity", 0);

				axis.transition()
					.duration(duration+1000)
						.attr("opacity", 1);

				svg.append("text")
					.text("Frequency Distribution for: " + title)
					.attr("x", w/2)
					.attr("y", margins.top)
					.attr("fill", "white");

			</script>

			<div id="descriptor">
				<p>The frequency plot above marks each occurence of the word(s) indicated on the above left.</p>
				<p>The axis runs from the first to the last word of the text.</p>
				<p>The brighter the color of the marks, the more frequently that word occurs in that section of the text.</p> </div>
		"""

def dataPrep(visualization, rawData, wordToTest=""):
	"""rawData for Histogram = wordCounter
		rawData for frequencyPlot = words

		Each visualization type requires that data come in a specific
		form. The bar chart works with key and value sets, in this case 
		word: string, count: integer. 
		
		The frequency distribution requires a JSON format, with the 
		word as a key: value and the occurrences of that word as a subset
		of data. The index of the word in the context of the word list
		generated (in the array) is the marker for that word's occurrence.
		
		As such, if a user specifies that stopwords should be removed,
		to preserve the 'life of the text' as an axis of words occurring 
		one after the other, the original word list is fed to this function.
		The removal of stopwords was moved to the frequency distribution function,
		to keep the data displayed in the tokenizer output file, the bar chart,
		and the frequency distribution consistent, without requiring that the 
		program rerun its functions depending on the user's choice. 

		If a user specifies that beginning and end apostrophes be removed,
		or that single quotes are the quote delimiter for the text, the input
		for the frequency distribution will be post-apostrophe strip to ensure
		that the data presented is in-line with the user's choices.
	"""
	if visualization == 'histogram':
		numberMostCommon = 25
		fullTextString = "["
		n = 1
		for tup in rawData:
			if n == 1:
				fullTextString += "{word: " + '"' + tup[0] + '"'
				fullTextString += ", count: " + str(tup[1]) + "},"
			
			if n > 1 and n < numberMostCommon:
				fullTextString += "\n\t{word: " + '"' + tup[0] + '"'
				fullTextString += ", count: " + str(tup[1]) + "},"

			if n == numberMostCommon:
				fullTextString += "\n\t{word: " + '"' + tup[0] + '"'
				fullTextString += ", count: " +  str(tup[1])  + "}]"
			n+=1
		fullTextString += ";"
		return fullTextString

	elif visualization == 'frequencyPlot':
		wordPositions = "["
		
		for userSelectedItem in wordToTest:
			wordPositions += "{word: " + '"' + userSelectedItem + '"' + ", occurence: "
			indices = [i for i, x in enumerate(rawData) if x.lower() == userSelectedItem]
			wordPositions += str(indices) + "}, "

		wordPositions = wordPositions[:-2]
		wordPositions += "];"
		return wordPositions

def histogram(title, rawData, length):
	header = writeHeader()
	title = '"' + title[:-4] + '"'
	style = writeStyle('histogram')
	dataset = dataPrep('histogram', rawData)
	body = writeBody('histogram', dataset, title, length)
	
	script = header + body + style

	runVisualization(script)

def frequencyPlot(wordToTest, rawData, title):
	header = writeHeader()
	style = writeStyle('frequencyPlot')
	title = '"' + title[:-4] + '"'
	textLength = len(rawData)
	dataset = dataPrep('frequencyPlot', rawData, wordToTest)
	body = writeBody('frequencyPlot', dataset, title, textLength)
	
	script = header + body + style

	runVisualization(script)

def runVisualization(script):
	"""
		Executes the container.html file using the webbrowser class.
	"""
	import webbrowser
	import os.path

	containerHTML = open("src/container.html", 'w')
	containerHTML.write(script)
	containerHTML.close()

	# sys.stdout = os.devnull
	# sys.stderr = os.devnull	
	
	webbrowser.open("file:///" + os.path.realpath('src/container.html'))
