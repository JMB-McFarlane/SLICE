import os
from operator import itemgetter
import math
import shutil
import timeit
import time
import subprocess

workingdir = str(os.getcwd())
charges =  []

def pdb_reader():

        for file in os.listdir(workingdir):
                lines = []
	        x = []
                y = []
                z = []
                a = []
                b = []
                c = []
                d = []
                e = []
                f = []
                g = []
                h = []
                o = []
                j = []

                if "OUT.pdb" in file:
                        inp = open(file,'r')
                        print file
                        for line in inp:
                                if "ATOM" in line:
                                    if len(line.split()) >= 6:
                                      #  print line
                                        x.append(line.split()[5])
                                        y.append(line.split()[6])
                                        z.append(line.split()[7])

                        pout = open("MBP_" + file.split(".pdb.")[1] + "host.pdbqt",'wr')
                        print pout
                        ref = open('MBP.receptor.pdbqt','r')
                        i=0
                        for line in ref:
                                if "ATOM" in line:
                                        a.append(line.split()[0])
                                        b.append(line.split()[1])
                                        c.append(line.split()[2])
                                        d.append(line.split()[3])
                                        e.append(line.split()[4])
                                        f.append(line.split()[8])
                                        g.append(line.split()[9])
                                        h.append(line.split()[10])
                                        o.append(line.split()[11])
             #                          j.append(line.split()[12])
			
			print len(x)
                        print len(y)
                        print len(z)
                        print len(a)
                        print len(b)
                        print len(c)
                        print len(d)
                        print len(e)
                        print len(f)
                        print len(g)


                        for i in range(len(a)):
                                lines.append(a[i]+ ' '+ b[i]+ ' '+ c[i]+ ' '+ d[i]+ ' '+ e[i]+ ' ' + x[i]+ ' '+ y[i]+ ' '+ z[i]+ ' ' + f[i] + ' '+ g[i]+ ' '+ h[i]+ ' '+ o[i])
                            
                        i = 0
                        ref.close()
                        ref = open('MBP.receptor.pdbqt','r')
                        for line in ref:
                                if "ATOM" in line:
                                       
                                          pout.write('{:>4} {:>6} {:<4} {:>3} {:>5} {:>11} {:>7} {:>7} {:>5} {:>5} {:>9} {:<2}  ' .format(*lines[i].split()))
                                          pout.write('\n')
                                          i = i + 1
                                if "ATOM" not in line:
                                        pout.write(line)
                       # print len(a)
                            


pdb_reader()		
	

def docker(hostname,ligandname,poses):
	config = open(hostname.split("host.")[0] + ".conf", 'w')
	#ligandname = raw_input("ligand pdbqt:")
	#hostname = raw_input("host pdbqt:")
	#poses = raw_input("number of poses:")
	config.write('receptor = '+ hostname + '\n')
	config.write('ligand = ' + ligandname + '\n' + '\n')

	# Box configuration

	boxresidues = []
	res_x = []
	res_y = []
	res_z = []

	cyx = []

	with open('box.in') as file:
   		for line in file:
        		boxresidues = str.split(line)

	for res in boxresidues:
    		with open(hostname) as file:
        		for line in file:
            			if ' ' + res + ' ' in line:
                			if 'ATOM' in line:
                    				clean = line.split()
                    				res_x.append(float(clean[5]))
                  			  	res_y.append(float(clean[6]))
               				     	res_z.append(float(clean[7]))

