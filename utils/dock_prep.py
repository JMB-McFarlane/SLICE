import os
import math
import subprocess as sp
import time
import wait 

testpath = "/storage/home/jmbm87/SLICE_dev/utils/unit_test_files/"

def dock_prep(write_path,read_path,host_name,ligand_name,box_residues,poses,exhaust,cpu):
	config = open(write_path+host_name.split(".pdbqt")[0] + ".conf", 'w')
	config.write('receptor = '+ write_path + host_name + '\n')
	config.write('ligand = ' + read_path + ligand_name + '\n' + '\n')

	# Box configuration

	boxresidues = []
	res_x = []
	res_y = []
	res_z = []

	cyx = []

        box_residues = str.split(box_residues)
	for res in box_residues:
    		with open(write_path + host_name) as file:
        		for line in file:
            			if ' ' + res + ' ' in line:
                			if 'ATOM' in line:
                    				clean = line.split()
                    				res_x.append(float(clean[5]))
                  			  	res_y.append(float(clean[6]))
               				     	res_z.append(float(clean[7]))
        # Disulfide bridge finder
	with open(write_path + host_name) as file:
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
        #print Cx,Cy,Cz

	Sx = str((float(max(res_x)) - float(min(res_x)) +8))
	Sy = str((float(max(res_y)) - float(min(res_y)) +8))
	Sz = str((float(max(res_z)) - float(min(res_z)) + 8))
	#print("Box size = ")
	#print Sx,Sy,Sz
         
	# Configuration file
	config.write('center_x = ' + Cx + '\n')
	config.write('center_y = ' + Cy + '\n')
	config.write('center_z = ' + Cz + '\n' + '\n')
	
	config.write('size_x = ' + Sx + '\n')
	config.write('size_y = ' + Sy + '\n')
	config.write('size_z = ' + Sz + '\n' + '\n')

	config.write('out = ' + write_path + host_name +'.out'+ '\n')
	config.write('exhaustiveness = ' + exhaust + '\n')
	config.write('num_modes = ' + poses + '\n')
	config.write('cpu = ' + cpu)
	config.close()

def dock_pbs_script(script_path,write_path,host_name):
        scr = open(script_path + "/script.pbs",'r')
        newscr = open(write_path + host_name.split('.')[0] + ".pbs", "wr")
        for line in scr:
            newline = line.replace("CONFIG_FILE",write_path + host_name.split('.')[0] + ".conf")
            newscr.write(newline)
        newscr.close()
        submit_dock(write_path + host_name.split('.')[0] + ".pbs")
        print(write_path + host_name.split('.')[0] + ".pbs")

def test_dockprep():
    dock_prep(testpath,testpath,"RBP.receptor.pdbqt","ligand.pdbqt","1 2 3","10","7","7")
    dock_pbs_script(testpath,testpath,"RBP.receptor.pdbqt")


def submit_dock(pbs_file):
    try:
            out = sp.check_output('qsub ' + pbs_file+ ' -q prometheus', stderr=sp.STDOUT, shell=True)
            print(out)
                
    except sp.CalledProcessError as e:
            print("Command: {}\nReturn Code: {}\n Output: {}".format(e.cmd, e.returncode, e.output))
    if "initial" in pbs_file:
        wait.wait_q(pbs_file)
#test_dockprep()
	

