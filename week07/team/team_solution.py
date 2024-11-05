"""
Course: CSE 251
Lesson Week: Week 07
File: team.py
Purpose: Week 07 Team Activity

Instructions:

1) Make a copy of your assignment 2 program.  Since you are 
   working in a team, you can decide which assignment 2 program 
   that you will use for the team activity.

2) Convert the program to use a process pool and use 
   apply_async() with a callback function to retrieve data 
   from the Star Wars website.  Each request for data must 
   be a apply_async() call.

3) You can continue to use the Request_Thread() class from 
   assignment 02 that makes the call to the server.

"""

"""
Course: CSE 251 
Lesson Week: 02
File: assignment.py 
Author: Brother Comeau

Purpose: Retrieve Star Wars details from a server

Instructions:

- Each API call must only retrieve one piece of information
- You are not allowed to use any other modules/packages except for the ones used
  in this assignment.
- Run the server.py program from a terminal/console program.  Simply type
  "python server.py"
- The only "fixed" or hard coded URL that you can use is TOP_API_URL.  Use this
  URL to retrieve other URLs that you can use to retrieve information from the
  server.
- You need to match the output outlined in the decription of the assignment.
  Note that the names are sorted.
- You are requied to use a threaded class (inherited from threading.Thread) for
  this assignment.  This object will make the API calls to the server. You can
  define your class within this Python file (ie., no need to have a seperate
  file for the class)
- Do not add any global variables except for the ones included in this program.

The call to TOP_API_URL will return the following Dictionary(JSON).  Do NOT have
this dictionary hard coded - use the API call to get this.  Then you can use
this dictionary to make other API calls for data.

{
   "people": "http://127.0.0.1:8790/people/", 
   "planets": "http://127.0.0.1:8790/planets/", 
   "films": "http://127.0.0.1:8790/films/",
   "species": "http://127.0.0.1:8790/species/", 
   "vehicles": "http://127.0.0.1:8790/vehicles/", 
   "starships": "http://127.0.0.1:8790/starships/"
}
"""

from datetime import datetime, timedelta
import requests
import json
import threading
import multiprocessing as mp

# Include cse 251 common Python files
from cse251 import *

# Const Values
TOP_API_URL = 'http://127.0.0.1:8790'

# Global Variables
call_count = 0


# TODO Add your threaded class definition here
class RequestThread(threading.Thread):

    def __init__(self, url):
        super().__init__()
        self.url = url
        self.response = {}
        self.info = {}

    def run(self):
        response = requests.get(self.url)
        global call_count
        call_count += 1
        if response.status_code == 200:
            self.response = response.json()
        else:
            print(f"Response: {response.status_code}")


def get_api_result(url):
    request = RequestThread(url)
    request.start()
    request.join()
    return request


def request_func(url):
    response = requests.get(url)
    global call_count
    call_count += 1
    if response.status_code == 200:
        response = response.json()
        return response
    else:
        print(f"Response: {response.status_code}")
        return None


def movie_func(url: str, movie=6):
    init_req = request_func(f'{url}{movie}')
    return init_req


def get_name(x):
    return x['name']


# TODO Add any functions you need here
# def top_api_func(url: str):
#     pool = mp.pool
#     req = pool.apply_async(, args=(x,), callback=finished_callback)
#     req.start()
#     req.join()
#     return req.response


# def object_req_func(urls:list):
#     objects = []
#     request_threads = []
#     for url in urls:
#         req = RequestThread(url)
#         req.start()
#         request_threads.append(req)
#
#     for thread in request_threads:
#         thread.join()
#
#     for thread in request_threads:
#         objects.append(thread.response['name'])
#
#     return objects


def main():
    log = Log(show_terminal=True)
    log.start_timer('Starting to retrieve data from the server')
    # movie = 6
    call_count = 0

    pool = mp.Pool(4)
    # req = pool.apply_async(, args = (x,), callback = finished_callback)

    # getting the top url
    result = pool.apply_async(get_api_result, args=(TOP_API_URL,), callback=movie_func)
    call_count +=1
    film_result = result.get()

    # getting the movie url
    # response2 = pool.apply_async(movie_func, args=(response1['films'], movie))

    # getting the info from the movie url
    print(result.get())
    title = response['title']
    director = response['director']
    producer = response['producer']
    release_date = response['release_date']

    # requesting lists of names from each url section
    characters = [pool.apply_async(request_func, args=url, callback=get_name) for url in response['characters']]
    planets = [pool.apply_async(request_func, args=url, callback=get_name) for url in response['planets']]
    starships = [pool.apply_async(request_func, args=url, callback=get_name) for url in response['starships']]
    vehicles = [pool.apply_async(request_func, args=url, callback=get_name) for url in response['vehicles']]
    species = [pool.apply_async(request_func, args=url, callback=get_name) for url in response['species']]

    # printing results
    log.write(f'-----------------------------------------------')
    log.write(f'Title   : {title}')
    log.write(f"Director: {director}")
    log.write(f"Producer: {producer}")
    log.write(f"Released: {release_date}")
    log.write()
    log.write(f"Characters: {len(characters)}")
    log.write(', '.join(characters))
    log.write()
    log.write(f'Planets: {len(planets)}')
    log.write(', '.join(planets))
    log.write()
    log.write(f"Starships: {len(starships)}")
    log.write(', '.join(starships))
    log.write()
    log.write(f"Vehicles: {len(vehicles)}")
    log.write(', '.join(vehicles))
    log.write()
    log.write(f"Species: {len(species)}")
    log.write(', '.join(species))
    log.write()

    log.stop_timer('Total Time To complete')
    log.write(f'There were {call_count} calls to the server')


if __name__ == "__main__":
    main()
