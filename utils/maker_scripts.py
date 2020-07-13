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

# File mover for moving tops and crds

def mv_files(file,write_path):
    os.popen("cp " + file + " " + write_path)

# Block of functions for making the MD input files

def make_MD_min_input():
    print("Makes min.in")

def make_MD_heat_input():
    print("Makes heat.in")

def make_MD_heat_input():
    print("Makes heat.in")

def make_MD_prod_input():
    print("Makes prod.in")


# Sorts through scored poses and generates script for tleap for MD file generation 
def parse_docked_replicates(slice_num,parse_method):
    if parse_method == "1":
        print("Skimming")
    print(parse_method)
    print("| Parsing docked poses | "),
    sys.stdout.flush()
def make_crd_tops():
    print("Converting poses to MD | "),
    sys.stdout.flush()
def submit_MD(pbs_script,write_path):
    try:
     #  out = sp.check_output('qsub -l nodes=1:ppn=28,mem=2gb ' + pbs_script+ ' -q prometheus', stderr=sp.STDOUT, shell=True, cwd=write_path)
        out = sp.check_output('qsub -l nodes=1:ppn=28,mem=2gb,walltime=3:00:00 '+ pbs_script + ' -q prometheus', stderr=sp.STDOUT, shell=True, cwd=write_path)
    except sp.CalledProcessError as e:
        print("Command: {}\nReturn Code: {}\n Output: {}".format(e.cmd, e.returncode, e.output))
    sys.stdout.flush()


#returns last save state for a file
def check_file_status(filename):
        fileinfo = str(os.stat(filename))
        return fileinfo.split("st_ctime=")[1].split(")")[0]
