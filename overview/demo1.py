from cse251 import *
import threading

print("hello world")


# variable
t1 = 1
t2 = dict()
t2["myKey"] = 12341234
t3 = [1,2,3]

# functions
def do_something(param1=0, param2=0, param3=0):
    print("before", param1, param2, param3)
    time.sleep(3) # could be I/O
    print("after", param1, param2, param3)

# do_something(param3=45)

t4 = threading.Thread(target=do_something, args=(4, )) # making a thread the target being the set of instructions.
t5 = threading.Thread(target=do_something, args=(5, ))
t4.start() # starts the thread
t5.start()
t4.join() # ends the thread
t5.join()