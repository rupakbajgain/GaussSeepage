import os
import logging
import numpy as np

PERSIST_PATH = '.'

def persist_helper(name, func, *args, **kwargs):
    if len(args):
        argss=''
        for i in args:
            argss+=str(i)+','
        argss=argss[:-1]
        name+='('+argss+')'
    if len(kwargs):
        kwargss = ''
        for i in kwargs:
            kwargss+=str(i)+'-'+str(kwargs[i])+','
        kwargss=kwargss[:-1]
        name+='{'+kwargss+'}'
    logging.debug(f"Variable requested: {name}")
    file_path = os.path.join(PERSIST_PATH, f"{name}")
    if os.path.exists(file_path):
        logging.debug(f"Found on file: {file_path}")
        db = np.load(file_path)
        return db
    else:
        logging.debug(f"Cache to new file: {file_path}")
        db=func(*args, **kwargs)
        np.save(file_path,db)
        return db

def cache_to_file(p):
    def inner(func):
        def actual_function(*args, **kwargs):
            return persist_helper(p, func, *args, **kwargs)
        return actual_function
    return inner
