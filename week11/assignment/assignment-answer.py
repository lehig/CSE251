"""
Course: CSE 251
Lesson Week: 11
File: Assignment.py
"""

import time
import random
import multiprocessing as mp

# number of cleaning staff and hotel guests
CLEANING_STAFF = 2
HOTEL_GUESTS = 5

# Run program for this number of seconds
TIME = 60

STARTING_PARTY_MESSAGE =  'Turning on the lights for the party vvvvvvvvvvvvvv'
STOPPING_PARTY_MESSAGE  = 'Turning off the lights  ^^^^^^^^^^^^^^^^^^^^^^^^^^'

STARTING_CLEANING_MESSAGE =  'Starting to clean the room >>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
STOPPING_CLEANING_MESSAGE  = 'Finish cleaning the room <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'

def cleaner_waiting():
    time.sleep(random.uniform(0, 2))

def cleaner_cleaning(id):
    print(f'Cleaner: {id}')
    time.sleep(random.uniform(0, 2))

def guest_waiting():
    time.sleep(random.uniform(0, 2))

def guest_partying(id, count):
    print(f'Guest: {id}, count = {count.value}')
    time.sleep(random.uniform(0, 1))

def cleaner(id, start_time: time.time(), cleaned_room, dirty_room, cleaned_count: mp.Value):
    """
    do the following for TIME seconds
        cleaner will wait to try to clean the room (cleaner_waiting())
        get access to the room
        display message STARTING_CLEANING_MESSAGE
        Take some time cleaning (cleaner_cleaning())
        display message STOPPING_CLEANING_MESSAGE
    """
    while  time.time() - start_time< TIME:
        cleaner_waiting()
        # with room_lock:
        dirty_room.acquire()
        print(STARTING_CLEANING_MESSAGE)
        cleaner_cleaning(id)
        print(STOPPING_CLEANING_MESSAGE)
        cleaned_count.value += 1
        cleaned_room.release()

def guest(id, start_time: time.time(), cleaned_room, dirty_room, doorway: mp.Lock, room_count: mp.Value, party_count: mp.Value):
    """
    do the following for TIME seconds
        guest will wait to try to get access to the room (guest_waiting())
        get access to the room
        display message STARTING_PARTY_MESSAGE if this guest is the first one in the room
        Take some time partying (call guest_partying())
        display message STOPPING_PARTY_MESSAGE if the guest is the last one leaving in the room
    """
    while time.time() - start_time < TIME:
        guest_waiting()
        with doorway:
            room_count.value += 1
            if room_count.value == 1:
                cleaned_room.acquire()
                print(STARTING_PARTY_MESSAGE)

        guest_partying(id, room_count)

        with doorway:
            room_count.value -= 1
            if room_count.value == 0:
                print(STOPPING_PARTY_MESSAGE)
                dirty_room.release()
                party_count.value += 1







def main():
    # Start time of the running of the program. 
    start_time = time.time()

    # TODO - add any variables, data structures, processes you need

    acquired_first = mp.Value('b', False)
    # room_lock = mp.Lock()
    cleaned_room = mp.Semaphore(0)
    dirty_room = mp.Semaphore(1)
    door_way = mp.Lock()
    room_count = mp.Value('i', 0)
    cleaned_count = mp.Value('i', 0)
    party_count = mp.Value('i', 0)

    # id, start_time: time.time(), room_lock: mp.Lock, cleaned_count: mp.Value
    clean_p = [mp.Process(target=cleaner, args=(i, start_time, cleaned_room, dirty_room, cleaned_count)) for i in range(HOTEL_GUESTS)]

    # id, start_time: time.time(), room_lock: mp.Lock, doorway: mp.Lock, room_count: mp.Value, party_count: mp.Value
    guest_p = [mp.Process(target=guest, args=(i, start_time, cleaned_room, dirty_room, door_way, room_count, party_count)) for i in range(CLEANING_STAFF)]

    # TODO - add any arguments to cleaner() and guest() that you need
    for p in guest_p:
        p.start()

    for p in clean_p:
        p.start()

    for p in guest_p:
        p.join()
    for p in clean_p:
        p.join()

    # Results
    print(f'Room was cleaned {cleaned_count.value} times, there were {party_count.value} parties')


if __name__ == '__main__':
    main()


'''
Turning off the lights  ^^^^^^^^^^^^^^^^^^^^^^^^^^
Starting to clean the room >>>>>>>>>>>>>>>>>>>>>>>>>>>>>
Cleaner: 2
Finish cleaning the room <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
Turning on the lights for the party vvvvvvvvvvvvvv
Guest: 1, count = 1
Guest: 3, count = 2
Guest: 4, count = 3
Guest: 5, count = 4
Guest: 2, count = 4
Guest: 4, count = 4
Guest: 1, count = 5
Turning off the lights  ^^^^^^^^^^^^^^^^^^^^^^^^^^
Starting to clean the room >>>>>>>>>>>>>>>>>>>>>>>>>>>>
'''

