# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 18:36:01 2019

@author: A292796
"""

import multiprocessing
from os import getpid

def worker(procnum):
    print('I am number %d in process %d' % (procnum, getpid()))
    return (procnum, getpid())

if __name__ == '__main__':
    print('main', getpid())
    pool = multiprocessing.Pool(processes = 3)
    print(pool.map(worker, range(5)))
