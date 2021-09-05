from codecs import xmlcharrefreplace_errors
import numpy as np
from PIL import Image
import PIL
import re
import math
import json
import time
import os
import ultlfgen
import discord
import asyncio
import bidi.algorithm as bidi


from dotenv import load_dotenv
load_dotenv()
PNG_LOC = os.getenv('PNG_LOC')
SUSSY_LOC = os.getenv('SUSSY_LOC')

with open(SUSSY_LOC + "/replacements.json") as f:
	replacements = json.load(f)["array"]

def format(str, spacing = 1):

	if os.path.getmtime("ultlf-data/data.json") < os.path.getmtime(PNG_LOC + "/ultlf.png"):
		print("out of date; regenerating from file")
		ultlfgen.generate()
	
	with open('ultlf-data/data.json') as f:
		chardata = json.load(f)
	with open('ultlf-data/codepoints.json') as f:
		codepoints = json.load(f)
	with open('ultlf-data/baselines.json') as f:
		baselines = json.load(f)                     # load the things.

	string = bidi.get_display(str)
	for n in range(len(replacements)):
		string = string.replace(replacements[n][0],replacements[n][1])
	# `string` now has the replacements
	array = [] # array of the characters, copied from data.json
	baselinoids = [] # array of baselines for the string being rendered
	heightoids = [] # array of `array` subarrays' lengths, i think
	i = 0

	for i,c in enumerate(string): # find baselines for every char in string
		try:
			baselinoids.append( baselines[codepoints.index(ord(c))] )
		except: return [["no"]], 0, "char_invalid: " + c
	
	for i, c in enumerate(string):
		numval = codepoints.index(ord(c)) # numval is the index of the char codepoint in `codepoints`, i think
		array.append(chardata[numval].copy())
		while max(baselinoids) > baselinoids [i] :
			array[i].insert( 0, " "*len(array[i][0]) ) # add blanks to the start so that the baseline matches the lowest one 
			baselinoids[i] += 1
		heightoids.append(len(array[i]))
	
	for i, c in enumerate(string):
		while max(heightoids) > heightoids [i] :
			array[i].append(" "*len(array[i][0]) )
			heightoids[i] += 1
		# ok so by now, `array` should contain data for all the characters in order with matching heights (filled w blanks).

	sussoids = []
	output = []

	for row in range(heightoids[0]):
		line = ""
		for ch in range(len(array)):
			if ch + 1 != len(array):
				line += array[ch][row] + spacing * " "
			else:
				line += array[ch][row] + " "

		if line.strip() != "" or ( baselinoids[0] - row < 7 and baselinoids[0] - row > 0):
			sussoids.append(row)
			# ok. so i'm p sure that this makes `sussoids` the row numbers which have any content OR are in the always shown range.
	
	for row in range(min(sussoids), max(sussoids)+1):
		line = ""
		for ch in range(len(array)):
			if string[ch] == "\ue07f" and ch != 0:
				line += (14 - len(array[ch-1][row])) * " "
			elif ch + 1 != len(array):
				line += array[ch][row] + spacing * " "
			else:
				line += array[ch][row] + " "
			if "X" in line:
				return [["no"]], 0, "char_invalid: " + string[ch]	
		output.append(line[:-1])
		# and this then assembles the `output`. sus
	bline = baselinoids[0] - min(sussoids)
	return output, bline, "OK"

def termprint(string):
	data, bline, err = format(string, 1)
	for line in data:
		print("".join([2*char for char in line]))

def imgprint(imgarray, str, xpos, ypos, colour, spacing):
	formatted, baseline, err = format(str, spacing)
	if err == "OK":
		for y, row in enumerate(formatted):
			arrayoid = list(row)
			for x, achar in enumerate(arrayoid):
				if achar == "#":
					imgarray[y+ypos-baseline,x+xpos] = colour
	else:
		print("uh oh")

def genimage(text, col = [0,0,0], bg = [255,255,255], spacing = 1, vspacing = 11):
	# if bold:
	# 	text = "".join([chr(ord(i) + 57344) for i in text]) : removed


	text = bidi.get_display(text)
	for n in range(len(replacements)):
		text = text.replace(replacements[n][0],replacements[n][1])

	lines = text.split("\n")

	linethreshold = 200

	linesx = []

	for line in lines:
		if line == "":
			linesx  += " "
			continue
		linesussier = []
		amog = False
		sussoid = line
		while not amog:
			linesus = []
			if len( format(sussoid)[0][0] ) <= linethreshold:
				amog = True
				break
			while len( format(sussoid)[0][0] ) > linethreshold:
				thing = sussoid.split(" ")
				while len( format( thing[0])[0][0] ) > linethreshold:
					amogushappymeal = thing.pop(0)
					for x in reversed( range(len(amogushappymeal)) ):
						if len( format(amogushappymeal[:x] + "-")[0][0] ) < linethreshold:
							thing.insert(0, (amogushappymeal[:x] + "-"))
							thing.insert(1, amogushappymeal[x:])
							break

				linesus.insert(0, thing.pop())
				sussoid = " ".join(thing)
				print(sussoid)
			linesussier.append(sussoid)
			print(linesussier)
			sussoid = " ".join(linesus)
		linesx += linesussier
		linesx.append(sussoid)
	
	lines = linesx 

	formattedlines = []
	bls = []
	errs = []


	for line in lines:
		if line != "":
			output, bl, err = format(line, spacing)
			if re.match("char_invalid:",err):
				print("unsupported char " + err[-1])
				return "the character " + err[-1] + " is not supported by ultlf."
		else:
			output = "#"
			bl = 0
		formattedlines.append(output)
		bls.append(bl)
		
	sussy = bls[0]

	imgwidth  = max( len(i[0]) for i in formattedlines ) + 2
	imgheight = 2 + bls[0] + (len(lines)-1)*vspacing + len(formattedlines[-1]) - bls[-1]

	aaa = np.full( ( imgheight, imgwidth , 3), bg , dtype=np.uint8 )

	for l in range(len(lines)):
		if lines[l] != "":
			imgprint(aaa, lines[l] , 1 , 1+bls[0]+l*vspacing , col, spacing)

	im = Image.fromarray(aaa).resize([10 * imgwidth ,10 * imgheight],PIL.Image.NEAREST).save('ul.png')
	print("printed " + text)
	return True

if __name__ == "__main__":

	with open('ultlf-data/codepoints.json') as f:
		codepoints = json.load(f)
	with open('ultlf-data/data.json') as f:
		chardata = json.load(f)
	
	# æ = 0xe200 # sitelen pona
	# œ = 0xe288
	# æ = 0x0250 # ipa extensions
	# œ = 0x02af
	# æ = 0x02b0 # spacing mod. letters
	# œ = 0x02ff
	æ = 0x0180 # latin ext b
	œ = 0x024f

	c = 0
	thing = " " + " " * (æ % 16)
	for e in range(œ-æ+1):
		if (e+æ) in codepoints and "no" not in ["no" for item in chardata[codepoints.index(e+æ)] if "X" in item]:
			thing += chr(e+æ) + ""
		else:
			thing += "\ue22a"
		if (e+æ) % 16 == 15 and (e+æ) != œ:
			thing += "\n "
	thing += " " * (15 - (œ % 16))
	#genimage(thing, vspacing = 17)


	with open(SUSSY_LOC + "/tokirap_sp.txt") as f:
		tokirap_sp = f.read()
	with open(SUSSY_LOC + "/tokirap_la.txt") as f:
		tokirap_la = f.read()

	genimage(tokirap_sp)