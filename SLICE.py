"""SLICE (Selective Ligand Induced Conformational Selection) is a fusion of molecular dynamics and molecular docking for the accelerated structural prediction of ligands on a flexible protein host. 
Methods called in main program located in utils folder
"""
import os
import argparse
import ConfigParser
import sys
import time
import os

# Utilty files
from utils import print_config #Printing and status update functions
from utils import maker_scripts as ms # Contains the pdb and md file makers and parsers
from utils import dock_prep
from utils import parse_dock
from utils import pose2pdb
from utils import wait
from utils import parse_MD_frame
from utils import pdb2pqr
# Parses arguments for executing SLICE
parser = argparse.ArgumentParser(description="SLICE Usage:")
parser.add_argument('-L', metavar='LIG', type=str, help='Ligand prefix for .pdbqt file')
parser.add_argument('-R', metavar='REC', type=str, help='Receptor prefix for .pdbqt file')
parser.add_argument('-V', metavar='VERB', type=str, nargs='?', help='Verbosity')
parser.add_argument('-REF', metavar='DEV', type=str, nargs='?', help='Reference structure for developer mode')
args = parser.parse_args()

print("Starting SLICE")


# Make config object
config = ConfigParser.ConfigParser()
if "config.ini" not in os.listdir('.'):
    config.read(os.path.join(os.path.dirname(__file__), "config.ini"))
else:
    config.read("config.ini")

def cfg(a,b):                   #config file getter
    return config.get(a, b)


def main():
    # Print out configuration info, inputs, and a good sword
    print_config.print_configuration(config, cfg("System","ligand_name"), cfg("System","host_name"))
    
    host_mask = parse_MD_frame.mask_get(cfg("System","host_name"))
    #########################################################
    #########initial docking generation for MD poses######### 

    os.popen("mkdir initial_dock")
    
    #Creates docking files from local ligand and host pdbqt files
    os.popen("cp " +  cfg("System","host_name") + " initial_dock")
    dock_prep.dock_prep(os.getcwd()+"/initial_dock/",os.getcwd()+"/",
                cfg("System","host_name"),cfg("System","ligand_name"),
                cfg("Docking","box_residues"),cfg("Docking","num_poses"),
                cfg("Docking","Exhaustiveness"),cfg("Docking","cpu"))
    
    #Writes PBS submission script, submits it, and waits until the queue is void of the PBS file
    dock_prep.dock_pbs_script("/storage/home/jmbm87/SLICE_dev/utils/unit_test_files",
                os.getcwd()+"/initial_dock/", cfg("System","host_name")) 
    #Opens docking output files and scores all of the outputs and ranks them
    parse_dock.parse_SLICE(os.getcwd()+"/initial_dock/",1)
    
    #copies the host pdbqt file into docking directory for copying
    os.popen("cp *.pdbqt initial_dock")
    
    #Loop that goes through the organized scores and then constructs ligand/host complexes of the poses
    for file in os.listdir(os.getcwd()+"/initial_dock/"):
        if ".pdbqt.out" in file:
            pose2pdb.grabber(os.getcwd()+"/initial_dock/",file)
    
    #Generates the tleap script using the new poses
    pose2pdb.rose_script_writer(os.getcwd()+"/initial_dock/",
            cfg("Paths","TLEAP_SOURCE"),
            cfg("General","Replicates_skim"),
            cfg("General","Replicates_rose"))
    print("Repskim = " + cfg("General","Replicates_skim")) 
    #Executes tleap
    pose2pdb.call_leap(os.getcwd()+"/initial_dock/")
    time.sleep(30)
    
    ################################################
    ################SLICE MD BLOCK##################

    total_reps = (int(cfg("General", "Replicates_rose"))+int(cfg("General", "Replicates_rose")))

    for i in range(int(cfg("General", "SLICE_num"))):
            time.sleep(0.5)
            # sys.stdout.write('\r')
            print("Starting SLICE " + str(i + 1))
            # sys.stdout.flush()

            # Set up directory structure within SLICE iteration
            ms.make_folders(i+1, total_reps, cfg("Minimization", "Run_MIN"),
                            cfg("Heating", "Run_HEAT"), cfg("Equilibration", "Run_EQUIL"))
            
            # Move previous crd and top files to new MD directories
            
    for i in range(1,total_reps+1):
            ms.mv_files("initial_dock/" + "pose"+str(i)+".top", "SLICE_1/"+str(i)+"/MIN/pose.top")
            ms.mv_files("initial_dock/" + "pose"+str(i)+".crd", "SLICE_1/"+str(i)+"/MIN/pose.crd")
             
    for i in range(1,int(cfg("General", "SLICE_num"))+1):
            # Sort docked structures by scores and print output file
            
            #Mininimization
            for j in range(1,total_reps+1):
                ms.submit_MD(cfg("Paths","MIN_script"),"SLICE_"+str(i)+"/"+str(j)+"/MIN")
            wait.wait_q(cfg("Paths","MIN_script"))    
            print("Minimization Done")
           
           #Temperature Ramping
            for j in range(1,total_reps+1):
                os.popen("mv SLICE_"+str(i)+"/"+str(j)+"/MIN/min.rst " + "SLICE_"+str(i)+"/"+str(j)+"/HEAT/min.rst")
                os.popen("mv SLICE_"+str(i)+"/"+str(j)+"/MIN/pose.top " + "SLICE_"+str(i)+"/"+str(j)+"/HEAT")
                ms.submit_MD(cfg("Paths","TEMP_script"),"SLICE_"+str(i)+"/"+str(j)+"/HEAT")
            wait.wait_q(cfg("Paths","TEMP_script"))
            print("Heating Done")

     #       #Pressure equilibration
    #        for j in range(1,total_reps+1):
   #             os.popen("mv SLICE_"+str(i)+"/"+str(j)+"/HEAT/heat.rst " + "SLICE_"+str(i)+"/"+str(j)+"/EQUIL/heat.rst")
  #              os.popen("mv SLICE_"+str(i)+"/"+str(j)+"/HEAT/pose.top " + "SLICE_"+str(i)+"/"+str(j)+"/EQUIL")
 #               ms.submit_MD(cfg("Paths","PRES_script"),"SLICE_"+str(i)+"/"+str(j)+"/EQUIL")
