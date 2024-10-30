import numpy as np
from PIL import Image
import PIL # pillow
import re
import math
import json
import time
import os
import ultlfgen
import discord
import asyncio
import bidi.algorithm as bidi # python-bidi
import unicodedata as uni


from dotenv import load_dotenv # python-dotenv
load_dotenv()
PNG_LOC = os.path.expanduser(os.getenv('PNG_LOC'))
SUSSY_LOC = os.path.expanduser(os.getenv('SUSSY_LOC'))

replacements = tpreplacements = ktavreplacements = chardata = codepoints = baselinedata = puadia = puadiaall = ""
def load():
	global replacements, tpreplacements, ktavreplacements, chardata, codepoints, baselinedata, puadia, puadiaall
	with open(SUSSY_LOC + "/replacements.json") as f:
		replacements = json.load(f)["array"]
	with open(SUSSY_LOC + "/tpreplacements.json") as f:
		tpreplacements = json.load(f)["array"]
	with open(SUSSY_LOC + "/ktavreplacements.json", encoding = "utf8") as f:
		ktavreplacements = json.load(f)["array"]

	with open('ultlf-data/trimmed.json') as f:
		chardata = json.load(f)
	with open('ultlf-data/codepoints.json') as f:
		codepoints = json.load(f)
	with open('ultlf-data/trimmed_baselines.json') as f:
		baselinedata = json.load(f)
	with open('thingies/puadia.json') as f:
		puadia = json.load(f)
	puadiaall = sum(puadia.values(), [])
load()
		

###################################

def width(string, spacing = 1):
	width = 0
	for i, glyph in enumerate(sussysplit(string)):
		gwidth = 0
		for char in glyph:
			if ord(char) not in codepoints or any( "X" in bee for bee in chardata[codepoints.index(ord(char))] ):
				raise Exception(f"{char}")
			if (char in puadiaall) or uni.category(char)[0] == "M":
				if char in puadia["top"] or uni.combining(char) == 230 or uni.combining(char) == 214 or uni.combining(char) == 232:
					w = len( trim(chardata[codepoints.index(ord(char))][:-5]) [0] )
				elif char in puadia["bottom"] or  uni.combining(char) == 202 or uni.combining(char) == 220:
					w = len( trim(chardata[codepoints.index(ord(char))] [5:]) [0] )
				else:
					w = len(chardata [codepoints.index(ord(char))] [0] )
			else:
				w = len(chardata [codepoints.index(ord(char))] [0] )
			gwidth = max(gwidth, w)
		width += (gwidth + spacing) if i != 0 else gwidth
	return width

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
		if char in sum(puadia.values(), []) or uni.category(char)[0] == "M":
			out[-1] += char
		else:
			out.append(char)
	return out

def gen(string, spacing = 1):
	global chardata, codepoints, baselinedata

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
				if (char in puadiaall) or uni.category(char)[0] == "M":
					#print(uni.combining(char))
					if (char in puadia["top"]) or uni.combining(char) == 230 or uni.combining(char) == 214: # top nonconnected, top connected
						combglyph = trim( chardata[codepoints.index(ord(char))][:-5] )
						#print(combglyph)
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

					elif char in puadia["bottom"] or  uni.combining(char) == 202 or uni.combining(char) == 220: # bottom connected, bottom disconnected 
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

	linesp = text.split("\n")
	lines = []
	if linethreshold not in (0,"∞"):
		for line in linesp:
			try:
				lines.extend(lbreak(line, spacing, linethreshold))
			except Exception as e:
				print("unsupported char " + str(e))
				return f"the character {str(e)} (u+{ord(str(e)):04x}) is not supported by ultlf."
	else:
		lines = linesp

	formattedlines = []
	bls = []
	errs = []


	for line in lines:
		if line != "":
			output, bl, err = gen(line, spacing)
			if re.match("char_invalid:",err):
				print("unsupported char " + err[-1])
				return f"the character {err[-1]} (u+{ord(err[-1]):04x}) is not supported by ultlf."
		else:
			output = "#"
			bl = 0
		formattedlines.append(output)
		bls.append(bl)

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

def lbreak(text, spacing, max):
	bee = max
	out = []
	outl = ""
	wspace = width(" ")
	for word in text.split(" "):
		w = width(word, spacing) + 2*spacing + wspace
		if w > bee:
			out.append(outl[:-1])
			if width(outl[:-1], spacing) > max:
				print(f"width of '{outl[:-1]}': {width(outl[:-1], spacing)} > {max}")
			outl = word + " "
			bee = max - w
		else:
			outl += word + " "
			bee -= w
	out.append(outl[:-1])
	if width(outl[:-1], spacing) > max:
		print("not ideal")
	return out

if __name__ == "__main__":
	bee = True
	if bee:

		with open('ultlf-data/codepoints.json') as f:
			codepoints = json.load(f)
		with open('ultlf-data/data.json') as f:
			chardata = json.load(f)

		#region bees
		# æ = 0xe200 # sitelen pona
		# œ = 0xe288
		# æ = 0x0250 # ipa extensions
		# œ = 0x02af
		# æ = 0x02b0 # spacing mod. letters
		# œ = 0x02ff
		# æ = 0x0180 # latin ext b
		# œ = 0x024f
		# æ = 0xa720 # latin ext d
		# œ = 0xa7ff
		#endregion bees

		# c = 0
		# thing = " " + " " * (æ % 16)
		# for e in range(œ-æ+1):
		# 	if (e+æ) in codepoints and "no" not in ["no" for item in chardata[codepoints.index(e+æ)] if "X" in item]:
		# 		thing += chr(e+æ) + ""
		# 	else:
		# 		thing += "\ue22a"
		# 	if (e+æ) % 16 == 15 and (e+æ) != œ:
		# 		thing += "\n "
		# thing += " " * (15 - (œ % 16))
		# genimage(thing, vspacing = 17)

		# with open(SUSSY_LOC + "/tokirap_sp.txt") as f:
		# 	tokirap_sp = f.read()
		# with open(SUSSY_LOC + "/tokirap_la.txt") as f:
		# 	tokirap_la = f.read()

		# genimage("hello, this is amzzzzogus. this is the impostor. i am not sure if bees are real, but your mother is\n bee not...")
	else:
		import time
		t1 = time.time()
		for x in range(1,100):
			len(gen("sú́sඞ́"*x)[0][0])
		for x in range(1000,1100):
			len(gen("beȩ🐝̀"*x)[0][0])
		t2 = time.time()
		for x in range(1,100):
			width("sú́sඞ́"*x)
		for x in range(1000,1100):
			width("beȩ🐝̀"*x)
		t3 = time.time()
		print(t2-t1, t3-t2)

		#].[ ].̇[].́[].̀[ 

		# print("")
		# 
		# print("")
		# for line in gen(sus)[0]:
		# 	print("".join([2*char for char in line]))