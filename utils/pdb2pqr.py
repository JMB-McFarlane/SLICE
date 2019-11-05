#This method takes a pdb file generated from cpptraj outpdb format and appends charges from the receptor.pdbqt file. 
#This new receptor.pdbqt file with coordinates from the trajectory can be used as the new Vina receptor
#The method should probably be rewritten to include a catch statement if the pdb and pdbqt are not compatible? 


import os
import sys 

#test path for debugging
path = "/storage/home/jmbm87/SLICE_dev/materials/pyfiles/test_inps/"

def pdb2pqr(path,pdb,qt,hostqt):
    inp_pdb = open(path + pdb, 'r')
    inp_qt = open(path + qt,'r')
    newqt = open(hostqt,'wr')

    lines = []
    
    #XYZ coordinates to be parsed from the pdb file from MD snapshot
    x = []
    y = []
    z = []
    
    #Copied fields from the receptor pdbqt file
    a,b,c,d,e,f,g,h,o = [],[],[],[],[],[],[],[],[]


    #parsing xyz coordinates 
    for line in inp_pdb:
        if "ATOM" in line:
            if len(line.split()) >= 6:
                x.append(line.split()[5])
                y.append(line.split()[6])
                z.append(line.split()[7])
    #parsing the charge file fields
    for line in inp_qt:
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

    for i in range(len(a)):
        lines.append(a[i]+ ' '+ b[i]+ ' '+ c[i]+ ' '+ d[i]+ ' '+ e[i]+ ' ' + x[i]+ ' '+ y[i]+ ' '+ z[i]+ ' ' + f[i] + ' '+ g[i]+ ' '+ h[i]+ ' '+ o[i])
    inp_qt.close()
    inp_qt = open(path + qt,'r')
    i = 0
    #writing new charge file with pdb coordinates 
    for line in inp_qt:
        if "ATOM" in line:
            newqt.write('{:>4} {:>6} {:<4} {:>3} {:>5} {:>11} {:>7} {:>7} {:>5} {:>5} {:>9} {:<2}  ' .format(*lines[i].split()))
            newqt.write('\n')
            i = i+ 1
        if "ATOM" not in line:
            newqt.write(line)

#tester function for debugging
def test_pdb2pqr():
    pdb2pqr(path,"OUT.pdb.1","RBP.receptor.pdbqt","newqt_test.pdbqt")

test_pdb2pqr()
