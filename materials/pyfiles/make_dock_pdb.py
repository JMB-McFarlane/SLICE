""" This code takes the set of output files from the docking steps and creates PDBs using the docked coordinates of the ligand and superimposing them onto their respective host pose. Respective host pdbs that were used to generate the pdbqt files for docking are required in the directory as they are used as references for the new pdb."""


import os
from operator import itemgetter
from shutil import copyfile

workingdir = str(os.getcwd())

def make_dock_pdbs(file):
	connect_info = []
        hostname = file.split("host.pdbqt")[0]
        outfile = open(file,'r')
	lig_poses = [[]]

	i = 0

        #Parses Vina output file for coordinates for the separate docked poses on a the single host pose
	for line in outfile:
	    if "ATOM" in line:
	        lig_poses[i].append(line.split())
	    if "HETATM" in line:
	        lig_poses[i].append(line.split())
	    if "ENDMDL" in line:
	        lig_poses.append([])
	        i = i + 1

	lig_poses.pop()

        # Loop below takes the host pdb and writes the coordinates to a new pdb which will later have the ligand 
        # positions added on

	for n in range(len(lig_poses)):
	    rec_x_coords = []
	    num = str(n)
	    pdb = open('pose'+ num + "_" + hostname, 'w')
	    rec = open(hostname + "host.pdb",'r')
            
	    for line in rec:
	        if "ATOM" in line:
	            clean = line.split()
	            rec_x_coords.append(clean[5])
	            if len(rec_x_coords) > 4:
	                if (float(rec_x_coords[-1]) - float(rec_x_coords[-2])) >= 15:
	                    pdb.write("TER \n")
	            if ("HG  CYX") not in line:
	                pdb.write(line)
	    pdb.write("TER \n")
	    rec.close()
	    
            
        # Below here is the addition of the ligand coordinates onto the new docked pdb

            lig_poses[n].sort(key=lambda x: int(x[4])) # Rearrange line order for residue number
	# Writing to pdb format
	

        # Writes ligand coordinates to the new pdb file
	    for i in range(len(lig_poses[n])):
	        pdb.write('%-6s' % str(lig_poses[n][i][0]))
	        pdb.write('%5s' % str(lig_poses[n][i][1]))
	        if str(lig_poses[n][i][2][0]).isalpha() == True:
	            pdb.write('  ' + '%-4s' % str(lig_poses[n][i][2]))
	        if str(lig_poses[n][i][2][0]).isalpha() == False:
	            pdb.write(' ' + '%-5s' % str(lig_poses[n][i][2]))
	        pdb.write('%3s' % str(lig_poses[n][i][3]))
	        pdb.write('%6s' % str(lig_poses[n][i][4]))
	        pdb.write('%12s' % str(lig_poses[n][i][5]))
	        pdb.write('%8s' % str(lig_poses[n][i][6]))
	        pdb.write('%8s' % str(lig_poses[n][i][7]))
	        pdb.write('%6s' % str(lig_poses[n][i][8]))
	        pdb.write('%6s' % str(lig_poses[n][i][9]))
	        pdb.write('%10s' % str(lig_poses[n][i][10]) + ' ')
	        pdb.write('%-3s' % str(lig_poses[n][i][11]))
	        pdb.write('\n')
	    for i in range(len(connect_info)):
	        pdb.write(connect_info[i] + '\n')

#loops through the Vina outputs to and executes the pdb writer. 



for file in os.listdir(workingdir):
        if "host.pdbqt.out" in file:
		print(file) 
		make_dock_pdbs(file)



