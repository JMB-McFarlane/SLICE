# parses pdbqt file to generate a string mask used throughout SLICE including cpptraj and further pdbqt makers

def mask_get(receptor_pdbqt):
    inp_file = open(receptor_pdbqt,'r')
    lines = inp_file.read().splitlines()
    last_res_line = lines[-2]
    mask = last_res_ine
        
