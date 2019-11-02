import os

string = []
for i in range(1,51):
    string.append('qsub -l nodes=1:ppn=7,mem=2gb,walltime=3:00:00 ' + 'MBP_' + str(i) + ".pbs;")
    stringer = ''.join(string)
print stringer
