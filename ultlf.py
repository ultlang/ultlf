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
import unicodedata as uni


from dotenv import load_dotenv
load_dotenv()
PNG_LOC = os.path.expanduser(os.getenv('PNG_LOC'))
SUSSY_LOC = os.path.expanduser(os.getenv('SUSSY_LOC'))

with open(SUSSY_LOC + "/replacements.json") as f:
	replacements = json.load(f)["array"]
with open(SUSSY_LOC + "/tpreplacements.json") as f:
	tpreplacements = json.load(f)["array"]
with open(SUSSY_LOC + "/ktavreplacements.json", encoding = "utf8") as f:
	ktavreplacements = json.load(f)["array"]


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

	# string = bidi.get_display(str)
	string = str
	# for n in range(len(replacements)):
	# 	string = string.replace(replacements[n][0],replacements[n][1])
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

def o_imgprint(imgarray, str, xpos, ypos, colour, spacing):
	formatted, baseline, err = format(str, spacing)
	if err == "OK":
		for y, row in enumerate(formatted):
			arrayoid = list(row)
			for x, achar in enumerate(arrayoid):
				if achar == "#":
					imgarray[y+ypos-baseline,x+xpos] = colour
	else:
		print("uh oh")

def ullen(string, spacing = 1):
	with open('ultlf-data/data.json') as f:
		chardata = json.load(f)
	with open('ultlf-data/codepoints.json') as f:
		codepoints = json.load(f)
	if all( [(True if ord(char) in codepoints else False) for char in string] ):
		return sum( [len(chardata[codepoints.index(ord(char))][1]) for char in string] ) + spacing*(len(string)-1)
	else:
		return -100

def o_genimage(text, col = [0,0,0], bg = [255,255,255], spacing = 1, vspacing = 11, linethreshold = 200, repoptions = ""):
	# if bold:
	# 	text = "".join([chr(ord(i) + 57344) for i in text]) : removed

	text = bidi.get_display(text)

	for n in replacements:
		text = text.replace(n[0],n[1])

	if "t" in repoptions:
		for n in tpreplacements:
			text = re.sub(r"\b%s\b" % n[0] , n[1], text)
		text = text.replace(" ","")
	
	if "כ" in repoptions:
		for n in ktavreplacements:
			text = text.replace(n[0],n[1])

	if "𝒸" in repoptions:
		import random
		text = random.choice(["trolled","trollface","absolutely trolled","liberal destroyed","troled!!!!!!","trol!!!!","\ue000","amogn sus","sඞussy"])

	lines = text.split("\n")
	
	linesx = []

	print(lines)
	for line in lines:
		if line == "":
			linesx  += " "
			continue
		linesussier = []
		amog = False
		sussoid = line
		while not amog:
			linesus = []
			if ullen(sussoid) <= linethreshold:
				amog = True
				break
			while ullen(sussoid) > linethreshold:
				thing = sussoid.split(" ")
				while ullen(thing[0] + " ") > linethreshold + 4:
					amogushappymeal = thing.pop(0)
					for x in reversed( range(len(amogushappymeal)) ):
						if ullen(amogushappymeal[:x] + "-") < linethreshold:
							thing.insert(0, (amogushappymeal[:x] + "-"))
							thing.insert(1, amogushappymeal[x:])
							break

				linesus.insert(0, thing.pop())
				sussoid = " ".join(thing)
			linesussier.append(sussoid)
			#print(linesussier)
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

###################################

def termprint(string):
	data, bline, err = gen(string, 1)
	for line in data:
		print("".join([2*char for char in line]))

def trim(array):
	out = []
	for col in range( len(array[0])):
		if not all( array[n][col] == " " for n in range(len(array)) ):
			for n in range(len(array)):
				try:
					out[n] += array[n][col]
				except:
					out.append(array[n][col])
	return out

def sussysplit(string):
	out = []
	for char in string:
		if not uni.category(char)[0] == "M":
			out.append(char)
		else:
			out[-1] += char
	return out

