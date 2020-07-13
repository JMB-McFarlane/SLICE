import os



def parse_SLICE(SLICE_path):

    scores = []
    frame = []

    workingdir = SLICE_path

    for file in os.listdir(workingdir):
	mod = -1
	if os.path.isdir(file) == True:
		subdir = workingdir +'/'+ file + "/PROD/"
		print subdir
                os.popen("python " + subdir + "grabber.py")
		for file in os.listdir(subdir):
			if ".out" in file:
				submod = -1
				print file
				inp = open(subdir + file,"r")
				for line in inp:
					if "VINA RESULT" in line:
						scores.append([line.split()[3],subdir + 'pose'+str(submod)+'_'+file.split('host')[0]])
					if "MODEL" in line:
						mod = mod + 1
						submod = submod + 1	
    scores.sort(key=lambda x: float(x[0]))
    n = 1
    list_file = open("scores.dat",'w')
    for items in scores:
	list_file.write(items[0] +' '+ items[1]+'\n')
	n =  n + 1
    list_file.close()

def pose_selector(SLICE_path,selector_type):
    if selector_type == 1:
        print("Skim")
    if selector_type == 2:
        print("Rosenbluth")
    #make a folder in the SLICE_path to contain the chosen pdbs
    


def script_writer(SLICE_path,output_path,):
            skim = 10
            entry =1
            script = open("leap_script.scr","wr")
            script.write('source build.scr \n\n')
            for line in open("scores.dat",'r'):
                if entry <= skim:
                    if "pose" in line:
                        filesource = line.split()[1]
                        filename = "pose" + str(entry)
                        print(filename  + " " + filesource)
                        script.write(filename + ' = loadpdb ' + filesource + '\n')
                        script.write('addions ' + filename + ' Na+ 0' +'\n')
                        script.write('addions ' + filename + ' Cl- 0' +'\n')    
                        script.write('solvatebox ' + filename + ' TIP3PBOX 14' +'\n')
                        script.write('saveamberparm ' + filename + ' ' + filename + '.top ' + filename +'.crd \n\n' )
                        entry = entry + 1


