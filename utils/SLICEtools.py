#Combined module for all writer/reader/analyzer tools for the SLICE method

# A collection of methods used in the parsing of output files and generation of compatible input formats for Vina and AMBER
import subprocess as sp
import sys
import os
cwd = os.getcwd()

# Makes the file structures for each SLICE iteration 

def make_folders(slice_rep,rep_num,min_bool,heat_bool,equil_bool):
    os.popen("mkdir " + cwd + "/" + "SLICE_" + str(slice_rep))
    for i in range(int(rep_num)):
        os.popen("mkdir " + cwd + "/" + "SLICE_" + str(slice_rep) + "/" + str(i+1))
        if bool(min_bool) == True:
            os.popen("mkdir " + cwd + "/SLICE_" +str(slice_rep) + "/" + str(i+1) + "/MIN")    
        if bool(heat_bool) == True:
            os.popen("mkdir " + cwd + "/SLICE_" +str(slice_rep) + "/" + str(i+1) + "/HEAT")
        if bool(equil_bool) == True:
            os.popen("mkdir " + cwd + "/SLICE_" +str(slice_rep) + "/" + str(i+1) + "/EQUIL")
        os.popen("mkdir " + cwd + "/SLICE_" +str(slice_rep) + "/" + str(i+1) + "/PROD")