def gen(string, spacing = 1):

	if os.path.getmtime("ultlf-data/data.json") < os.path.getmtime(PNG_LOC + "/ultlf.png"):
			print("out of date; regenerating from file")
			ultlfgen.generate()

	with open('ultlf-data/trimmed.json') as f:
		chardata = json.load(f)
	with open('ultlf-data/codepoints.json') as f:
		codepoints = json.load(f)
	with open('ultlf-data/trimmed_baselines.json') as f:
		baselinedata = json.load(f)                     # load the things.

	for char in string:
		if ord(char) not in codepoints:
			return "", 0, "char_invalid: " + char
		for x in chardata[codepoints.index(ord(char))]:
			if "X" in x:
				return "", 0, "char_invalid: " + char

	glyphforms = []
	baselines = []
	
	for glyph in sussysplit(string):
		if len(glyph) > 1:   # ≈ has combining characters (is suspicious (ඞ))
			if 230 in [uni.combining(char) for char in glyph] or 214 in [uni.combining(char) for char in glyph]:
				if glyph[0] == "i":
					glyph = "ı" + glyph[1:]

			baseglyph = chardata[codepoints.index(ord(glyph[0]))]
			baseline = baselinedata[codepoints.index(ord(glyph[0]))]
			pos = len(glyphforms)
			for char in glyph[1:]:
				if uni.category(char)[0] == "M":
					#print(uni.combining(char))
					if uni.combining(char) == 230 or uni.combining(char) == 214: # top nonconnected, top connected
						combglyph = trim( chardata[codepoints.index(ord(char))][:-5] )
						print(combglyph)
						combbaseline = baselinedata[codepoints.index(ord(char))]
						if len(combglyph[1]) > len(baseglyph[1]):
							baseglyph = [math.floor((len(combglyph[1])-len(row))/2) * " "+ row + (math.ceil((len(combglyph[1])-len(row))/2) * " ") for row in baseglyph]
						elif len(combglyph[1]) < len(baseglyph[1]):
							combglyph = [math.ceil((len(baseglyph[1])-len(row))/2) * " " + row + (math.floor((len(baseglyph[1])-len(row))/2) * " ") for row in combglyph]
						baseglyph = combglyph + baseglyph
						baseline = baseline + combbaseline - 4
					
					elif uni.combining(char) == 232: # above right
						combglyph = trim( chardata[codepoints.index(ord(char))][:-5] )
						combbaseline = baselinedata[codepoints.index(ord(char))]
						if len(combglyph[1]) > len(baseglyph[1]):
							baseglyph = [ row + (len(baseglyph[1])-len(row)) * " " for row in baseglyph]
						elif len(combglyph[1]) < len(baseglyph[1]):
							combglyph = [ (len(combglyph[1])-len(row)) * " " + row  for row in combglyph]
						baseglyph = combglyph + baseglyph
						baseline = baseline + combbaseline - 4

					elif uni.combining(char) == 202 or uni.combining(char) == 220: # bottom connected, bottom disconnected 
						combglyph = trim( chardata[codepoints.index(ord(char))][5:] )
						combbaseline = baselinedata[codepoints.index(ord(char))]
						if len(combglyph[1]) > len(baseglyph[1]):
							baseglyph = [math.ceil((len(combglyph[1])-len(row))/2) * " "+ row + (math.floor((len(combglyph[1])-len(row))/2) * " ") for row in baseglyph]
						elif len(combglyph[1]) < len(baseglyph[1]):
							combglyph = [math.floor((len(baseglyph[1])-len(row))/2) * " " + row + (math.ceil((len(baseglyph[1])-len(row))/2) * " ") for row in combglyph]
						baseglyph = baseglyph + combglyph
					
					else:
						glyphforms.append( chardata[codepoints.index(ord(char))] )
						baselines.append( baselinedata[codepoints.index(ord(char))] )
						print("when the sussy sus among us is sus!")
			glyphforms.insert(pos, baseglyph )
			baselines.insert(pos, baseline )
				
		else:
			glyphforms.append( chardata[codepoints.index(ord(glyph))] )
			baselines.append( baselinedata[codepoints.index(ord(glyph))] )
	

	# pad with blanks
	padded = []
	descend = max( [len(x[0]) - x[1] for x in list(zip(glyphforms, baselines))] )
	ascend =  max( [x[1]             for x in list(zip(glyphforms, baselines))] )
	for glyph, base in list(zip(glyphforms, baselines)):
		padded.insert(0,  (ascend - base) * [" " * len(glyph[0])]    + glyph +   [" " * len(glyph[0])] * (descend - (len(glyph) - base)))

	out = [(' ' * spacing).join(row) for row in np.rot90(padded, axes=(1,0))]
	out = [row.replace("v"," ") for row in out]
	baseline = ascend
	# print(np.asarray(out))

	return out, baseline, "OK"

def genimage(text, col = [0,0,0], bg = [255,255,255], spacing = 1, vspacing = 11, linethreshold = 200, repoptions = ""):
	# if bold:
	# 	text = "".join([chr(ord(i) + 57344) for i in text]) : removed

	text = bidi.get_display(text)

	for n in replacements:
		text = text.replace(n[0],n[1])

	if "t" in repoptions:
		for n in tpreplacements:
			text = re.sub(r"\b%s\b" % n[0] , n[1], text)
		text = text.replace(" ","")
	
	if "כ" in repoptions:
		for n in ktavreplacements:
			text = text.replace(n[0],n[1])

	if "𝒸" in repoptions:
		import random
		text = random.choice(["trolled","trollface","absolutely trolled","liberal destroyed","troled!!!!!!","trol!!!!","\ue000","amogn sus","sඞussy"])

	lines = text.split("\n")

	formattedlines = []
	bls = []
	errs = []


	for line in lines:
		if line != "":
			output, bl, err = gen(line, spacing)
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

def imgprint(imgarray, str, xpos, ypos, colour, spacing):
	formatted, baseline, err = gen(str, spacing)
	if err == "OK":
		for y, row in enumerate(formatted):
			arrayoid = list(row)
			for x, achar in enumerate(arrayoid):
				if achar == "#":
					imgarray[y+ypos-baseline,x+xpos] = colour
	else:
		print("uh oh")

if __name__ == "__main__":
	bee = False
	if bee:

		with open('ultlf-data/codepoints.json') as f:
			codepoints = json.load(f)
		with open('ultlf-data/data.json') as f:
			chardata = json.load(f)
		
		print( ullen("ll") )

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
	else:
		# import time
		# t1 = time.time()
		# for x in range(1,200):
		# 	format("susඞ"*500)
		# 	if x%10 == 0:
		# 		print(x/10)
		# t2 = time.time()
		# for x in range(1,200):
		# 	gen("susඞ"*500)
		# 	if x%10 == 0:
		# 		print(x/10)
		# t3 = time.time()
		# print(t2-t1, t3-t2)

		#].[ ].̇[].́[].̀[ 

		# print("")
		# 
		# print("")
		# for line in gen(sus)[0]:
		# 	print("".join([2*char for char in line]))

		sus = input()
		genimage(sus)
		termprint(sus)