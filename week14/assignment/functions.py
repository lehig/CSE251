"""
Course: CSE 251, week 14
File: functions.py
Author: lehi gracia

Instructions:

Depth First Search
https://www.youtube.com/watch?v=9RHO6jU--GU

Breadth First Search
https://www.youtube.com/watch?v=86g8jAQug04


Requesting a family from the server:
request = Request_thread(f'{TOP_API_URL}/family/{id}')
request.start()
request.join()

Example JSON returned from the server
{
    'id': 6128784944, 
    'husband_id': 2367673859,        # use with the Person API
    'wife_id': 2373686152,           # use with the Person API
    'children': [2380738417, 2185423094, 2192483455]    # use with the Person API
}

Requesting an individual from the server:
request = Request_thread(f'{TOP_API_URL}/person/{id}')
request.start()
request.join()

Example JSON returned from the server
{
    'id': 2373686152, 
    'name': 'Stella', 
    'birth': '9-3-1846', 
    'parent_id': 5428641880,   # use with the Family API
    'family_id': 6128784944    # use with the Family API
}

You will lose 10% if you don't detail your part 1 and part 2 code below

Describe how to speed up part 1

<Add your comments here>


Describe how to speed up part 2

<Add your comments here>


Extra (Optional) 10% Bonus to speed up part 3

<Add your comments here>

"""
import threading

from common import *
import queue


# -----------------------------------------------------------------------------

def request_child(child, tree):
    child_req = Request_thread(f'{TOP_API_URL}/person/{child}')
    child_req.start()
    child_req.join()
    c = child_req.get_response()
    small_person = Person(c)
    tree.add_person(small_person)

def recur_dfs(family_id, tree: Tree, person_id_list=None, threads=None, first=True):
    if threads is None:
        threads = []

    if person_id_list is None:
        person_id_list = []

    # requesting for the family and saving the response as a variable
    req = Request_thread(f'{TOP_API_URL}/family/{family_id}')
    req.start()
    req.join()
    family = req.get_response()

    # saving the data as variables
    fam_id = family['id']
    wife_id = family['wife_id']
    hus_id = family['husband_id']
    child_list = family['children']

    person_id_list.append(wife_id)
    person_id_list.append(hus_id)

    fam = Family(family)
    tree.add_family(fam)

    wife_req = Request_thread(f'{TOP_API_URL}/person/{wife_id}')
    wife_req.start()
    wife_req.join()
    wife = wife_req.get_response()

    p_id = wife['id']
    parent_id = wife['parent_id']

    person = Person(wife)
    tree.add_person(person)


    if parent_id is not None:
        thread = threading.Thread(target=recur_dfs, args=(parent_id, tree, person_id_list, threads, False))
        thread.start()
        threads.append(thread)


    hus_req = Request_thread(f'{TOP_API_URL}/person/{hus_id}')
    hus_req.start()
    hus_req.join()
    hus = hus_req.get_response()

    p_id = hus['id']
    parent_id = hus['parent_id']

    per = Person(hus)
    tree.add_person(per)

    if parent_id is not None:
        thread = threading.Thread(target=recur_dfs, args=(parent_id, tree, person_id_list, threads, False))
        thread.start()
        threads.append(thread)

    for child in child_list:
        if child not in person_id_list:
            thread = threading.Thread(target=request_child, args=(child, tree))
            thread.start()
            threads.append(thread)

    if first:
        for thread in threads:
            thread.join()


def depth_fs_pedigree(family_id, tree):
    # KEEP this function even if you don't implement it
    # TODO - implement Depth first retrieval
    # TODO - Printing out people and families that are retrieved from the server will help debugging

    recur_dfs(family_id, tree)


# -----------------------------------------------------------------------------

