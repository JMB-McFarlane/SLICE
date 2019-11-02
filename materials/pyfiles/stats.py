import os 
cwd = os.getcwd()

def parse_distances():
        slice_num = "10"
        distances = []
        for file in os.listdir(cwd):
                        if "ligdist" in file:
                            if file.split("_")[0] == slice_num:
                                    inp = open(file,'r')    
                                    print file
                                    for line in inp:
                                
                                        if "#" not in line:
                                            print line
                                            distances.append(float(line.split()[1]))
      #  print distances
        print sum(distances)/len(distances)
        print min(distances) 
        print max(distances)
        
        #                                    distances[int(file.split("_")[0])-1].append(line.split()[1])

parse_distances()
