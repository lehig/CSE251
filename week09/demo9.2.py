import threading
import time
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)

def consumer(cv):
    logging.debug('Consumer thread started ...')
    with cv: # <-- this is the lock that is needed for both wait/notify_all
        logging.debug('Consumer waiting ...')
        cv.wait()
        logging.debug('Consumer consumed the resource')
        # cv.notify()

def producer(cv:threading.Condition):
    logging.debug('Producer thread started ...')
    # with cv:
    cv.acquire()
    logging.debug('Making resource available')
    logging.debug('Notifying to all consumers')
    cv.notify_all()
    cv.release()

if __name__ == '__main__':
    condition = threading.Condition()
    cs1 = threading.Thread(name='consumer1', target=consumer, args=(condition,))
    cs2 = threading.Thread(name='consumer2', target=consumer, args=(condition,))
    pd = threading.Thread(name='producer', target=producer, args=(condition,))

    cs1.start()
    time.sleep(2)
    cs2.start()
    time.sleep(2)
    pd.start()