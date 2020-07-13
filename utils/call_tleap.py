import os

def call_leap(path):
    os.popen("tleap -f " + path + "/leap_script.scr")

