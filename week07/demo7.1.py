# Example using pool apply_asyc()

import multiprocessing as mp

from cse251 import *


class MyResult:
    def __init__(self, x, sum):
        self.x = x
        self.sum = sum

    def __str__(self):
        return f"{self.x}: {self.sum}"


def finished_callback(result):
    print(f"Brother Kay was right! {result}")


def sum_all_values(x):
    total = 0
    for i in range(1, x + 1):
        total += i
    return MyResult(x, total)


def print_sum_of_numbers(x):
    print(sum(range(x)))
    return True


if __name__ == "__main__":
    log = Log(filename_log='apply_async.log', show_terminal=True)
    log.start_timer()
    pool = mp.Pool(4)
    print("pool is initialized")
    results = [pool.apply_async(sum_all_values, args=(x,), callback=finished_callback) for x in
               range(10000, 10000 + 10)]
    results2 = [pool.apply_async(print_sum_of_numbers, args=(x,)) for x in range(10000, 10000 + 10)]

    # do something else
    print("Brother Kay is Happy")
    # time.sleep(1)
    print("brother Kay is well rested")

    # collect all of the results into a list
    # output = [p.get() for p in results]
    # for r in results2:
    #     r.get()
    #     print(r)
    #     if not r.get():
    #         print(f"{r.get()} failed")
    log.stop_timer('Finished: ')
    # print(output)
    pool.close()
    pool.join()
