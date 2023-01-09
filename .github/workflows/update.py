#!/usr/bin/env python
#
#
#
import json
import os
import re
import sys
import glob
from jinja2 import Environment, FileSystemLoader



def readFile(file):
	f = open(file,"rt");
	data = f.read()
	f.close()
	return data

#def removeBrackets(file):
		# remove [ and ] from begining and end of files
	        #print(file)
		#f = open(file,"rt");
		#data = f.read()
		#f.close()
		#data = data.replace('[','',1)
		#pos = data.rfind(']')
		#if pos > -1:
		#	data = data[:pos] +  data[pos + len(']'): ]
			#.close()		
		#f = open(file,'wt')
		#f.write(data);
		#f.close()
	

def expandFiles(files):
	notDone = 0
	for index, file in enumerate(files):
		#print(file)
		# Remove [ and ] from beginning and end of file
		#removeBrackets(file)
		f =  open(file,'rt')
		fout = open(file + ".out",'wt')
		
		p = re.compile('(gcn.*?)(")')

		# Use regexp, match on gcn 
		for lin in f:
			#print(lin)
			if p.search(lin) and 'namespace' not in lin:
				print("Fixing " + file) 
				notDone = 1
				matches =  re.search(r"(.*?)(\")(gcn.*?)(\")(.*)",lin)
				newf = matches.group(3)+ ".avsc"
				contents = readFile(newf)
				#print(newf);
				#print(contents)
				fout.write(matches.group(1) + contents + matches.group(5))
			else:
				fout.write(lin)

		f.close()
		
		# Rename file
		os.rename(file + ".out", file)

	return notDone


if  __name__ == "__main__":
	# Store the JSON file names
	files = glob.glob('*avsc')
	
	print (files)
	for x in range (0,9):
		print("Loop:" + str(x))
		notDone = expandFiles(files)
		print("Status " + str(notDone))
		if not notDone:
			print("no more processing needed\n")
			exit()

