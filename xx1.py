# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 18:42:44 2019

@author: A292796
"""

import multiprocessing

def worker(procnum, send_end):
    '''worker function'''
    result = str(procnum) + ' represent!'
    print(result)
    send_end.send(result)

def main():
    jobs = []
    pipe_list = []
    for i in range(5):
        recv_end, send_end = multiprocessing.Pipe(False)
        p = multiprocessing.Process(target=worker, args=(i, send_end))
        jobs.append(p)
        pipe_list.append(recv_end)
        p.start()

    for proc in jobs:
        proc.join()
    result_list = [x.recv() for x in pipe_list]
    print(result_list)

if __name__ == '__main__':
    main()
