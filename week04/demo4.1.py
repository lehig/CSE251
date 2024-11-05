import threading
import time
def tocker(tick_done_sem:threading.Semaphore, tock_done_sem:threading.Semaphore):
    for _ in range(100):
        tick_done_sem.acquire()
        time.sleep(.1)
        print("Tock!!")
        tock_done_sem.release()

def ticker(tick_done_sem:threading.Semaphore, tock_done_sem:threading.Semaphore):
    for _ in range(100):
        tock_done_sem.acquire()
        time.sleep(.1)
        print("***TICK***")
        tick_done_sem.release()


def main():
    tick_done_sem = threading.Semaphore(0)
    tock_done_sem = threading.Semaphore(1)

    tick = threading.Thread(target=ticker, args=(tick_done_sem, tock_done_sem))
    tock = threading.Thread(target=tocker, args=(tick_done_sem, tock_done_sem))

    tick.start()
    tock.start()

    tick.join()
    tock.join()

if __name__ == '__main__':
    main()