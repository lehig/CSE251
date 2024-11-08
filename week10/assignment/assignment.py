"""
Course: CSE 251
Lesson Week: 10
File: assignment.py
Author: <your name>

Purpose: assignment for week 10 - reader writer problem

Instructions:

- Review TODO comments

- writer: a process that will send numbers to the reader.  
  The values sent to the readers will be in consecutive order starting
  at value 1.  Each writer will use all of the sharedList buffer area
  (ie., BUFFER_SIZE memory positions)

- reader: a process that receive numbers sent by the writer.  The reader will
  accept values until indicated by the writer that there are no more values to
  process.  

- Do not use try...except statements

- Display the numbers received by the reader printing them to the console.

- Create WRITERS writer processes

- Create READERS reader processes

- You can use sleep() statements for any process.

- You are able (should) to use lock(s) and semaphores(s).  When using locks, you can't
  use the arguments "block=False" or "timeout".  Your goal is to make your
  program as parallel as you can.  Over use of lock(s), or lock(s) in the wrong
  place will slow down your code.

- You must use ShareableList between the two processes.  This shareable list
  will contain different "sections".  There can only be one shareable list used
  between your processes.
  1) BUFFER_SIZE number of positions for data transfer. This buffer area must
     act like a queue - First In First Out.
  2) current value used by writers for consecutive order of values to send
  3) Any indexes that the processes need to keep track of the data queue
  4) Any other values you need for the assignment

- Not allowed to use Queue(), Pipe(), List(), Barrier() or any other data structure.

- Not allowed to use Value() or Array() or any other shared data type from 
  the multiprocessing package.

- When each reader reads a value from the sharedList, use the following code to display
  the value:
  
                    print(<variable>, end=', ', flush=True)

Add any comments for me:

"""

import random
import threading
from multiprocessing.managers import SharedMemoryManager
import multiprocessing as mp

BUFFER_SIZE = 10
READERS = 2
WRITERS = 2


# def read_func(data: SharedMemoryManager, read_sem: mp.Semaphore, write_sem: mp.Semaphore, items_to_send):
#     read_sem.acquire()
#

# def readers_func(data: SharedMemoryManager, read_sem: mp.Semaphore, write_sem: mp.Semaphore, items_to_send):
#     head = 10
#     tail = 11
#     num_to_add = 12
#     values_processed = 13
#
#     while data[values_processed] != items_to_send:
#         read_sem.acquire()
#         print(f'{data[data[head]]}', end=', ', flush=True)
#
#         # update the tail
#         data[head] = (data[head] + 1) % 9
#         data[values_processed] += 1
#         write_sem.release()
#
#
# def writers_func(data: SharedMemoryManager, read_sem: mp.Semaphore, write_sem: mp.Semaphore, writer_lock: mp.Lock, items_to_send):
#     head = 10
#     tail = 11
#     num_to_add = 12
#     values_processed = 13
#
#     for i in range(items_to_send):
#         write_sem.acquire()
#         with writer_lock:
#             data[num_to_add] = i
#             data[tail] = data[num_to_add]
#
#             # update the head
#             data[tail] = (data[tail] + 1) % 9
#         read_sem.release()


def reader_func(data: SharedMemoryManager, read_sem: mp.Semaphore, write_sem: mp.Semaphore, items_to_send):
    for i in range(items_to_send):
        read_sem.acquire()

        print(f'{data[data[11]]}', end=', ', flush=True)
        data[13] += 1
        write_sem.release()


def writer_func(data: SharedMemoryManager, read_sem: mp.Semaphore, write_sem: mp.Semaphore, writer_lock: mp.Lock, items_to_send):
    for i in range(items_to_send):
        write_sem.acquire()
        data[12] = i
        data[data[10]] = data[12]

        # update the head
        data[10] = (data[10] + 1) % 9

        # update the tail
        if data[10] == 0:
            data[11] = 9
        else:
            data[11] = data[10] - 1
        read_sem.release()


def main():
    # This is the number of values that the writer will send to the reader
    items_to_send = random.randint(1000, 10000)

    smm = SharedMemoryManager()
    smm.start()

    # TODO - Create a ShareableList to be used between the processes
    #      - The buffer should be size 10 PLUS at least three other
    #        values (ie., [0] * (BUFFER_SIZE + 3)).  The extra values
    #        are used for the head and tail for the circular buffer.
    #        The another value is the current number that the writers
    #        need to send over the buffer.  This last value is shared
    #        between the writers.
    #        You can add another value to the sharedable list to keep
    #        track of the number of values received by the readers.
    #        (ie., [0] * (BUFFER_SIZE + 4))
    data = smm.ShareableList([0] * (BUFFER_SIZE + 5))

    # TODO - Create any lock(s) or semaphore(s) that you feel you need
    reader_semaphore = mp.Semaphore(0)
    writer_semaphore = mp.Semaphore(2)
    writer_lock = mp.Lock()

    # TODO - create reader and writer processes
    readers = [mp.Process(target=reader_func, args=(data, reader_semaphore, writer_semaphore, items_to_send)) for i in range(READERS)]
    writers = [mp.Process(target=writer_func, args=(data, reader_semaphore, writer_semaphore, writer_lock, items_to_send)) for i in range(WRITERS)]

    # TODO - Start the processes and wait for them to finish
    for writer in writers:
        writer.start()
    for reader in readers:
        reader.start()

    for writer in writers:
        writer.join()
    for reader in readers:
        reader.join()

    print(f'\n{items_to_send} values sent')

    # TODO - Display the number of numbers/items received by the reader.
    #        Can not use "items_to_send", must be a value collected
    #        by the reader processes.
    print(f'{data[13]} values received')

    smm.shutdown()


if __name__ == '__main__':
    main()
