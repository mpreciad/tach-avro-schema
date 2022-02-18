#!/usr1/local/anaconda_py3/ana37/bin//python
##!/usr/bin/python
# 
# Name:        main.py
# Author:      Michael Preciado
# Description: Reads in the JSON files from the json subdirectory and uses a jinja
#              template to render the JSON Files in nice html pages. The output
#              is dumped to the html directory.
#             
#
import json
import os
import glob;
from jinja2 import Environment,FileSystemLoader


def render(template,tachFile,fileName):
    fileLoader = FileSystemLoader("templates");
    env = Environment(loader=fileLoader);
    rendered = env.get_template(template).render(tachFile=tachFile,title=fileName)
    return rendered

def writeToFile(rendered,fileName):
    with open(f'html1/{fileName}.html','w') as writer: 
      writer.write(rendered)
 
def run(template,files): 
    # Loop over each JSON file and apply the jinja template to each 
    names = [os.path.basename(x) for x in (files)]
    for fileName in names:
      with open("../../" + fileName,"r") as d:
        tachFile = json.load(d)

      # Get rendered template
      rendered = render(template, tachFile, fileName)
 
      # Write the new html to a file
      writeToFile(rendered,fileName) 


if __name__ == "__main__":
    # Store the JSON file names
    files   = glob.glob('../../*avsc')

    # Define the Jinja template
    template =  'tach.html.jinja';      
  
    # Run (generate html for each tach file by using the jinja template) 
    run(template,files) 