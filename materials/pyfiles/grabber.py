import os
from operator import itemgetter
from shutil import copyfile

workingdir = str(os.getcwd())



def grabber(file):
	connect_info = []
        hostname = file.split("host.pdbqt")[0]
        outfile = open(file,'r')
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


for file in os.listdir(workingdir):
            if "OUT" in file:
                copyfile(file,"MBP_"+file.split(".pdb.")[1] +"host.pdb")           
                
              #  open("cbx8_"+file.split(".pdb.")[1] +"host.pdb","wr")

for file in os.listdir(workingdir):
    #    if "OUT" in file:
     #       open("cbx8_"+file.split(".pdb.")[1] +"host.pdb","wr")
        if "host.pdbqt.out" in file:
		print(file) 
		grabber(file)



