"""
Course: CSE 251
Lesson Week: 04
File: assignment.py
Author: <Your name>

Purpose: Assignment 04 - Factory and Dealership

Instructions:

- See I-Learn

"""

import time
import threading
import random

# Include cse 251 common Python files
from cse251 import *

# Global Consts - Do not change
CARS_TO_PRODUCE = 500
MAX_QUEUE_SIZE = 10
SLEEP_REDUCE_FACTOR = 50

# NO GLOBAL VARIABLES!

class Car():
    """ This is the Car class that will be created by the factories """

    # Class Variables
    car_makes = ('Ford', 'Chevrolet', 'Dodge', 'Fiat', 'Volvo', 'Infiniti', 'Jeep', 'Subaru', 
                'Buick', 'Volkswagen', 'Chrysler', 'Smart', 'Nissan', 'Toyota', 'Lexus', 
                'Mitsubishi', 'Mazda', 'Hyundai', 'Kia', 'Acura', 'Honda')

    car_models = ('A1', 'M1', 'XOX', 'XL', 'XLS', 'XLE' ,'Super' ,'Tall' ,'Flat', 'Middle', 'Round',
                'A2', 'M1X', 'SE', 'SXE', 'MM', 'Charger', 'Grand', 'Viper', 'F150', 'Town', 'Ranger',
                'G35', 'Titan', 'M5', 'GX', 'Sport', 'RX')

    car_years = [i for i in range(1990, datetime.now().year)]

    def __init__(self):
        # Make a random car
        self.model = random.choice(Car.car_models)
        self.make = random.choice(Car.car_makes)
        self.year = random.choice(Car.car_years)

        # Sleep a little.  Last statement in this for loop - don't change
        time.sleep(random.random() / (SLEEP_REDUCE_FACTOR))

        # Display the car that has just be created in the terminal
        self.display()
           
    def display(self):
        print(f'{self.make} {self.model}, {self.year}')


class Queue251():
    """ This is the queue object to use for this assignment. Do not modify!! """

    def __init__(self):
        self.items = []

    def size(self):
        return len(self.items)

    def put(self, item):
        assert len(self.items) <= 10
        self.items.append(item)

    def get(self):
        return self.items.pop(0)


class Factory(threading.Thread):
    """ This is a factory.  It will create cars and place them on the car queue """

    def __init__(self, q: Queue251, fac_sem: threading.Semaphore, deal_sem: threading.Semaphore, barrier):
        # to create cars and to place them in a queue.
        super().__init__()
        self.queue = q
        self.fac_sem = fac_sem
        self.deal_sem = deal_sem
        self.barrier = barrier


    def run(self):
        for i in range(CARS_TO_PRODUCE):
            """
            create a car
            place the car on the queue
            signal the dealer that there is a car on the queue
           """
            self.fac_sem.acquire()
            car = Car()
            self.queue.put(car)
            self.deal_sem.release()


        # signal the dealer that there there are not more cars
        self.queue.put("No More Cars")
        print('Factory Done!')
        self.deal_sem.release()
        print(self.deal_sem)



class Dealer(threading.Thread):
    """ This is a dealer that receives cars """

    def __init__(self, q: Queue251, fac_sem: threading.Semaphore, deal_sem: threading.Semaphore, q_stats: list):
        super().__init__()
        self.queue = q
        self.fac_sem = fac_sem
        self.deal_sem = deal_sem
        self.q_stats = q_stats

    def run(self):
        while True:
            """
            take the car from the queue
            signal the factory that there is an empty slot in the queue
            """

            self.deal_sem.acquire()

            car = self.queue.get()
            if car == "No More Cars":
                print('Dealer Done!')
                break
            self.q_stats[self.queue.size() - 1] += 1
            print('---SOLD---')
            car.display()
            print('----------')
            self.fac_sem.release()
            # Sleep a little after selling a car
            # Last statement in this for loop - don't change
            time.sleep(random.random() / (SLEEP_REDUCE_FACTOR))



def main():
    log = Log(show_terminal=True)

    # Create semaphore(s)
    fac_sem = threading.Semaphore(10)
    deal_sem = threading.Semaphore(0)
    # Create queue251
    queue = Queue251()

    # This tracks the length of the car queue during receiving cars by the dealership
    # i.e., update this list each time the dealer receives a car
    queue_stats = [0] * MAX_QUEUE_SIZE

    # create your one factory
    factory_thread = Factory(queue, fac_sem, deal_sem)
    # create your one dealership
    dealership_thread = Dealer(queue, fac_sem, deal_sem, queue_stats)

    log.start_timer()

    # Start factory and dealership
    factory_thread.start()
    dealership_thread.start()

    # Wait for factory and dealership to complete
    factory_thread.join()
    dealership_thread.join()
    log.stop_timer(f'All {sum(queue_stats)} have been created')

    xaxis = [i for i in range(1, MAX_QUEUE_SIZE + 1)]
    plot = Plots()
    plot.bar(xaxis, queue_stats, title=f'{sum(queue_stats)} Produced: Count VS Queue Size', x_label='Queue Size', y_label='Count')


if __name__ == '__main__':
    main()
