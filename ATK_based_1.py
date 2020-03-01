# -*- coding: utf-8 -*-
"""
Created on Sat Jul 13 20:46:08 2019

@author: Berthold
"""


# import itertools as IT -> cycle
from itertools import cycle
# import collections as CL -> deque
# import collections as CL -> OrderedDict
from collections import deque

MAX = 2500
DIF = [2, 6, 4, 2, 4, 2, 4, 6]
# if 29 then 2 is first - on 31 start with 6 end is 2
#    BAS = 30
#    HAL = [1, 7, 11, 13, 17, 19, 23, 29]

PPP = deque([])


def gen_Primes():
    for pq in PPP:
        p, q = pq
        yield p


print("###", flush=True)
PPP.append(tuple([7, 49]))
PPP.append(tuple([11, 121]))
PPP.append(tuple([13, 169]))
PPP.append(tuple([17, 289]))
PPP.append(tuple([19, 361]))
PPP.append(tuple([23, 529]))
PPP.append(tuple([29, 841]))
NN = 29
#
for d in cycle(DIF):
    NN += d
    # print(NN)
    if NN >= MAX:
        break
    for pq in PPP:
        p, q = pq
        if q > NN:
            # print(NN, end="\t")
            M = tuple([NN, NN*NN])
            PPP.append(M)
            # print("add prime: ", NN)
            break
        # print(NN, p, q)
        st = divmod(NN, p)
        s, t = st
        if t == 0:
            # print("drop this: ", NN)
            break
#
PPP.appendleft(tuple([5, 25]))
PPP.appendleft(tuple([3, 9]))
PPP.appendleft(tuple([2, 4]))
print("-->", flush=True)
print([p for p in gen_Primes()])
