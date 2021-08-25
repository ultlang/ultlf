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
	[":penis:","\U000130b8"],
	["[penis]","\U000130b8"],
	[":chungus:","\ue004"],
	["[chungus]","\ue004"],
	#region toki pona
	["[tpA]","\ue200"],
	["[tpAkesi]","\ue201"],
	["[tpAla]","\ue202"],
	["[tpAlasa]","\ue203"],
	["[tpAle]","\ue204"],
	["[tpAli]","\ue204"], # alternates c:
	["[tpAnpa]","\ue205"],
	["[tpAnte]","\ue206"],
	["[tpAnu]","\ue207"],
	["[tpAwen]","\ue208"],
	["[tpE]","\ue209"],
	["[tpEn]","\ue20a"],
	["[tpEsun]","\ue20b"],
	["[tpIjo]","\ue20c"],
	["[tpIke]","\ue20d"],
	["[tpIlo]","\ue20e"],
	["[tpInsa]","\ue20f"],
	["[tpJaki]","\ue210"],
	["[tpJan]","\ue211"],
	["[tpJelo]","\ue212"],
	["[tpJo]","\ue213"],
	["[tpKala]","\ue214"],
	["[tpKalama]","\ue215"],
	["[tpKama]","\ue216"],
	["[tpKasi]","\ue217"],
	["[tpKen]","\ue218"],
	["[tpKepeken]","\ue219"],
	["[tpKili]","\ue21a"],
	["[tpKiwen]","\ue21b"],
	["[tpKo]","\ue21c"],
	["[tpKon]","\ue21d"],
	["[tpKule]","\ue21e"],
	["[tpKulupu]","\ue21f"],
	["[tpKute]","\ue220"],
	["[tpLa]","\ue221"],
	["[tpLape]","\ue222"],
	["[tpLaso]","\ue223"],
	["[tpLawa]","\ue224"],
	["[tpLen]","\ue225"],
	["[tpLete]","\ue226"],
	["[tpLi]","\ue227"],
	["[tpLili]","\ue228"],
	["[tpLinja]","\ue229"],
	["[tpLipu]","\ue22a"],
	["[tpLoje]","\ue22b"],
	["[tpLon]","\ue22c"],
	["[tpLuka]","\ue22d"],
	["[tpLukin]","\ue22e"],
	["[tpLupa]","\ue22f"],
	["[tpMa]","\ue230"],
	["[tpMama]","\ue231"],
	["[tpMani]","\ue232"],
	["[tpMeli]","\ue233"],
	["[tpMi]","\ue234"],
	["[tpMije]","\ue235"],
	["[tpMoku]","\ue236"],
	["[tpMoli]","\ue237"],
	["[tpMonsi]","\ue238"],
	["[tpMu]","\ue239"],
	["[tpMun]","\ue23a"],
	["[tpMusi]","\ue23b"],
	["[tpMute]","\ue23c"],
	["[tpNanpa]","\ue23d"],
	["[tpNasa]","\ue23e"],
	["[tpNasin]","\ue23f"],
	["[tpNena]","\ue240"],
	["[tpNi]","\ue241"],
	["[tpNimi]","\ue242"],
	["[tpNoka]","\ue243"],
	["[tpO]","\ue244"],
	["[tpOlin]","\ue245"],
	["[tpOna]","\ue246"],
	["[tpOpen]","\ue247"],
	["[tpPakala]","\ue248"],
	["[tpPali]","\ue249"],
	["[tpPalisa]","\ue24a"],
	["[tpPan]","\ue24b"],
	["[tpPana]","\ue24c"],
	["[tpPi]","\ue24d"],
	["[tpPilin]","\ue24e"],
	["[tpPimeja]","\ue24f"],
	["[tpPini]","\ue250"],
	["[tpPipi]","\ue251"],
	["[tpPoka]","\ue252"],
	["[tpPoki]","\ue253"],
	["[tpPona]","\ue254"],
	["[tpPu]","\ue255"],
	["[tpSama]","\ue256"],
	["[tpSeli]","\ue257"],
	["[tpSelo]","\ue258"],
	["[tpSeme]","\ue259"],
	["[tpSewi]","\ue25a"],
	["[tpSijelo]","\ue25b"],
	["[tpSike]","\ue25c"],
	["[tpSin]","\ue25d"],
	["[tpSina]","\ue25e"],
	["[tpSinpin]","\ue25f"],
	["[tpSitelen]","\ue260"],
	["[tpSona]","\ue261"],
	["[tpSoweli]","\ue262"],
	["[tpSuli]","\ue263"],
	["[tpSuno]","\ue264"],
	["[tpSupa]","\ue265"],
	["[tpSuwi]","\ue266"],
	["[tpTan]","\ue267"],
	["[tpTaso]","\ue268"],
	["[tpTawa]","\ue269"],
	["[tpTelo]","\ue26a"],
	["[tpTenpo]","\ue26b"],
	["[tpToki]","\ue26c"],
	["[tpTomo]","\ue26d"],
	["[tpTu]","\ue26e"],
	["[tpUnpa]","\ue26f"],
	["[tpUta]","\ue270"],
	["[tpUtala]","\ue271"],
	["[tpWalo]","\ue272"],
	["[tpWan]","\ue273"],
	["[tpWaso]","\ue274"],
	["[tpWawa]","\ue275"],
	["[tpWeka]","\ue276"],
	["[tpWile]","\ue277"],
	["[tpNamako]","\ue278"],
	["[tpKin]","\ue279"],
	["[tpOko]","\ue27a"],
	["[tpKipisi]","\ue27b"],
	["[tpLeko]","\ue27c"],
	["[tpMonsuta]","\ue27d"],
	["[tpMisikeke]","\ue27e"],
	["[tpTonsi]","\ue27f"],
	["[tpJasima]","\ue280"],
	["[tpSoko]","\ue281"],
	["[tpMeso]","\ue282"],
	["[tpEpiku]","\ue283"],
	["[tpKokosila]","\ue284"],
	["[tpLanpan]","\ue285"],
	["[tpN]","\ue286"],
	["[tpKijetesantakalu]","\ue287"],
	["[tpKu]","\ue288"],
	#endregion
	["​",""] #zwsp deletion trol
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
		baselines = json.load(f)                     # load the things.

	string = str
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

def genimage(text, col = [0,0,0], bg = [255,255,255], bold = False, spacing = 1, vspacing = 11):
	if bold:
		text = "".join([chr(ord(i) + 57344) for i in text])

	lines = text.split("\n")
	
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
			output = "bee"
			bl = "yo mama"
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
	format("æ")

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
	genimage(thing, vspacing = 17)