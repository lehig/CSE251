# Taken from:
# https://www.geeksforgeeks.org/understanding-python-pickling-example/

import pickle

# initializing data to be stored in db
Omkar = {'key': 'Omkar', 'name': 'Omkar Pathak', 'age': 21, 'pay': 40000}
Jagdish = {'key': 'Jagdish', 'name': 'Jagdish Pathak', 'age': 50, 'pay': 50000}

# database
db = {}
db['Omkar'] = Omkar
db['Jagdish'] = Jagdish

print('Before:')
print(db)

# For storing
b = pickle.dumps(db)  # type(b) gives <class 'bytes'>
print()
print(type(b))
print(b)

# For loading
print('\nAfter:')
myEntry = pickle.loads(b)
print(myEntry)

