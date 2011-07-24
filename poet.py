#!/usr/bin/python
from sys import argv

def chop80bytes(inlist):
	return [inlist[i:i+10] for i in range(0, len(inlist), 10)]

def chop1byte(inlist):
	return [inlist[i:i+8] for i in range(0, len(inlist), 8)]

def encode_sentence_past(nouns, verbs, adjectives, inbits):
	adjective1 = adjectives[int(inbits[0:15], 2)]
	noun1 = nouns[int(inbits[15:32], 2)]
	verb = verbs[int(inbits[32:45], 2)]
	adjective2 = adjectives[int(inbits[45:60], 2)]
	noun2 = nouns[int(inbits[60:], 2)]
	return "The %s %s %s the %s %s" % (adjective1[:-1], noun1[:-1], verb[:-1], adjective2[:-1], noun2[:-1])

def encode_sentence_present(nouns, verbs, adjectives, inbits):
	adjective1 = adjectives[int(inbits[0:15], 2)]
	noun1 = nouns[int(inbits[15:32], 2)]
	verb = verbs[int(inbits[32:45], 2)]
	adjective2 = adjectives[int(inbits[45:60], 2)]
	noun2 = nouns[int(inbits[60:], 2)]
	return "%s %s is %s the %s %s" % (adjective1[:-1], noun1[:-1], verb[:-1], adjective2[:-1], noun2[:-1])

def decode_sentence_past(nouns, verbs, adjectives, insentence):
	if insentence[-1] == '.':
		punct = '000'
	elif insentence [-3:] == "!!!":
		punct = '011'
	elif insentence[-2:] == "!!":
		punct = '010'
	else:
		punct = '001'
	adjective1 = bin(adjectives.index(insentence.split()[1]+"\n"))[2:]
	noun1 = bin(nouns.index(insentence.split()[2]+"\n"))[2:]
	verb = bin(verbs.index(insentence.split()[3]+"\n"))[2:]
	adjective2 = bin(adjectives.index(insentence.split()[5]+"\n"))[2:]
	noun2 = bin(nouns.index(insentence.split()[6].split('!')[0].split('.')[0]+"\n"))[2:]
	while len(adjective1) < 15:
		adjective1 = '0'+adjective1
	while len(noun1) < 17:
		noun1 = '0'+noun1
	while len(verb) < 13:
		verb = '0'+verb
	while len(adjective2) < 15:
		adjective2 = '0'+adjective2
	while len(noun2) < 17:
		noun2 = '0'+noun2
	return punct+adjective1+noun1+verb+adjective2+noun2

def decode_sentence_present(nouns, verbs, adjectives, insentence):
	if insentence[-1] == '.':
		punct = '000'
	elif insentence [-3:] == "!!!":
		punct = '011'
	elif insentence[-2:] == "!!":
		punct = '010'
	else:
		punct = '001'
	adjective1 = bin(adjectives.index(insentence.split()[0]+"\n"))[2:]
	noun1 = bin(nouns.index(insentence.split()[1]+"\n"))[2:]
	verb = bin(verbs.index(insentence.split()[3]+"\n"))[2:]
	adjective2 = bin(adjectives.index(insentence.split()[5]+"\n"))[2:]
	noun2 = bin(nouns.index(insentence.split()[6].split('!')[0].split('.')[0]+"\n"))[2:]
	while len(adjective1) < 15:
		adjective1 = '0'+adjective1
	while len(noun1) < 17:
		noun1 = '0'+noun1
	while len(verb) < 13:
		verb = '0'+verb
	while len(adjective2) < 15:
		adjective2 = '0'+adjective2
	while len(noun2) < 17:
		noun2 = '0'+noun2
	return punct+adjective1+noun1+verb+adjective2+noun2

if __name__ == "__main__":
	if len(argv) < 3:
		print "Insufficient Arguments"
		print "Usage: poet.py encode/decode inputfile"
		exit(1)
	nounlist = open("nouns.txt").readlines()
	adjectivelist = open("adjectives.txt").readlines()
	pastverblist = open("pastverbs.txt").readlines()
	presentverblist = open("presentverbs.txt").readlines()
	mode = argv[1]
	infile = open(argv[2])
	if mode == "encode":
		outfile = open("Ballad of "+argv[2], 'w')
		for i in chop80bytes(infile.read()):
			binary = ''
			for j in i:
				bintmp = bin(ord(j))[2:]
				while len(bintmp) < 8:
					bintmp = '0'+bintmp
				binary += bintmp
			if len(binary) == 80:
				if binary[1:3] == '00':
					punct = '.\n'
				if binary[1:3] == '01':
					punct = '!\n'
				if binary[1:3] == '10':
					punct = '!!\n'
				if binary[1:3] == '11':
					punct = '!!!\n'
				if binary[0] == '0':
					sentence = encode_sentence_past(nounlist, pastverblist, 
					adjectivelist, binary[3:])+punct
					outfile.write(sentence)
				if binary[0] == '1':
					sentence = encode_sentence_present(nounlist, 
					presentverblist, adjectivelist, binary[3:])+punct
					outfile.write(sentence)
			else:
				outfile.write("All that remains are %d memories and %d regrets.\n" % (int(binary, 2), len(binary)))
			
	elif mode == "decode":
		outfile = open("Decoded_"+argv[2], 'w')
		for i in infile.readlines():
			if i[:21] == "All that remains are ":
				lineval = bin(int(i.split()[4]))[2:]
				while len(lineval) < int(i.split()[7]):
					lineval = '0'+lineval
			elif i.split()[0] == "The":
				lineval = decode_sentence_past(nounlist, pastverblist,
				adjectivelist, i)
			else:
				lineval = decode_sentence_present(nounlist, presentverblist,
				adjectivelist, i)
			for j in chop1byte(lineval):
				print j
				outfile.write(chr(int(j, 2)))
	else:
		print "Invalid Syntax"
		print "Usage: poet.py encode/decode inputfile"
		exit(2)
	outfile.close()
	exit(0)
