#!/usr/bin/env python
# 
# Name:        update.py 
# Author:      Michael Preciado
# Description: This script reads in each schema file and:
#	       1) Replaces all references to JSON files with the contents of the JSON files
#              2) Repeats (1) until there are no more JSON refs in the file 
#              
#              Note: This script is meant to be run in a CI setup through GitHub and within
#		     a docker container. It updates the schema files so that they can be later
#		     tranformed into Tree View html by main.py. 
# 
# usage:       ./update.py
#
#
import json
import os
import re
import sys
import glob
from jinja2 import Environment, FileSystemLoader



def readFile(file):
	f = open("../../" + file,"rt");
	data = f.read()
	f.close()
	return data


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
	files = glob.glob('../../*avsc')
	
	print (files)
	for x in range (0,9):
		print("Loop:" + str(x))
		notDone = expandFiles(files)
		print("Status " + str(notDone))
		if not notDone:
			print("no more processing needed\n")
			exit()

