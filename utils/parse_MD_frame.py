#This script will make a temporary script for parsing out a single frame of an MD trajectory
#into a pdb suitable for charge assignment (pdbqt) and subsequent docking.

import os
import subprocess as sp

path = "/storage/home/jmbm87/SLICE_dev/materials/pyfiles/test_inps/"

def mask_get(receptor_pdbqt):
    """Mask detector for cpptraj inputs.

    This function returns a string indicating the residue numbers involved with the host protein.

    Parameters
    __________

    receptor_pdbqt : string
        The receptor file including path to be parsed.


    Returns
    _______
    
    Mask : string

    """
    inp_file = open(receptor_pdbqt,'r')
    lines = inp_file.read().splitlines()
    last_res_line = lines[-2]
    mask = last_res_line.split()[4]
    print("Host mask set: 1-"+mask)
    return(":1-"+mask)

def MD_to_pdb(path,frame_start,frame_end,trajectory,top,output,mask):
    """ AMBER mdcrd to pdb snapshots
    
    This function cals cpptraj from the AMBER tools suite to parse trajectory files of the ligand-host complexes for individual PDB snapshots.

    Parameters
    __________

    path : string
        Path to read/write location.

    frame_start : int
        Starting frame for parsing.

    frame_end : int
        Ending frame for parsing.

    trajectory : string
        mdcrd file name for parsing.

    top : string
        file name of AMBER topology file

    output : string
        output prefix to .# of the frame number output file.

    mask : string
        Residue mask of type ":#-#" indicating the host protein in the pdb or pdbqt files.

    """
    cpp_in = open("temp_cpp.in", 'w')
    cpp_in.write("parm " + path+top + "\n")
    cpp_in.write("trajin " + path+trajectory + " "+str(frame_start) +" "+str(frame_end)+" "+str(1)+ "\n")
    cpp_in.write("mask " + mask + " maskpdb " + path+output + "\n")
    cpp_in.write("run") 
    cpp_in.close()
#    subprocess.call("cpptraj -i temp_cpp.in",shell=True)
    try:
        out = sp.check_output("cpptraj -i temp_cpp.in", stderr=sp.STDOUT, shell=True)
       # print(out)
    except sp.CalledProcessError as e:
        print("Command: {}\nReturn Code: {}\n Output: {}".format(e.cmd, e.returncode, e.output))
    os.popen("rm temp_cpp.in")

def check_method():
    MD_to_pdb(path,1,50,"mdcrd","pep.top","host_frame",":1-5")

check_method()

