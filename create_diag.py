# -*- coding: utf-8 -*-
"""
Created on Wed Jan 16 07:45:49 2019

@author: Colleen
"""

import json
import re
import argparse

parser=argparse.ArgumentParser(description='Create diag_json file')
parser.add_argument('--variables', nargs='+', default=[], help='List of variables to create diag table for')
parser.add_argument('--input', help='Name of input diag table')
parser.add_argument('--output', help='Name of output diag table')
args=parser.parse_args()
diag_in=args.input
diag_out=args.output
input_vars=args.variables
## Open the input json diag_table
####################################################################
f=open(diag_in)
data=json.load(f)
f.close()
#####################################################################
# sort by user defined variables
variables={}
if input_vars:
    print("Extracting info for variable(s) {}".format(input_vars))
    for (k,v) in data.items():
        for item in input_vars:
            if re.match(r"\b" + item + r"\b", k):
                variables[k]=v
                #find associated files
                for key in v.keys():
                    f=v[key][0][1]
                    variables[f]=data['files'][f]
        #add date and experiment info
        if re.match(r"\bexperiment|date\b",k):
            variables[k]=v  
#####################################################################
## Write the json to the output file
with open(diag_out,'w') as json_out:
    json.dump(variables,json_out, sort_keys=True, indent=2)