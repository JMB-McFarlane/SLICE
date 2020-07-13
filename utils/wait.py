
import os
import subprocess as sp
import time

def wait_q(pbs_file):
        running = True
        while running == True:
            try:
                out = sp.check_output('qstat -u jmbm87', stderr=sp.STDOUT, shell=True)
                out1 = str(out)
               # print("Checking for PBS file: " + pbs_file.split("/")[-1]) 
               # print(out1)
                if pbs_file.split("/")[-1] in out1:
                    time.sleep(10)
                if pbs_file.split("/")[-1] not in out1:
                    print("Next Step")
                    break
            except sp.CalledProcessError as e:
                print("Command: {}\nReturn Code: {}\n Output: {}".format(e.cmd, e.returncode, e.output))
            

