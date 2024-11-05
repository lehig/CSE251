"""
Course: CSE 251
Lesson Week: 07
File: assingnment.py
Author: <Your name here>
Purpose: Process Task Files

Instructions:  See I-Learn

TODO

Add your comments here on the pool sizes that you used for your assignment and
why they were the best choices.

I chose to have to have the value, word, and sum pools at 3 processors, since more than
that at each of them was just tenths of a second faster. The upper pool had no difference
adding more processors. The name pool I chose 5, because after that it didn't make the program
any faster. 

"""

from datetime import datetime, timedelta
import requests
import multiprocessing as mp
from matplotlib.pylab import plt
import numpy as np
import glob
import math

# Include cse 251 common Python files - Dont change
from cse251 import *

TYPE_PRIME = 'prime'
TYPE_WORD = 'word'
TYPE_UPPER = 'upper'
TYPE_SUM = 'sum'
TYPE_NAME = 'name'

# Global lists to collect the task results
result_primes = []
result_words = []
result_upper = []
result_sums = []
result_names = []


class Task:
    def __init__(self, return_value, task_type):
        self.value = return_value
        self.type = task_type
        # print(return_value)
        # print(result_list)


def is_prime(n: int):
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


def task_prime(value):
    """
    Use the is_prime() above
    Add the following to the global list:
        {value} is prime
            - or -
        {value} is not prime
    """
    task: Task = Task(f'{value} is prime' if is_prime(value) else f'{value} is not prime', 'prime')
    return task

words_text = None
def task_word(task_word):
    """
    search in file 'words.txt'
    Add the following to the global list:
        {word} Found
            - or -
        {word} not found *****
    """
    global words_text
    if words_text is None:
        with open('data.txt') as file:
            words_text = file.read()
    if task_word in words_text:
        task = Task(f'{task_word} Found', 'word')
        return task
    else:
        task = Task(f'{task_word} not found', 'word')
        return task


def task_upper(text):
    """
    Add the following to the global list:
        {text} ==>  uppercase version of {text}
    """
    task = Task(f'{text} ==> {text.upper()}', 'upper')
    return task


def task_sum(start_value, end_value):
    """
    Add the following to the global list:
        sum of {start_value:,} to {end_value:,} = {total:,}
    """
    # total = sum(range(start_value, end_value+1)) # change----------------------------------------------
    total = (end_value - start_value)*(end_value + start_value) / 2
    task = Task(f'sum of start_vlaue: {start_value} to end_value: {end_value} = total: {total}', 'sum')
    return task


def task_name(url):
    """
    use requests module
    Add the following to the global list:
        {url} has name <name>
            - or -
        {url} had an error receiving the information
    """
    response = requests.get(url)
    if response.status_code == 200:
        response = response.json()
        task = Task(f'{url} has name {response["name"]}', 'name')
        return task
    else:
        task = Task(f'{url} had an error receiving the information', 'name')
        return task


def add_to_list(task: Task):
    result_lists = {'name': result_names, 'upper': result_upper, 'sum': result_sums, 'prime': result_primes,
                    'word': result_words}
    result_lists[task.type].append(task.value)


def main():
    log = Log(show_terminal=True)
    log.start_timer()

    # TODO Create process pools

    # TODO you can change the following
    # TODO start and wait pools
    value_pool = mp.Pool(3)
    word_pool = mp.Pool(3)
    text_pool = mp.Pool(1)
    sum_pool = mp.Pool(3)
    name_pool = mp.Pool(5)

    count = 0
    task_files = glob.glob("*.task")
    for filename in task_files:
        # print()
        # print(filename)
        task = load_json_file(filename)
        print(task)
        count += 1
        task_type = task['task']
        if task_type == TYPE_PRIME:
            value_pool.apply_async(task_prime, args=(task['value'],), callback=add_to_list)
        elif task_type == TYPE_WORD:
            word_pool.apply_async(task_word, args=(task['word'],), callback=add_to_list)
        elif task_type == TYPE_UPPER:
            text_pool.apply_async(task_upper, args=(task['text'],), callback=add_to_list)
        elif task_type == TYPE_SUM:
            sum_pool.apply_async(task_sum, args=(task['start'], task['end']), callback=add_to_list)
        elif task_type == TYPE_NAME:
            name_pool.apply_async(task_name, args=(task['url'],), callback=add_to_list)
        else:
            log.write(f'Error: unknown task type {task_type}')

    value_pool.close()
    word_pool.close()
    text_pool.close()
    sum_pool.close()
    name_pool.close()

    value_pool.join()
    word_pool.join()
    text_pool.join()
    sum_pool.join()
    name_pool.join()

    # Do not change the following code (to the end of the main function)
    def log_list(lst, log):
        for item in lst:
            log.write(item)
        log.write(' ')

    log.write('-' * 80)
    log.write(f'Primes: {len(result_primes)}')
    log_list(result_primes, log)

    log.write('-' * 80)
    log.write(f'Words: {len(result_words)}')
    log_list(result_words, log)

    log.write('-' * 80)
    log.write(f'Uppercase: {len(result_upper)}')
    log_list(result_upper, log)

    log.write('-' * 80)
    log.write(f'Sums: {len(result_sums)}')
    log_list(result_sums, log)

    log.write('-' * 80)
    log.write(f'Names: {len(result_names)}')
    log_list(result_names, log)

    log.write(f'Number of Primes tasks: {len(result_primes)}')
    log.write(f'Number of Words tasks: {len(result_words)}')
    log.write(f'Number of Uppercase tasks: {len(result_upper)}')
    log.write(f'Number of Sums tasks: {len(result_sums)}')
    log.write(f'Number of Names tasks: {len(result_names)}')
    log.stop_timer(f'Finished processes {count} tasks')


if __name__ == '__main__':
    main()
