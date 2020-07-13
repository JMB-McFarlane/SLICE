import os
from operator import itemgetter
from shutil import copyfile
import math
import random

def grabber(path,file):
	connect_info = []
        hostname = file.split(".pdbqt")[0]  #host replicate pdbqt
        outfile = open(path+file,'r')   #vina output
	lig_poses = [[]]

	i = 0
	for line in outfile:
	    if "ATOM" in line:
	        lig_poses[i].append(line.split())
	    if "HETATM" in line:
	        lig_poses[i].append(line.split())
	    if "ENDMDL" in line:
	        lig_poses.append([])
	        i = i + 1
        
	lig_poses.pop()

# generating poses for tleap

	for n in range(len(lig_poses)):
	    rec_x_coords = []
	    num = str(n)
	    pdb = open(path+'pose'+ num + "_" + hostname, 'w')
	    rec = open(path+hostname + ".pdbqt",'r')
            
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
	    lig_poses[n].sort(key=lambda x: int(x[4])) # Rearrange line order for residue number
	# Writing to pdb format
	
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


def rose_script_writer(path,tleap_sourcepath,replicates_skim,replicates_rose):
            selected_files = open(path+"selected.txt",'wr')
            skim = replicates_skim
            entry =1
            script = open(path+"leap_script.scr","wr")
            script.write('source ' + tleap_sourcepath + ' \n\n')
            scores = []
            lines = []
            for line in open(path+"scores.dat",'r'):
                scores.append(float(line.split()[0]))
                lines.append(line)
                if entry <= int(skim):
                    selected_files.write(line + "\n")
                    entry = entry + 1        
            minE = min(scores)
            maxE = max(scores)
            beta = math.log(0.01)/(minE-maxE)
            px_fill = []
            for i in range(len(scores)):
                    px = (math.exp(beta*(minE - float(scores[i]))))
                    px_fill.append(px)
            i=0
            while i <= (int(replicates_rose)-1):
                random_pick = random.randint(0,len(scores)-1)
                if px_fill[random_pick] >= random.uniform(0,1):
                    i = i+1
                    selected_files.write(lines[random_pick] + "\n")
            selected_files.close()
            selected = open(path+"selected.txt",'r')
            entry = 1
            for line in selected:
                    if "pose" in line:
                        filesource = line.split()[1]
                        filename = "pose" + str(entry)
                        script.write(filename + ' = loadpdb ' + filesource + '\n')
                        script.write('addions ' + filename + ' Na+ 0' +'\n')
                        script.write('addions ' + filename + ' Cl- 0' +'\n')    
                        script.write('solvatebox ' + filename + ' TIP3PBOX 14' +'\n')
                        script.write('saveamberparm ' + filename + ' ' + path+filename + '.top ' + path+filename +'.crd \n\n' )
                        entry = entry + 1
            script.write("quit")
def call_leap(path):
        os.popen("tleap -f " + path + "/leap_script.scr")
def mv_initial_docked(path):
    pass
