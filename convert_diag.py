# -*- coding: utf-8 -*-
"""
Created on Wed Jan 16 07:45:49 2019

@author: Colleen
"""

import json
import re
import argparse


parser=argparse.ArgumentParser(description='Create diag_json file')
parser.add_argument('--variables', nargs='+', default=[], help='List of variables to extract info for')
args=parser.parse_args()
input_vars=args.variables
## Open the input (diag_table) and output (diag_json) files
diag_table=open("diag_table",'r')
diag_json=open("diag_json",'w')
#####################################################################
## Set up the lists
files = []
variables = []
topinfo = []
## Loop through the lines in diag_table
for lines in diag_table:
## Clean up the lines and remove quotes, white space on the ends, and trailing commas
 templine = lines.strip(',\n')
 templine = templine.replace('"',"")
 templine = templine.strip()
 diagline = templine.split(",")
## Seperate out comments in the diag table
 if re.search('^#.*',diagline[0]):
  #print diagline[0]
  continue
## Entries with 6 members are files
 elif len(diagline) == 6:
  files.append(diagline)
#  print "This is a file"
## Entries with 8 mebers are diagnostic variables
 elif len(diagline)>= 8:
  variables.append(diagline)
#  print "This is a variable"
## Entries without commas are the experiment and base date
 elif len(diagline) == 1:
  topinfo.append(diagline)
 else:
  print lines
  print "This is an error or is not yet supported."
  quit()
## Close the input file
diag_table.close()
#####################################################################
## Sort out the experimnet and base date
exp = topinfo[0][0]
dt = topinfo[1][0]
## Start the json dictionary
fullJson = {
  "experiment": exp,
  "date": dt
}
fnames=[]
filesJson={}
## Loop through the files and crate their entries in the dictionary
for i in range(len(files)):
 if files[i][0] in fnames:
    print files[i][0]+" Is already listed as a filename.  skipping duplicate"
 else:
    fnames.append(files[i][0])
    filesJson[files[i][0]] = [files[i][1].strip(),files[i][2].strip(),files[i][3].strip(),files[i][4].strip(),files[i][5].strip()]
## Write the files dictionary to the fill dictionary
fullJson['files']=filesJson
# sort by user defined variables
variables_mod=[]
if input_vars:
    print("Extracting info for variable(s) {}".format(input_vars))
    for i in range(len(variables)):
        for item in input_vars:
            if re.match(r"\b" + item + r"\b", variables[i][1].strip()):
                variables_mod.append(variables[i])
#overwrite variables to continue
    variables=variables_mod
#####################################################################
modnames=[]
varsJson={}
for i in range(len(variables)):
 if variables[i][1] in modnames:
    if not variables[i][0].strip() in varsJson[variables[i][1].strip()]:
       varsJson[variables[i][1].strip()][variables[i][0].strip()]=[]
 else:
    modnames.append(variables[i][1])
    varsJson[variables[i][1].strip()] = {}
    varsJson[variables[i][1].strip()][variables[i][0].strip()]=[]
 varsJson[variables[i][1].strip()][variables[i][0].strip()].append(map(str.strip,variables[i][2:7]))
fullJson.update(varsJson)
#####################################################################
## Write the json to the output file
diag_json.write(json.dumps(fullJson, sort_keys=True, indent=2))

diag_json.close()