# Disulfide bridge finder
	with open(hostname) as file:
	    for line in file:
	        if "SG" in line:
	            cyx.append(line.split())
	connect_info = []
	for i in range(len(cyx)):
	    for j in range(len(cyx)):
       		if j != i:
            		if math.sqrt((float(cyx[i][6]) - float(cyx[j][6]))**2) <= 4:
                		connect_info.append('CONECT ' + cyx[i][1] + ' ' + cyx[j][1])

	Cx = str((float(max(res_x)) - float(min(res_x)))/2 +float(min(res_x)))
	Cy = str((float(max(res_y)) - float(min(res_y)))/2 +float(min(res_y)))
	Cz = str((float(max(res_z)) - float(min(res_z)))/2 +float(min(res_z)))
	print Cx,Cy,Cz

	Sx = str((float(max(res_x)) - float(min(res_x)) +8))
	Sy = str((float(max(res_y)) - float(min(res_y)) +8))
	Sz = str((float(max(res_z)) - float(min(res_z)) + 8))
	print("Box size = ")
	print Sx,Sy,Sz
         
	# Configuration file
	config.write('center_x = ' + Cx + '\n')
	config.write('center_y = ' + Cy + '\n')
	config.write('center_z = ' + Cz + '\n' + '\n')
	
	config.write('size_x = ' + Sx + '\n')
	config.write('size_y = ' + Sy + '\n')
	config.write('size_z = ' + Sz + '\n' + '\n')

	config.write('out = ' + hostname +'.out'+ '\n')
	config.write('exhaustiveness = 7' + '\n')
	config.write('num_modes = ' + poses + '\n')
	config.write('cpu = 7')
	config.close()

#	print ('Submitting to queue...')

	#os.popen('/Users/jmbm/Desktop/RA_docking/jdock/vina' + ' --config ' + workingdir + '/conf.txt')
        def pbs_script():
            scr = open("script.pbs",'r')
            newscr = open(hostname.split('host.')[0] + ".pbs", "wr")
            for line in scr:
                newline = line.replace("CONFIG_FILE",hostname.split('host.')[0] + ".conf")
                newscr.write(newline)
                arg = str(workingdir+"/"+hostname.split('host.')[0] + ".pbs")
            
            #subprocess.Popen("qsub -l nodes=1:ppn=4,mem=2gb,walltime=30:00:00 " + arg, shell =True).wait()
            #p = subprocess.check_output(["qsub", "-l", "nodes=1:ppn=4,mem=2gb,walltime=0:30:00",arg])
            #os.popen('/opt/torque-2.5.13/bin/qsub -q prometheus -l nodes=1:ppn=2,mem=2gb,walltime=1:00:00 ' + hostname.split('host.')[0] + ".pbs")
          # p.wait()
            print(arg)
            print(hostname.split('host.')[0] + ".pbs")
            
        pbs_script()
        
#	print ('Writing pose pdbs...')

# reading outfile and creating list of models and lines
	

#	outfile = open(hostname+'.out','r')
#	lig_poses = [[]]

#	i = 0
"""	for line in outfile:
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
	    rec = open(hostname)
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
"""	
	# Building tleap script
"""	
	def leapscript_gen():
	    leap_script = open(hostname + '_' + ligandname + '_build.scr','w')
	    for n in range(len(lig_poses)):
	        filename = hostname + '_' + ligandname + '_pose' + str(n) 
	        leap_script.write(filename + ' = loadpdb ' + 'pose' + str(n) + hostname +'\n')
	        leap_script.write('addions ' + filename + ' Na+ 0' +'\n')
	        leap_script.write('addions ' + filename + ' Cl- 0' +'\n')
	        leap_script.write('solvatebox ' + filename + ' TIP3PBOX 11' +'\n')
	        leap_script.write('saveamberparm ' + filename + ' ' + filename + '.top ' + filename +'.crd \n\n' )
	
#	leapscript_gen()
	end_time = timeit.timeit()
	
	print('Total run time: ' + str(end_time -start_time) + ' seconds')
"""	
#ligandname = raw_input("ligand pdbqt:")

for file in os.listdir(workingdir):
            if "ligand.pdbqt" in file:
                ligandname = str(file)

for file in os.listdir(workingdir):
        if "host.pdbqt" in file:
		start_time = timeit.timeit()
		print(file) 
		docker(file,ligandname,"10")
"""
def script_writer():
        script = open("leap_script.scr","wr")
        script.write('source build.scr \n\n')
        for file in os.listdir(workingdir):
                if "pose" in file:
                         filename = file.split('.pdbqt')[0]
                         print filename
                         script.write(filename + ' = loadpdb ' + file + '\n')
                         script.write('addions ' + filename + ' Na+ 0' +'\n')
                         script.write('addions ' + filename + ' Cl- 0' +'\n')
                         script.write('solvatebox ' + filename + ' TIP3PBOX 14' +'\n')
                         script.write('saveamberparm ' + filename + ' ' + filename + '.top ' + filename +'.crd \n\n' )
#script_writer()
"""		
