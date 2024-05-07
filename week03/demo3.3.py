import os
import time
import multiprocessing as mp


def add_two_numbers(values):
    # The sleep is here to slow down the program
    time.sleep(0.5)
    number1 = values[0]
    number2 = values[1]
    print(f'PID = {os.getpid()}: {number1} + {number2} = {number1 + number2}')


if __name__ == '__main__':
    # create argument list for the pool
    numbers = []
    numbers.append((1, 2))
    numbers.append((11, 52))
    numbers.append((12, 62))
    numbers.append((13, 72))
    numbers.append((1312, 2272))
    numbers.append((1332, 732))
    numbers.append((13434, -23272))
    numbers.append((1, 2))
    numbers.append((11, 52))
    numbers.append((12, 62))
    numbers.append((13, 72))
    numbers.append((1312, 2272))
    numbers.append((1332, 732))
    numbers.append((13434, -23272))
    numbers.append((1, 2))
    numbers.append((11, 52))
    numbers.append((12, 62))
    numbers.append((13, 72))
    numbers.append((1312, 2272))
    numbers.append((1332, 732))
    numbers.append((13434, -23272))
    numbers.append((1, 2))
    numbers.append((11, 52))
    numbers.append((12, 62))
    numbers.append((13, 72))
    numbers.append((1312, 2272))
    numbers.append((1332, 732))
    numbers.append((13434, -23272))
    print(f'Numbers list: {numbers}')

    # Create a pool of 2 processes
    with mp.Pool(80) as p:
        p.map(add_two_numbers, numbers)
