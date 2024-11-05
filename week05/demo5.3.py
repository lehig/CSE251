import multiprocessing as mp
import time

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

def process_function(process_id, barrier, start_value, end_value):
    start_time = time.perf_counter()
    primes = []
    for i in range(start_value, end_value + 1):
        if is_prime(i):
            primes.append(i)
    total_time = time.perf_counter() - start_time

    barrier.wait()  # Wait for all processes to complete the task before printing
    print(f'Process {process_id}: time = {total_time:.5f}: primes found = {len(primes)}')

def main():

    barrier = mp.Barrier(4)         # 4 is the number of processes to wait

    # Create 4 processes, pass a "process_id" and a barrier to each thread
    processes = []
    processes.append(mp.Process(target=process_function, args=(1, barrier, 1, 1000000)))
    processes.append(mp.Process(target=process_function, args=(2, barrier, 1000000, 2000000)))
    processes.append(mp.Process(target=process_function, args=(3, barrier, 2000000, 3000000)))
    processes.append(mp.Process(target=process_function, args=(4, barrier, 3000000, 4000000)))

    for p in processes:
        p.start()

    for p in processes:
        p.join()

if __name__ == '__main__':
    main()