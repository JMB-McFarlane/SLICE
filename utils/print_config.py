""" Prints information about the configuration file. Throw in some cool ASCII shit here."""


def ASCII_crap():
    print("""
       _____ _     _____ _____  _____ 
      /  ___| |   |_   _/  __ \|  ___|             
      \ `--.| |     | | | /  \/| |__                McFarlane, Henderson, Krause, Paci. 2019       
       `--. \ |     | | | |    |  __|            />_________________________________
      /\__/ / |_____| |_| \__/\| |___   [########[]_________________________________>
      \____/\_____/\___/ \____/\____/            \>
        
        """)

def print_configuration(config,ligand_file,receptor_file):
        
        ASCII_crap()
        print("Number of SLICE Iterations: " + config.get("General", "SLICE_num"))
        print("Number of poses per MD frame: " + config.get("General", "SLICE_num"))
        print("Length of MD trajectories: " + config.get("General", "SLICE_num"))
        print("Length of MD trajectories: " + config.get("General", "SLICE_num"))
        print("Ligand file:" + ligand_file)
        print("Receptor file:" + receptor_file)

def progress(val, start=0, end=100, maxlen=40, hash='#'):
    decimal = val / (end - start)
    progress = decimal * 100
    if progress < 99.999:
        num_hash = int(maxlen * decimal)
        hashes = hash * num_hash + ' ' * (maxlen - num_hash) * len(hash)
        print('\r|'+'{}'.format(hashes)+'| {:.1f}%'.format(progress), end='', flush=True)
    else:
        hashes = hash * maxlen
        print('\r|'+'{}'.format(hashes)+'| DONE!'.format(progress), end='', flush=True)