from random import random
import threading
import time
import os

needed_file = "/home/brett/Projects/SLICE/test_directory/test.out"

def process_file(path):
    print("Found file {}".format(os.path.split(path)[1]))


def do_something_1():
    time.sleep(5)
    print("did something 1")


def do_something_2():
    time.sleep(5)
    print("did something else")


def do_something_3():
    time.sleep(3)
    print("did a third thing")


def check_for_file(path):
    while True:
        if not os.path.isfile(path):
            time.sleep(1)
        else:
            process_file(path)
            break


def main():

    thread = threading.Thread(target=check_for_file, args=[needed_file])
    thread.start()

    do_something_1()
    do_something_2()
    do_something_3()

    thread.join()


if __name__ == '__main__':
    main()