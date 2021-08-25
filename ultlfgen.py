import numpy as np
from PIL import Image
import re
import json

from dotenv import load_dotenv
import os

os.system("color")

load_dotenv()
PNG_LOC = os.getenv('PNG_LOC')

def generate():
	white = [255,255,255]
	black = [0,0,0]
	gray = [195,195,195]
	space = [127,127,127]
	intentionallyleftblank = [231,231,231]
	beige = [239,228,176]
	blue = [63,72,204]
	red = [237,28,36]
	purple = [163,73,164]


	image = Image.open(PNG_LOC + "/ultlf.png").convert('RGB')
	data = np.asarray(image)

	fontrgb = []
	fontdata = []
	unirgb = []
	unithing = []
	baselines = []
	codepointrows = []

	tablerow = 0

	rowcount = 0
	for px in np.swapaxes(data, 0, 1)[17]:
		if np.all(px == gray):
			rowcount += 1
	print(rowcount)

	for rowindex, row in enumerate(range(0,data.shape[0])):
		the = rowindex
		
		if all( np.all(data[the,n] == gray) for n in range( 21, data.shape[1] - 4 ) ) and not all( np.all(data[the+1,n] == white) for n in range( 17, data.shape[1] - 4 ) ):

			the+=1

			fontrgb.append([])
			fontdata.append([])
			unirgb.append([])
			unithing.append([])

			while all( np.all(data[the,n] == gray) for n in range(21,213,12) ) and not all( np.all(data[the,n] == gray) for n in range( 21, data.shape[1] - 4 ) ):
				fontrgb[tablerow].append(data[the,22:213])
				unirgb[tablerow].append(data[the,4:19])
				the+=1
			for row in fontrgb[tablerow]:
				line = ""
				for val in row:
					if np.all(val == black):
						line += "#"
					elif np.all(val == gray):
						line += "_"
					elif np.all(val == intentionallyleftblank):
						line += "X"
					elif np.all(val == space):
						line += "v"
					elif np.all(val == beige):
						line += "  "
					elif np.all(val == red):
						line += "# "
					elif np.all(val == blue):
						line += " #"
					elif np.all(val == purple):
						line += "##"
					else:
						line += " "
				fontdata[tablerow].append(line)
			for row in unirgb[tablerow]:
				line = ""
				for val in row:
					if np.all(val == gray):
						line += "#"
					elif np.all(val == space):
						line += "1"
					else:
						line += " "
				unithing[tablerow].append(line)
			
			tablerow += 1
			print("\033[1Fgenerating, " +str(round(tablerow / (rowcount/100))) + "% complete")

	for metarow in unithing:

		hexfont = {
			" ### ## ### ": "0",
			" #  #  #  # ": "1",
			"###  ##  ###": "2",
			"##   # #####": "3",
			"#  # ####  #": "4",
			"####    ####": "5",
			" ###  ######": "6",
			"###  # #  # ": "7",
			"#### #######": "8",
			"######  ### ": "9",
			" ### ##### #": "a",
			"#  ## # ### ": "b",
			" ###  #   ##": "c",
			"## # ## ### ": "d",
			"####  ## ###": "e",
			"####  ## #  ": "f",
			" 111 11 111 ": "10",
			" 1  1  1  1 ": "11",
			"111  11  111": "12",
			"11   1 11111": "13",
			"1  1 1111  1": "14",
			"1111    1111": "15",
			" 111  111111": "16",
			"111  1 1  1 ": "17",
			"1111 1111111": "18",
			"111111  111 ": "19",
			" 111 11111 1": "1a",
			"1  11 1 111 ": "1b",
			" 111  1   11": "1c",
			"11 1 11 111 ": "1d",
			"1111  11 111": "1e",
			"1111  11 1  ": "1f",
			"# # # # #": "",
			"": ""

		}

		char1 = []
		char2 = []
		char3 = []
		char4 = []
		getbaseline = []
		for row in metarow:
			if row[0:3] != "   ":
				char1.append(row[0:3])
			if row[4:7] != "   ":
				char2.append(row[4:7])
			if row[8:11] != "   ":
				char3.append(row[8:11])
			if row[12:15] != "   ":
				char4.append(row[12:15])
			getbaseline.append(row[12:15])
		baselines.append(getbaseline.index(" # ")+2)
		codepointrows.append(hexfont["".join(char1)] + hexfont["".join(char2)] + hexfont["".join(char3)] +  hexfont["".join(char4)])

	chardata = []
	index = 0
	among = []
	the = []
	final = []
	for small in fontdata:
		among.append([])
		for element in small:
			among[index].append(element.split("_"))
		index+=1
	for small in among:
		the.append(np.transpose(small))

	indexoid = 0
	for thing in the:
		for smallthing in thing:
			start = 10
			end = 0
			for el in smallthing:
				if re.search("\S",el) :
					start = min(start, re.search("\S",el).start())
					for match in re.finditer("\S",el):
						pass
					end = max(end,match.end())
			chardata.append([])
			for el in smallthing:
				chardata[indexoid].append(el[start:end].replace("v"," "))
			indexoid+=1

	codepoints = [int(val + sus, 16) for val in codepointrows for sus in ["0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f"]]
	baselines = [val for val in baselines for sus in range(16)]

	with open('ultlf-data/data.json', 'w') as outfile:
		json.dump(chardata, outfile)
	with open('ultlf-data/codepoints.json', 'w') as outfile:
		json.dump(codepoints, outfile)
	with open('ultlf-data/baselines.json', 'w') as outfile:
		json.dump(baselines, outfile)

if __name__ == "__main__":
	generate()