import subprocess
import os
import random
import math

scores = []
frame = []


workingdir = str(os.getcwd())

for file in os.listdir(workingdir):
	mod = -1
	if os.path.isdir(file) == True:
		subdir = workingdir +'/'+ file + "/PROD/"
		print subdir
                os.popen("cd " + subdir)
                subprocess.call("python " + subdir + "grabber.py",shell=True)
                os.popen("cd " + workingdir)
		print("python " + subdir + "grabber.py")
                for file in os.listdir(subdir):
			if ".out" in file:
				submod = -1
	#			print file
				inp = open(subdir + file,"r")
				for line in inp:
					if "VINA RESULT" in line:
						scores.append([line.split()[3],subdir + 'pose'+str(submod)+'_'+file.split('.')[0]])
					if "MODEL" in line:
						mod = mod + 1
						submod = submod + 1	
scores.sort(key=lambda x: float(x[0]))

#cat = open("pdb_cat.pdbqt",'w')
n = 1
list_file = open("scores.dat",'w')
for items in scores:
	
#	print items[1]
	list_file.write(items[0] +' '+ items[1]+'\n')
#	cat.write("MODEL " + str(n) + '\n')
#	inp = open(items[1],'r')
#	for line in inp:
#		cat.write(line)
#	cat.write('ENDMDL' +'\n')	
	n =  n + 1

list_file.close()


def script_writer():
            selected_files = open("selected.txt",'wr')
            skim = 5
            entry =1
            script = open("leap_script.scr","wr")
            script.write('source build.scr \n\n')
            scores = []
            lines = []
            for line in open("scores.dat",'r'):
                scores.append(float(line.split()[0]))
                lines.append(line)
                if entry <= skim:
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
            while i <= 4:
                random_pick = random.randint(0,len(scores))
                if px_fill[random_pick] >= random.uniform(0,1):
                    i = i+1
                    selected_files.write(lines[random_pick] + "\n")
            selected_files.close()
            selected = open("selected.txt",'r')
            entry = 1
            for line in selected:
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

script_writer()
