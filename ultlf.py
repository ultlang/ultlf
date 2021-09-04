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
	["[tp_a]","\ue200"],
	["[tp_akesi]","\ue201"],
	["[tp_ala]","\ue202"],
	["[tp_alasa]","\ue203"],
	["[tp_ale]","\ue204"],
	["[tp_ali]","\ue204"], # alternates c:
	["[tp_anpa]","\ue205"],
	["[tp_ante]","\ue206"],
	["[tp_anu]","\ue207"],
	["[tp_awen]","\ue208"],
	["[tp_e]","\ue209"],
	["[tp_en]","\ue20a"],
	["[tp_esun]","\ue20b"],
	["[tp_ijo]","\ue20c"],
	["[tp_ike]","\ue20d"],
	["[tp_ilo]","\ue20e"],
	["[tp_insa]","\ue20f"],
	["[tp_jaki]","\ue210"],
	["[tp_jan]","\ue211"],
	["[tp_jelo]","\ue212"],
	["[tp_jo]","\ue213"],
	["[tp_kala]","\ue214"],
	["[tp_kalama]","\ue215"],
	["[tp_kama]","\ue216"],
	["[tp_kasi]","\ue217"],
	["[tp_ken]","\ue218"],
	["[tp_kepeken]","\ue219"],
	["[tp_kili]","\ue21a"],
	["[tp_kiwen]","\ue21b"],
	["[tp_ko]","\ue21c"],
	["[tp_kon]","\ue21d"],
	["[tp_kule]","\ue21e"],
	["[tp_kulupu]","\ue21f"],
	["[tp_kute]","\ue220"],
	["[tp_la]","\ue221"],
	["[tp_lape]","\ue222"],
	["[tp_laso]","\ue223"],
	["[tp_lawa]","\ue224"],
	["[tp_len]","\ue225"],
	["[tp_lete]","\ue226"],
	["[tp_li]","\ue227"],
	["[tp_lili]","\ue228"],
	["[tp_linja]","\ue229"],
	["[tp_lipu]","\ue22a"],
	["[tp_loje]","\ue22b"],
	["[tp_lon]","\ue22c"],
	["[tp_luka]","\ue22d"],
	["[tp_lukin]","\ue22e"],
	["[tp_lupa]","\ue22f"],
	["[tp_ma]","\ue230"],
	["[tp_mama]","\ue231"],
	["[tp_mani]","\ue232"],
	["[tp_meli]","\ue233"],
	["[tp_mi]","\ue234"],
	["[tp_mije]","\ue235"],
	["[tp_moku]","\ue236"],
	["[tp_moli]","\ue237"],
	["[tp_monsi]","\ue238"],
	["[tp_mu]","\ue239"],
	["[tp_mun]","\ue23a"],
	["[tp_musi]","\ue23b"],
	["[tp_mute]","\ue23c"],
	["[tp_nanpa]","\ue23d"],
	["[tp_nasa]","\ue23e"],
	["[tp_nasin]","\ue23f"],
	["[tp_nena]","\ue240"],
	["[tp_ni]","\ue241"],
	["[tp_nimi]","\ue242"],
	["[tp_noka]","\ue243"],
	["[tp_o]","\ue244"],
	["[tp_olin]","\ue245"],
	["[tp_ona]","\ue246"],
	["[tp_open]","\ue247"],
	["[tp_pakala]","\ue248"],
	["[tp_pali]","\ue249"],
	["[tp_palisa]","\ue24a"],
	["[tp_pan]","\ue24b"],
	["[tp_pana]","\ue24c"],
	["[tp_pi]","\ue24d"],
	["[tp_pilin]","\ue24e"],
	["[tp_pimeja]","\ue24f"],
	["[tp_pini]","\ue250"],
	["[tp_pipi]","\ue251"],
	["[tp_poka]","\ue252"],
	["[tp_poki]","\ue253"],
	["[tp_pona]","\ue254"],
	["[tp_pu]","\ue255"],
	["[tp_sama]","\ue256"],
	["[tp_seli]","\ue257"],
	["[tp_selo]","\ue258"],
	["[tp_seme]","\ue259"],
	["[tp_sewi]","\ue25a"],
	["[tp_sijelo]","\ue25b"],
	["[tp_sike]","\ue25c"],
	["[tp_sin]","\ue25d"],
	["[tp_sina]","\ue25e"],
	["[tp_sinpin]","\ue25f"],
	["[tp_sitelen]","\ue260"],
	["[tp_sona]","\ue261"],
	["[tp_soweli]","\ue262"],
	["[tp_suli]","\ue263"],
	["[tp_suno]","\ue264"],
	["[tp_supa]","\ue265"],
	["[tp_suwi]","\ue266"],
	["[tp_tan]","\ue267"],
	["[tp_taso]","\ue268"],
	["[tp_tawa]","\ue269"],
	["[tp_telo]","\ue26a"],
	["[tp_tenpo]","\ue26b"],
	["[tp_toki]","\ue26c"],
	["[tp_tomo]","\ue26d"],
	["[tp_tu]","\ue26e"],
	["[tp_unpa]","\ue26f"],
	["[tp_uta]","\ue270"],
	["[tp_utala]","\ue271"],
	["[tp_walo]","\ue272"],
	["[tp_wan]","\ue273"],
	["[tp_waso]","\ue274"],
	["[tp_wawa]","\ue275"],
	["[tp_weka]","\ue276"],
	["[tp_wile]","\ue277"],
	["[tp_namako]","\ue278"],
	["[tp_kin]","\ue279"],
	["[tp_oko]","\ue27a"],
	["[tp_kipisi]","\ue27b"],
	["[tp_leko]","\ue27c"],
	["[tp_monsuta]","\ue27d"],
	["[tp_misikeke]","\ue27e"],
	["[tp_tonsi]","\ue27f"],
	["[tp_jasima]","\ue280"],
	["[tp_soko]","\ue281"],
	["[tp_meso]","\ue282"],
	["[tp_epiku]","\ue283"],
	["[tp_kokosila]","\ue284"],
	["[tp_lanpan]","\ue285"],
	["[tp_n]","\ue286"],
	["[tp_kijetesantakalu]","\ue287"],
	["[tp_ku]","\ue288"],
	["[tp_apeja]","\ue289"],
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

	genimage("amoguguguguguisdgsfhdgosdjiofgsdnfgiovaudrféviaufiovauovghi da  fhiauf ahf dhf jdhf jhdf jhd fj hdjfh jdf fhiauf ahf dhf jdhf jhdf jhd fj hdjfh jdf fhiau\nf ahf dhf jdhf jhdf jhd fj hdjfh jdf jdhf hd fjh")

	#region tokirap lyrics
	tokirap_sp = """[tp_toki]! [tp_ni][tp_la][tp_mi][tp_toki][tp_musi][tp_e][tp_nimi][tp_ale][tp_pi][tp_toki][tp_pona]! 
[tp_sina][tp_ken][tp_kute][tp_taso]. [tp_mi][tp_pali][tp_e][tp_ijo][tp_suli].
[tp_mi][tp_o][tp_open]!
 
[tp_jan][tp_li][tp_wile][tp_awen][tp_sona][tp_e][tp_nimi] 
[tp_la][tp_ona][tp_li][tp_wile][tp_kute][tp_e][tp_musi][tp_ni]!
 
[tp_mi],[tp_sina],[tp_ni],[tp_ona]
[tp_olin],[tp_musi],[tp_suwi],[tp_pona]
[tp_li],[tp_e],[tp_la],[tp_pi],[tp_o]
[tp_anu],[tp_en],[tp_seme],[tp_ijo]

[tp_toki][tp_ni][tp_li][tp_jo][tp_e][tp_nimi][tp_ni]
[tp_toki][tp_pona]!

[tp_ni][tp_li][tp_nasin][tp_nasa][tp_pi][tp_kama][tp_sona]
[tp_taso],[tp_ona][tp_li][tp_pali][tp_la][tp_ale][tp_li][tp_pona]
 
[tp_kule],[tp_lukin],[tp_kalama],[tp_kute]
[tp_ala],[tp_wan],[tp_tu],[tp_mute]
[tp_soweli],[tp_akesi],[tp_pipi],[tp_waso]
[tp_kala],[tp_loje],[tp_jelo],[tp_laso]

[tp_toki][tp_ni][tp_li][tp_jo][tp_e][tp_nimi][tp_ni]
[tp_nimi][tp_ale][tp_lon][tp_toki]...!
 
[tp_moli],[tp_utala],[tp_pakala],[tp_ike]
[tp_nena],[tp_lupa],[tp_leko],[tp_sike]
[tp_lon],[tp_tan],[tp_kepeken],[tp_tawa]
[tp_luka],[tp_noka],[tp_sijelo],[tp_lawa]
 
[tp_o][tp_kama][tp_sona]! [tp_o][tp_kama][tp_sona]!
[tp_o][tp_kama][tp_sona]! [tp_o][tp_kama][tp_sona]! [tp_e]
[tp_nimi][tp_ale][tp_lon][tp_toki][tp_pona]!
 
[tp_supa],[tp_linja],[tp_insa],[tp_selo]
[tp_ko],[tp_kiwen],[tp_kon],[tp_telo]
[tp_sewi],[tp_anpa],[tp_sinpin],[tp_monsi]
[tp_jan],[tp_meli],[tp_mije],[tp_tonsi]
 
[tp_pona]! [tp_ni][tp_la][tp_mi][tp_tu][tp_e][tp_nasin]!
[tp_taso],[tp_musi][tp_li][tp_pini][tp_ala].
[tp_mi][tp_o][tp_awen]!
 
[tp_poka],[tp_nasin],[tp_kulupu],[tp_poki]
[tp_sitelen],[tp_nimi],[tp_lipu],[tp_toki]
[tp_lete],[tp_seli],[tp_suli],[tp_lili]
[tp_kasi],[tp_pan],[tp_moku],[tp_kili]
 
[tp_nimi][tp_ale][tp_mute][tp_luka][tp_luka][tp_tu][tp_taso][tp_la]
[tp_jan][tp_ale][tp_li][tp_ken][tp_lon][tp_kulupu][tp_pi][tp_toki][tp_pona]
 
[tp_nasa],[tp_ante],[tp_jasima],[tp_sama]
[tp_lape],[tp_tomo],[tp_pali],[tp_mama]
[tp_ma],[tp_suno],[tp_mun],[tp_palisa]
[tp_ilo],[tp_nanpa],[tp_sona],[tp_alasa]
 
[tp_pona][tp_a]! [tp_o][tp_moku][tp_e][tp_kon]. [tp_nimi][tp_mute][tp_mute][tp_taso][tp_li][tp_kama].
[tp_o][tp_kute][tp_pona]!
 
[tp_kama],[tp_open],[tp_awen],[tp_pini]
[tp_wile],[tp_esun],[tp_mani],[tp_kipisi]
[tp_pana],[tp_jo],[tp_lanpan],[tp_tenpo]
[tp_weka],[tp_jaki],[tp_ale],[tp_meso]
[tp_pilin],[tp_uta],[tp_unpa],[tp_oko]
[tp_ken],[tp_sin],[tp_namako],[tp_soko]
 
[tp_o][tp_kama][tp_sona]! [tp_o][tp_kama][tp_sona]!
[tp_o][tp_kama][tp_sona]! [tp_o][tp_kama][tp_sona]! [tp_e]
[tp_nimi][tp_ale][tp_lon][tp_toki][tp_pona]!
 
[tp_len],[tp_taso],[tp_walo],[tp_pimeja]
[tp_mu],[tp_wawa],[tp_a],[tp_monsuta]
[tp_n],[tp_kin],[tp_misikeke],[tp_epiku]
[tp_kokosila],[tp_pu],[tp_ku],[tp_kijetesantakalu]
 
[tp_toki][tp_ni][tp_li][tp_jo][tp_e][tp_nimi][tp_ni]
[tp_nimi][tp_ale][tp_lon][tp_toki]...
[tp_toki][tp_ni][tp_li][tp_jo][tp_e][tp_nimi][tp_ni]
[tp_nimi][tp_ale][tp_lon][tp_toki]...
[tp_toki][tp_ni][tp_li][tp_jo][tp_e][tp_nimi][tp_ni]
[tp_nimi][tp_ale][tp_lon][tp_toki]...
[tp_toki][tp_ni][tp_li][tp_jo][tp_e][tp_nimi][tp_ni]
[tp_nimi][tp_ale][tp_lon][tp_toki][tp_pona]!"""

	tokirap_la = """toki! ni la mi toki musi e nimi ale pi toki pona! 
sina ken kute taso. mi pali e ijo suli .
mi o open!
 
jan li wile awen sona e nimi 
la ona li wile kute e musi ni!
 
mi, sina, ni, ona
olin, musi, suwi, pona
li, e, la, pi, o
anu, en, seme, ijo

toki ni li jo e nimi ni
toki pona!

ni li nasin nasa pi kama sona
taso, ona li pali la ale li pona
 
kule, lukin, kalama, kute
ala, wan, tu, mute
soweli, akesi, pipi, waso
kala, loje, jelo, laso

toki ni li jo e nimi ni
nimi ale lon toki...!
 
moli, utala, pakala, ike
nena, lupa, leko, sike
lon, tan, kepeken, tawa
luka, noka, sijelo, lawa
 
o kama sona! o kama sona!
o kama sona! o kama sona! e
nimi ale lon toki pona!
 
supa, linja, insa, selo
ko, kiwen, kon, telo
sewi, anpa, sinpin, monsi
jan, meli, mije, tonsi
 
pona! ni la mi tu e nasin!
taso, musi li pini ala.
mi o awen!
 
poka, nasin, kulupu, poki
sitelen, nimi, lipu, toki
lete, seli, suli, lili
kasi, pan, moku, kili
 
nimi ale mute luka luka tu taso la
jan ale li ken lon kulupu pi toki pona
 
nasa, ante, jasima, sama
lape, tomo, pali, mama
ma, suno, mun, palisa
ilo, nanpa, sona, alasa
 
pona a! o moku e kon. nimi mute mute taso li kama.
o kute pona!
 
kama, open, awen, pini
wile, esun, mani, kipisi
pana, jo, lanpan, tenpo
weka, jaki, ale, meso
pilin, uta, unpa, oko
ken, sin, namako, soko
 
o kama sona! o kama sona!
o kama sona! o kama sona! e
nimi ale lon toki pona!
 
len, taso, walo, pimeja
mu, wawa, a, monsuta
n, kin, misikeke, epiku
kokosila, pu, ku, kijetesantakalu
 
toki ni li jo e nimi ni
nimi ale lon toki...
toki ni li jo e nimi ni
nimi ale lon toki...
toki ni li jo e nimi ni
nimi ale lon toki...
toki ni li jo e nimi ni
nimi ale lon toki pona!
"""
	#endregion
	
	# genimage(tokirap_sp)