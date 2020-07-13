import subprocess as sp

try:
    out = sp.check_output('qsub RBP_44.pbs -q prometheus', stderr=sp.STDOUT, shell=True)
    print(out)
except sp.CalledProcessError as e:
    print("Command: {}\nReturn Code: {}\n Output: {}".format(e.cmd, e.returncode, e.output))
