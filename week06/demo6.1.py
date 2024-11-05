import multiprocessing
import time

def sender(conn):
    """ function to send messages to other end of pipe """
    conn.send('Hello')
    time.sleep(1)
    conn.send('World')
    time.sleep(1)
    print(conn.recv())
    conn.close() 			# Close this connection when done

def receiver(conn):
    """ function to print the messages received from other end of pipe  """
    print(f'Received: {conn.recv()}')
    print(f'Received: {conn.recv()}')
    conn.send('10-4')

if __name__ == "__main__":

    # creating a pipe
    parent_conn, child_conn = multiprocessing.Pipe()

    # creating new processes
    p1 = multiprocessing.Process(target=sender, args=(parent_conn,))
    p2 = multiprocessing.Process(target=receiver, args=(child_conn,))

    # running processes
    p1.start()
    p2.start()

    # wait until processes finish
    p1.join()
    p2.join()