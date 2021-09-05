import base64
the = base64.a85decode( b"^d(.M5X7S\"!'gMa" )
sus = bytearray()
print(the)
for byte in bytes(the):
	print(format(byte, "08b").replace("0"," ").replace("1","#") )
	sus.append(byte)
print(base64.a85encode(sus))
