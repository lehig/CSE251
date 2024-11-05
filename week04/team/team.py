"""
Course: CSE 251
Lesson Week: 04
File: team.py
Author: Brother Comeau

Purpose: Team Activity

Instructions:

- See in I-Learn

Question: is the Python Queue thread safe?  (https://en.wikipedia.org/wiki/Thread_safety)

"""

import threading
import queue
import requests
import json

# Include cse 251 common Python files
from cse251 import *

RETRIEVE_THREADS = 40  # Number of retrieve_threads
NO_MORE_VALUES = 'No more'  # Special value to indicate no more items in the queue


def retrieve_thread(q: queue, log):
    """ Process values from the data_queue """

    while True:
        url = q.get()
        if url == 'No more':
            break

        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                name = data['name']
                log.write(f'Retrieved: {name}')
            else:
                log.write(f"Error retrieving {url}: Status code {response.status_code}")

        except requests.RequestException as e:
            log.write(f"Request exception for {url}: {e}")
        finally:
            q.task_done()

    q.task_done()


def file_reader(file: str, q: queue, log: Log):
    """ This thread reading the data file and places the values in the data_queue """

    with open(file, 'r') as file:
        for line in file:
            url = line.strip()
            q.put(url)
    log.write('finished reading file')

    for _ in range(RETRIEVE_THREADS):
        q.put(NO_MORE_VALUES)


def main():
    """ Main function """

    log = Log(show_terminal=True)

    # creating a queue
    q = queue.Queue()

    # Pass any arguments to these thread need to do their job
    file_reader_thread = threading.Thread(target=file_reader, args=('urls.txt', q, log))
    retrieve_threads = [threading.Thread(target=retrieve_thread, args=(q, log)) for _ in range(RETRIEVE_THREADS)]

    log.start_timer()

    for t in retrieve_threads:
        t.start()

    file_reader_thread.start()

    file_reader_thread.join()

    q.join()

    log.stop_timer('Time to process all URLS')


if __name__ == '__main__':
    main()
