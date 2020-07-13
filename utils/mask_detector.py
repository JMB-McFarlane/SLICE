# parses pdbqt file to generate a string mask used throughout SLICE including cpptraj and further pdbqt makers

def mask_get(receptor_pdbqt):
    inp_file = open(receptor_pdbqt,'r')
    lines = inp_file.read().splitlines()
    last_res_line = lines[-2]
  #  print lines[-2]
    mask = last_res_line.split()[4]
    print("Host Residue Mask Detected: 1-"+mask)
    return(":1-"+mask)
    

def test_mask():
    mask_get("/storage/home/jmbm87/SLICE_dev/utils/unit_test_files/RBP.receptor.pdbqt")
    print("Test")
test_mask()
