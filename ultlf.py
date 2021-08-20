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


from dotenv import load_dotenv
load_dotenv()
PNG_LOC = os.getenv('PNG_LOC')

replacements = [
	["[trollface]","\ue000"],
	["<:trollface:767002124382240799>","\ue000"],
	["<:Trolxel:846082357525610506>","\ue000"],
	[":trollface:","\ue000"],
	["[altV]","\ue001"],
	["[piguy]","\ue002"],
	["[sus]","\u0d9e"],
	["[amogus]","\u0d9e"],
	[":sus:","\u0d9e"],
	[":amogus:","\u0d9e"],
	["​",""], #zwsp deletion trol
	[":penis:","\U000130b8"],
	["[penis]","\U000130b8"],
	[":chungus:","\ue004"],
	["[chungus]","\ue004"]
]

















def format(str, spacing = 1):

	if os.path.getmtime("ultlf-data/data.json") < os.path.getmtime(PNG_LOC + "/ultlf.png"):
		print("out of date; regenerating from file")
		ultlfgen.generate()
	
	with open('ultlf-data/data.json') as f:
		chardata = json.load(f)
	with open('ultlf-data/codepoints.json') as f:
		codepoints = json.load(f)
	with open('ultlf-data/baselines.json') as f:
		baselines = json.load(f)

	string = str
	for n in range(len(replacements)):
		string = string.replace(replacements[n][0],replacements[n][1])
	array = []
	baselinoids = []
	heightoids = []
	i = 0
	for i,c in enumerate(string):
		try:
			baselinoids.append( baselines[codepoints.index(ord(c))] )
		except: return [["no"]], 0, "char_invalid: " + c
	for i, c in enumerate(string):
		numval = codepoints.index(ord(c))
		array.append(chardata[numval].copy())
		while max(baselinoids) > baselinoids [i] :
			array[i].insert( 0, " "*len(array[i][0]) )
			baselinoids[i] += 1
		heightoids.append(len(array[i]))
	for i, c in enumerate(string):
		while max(heightoids) > heightoids [i] :
			array[i].append(" "*len(array[i][0]) )
			heightoids[i] += 1
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
	for row in range(min(sussoids), max(sussoids)+1):
		line = ""
		for ch in range(len(array)):
			if ch + 1 != len(array):
				line += array[ch][row] + spacing * " "
			else:
				line += array[ch][row] + " "
			if "X" in line:
				print(line)
				return [["no"]], 0, "char_invalid: " + string[ch]	
		output.append(line[:-1])
	bline = baselinoids[0] - min(sussoids)
	return output, bline, "OK"

def termprint(string):
	data, bline, err = format(string, 1)
	for line in data:
		print(line)

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

def genimage(text, col, bg, bold, spacing):
	if bold:
		text = "".join([chr(ord(i) + 57344) for i in text])

	output, bl, err = format(text, spacing)
	if re.match("char_invalid:",err):
		print("unsupported char " + err[-1])
		return "the character " + err[-1] + " is not supported by ultlf."
	else:
		aaa = np.full( ( len(output)+2, len(output[0])+2 , 3), bg , dtype=np.uint8 )
		imgprint(aaa,text,1,bl+1,col, spacing)
		im = Image.fromarray(aaa).resize([10 * ((len(output[0])+2)) ,10 * (len(output)+2)],PIL.Image.NEAREST).save('ul.png')
		print("printed " + text)
		return True

termprint("amogus trolface")