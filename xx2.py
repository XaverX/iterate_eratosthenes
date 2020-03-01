# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 18:48:06 2019

@author: A292796
"""

from concurrent.futures import ProcessPoolExecutor

def worker(procnum):
    '''worker function'''
    print(str(procnum) + ' represent!')
    return procnum


if __name__ == '__main__':
    with ProcessPoolExecutor() as executor:
        print(list(executor.map(worker, range(5))))
