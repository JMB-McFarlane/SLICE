import os 


cwd = os.getcwd()
    

# Creates directories for MD
def make_dirs():
    for i in range(1,11):
        os.popen("mkdir " + str(i))
        os.popen("mkdir " + cwd + "/" + str(i) + "/MIN")
        os.popen("mkdir " + cwd + "/" + str(i) + "/HEAT")
        os.popen("mkdir " + cwd + "/" + str(i) + "/PROD")
   #     os.popen('mv pose' + str(i) + ".crd " + cwd + "/" + str(i) + "/MIN/pose.crd") 
   #     os.popen('mv pose' + str(i) + ".top " + cwd + "/" + str(i) + "/MIN/pep.top")
def copy_inputs():
    for i in range(1,11):
        os.popen("cp /storage/home/jmbm87/md_run_files/MIN.scr " + cwd + "/" + str(i) + "/MIN")
        os.popen("cp /storage/home/jmbm87/md_run_files/min.in " + cwd + "/" + str(i) + "/MIN")
        
        os.popen("cp /storage/home/jmbm87/md_run_files/HEAT.scr " + cwd + "/" + str(i) + "/HEAT")
        os.popen("cp /storage/home/jmbm87/md_run_files/heat.in " + cwd + "/" + str(i) + "/HEAT")

        os.popen("cp /storage/home/jmbm87/md_run_files/PROD1.scr " + cwd + "/" + str(i) + "/PROD")
        os.popen("cp /storage/home/jmbm87/md_run_files/prod1.in " + cwd + "/" + str(i) + "/PROD")
        
        os.popen("cp pose" + str(i) + ".top " + str(i) + "/MIN/pep.top")
        os.popen("cp pose" + str(i) + ".crd " + str(i) + "/MIN/pose.crd")
        os.popen("cp pose" + str(i) + ".top " + str(i) + "/HEAT/pep.top")
        os.popen("cp pose" + str(i) + ".top " + str(i) + "/PROD/pep.top")

        os.popen("cp " + cwd + "/" + str(i) + "/MIN/min.rst " + cwd + "/" + str(i) + "/HEAT")
        os.popen("cp " + cwd + "/" + str(i) + "/HEAT/heat.rst " + cwd + "/" + str(i) + "/PROD")
        os.popen("cp /storage/home/jmbm87/SLICE_validation/system1/source_files/MD_source/* " + cwd + "/" + str(i) + "/PROD")

make_dirs()
copy_inputs()
print("qsub -l nodes=1:ppn=28,mem=2gb,walltime=3:00:00 MIN.scr")
print("qsub -l nodes=1:ppn=28,mem=2gb,walltime=12:00:00 HEAT.scr")
print("qsub -l nodes=1:ppn=28,mem=2gb,walltime=24:00:00 PROD1.scr")
