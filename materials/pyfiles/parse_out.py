import os

scores = []
frame = []

workingdir = str(os.getcwd())
for file in os.listdir(workingdir):
	if ".out" in file:
		inp = open(file,"r")
		mod = -1
		for line in inp:
			if "VINA RESULT" in line:
				scores.append([line.split()[3],('pose'+str(mod)+'_'+file.split('host')[0])])
			if "MODEL" in line:
				mod = mod + 1	
#scores.pop(0)
scores.sort(key=lambda x: float(x[0]))
#print scores

cat = open("pdb_cat.pdbqt",'w')
n = 1
list_file = open("scores.dat",'wr')
for items in scores:
	
	print items[1]
	list_file.write(items[0] +' '+ items[1]+'\n')
	cat.write("MODEL " + str(n) + '\n')
	inp = open(items[1],'r')
	ter = 0
	for line in inp:
		#print type(line)
		if "ATOM" in line or "HETATM" in line:
			if ter == 0:
				eline = list(line)
				eline[21] = "A"
				edline = "".join(eline)
				#print type(edline)
				cat.write(edline)
		if 'TER' in line:
			ter = 1
			cat.write(line)
		if "ATOM" in line or "HETATM" in line: 
			if ter == 1:
				eline = list(line)
                        	eline[21] = "B"
                        	edline = "".join(eline)
                        	cat.write(edline)
	cat.write('ENDMDL' +'\n')	
	n =  n + 1


def script_writer():
        skim = 10
	entry =0
	script = open("leap_script.scr","wr")
        script.write('source build.scr \n\n')
	for line in open("scores.dat",'r'):
          	print line     
		if entry <= skim:
			if "pose" in line:
                        
				filename = line.split()[1]
                       		print filename
                       		script.write(filename + ' = loadpdb ' + file + '\n')
                       		script.write('addions ' + filename + ' Na+ 0' +'\n')
                       		script.write('addions ' + filename + ' Cl- 0' +'\n')
                       		script.write('solvatebox ' + filename + ' TIP3PBOX 14' +'\n')
                       		script.write('saveamberparm ' + filename + ' ' + filename + '.top ' + filename +'.crd \n\n' )
		 		entry = entry + 1
script_writer()

	 
