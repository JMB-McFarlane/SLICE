from random import random
import threading
import time
import os

needed_file = "/home/brett/Projects/SLICE/test_directory/test.out"

def process_file(path, start):
    print("\t\t-Found file {} in {:.2f} seconds".format(os.path.split(path)[1], time.time() - start))


def do_something_1():
    start = time.time()
    time.sleep(10)
    print("\t\t-did thing 1 in {:.2f} seconds".format(time.time() - start))


def do_something_2():
    start = time.time()
    time.sleep(4)
    print("\t\t-did thing 2 in {:.2f} seconds".format(time.time() - start))


def do_something_3():
    start = time.time()
    time.sleep(3)
    print("\t\t- did thing 3 in {:.2f} seconds".format(time.time() - start))


def check_for_file(path):
    start = time.time()
    while True:
        if not os.path.isfile(path):
            time.sleep(1)
        else:
            process_file(path, start)
            break


def main():
    print("Entering Main Loop:")
    thread = threading.Thread(target=check_for_file, args=[needed_file])
    thread.start()
    print("\t* Start looking for file test.out")
    start = time.time()
    t2 = threading.Thread(target=do_something_1)
    t2.start()
    print("\t* Start doing thing 1")
    t3 = threading.Thread(target=do_something_2)
    t3.start()
    print("\t* Start doing thing 2")
    t4 = threading.Thread(target=do_something_3)
    t4.start()
    print("\t* Start doing thing 3")
    t2.join()
    t3.join()
    t4.join()
    print("Time for 3 tasks combined: {:.2f} seconds".format(time.time() - start))
    thread.join()


if __name__ == '__main__':
    main()