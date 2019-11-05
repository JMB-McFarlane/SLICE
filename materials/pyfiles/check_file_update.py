#checks file update value

import os

def check_file_status(filename):
    test = str(os.stat(filename))
  # print test.split("st_ctime=")[1].split(")")[0]
    return test.split("st_ctime=")[1].split(")")[0]

   # print type(test)
check_file_status("/storage/home/jmbm87/SLICE_dev/materials/pyfiles/test_inps/text.txt")
