import os
import subprocess
import time
#/storage/home/jmbm87/SLICE_validation/system1/distances

cwd = os.getcwd()

def execute_cpptraj():
    for i in range(10,11):    
        for y in range(1,11):
            trajin = open("dummy.in",'wr')
            trajin.write("parm /storage/home/jmbm87/SLICE_validation/system1/SLICE_" + str(i) + "/" + str(y) + "/PROD/pep.top" + '\n')
            trajin.write("trajin /storage/home/jmbm87/SLICE_validation/system1/SLICE_" + str(i) + "/" + str(y) + "/PROD/mdcrd" + '\n')
            trajin.write('distance :155 :4GA out ' +  "/storage/home/jmbm87/SLICE_validation/system1/distances/" +str(i) + "_" +str(y) + '_ligdist.dat'+"\n")
            trajin.write("run")
            trajin.close()
            subprocess.call("cpptraj -i dummy.in",shell=True)

          #  os.popen("rm dummy.in")
        

#def parse_distances():
    distances = [[],[],[],[],[],[]]
    for file in os.listdir(cwd): 
        if "hingedist" in file:
            for line in file:
                
                 distances[int(file.split("_")[0])-1].append(line.split()[1])
            
#parse_distances()


execute_cpptraj()

