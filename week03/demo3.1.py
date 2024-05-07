import os
import threading
import time
import multiprocessing as mp
import os


global_var = 0

def my_function():
    global global_var
    global_var = os.getpid()
    print(f"I started ({global_var})")

    time.sleep(1)
    print(f"I finished ({global_var})")


def main():
    p = mp.Process(target=my_function)
    p1 = mp.Process(target=my_function)
    p2 = mp.Process(target=my_function)
    p.start()
    p1.start()
    p2.start()
    p.join()
    p1.join()
    p2.join()
    print(f"global var: {global_var}")


if __name__ == "__main__":
    main()

print(f"I do bad things ({os.getpid()})")
