import json

sfd = """SplineFontDB: 3.2
FontName: ultlf
FullName: ultlf
FamilyName: ultlf
Copyright: Copyright (c) 2023, ultlang
License: http://scripts.sil.org/OFL
UComments: "Created with Bees"
Version: 000.002
ItalicAngle: 0
UnderlinePosition: -115
UnderlineWidth: 57
Ascent: 896
Descent: 256
LayerCount: 2
Layer: 0 0 "Back" 1
Layer: 1 0 "Fore" 0
TTFWeight: 500
TTFWidth: 5
LineGap: 200
OS2TypoAscent: 896
OS2TypoAOffset: 0
OS2TypoDescent: -256
OS2TypoDOffset: 0
OS2TypoLinegap: 200
OS2WinAscent: 1152
OS2WinAOffset: 0
OS2WinDescent: 256
OS2WinDOffset: 0
HheadAscent: 896
HheadAOffset: 0
HheadDescent: -256
HheadDOffset: 0
DEI: 91125
Encoding: UnicodeFull
UnicodeInterp: none
BeginChars: 1114112 """

sfdchars = ""

import ultlfgen
ultlfgen.generate()

with open('./ultlf-data/trimmed.json') as f:
	chardata = json.load(f)
with open('./ultlf-data/codepoints.json') as f:
	codepoints = json.load(f)
with open('./ultlf-data/trimmed_baselines.json') as f:
	baselines = json.load(f)

chnum = 1

for charindex, char in enumerate(chardata):
	invalid = False
	charrepr = f"StartChar: u{hex(codepoints[charindex])}\nEncoding: {codepoints[charindex]} {codepoints[charindex]} {chnum}\nWidth: {128*len(char[0]) + 128}\nFlags: W\nLayerCount: 2\nFore\nSplineSet\n"
	for lineindex, line in enumerate(char):
		if "X" in line:
			invalid = True
			break
		for pxindex, px in enumerate(line):
			if px == "#":
				charrepr += f"{128*pxindex} {128*(baselines[charindex] - lineindex)} m 25\n {128*pxindex} {128*(baselines[charindex] - lineindex) + 128} l 25\n {128*pxindex + 128} {128*(baselines[charindex] - lineindex) + 128} l 25\n {128*pxindex + 128} {128*(baselines[charindex] - lineindex)} l 25\n {128*pxindex} {128*(baselines[charindex] - lineindex)} l 25\n"
	
	if not invalid:
		charrepr += "EndSplineSet\nEndChar\n\n"
		# print(charrepr)
		sfdchars += charrepr
		chnum += 1

sfd = sfd + str(chnum) + "\n" + sfdchars

with open('files/ultlf.sfd', "w") as f:
	f.write(sfd)
	print("the")

import subprocess, os
subprocess.run(["fontforge", "-lang", "ff", "-c","Open($1); Generate($2)", "ultlf.sfd", "ultlf.ttf"], cwd=os.getcwd() + "/files")
subprocess.run(["fontforge", "-lang", "ff", "-c","Open($1); Generate($2)", "ultlf.sfd", "ultlf.otf"], cwd=os.getcwd() + "/files")
subprocess.run(["fontforge", "-lang", "ff", "-c","Open($1); Generate($2)", "ultlf.sfd", "ultlf.woff"], cwd=os.getcwd() + "/files")
subprocess.run(["fontforge", "-lang", "ff", "-c","Open($1); Generate($2)", "ultlf.sfd", "ultlf.woff2"], cwd=os.getcwd() + "/files")