#            wait.wait_q(cfg("Paths","PRES_script"))


            #Production run
            print("Submitting MD")
            for j in range(1,total_reps+1):
                os.popen("mv SLICE_"+str(i)+"/"+str(j)+"/HEAT/heat.rst " + "SLICE_"+str(i)+"/"+str(j)+"/PROD/heat.rst")
                os.popen("mv SLICE_"+str(i)+"/"+str(j)+"/HEAT/pose.top " + "SLICE_"+str(i)+"/"+str(j)+"/PROD")
                ms.submit_MD(cfg("Paths","PROD_script"),"SLICE_"+str(i)+"/"+str(j)+"/PROD")
            wait.wait_q(cfg("Paths","PROD_script"))
            print("Production MD Complete")

    ########################################################
    ############# Docking on MD Ensembles #################
            
            #Printing out host coordinates per frame from trajectories
            print("Converting MD to PDBs with cpptraj for docking")
            for j in range(1,total_reps+1):
                parse_MD_frame.MD_to_pdb("SLICE_"+str(i)+"/"+str(j)+"/PROD/",1,50,"mdcrd","pose.top","host_frame",host_mask)
            

            print("Adding Charges to Ensemble Snapshots")
            for j in range(1,total_reps+1):
                write_path = "SLICE_"+str(i)+"/"+str(j)+"/PROD/" 
                for file in os.listdir(write_path):
                    if "host_frame" in file:
                        new_pdbqt = "frame_" + file.split(".")[-1] + ".pdbqt"
                        pdb2pqr.pdb2pqr(write_path,file,cfg("System","host_name"),new_pdbqt)
            
            print("Creating config files for Vina")
            for j in range(1,total_reps+1):
                os.popen("rm "+ "SLICE_"+str(i)+"/"+str(j)+"/PROD/*.conf")
                for file in os.listdir("SLICE_"+str(i)+"/"+str(j)+"/PROD/"):
                    if ".pdbqt" in file:
                        host = file
                        dock_prep.dock_prep("SLICE_"+str(i)+"/"+str(j)+"/PROD/",os.getcwd()+"/",
                                     host,cfg("System","ligand_name"),
                                     cfg("Docking","box_residues"),cfg("Docking","num_poses"),
                                     cfg("Docking","Exhaustiveness"),cfg("Docking","cpu"))

            print("Submitting docking jobs")
            for j in range(1,total_reps+1):
                write_path =  "SLICE_"+str(i)+"/"+str(j)+"/PROD/"
                os.popen("rm "+ "SLICE_"+str(i)+"/"+str(j)+"/PROD/*.pbs")
                for file in os.listdir("SLICE_"+str(i)+"/"+str(j)+"/PROD/"):
                    if ".pdbqt" in file:
                        if ".conf" not in file:
                            host_name = file
                            dock_prep.dock_pbs_script("/storage/home/jmbm87/SLICE_dev/utils/unit_test_files",write_path,host_name) 
                

if __name__ == "__main__":
    main()
