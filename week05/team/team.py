"""
Course: CSE 251
Lesson Week: 05
File: team.py
Author: Brother Comeau

Purpose: Check for prime values

Instructions:

- You can't use thread pools or process pools
- Follow the graph in I-Learn 
- Start with PRIME_PROCESS_COUNT = 1, then once it works, increase it

"""
import queue
import time
import threading
import multiprocessing as mp
import random
from os.path import exists

# Include cse 251 common Python files
from cse251 import *

PRIME_PROCESS_COUNT = 5


def is_prime(n: int) -> bool:
    """Primality test using 6k+-1 optimization.
    From: https://en.wikipedia.org/wiki/Primality_test
    """
    if n <= 3:
        return n > 1
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i ** 2 <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


# TODO create read_thread function
def read_thread(q: mp.Queue, filename: str):
    with open(filename, 'r') as file:
        for line in file:
            q.put(int(line.strip()))

    for _ in range(PRIME_PROCESS_COUNT):
        q.put('NO MORE')


# TODO create prime_process function
def prime_process(prime_list: list, q: mp.Queue):
    while True:
        num = q.get()
        if num == 'NO MORE':
            break
        if is_prime(num):
            print(f'prime: {num}')
            prime_list.append(num)


def create_data_txt(filename):
    # only create if is doesn't exist 
    if not exists(filename):
        with open(filename, 'w') as f:
            for _ in range(1000):
                f.write(str(random.randint(10000000000, 100000000000000)) + '\n')


def main():
    """ Main function """

    filename = 'data.txt'
    create_data_txt(filename)

    log = Log(show_terminal=True)
    log.start_timer()

    # TODO Create shared data structures
    q = mp.Queue()
    prime_list = mp.Manager().list()

    # TODO create reading thread
    t = threading.Thread(target=read_thread, args=(q, filename))

    # TODO create prime processes
    processes = [mp.Process(target=prime_process, args=(prime_list, q)) for _ in range(PRIME_PROCESS_COUNT)]

    # TODO Start them all
    t.start()
    for p in processes:
        p.start()

    # TODO wait for them to complete
    t.join()
    for p in processes:
        p.join()
    log.stop_timer(f'All primes have been found using {PRIME_PROCESS_COUNT} processes')

    # display the list of primes
    print(f'There are {len(prime_list)} found:')
    for prime in prime_list:
        print(prime)


if __name__ == '__main__':
    main()