def bfs_requesting(q, tree, person_id_list, total_people):

    while len(person_id_list) < total_people:
        family_id = q.get()
        if family_id is None:
            q.put('finished')

        elif family_id == 'finished':
            break

        else:
            request = Request_thread(f'{TOP_API_URL}/family/{family_id}')
            request.start()
            request.join()
            family_data = request.get_response()
            family = Family(family_data)
            tree.add_family(family)

            hus_id = family.get_husband()
            wife_id = family.get_wife()
            children_ids = family.get_children()

            req_ts = []

            hus_req = Request_thread(f'{TOP_API_URL}/person/{hus_id}')
            req_ts.append(hus_req)
            wife_req = Request_thread(f'{TOP_API_URL}/person/{wife_id}')
            req_ts.append(wife_req)
            for child in children_ids:
                req = Request_thread(f'{TOP_API_URL}/person/{child}')
                req_ts.append(req)

            for req in req_ts:
                req.start()

            for req in req_ts:
                req.join()

            i = 0
            for req in req_ts:
                if i == 0:
                    husband = req.get_response()
                    person = Person(husband)
                    person_id_list.append(person.get_id())
                    tree.add_person(person)
                    q.put(person.get_parentid())
                if i == 1:
                    wife = req.get_response()
                    person = Person(wife)
                    person_id_list.append(person.get_id())
                    tree.add_person(person)
                    q.put(person.get_parentid())
                child = req.get_response()
                person = Person(child)
                if person.get_id() not in person_id_list:
                    tree.add_person(person)
                i += 1






def breadth_fs_pedigree(family_id, tree):
    # KEEP this function even if you don't implement it
    # TODO - implement breadth first retrieval
    # TODO - Printing out people and families that are retrieved from the server will help debugging


    # generations = []
    # with open('runs.txt') as gens:
    #     for line in gens:
    #         parts = line.split(',')
    #         generations.append(int(parts[1]))
    #
    # bfs_last_gen = 2 ** generations[1]

    req = Request_thread(f'{TOP_API_URL}/end')
    req.start()
    req.join()
    server_data = req.get_response()
    total_people = server_data['people']

    q = queue.Queue()
    q.put(family_id)
    person_id_list = []
    threads = [threading.Thread(target=bfs_requesting, args=(q, tree, person_id_list, total_people)) for _ in range(10)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

# -----------------------------------------------------------------------------

def bfs_5_requesting(q, tree, person_id_list, total_people, sem: threading.Semaphore):
    while len(person_id_list) < total_people:
        family_id = q.get()
        if family_id is None:
            q.put('finished')

        elif family_id == 'finished':
            break

        else:
            sem.acquire()
            request = Request_thread(f'{TOP_API_URL}/family/{family_id}')
            request.start()
            request.join()
            sem.release()
            family_data = request.get_response()
            family = Family(family_data)
            tree.add_family(family)

            hus_id = family.get_husband()
            wife_id = family.get_wife()
            children_ids = family.get_children()

            req_ts = []

            hus_req = Request_thread(f'{TOP_API_URL}/person/{hus_id}')
            req_ts.append(hus_req)
            wife_req = Request_thread(f'{TOP_API_URL}/person/{wife_id}')
            req_ts.append(wife_req)
            for child in children_ids:
                req = Request_thread(f'{TOP_API_URL}/person/{child}')
                req_ts.append(req)

            for req in req_ts:
                sem.acquire()
                req.start()
                req.join()
                sem.release()

            i = 0
            for req in req_ts:
                if i == 0:
                    husband = req.get_response()
                    person = Person(husband)
                    person_id_list.append(person.get_id())
                    tree.add_person(person)
                    q.put(person.get_parentid())
                if i == 1:
                    wife = req.get_response()
                    person = Person(wife)
                    person_id_list.append(person.get_id())
                    tree.add_person(person)
                    q.put(person.get_parentid())
                child = req.get_response()
                person = Person(child)
                if person.get_id() not in person_id_list:
                    tree.add_person(person)
                i += 1

def breadth_fs_pedigree_limit5(family_id, tree):
    # KEEP this function even if you don't implement it
    # TODO - implement breadth first retrieval
    #      - Limit number of concurrent connections to the FS server to 5
    # TODO - Printing out people and families that are retrieved from the server will help debugging

    sem = threading.Semaphore(5)

    req = Request_thread(f'{TOP_API_URL}/end')
    req.start()
    req.join()
    server_data = req.get_response()
    total_people = server_data['people']

    q = queue.Queue()
    q.put(family_id)
    person_id_list = []
    threads = [threading.Thread(target=bfs_5_requesting, args=(q, tree, person_id_list, total_people, sem)) for _ in range(20)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
