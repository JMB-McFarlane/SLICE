#This script will make a temporary script for parsing out a single frame of an MD trajectory
#into a pdb suitable for charge assignment (pdbqt) and subsequent docking.

import os
import subprocess

path = "/storage/home/jmbm87/SLICE_dev/materials/pyfiles/test_inps/"

def MD_to_pdb(path,frame,trajectory,top,output,mask):
    cpp_in = open("temp_cpp.in", 'wr')
    cpp_in.write("parm " + path+top + "\n")
    cpp_in.write("trajin " + path+trajectory + " "+str(frame) +" "+str(frame)+" "+str(1)+ "\n")
    cpp_in.write("mask " + mask + " maskpdb " + path+output + "\n")
    cpp_in.write("run") 
    cpp_in.close()
    subprocess.call("cpptraj -i temp_cpp.in",shell=True)
    subprocess.call("rm temp_cpp.in",shell=True)

def check_method():
    MD_to_pdb(path,4,"mdcrd","pep.top","test.out",":1-5")

check_method()

