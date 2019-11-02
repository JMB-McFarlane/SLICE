"""SLICE (Selective Ligand Induced Conformational Selection) is a fusion of molecular dynamics and molecular docking 
for the accelerated structural prediction of ligands on a flexible protein host. 

Accelerated Molecular Dynamics for Structural Prediction in Protein/Peptide Binding: The SLICE Method
https://doi.org/10.26434/chemrxiv.8297129.v1

Authors: James McFarlane, Brett Henderson, Katherine Krause, Irina Paci. 2019, University of Victoria

File run parameters stored in config.ini
Methods called in main program located in utils folder
"""
import os
import argparse
import ConfigParser
import sys
import time


# Appends path to SLICE utilities
sys.path.append("/storage/home/jmbm87/SLICE_dev/utils")

# Utilty files
import print_config #Printing and status update functions
import maker_scripts as ms # Contains the pdb and md file makers and parsers


# Parses arguments for executing SLICE
parser = argparse.ArgumentParser(description="SLICE Usage:")
parser.add_argument('-L', metavar='L', type=str, help='Ligand prefix for .pdbqt file')
parser.add_argument('-R', metavar='R', type=str, help='Receptor prefix for .pdbqt file')
parser.add_argument('-V', metavar='V', type=str, nargs='?', help='Verbosity')
parser.add_argument('-REF', metavar='D', type=str, nargs='?', help='Reference structure for developer mode')
args = parser.parse_args()

# Make config object
config = ConfigParser.ConfigParser();config.read("/storage/home/jmbm87/SLICE_dev/config.ini")

def cfg(a,b):                   #config file getter
    return config.get(a,b) 




def main(ligand,receptor):
    beep = lambda x: os.system("echo -n '\a';sleep 0.2;" * x)
    beep(3)
    print_config.print_configuration(config,ligand,receptor) # Prints out configuration info, inputs, and a good sword

#prestep1. Initialize directories method

  # ms.make_folders(cfg("General","SLICE_num"))
    

    for i in range(int(config.get("General","SLICE_num"))):
            time.sleep(0.5)
           # sys.stdout.write('\r')
            print("SLICE " + str(i + 1)),
           # sys.stdout.flush()

            ms.make_folders(i+1,cfg("Docking","num_poses"),cfg("Minimization","Run_MIN"),cfg("Heating","Run_HEAT"),cfg("Equilibration","Run_EQUIL")) # Makes folders in SLICE iteration
            ms.parse_docked_replicates(cfg("General","SLICE_num"),cfg("General","Selection_method")) #Calls parse total function to sort structures by scores and print output file 
            ms.make_crd_tops()
            ms.submit_MD()
#begin loop over number of iterations
    #parse MD with cpptraj
    #make_dock_files
    #execute dock
    #wait()
    
    #execute make_pdbs_from dock
    #execute select poses
    #update global ouput with dock scores and poses
    #execute make mdstart files (.crd and .top) 
    #move all files to starting directories

    #submit min jobs (if min flag = true);wait()
    #submit heat jobs (if heat flag = true);wait()
    #submit equil jobs (if equil flag = true);wait()
    #submit production jobs (if prod flag = true);wait()
        

if __name__ == "__main__":
    main(args.L,args.R)
